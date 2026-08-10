"""
measure_efficiency.py
══════════════════════════════════════════════════════════════════════
Computational-efficiency comparison between PGA-UNet (256x256, 512x512) and SAM-Med2D (256x256): total and trainable parameter counts, FLOPs/MACs, on-disk checkpoint size, peak GPU memory, GPU inference latency, and forced CPU inference latency (to simulate deployment on hardware without a GPU, matching the thesis motivation that lightweight CNNs may be more practical than foundation-model Transformers).

This script fills the measurement gap noted in the thesis methodology/results sections: the thesis reported only the approximate parameter count of PGA-UNet (~3M) and did not measure FLOPs, latency, or memory against SAM-Med2D.

How to run:
  - Kaggle / Colab (recommended, requires a GPU so that the measurements match the training hardware setup, e.g. a Tesla T4 16 GB):
        !python measure_efficiency.py
    or copy the full file contents into a single notebook cell and run it directly.
  - Local machine (CPU only): still supported, but latency and memory will not reflect the GPU conditions used in the thesis. The script prints a warning automatically when CUDA is unavailable.

Required packages (installed automatically if missing):
  - fvcore (for FLOP counting; handles attention/matmul in SAM-Med2D's ViT more reliably than `thop` for Transformer architectures)
  - gdown (to download checkpoints from Google Drive, consistent with the other notebooks)

Outputs:
  - Prints a comparison table to the console, along with SAM-Med2D/PGA-UNet ratios for each metric.
  - Saves `results/efficiency_comparison.csv`.
  - Saves the bar chart `results/efficiency_comparison.png` with six headline metrics: parameter count, GFLOPs, checkpoint size, peak GPU memory, latency on the current device, and forced CPU latency. The CSV also includes extra diagnostics such as trainable/frozen parameter split, trainable parameter ratio, latency percentiles, coefficients of variation, FPS, milliseconds per megapixel, and pixels processed per second.
══════════════════════════════════════════════════════════════════════
"""

import os
import sys
import time
import subprocess
import argparse

# ──────────────────────────────────────────────────────────────────────
# 0. Install missing packages
# ──────────────────────────────────────────────────────────────────────
def _pip_install(pkg):
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", pkg], check=False)


for _pkg, _import_name in [("fvcore", "fvcore"), ("gdown", "gdown"),
                            ("pandas", "pandas"), ("matplotlib", "matplotlib")]:
    try:
        __import__(_import_name)
    except ImportError:
        print(f"Installing {_pkg} ...")
        _pip_install(_pkg)

import gdown
import torch
import torch.nn as nn
import pandas as pd
import matplotlib.pyplot as plt
from fvcore.nn import FlopCountAnalysis

# ──────────────────────────────────────────────────────────────────────
# 1. Setup (consistent with the other thesis notebooks: BASE, repo clone, checkpoint download from Google Drive)
# ──────────────────────────────────────────────────────────────────────
BASE = "/kaggle/working" if os.path.exists("/kaggle/working") else \
       ("/content" if os.path.exists("/content") else os.getcwd())
os.chdir(BASE)

REPO_PGA = "https://github.com/ThongLuc2k3/PGA_Unet2D.git"
REPO_SAM = "https://github.com/OpenGVLab/SAM-Med2D/"

if not os.path.exists(f"{BASE}/PGA_Unet2D"):
    subprocess.run(["git", "clone", "-q", REPO_PGA, f"{BASE}/PGA_Unet2D"], check=False)
if not os.path.exists(f"{BASE}/SAM-Med2D"):
    subprocess.run(["git", "clone", "-q", REPO_SAM, f"{BASE}/SAM-Med2D"], check=False)

os.makedirs(f"{BASE}/PGA_Unet2D/Source/Prompt-Guided-XRay-Segmentation/checkpoints", exist_ok=True)
for cid, fpath in [
    ("", f"{BASE}/SAM-Med2D/best_sam.pth"),
    ("", f"{BASE}/PGA_Unet2D/Source/Prompt-Guided-XRay-Segmentation/checkpoints/pga_256_best.pth"),
    ("", f"{BASE}/PGA_Unet2D/Source/Prompt-Guided-XRay-Segmentation/checkpoints/pga_512_best.pth"),
]:
    if not os.path.exists(fpath):
        gdown.download(f"https://drive.google.com/uc?id={cid}", fpath, quiet=False)

sys.path.insert(0, f"{BASE}/PGA_Unet2D/Source/Prompt-Guided-XRay-Segmentation")
sys.path.insert(0, f"{BASE}/SAM-Med2D")
for _k in list(sys.modules.keys()):
    if "segment_anything" in _k:
        del sys.modules[_k]

# Patch `build_sam.py` to support a configurable `image_size` and `encoder_adapter`
# (identical to the patch used in `test-subcat-pga-vs-sam-r256-r512.ipynb`).
_build_sam_path = f"{BASE}/SAM-Med2D/segment_anything/build_sam.py"
os.makedirs(os.path.dirname(_build_sam_path), exist_ok=True)
_build_sam_code = '''import torch
from functools import partial
from .modeling import ImageEncoderViT, MaskDecoder, PromptEncoder, Sam, TwoWayTransformer
from torch.nn import functional as F

def build_sam_vit_b(args):
    return _build_sam(
        encoder_embed_dim=768, encoder_depth=12,
        encoder_num_heads=12, encoder_global_attn_indexes=[2,5,8,11],
        image_size=args.image_size, checkpoint=args.sam_checkpoint,
        encoder_adapter=args.encoder_adapter,
    )

build_sam       = build_sam_vit_b
build_sam_vit_h = build_sam_vit_b
build_sam_vit_l = build_sam_vit_b

sam_model_registry = {
    'default': build_sam_vit_b,
    'vit_h'  : build_sam_vit_b,
    'vit_l'  : build_sam_vit_b,
    'vit_b'  : build_sam_vit_b,
}

def _build_sam(encoder_embed_dim, encoder_depth, encoder_num_heads,
               encoder_global_attn_indexes, image_size, checkpoint, encoder_adapter):
    prompt_embed_dim = 256; vit_patch_size = 16
    image_embedding_size = image_size // vit_patch_size
    sam = Sam(
        image_encoder=ImageEncoderViT(
            depth=encoder_depth, embed_dim=encoder_embed_dim, img_size=image_size,
            mlp_ratio=4, norm_layer=partial(torch.nn.LayerNorm, eps=1e-6),
            num_heads=encoder_num_heads, patch_size=vit_patch_size, qkv_bias=True,
            use_rel_pos=True, global_attn_indexes=encoder_global_attn_indexes,
            window_size=14, out_chans=prompt_embed_dim, adapter_train=encoder_adapter,
        ),
        prompt_encoder=PromptEncoder(
            embed_dim=prompt_embed_dim,
            image_embedding_size=(image_embedding_size, image_embedding_size),
            input_image_size=(image_size, image_size), mask_in_chans=16,
        ),
        mask_decoder=MaskDecoder(
            num_multimask_outputs=3,
            transformer=TwoWayTransformer(
                depth=2, embedding_dim=prompt_embed_dim, mlp_dim=2048, num_heads=8),
            transformer_dim=prompt_embed_dim, iou_head_depth=3, iou_head_hidden_dim=256,
        ),
        pixel_mean=[123.675, 116.28, 103.53],
        pixel_std=[58.395, 57.12, 57.375],
    )
    if checkpoint is not None:
        with open(checkpoint, 'rb') as f:
            sd = torch.load(f, map_location='cpu', weights_only=False)
        try:
            sam.load_state_dict(sd.get('model', sd), strict=False)
        except Exception:
            sd2 = sam.state_dict()
            new = {k: v for k, v in sd.items() if k in sd2}
            pos = new.get('image_encoder.pos_embed')
            tok = image_size // vit_patch_size
            if pos is not None and pos.shape[1] != tok:
                pos = F.interpolate(pos.permute(0,3,1,2), (tok,tok),
                                    mode='bilinear', align_corners=False)
                new['image_encoder.pos_embed'] = pos.permute(0,2,3,1)
            sd2.update(new); sam.load_state_dict(sd2)
    return sam
'''
with open(_build_sam_path, "w") as f:
    f.write(_build_sam_code)

from models.networks.prompt_unet_2D import PGA_UNet
from segment_anything import sam_model_registry

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if DEVICE.type == "cpu":
    print("Warning: no GPU (CUDA) detected. Parameter counts and FLOPs remain valid, but CPU-only latency and memory measurements do not reflect the Tesla T4 conditions used for training and evaluation in the thesis. Treat them as relative comparisons only.")

RESULTS_DIR = f"{BASE}/results"
os.makedirs(RESULTS_DIR, exist_ok=True)


# ──────────────────────────────────────────────────────────────────────
# 2. Measurement utilities
# ──────────────────────────────────────────────────────────────────────
def count_params(model, only_trainable=False):
    if only_trainable:
        return sum(p.numel() for p in model.parameters() if p.requires_grad)
    return sum(p.numel() for p in model.parameters())


def count_sam_finetune_trainable(sam_model):
    """Actual trainable parameters updated during SAM-Med2D fine-tuning in the thesis:
    only the Adapter layers in the image encoder are updated (the remaining ViT backbone is frozen),
    together with the full prompt encoder and mask decoder, matching the freezing rule in
    Source/File_Train/Finetune_SAMMed2D_test_robust.ipynb."""
    n = 0
    for name, p in sam_model.image_encoder.named_parameters():
        if "Adapter" in name:
            n += p.numel()
    n += count_params(sam_model.prompt_encoder)
    n += count_params(sam_model.mask_decoder)
    return n


def checkpoint_size_mb(path):
    return os.path.getsize(path) / (1024 ** 2) if os.path.exists(path) else float("nan")


def _safe_div(num, den):
    return float("nan") if den == 0 else num / den


def measure_flops(model, inputs):
    """inputs: tuple of tensors passed to `model(*inputs)`. Returns `(GFLOPs, GMACs)`.

    FLOPs are counted on CPU even when the original model resides on GPU. `torch.jit.trace`
    (used internally by `fvcore`) may turn a value derived from `.shape[0]` into a CPU tensor
    during tracing, which can trigger a "tensors on different devices" error when the rest of
    the graph is on CUDA, as observed in the SAM-Med2D mask decoder. Moving the full model and
    inputs to CPU during FLOP counting avoids this conflict entirely. FLOPs depend only on tensor
    shapes, not on the compute device, so result accuracy is unaffected.
    """
    orig_device = next(model.parameters()).device
    model_cpu = model.to("cpu").eval()
    inputs_cpu = tuple(x.to("cpu") for x in inputs)
    try:
        with torch.no_grad():
            flop_counter = FlopCountAnalysis(model_cpu, inputs_cpu)
            flop_counter.unsupported_ops_warnings(False)
            flop_counter.uncalled_modules_warnings(False)
            macs = flop_counter.total()
    finally:
        model.to(orig_device)
    gmacs = macs / 1e9
    gflops = 2 * gmacs  # convention: 1 MAC = 2 FLOPs
    return gflops, gmacs


def _timed_runs(model, inputs, device_type, n_warmup, n_runs):
    model.eval()
    with torch.no_grad():
        for _ in range(n_warmup):
            model(*inputs)
        if device_type == "cuda":
            torch.cuda.synchronize()

        times = []
        for _ in range(n_runs):
            t0 = time.perf_counter()
            model(*inputs)
            if device_type == "cuda":
                torch.cuda.synchronize()
            times.append((time.perf_counter() - t0) * 1000.0)

    times = torch.tensor(times, dtype=torch.float64)
    mean_ms = times.mean().item()
    std_ms = times.std(unbiased=False).item()
    p50_ms = torch.quantile(times, 0.50).item()
    p95_ms = torch.quantile(times, 0.95).item()
    min_ms = times.min().item()
    max_ms = times.max().item()
    cv_pct = _safe_div(std_ms, mean_ms) * 100.0
    fps = _safe_div(1000.0, mean_ms)
    return dict(
        mean_ms=mean_ms,
        std_ms=std_ms,
        p50_ms=p50_ms,
        p95_ms=p95_ms,
        min_ms=min_ms,
        max_ms=max_ms,
        cv_pct=cv_pct,
        fps=fps,
    )


def measure_latency(model, inputs, n_warmup=10, n_runs=50):
    """Latency on the model's current device (GPU if CUDA is available)."""
    return _timed_runs(model, inputs, DEVICE.type, n_warmup, n_runs)


def measure_latency_cpu(model, inputs, n_warmup=5, n_runs=20):
    """Latency when forcing the model onto CPU, even on a GPU-equipped machine. This simulates deployment on medical hardware without a GPU, matching the thesis motivation that lightweight CNNs may be more practical than foundation-model Transformers. Fewer iterations are used than in `measure_latency` because CPU execution is much slower, especially for SAM-Med2D's ViT-B. The model is returned to its original device afterward."""
    orig_device = next(model.parameters()).device
    model_cpu = model.to("cpu")
    inputs_cpu = tuple(x.to("cpu") for x in inputs)
    try:
        stats = _timed_runs(model_cpu, inputs_cpu, "cpu", n_warmup, n_runs)
    finally:
        model.to(orig_device)
    return stats


def measure_peak_memory_mb(model, inputs):
    """Peak GPU memory (MB) during a single inference pass. Returns `NaN` on CPU."""
    if DEVICE.type != "cuda":
        return float("nan")
    model.eval()
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats(DEVICE)
    with torch.no_grad():
        model(*inputs)
    torch.cuda.synchronize()
    return torch.cuda.max_memory_allocated(DEVICE) / (1024 ** 2)


class SAMWrapper(nn.Module):
    """Wrap the three-stage SAM-Med2D inference pipeline (`image_encoder -> prompt_encoder -> mask_decoder`) into a single `forward()` call so that FLOPs, latency, and memory are measured under the same protocol as PGA-UNet (a single `model(*inputs)` invocation)."""

    def __init__(self, sam_model):
        super().__init__()
        self.sam = sam_model

    def forward(self, img, box):
        emb = self.sam.image_encoder(img)
        se, de = self.sam.prompt_encoder(points=None, boxes=box, masks=None)
        low, _ = self.sam.mask_decoder(
            image_embeddings=emb,
            image_pe=self.sam.prompt_encoder.get_dense_pe(),
            sparse_prompt_embeddings=se,
            dense_prompt_embeddings=de,
            multimask_output=False,
        )
        return low


# ──────────────────────────────────────────────────────────────────────
# 3. Load models
# ──────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("Loading models ...")
print("=" * 70)

pga256 = PGA_UNet(in_channels=1, n_classes=1, use_encoder_prompt=True).to(DEVICE)
pga256.load_state_dict(torch.load(f"{BASE}/PGA_Unet2D/Source/Prompt-Guided-XRay-Segmentation/checkpoints/pga_256_best.pth",
                                   map_location=DEVICE, weights_only=True))
pga256.eval()

pga512 = PGA_UNet(in_channels=1, n_classes=1, use_encoder_prompt=True).to(DEVICE)
pga512.load_state_dict(torch.load(f"{BASE}/PGA_Unet2D/Source/Prompt-Guided-XRay-Segmentation/checkpoints/pga_512_best.pth",
                                   map_location=DEVICE, weights_only=True))
pga512.eval()
print("PGA-UNet loaded successfully (`pga_256_best.pth` and `pga_512_best.pth`). "
      "The architecture is identical across resolutions, so parameter counts and FLOPs depend only on input shape, not on the checkpoint weights.")

args_sam = argparse.Namespace(image_size=256, encoder_adapter=True,
                               sam_checkpoint=f"{BASE}/SAM-Med2D/best_sam.pth")
sam_model = sam_model_registry["vit_b"](args_sam).to(DEVICE)
sam_model.eval()
sam_wrapped = SAMWrapper(sam_model).to(DEVICE)
sam_wrapped.eval()
print("SAM-Med2D loaded successfully (ViT-B, `encoder_adapter=True`, input size 256x256).")

# ──────────────────────────────────────────────────────────────────────
# 4. Prepare synthetic inputs for each configuration
# ──────────────────────────────────────────────────────────────────────
def make_pga_inputs(size):
    img = torch.randn(1, 1, size, size, device=DEVICE)
    prompt = torch.rand(1, 1, size, size, device=DEVICE)  # heatmap trong [0,1]
    return (img, prompt)


def make_sam_inputs():
    img = torch.randn(1, 3, 256, 256, device=DEVICE)
    box = torch.tensor([[[40.0, 40.0, 200.0, 200.0]]], device=DEVICE)  # [B,1,4]
    return (img, box)


configs = [
    ("PGA-UNet (256x256)", pga256, make_pga_inputs(256),
     f"{BASE}/PGA_Unet2D/Source/Prompt-Guided-XRay-Segmentation/checkpoints/pga_256_best.pth", count_params(pga256)),
    ("PGA-UNet (512x512)", pga512, make_pga_inputs(512),
     f"{BASE}/PGA_Unet2D/Source/Prompt-Guided-XRay-Segmentation/checkpoints/pga_512_best.pth", count_params(pga512)),
    ("SAM-Med2D (256x256)", sam_wrapped, make_sam_inputs(),
     f"{BASE}/SAM-Med2D/best_sam.pth", count_params(sam_model)),
]

# ──────────────────────────────────────────────────────────────────────
# 5. Run the measurements
# ──────────────────────────────────────────────────────────────────────
rows = []
for name, model, inputs, ckpt_path, n_params_total in configs:
    print(f"\nMeasuring: {name} ...")
    gflops, gmacs = measure_flops(model, inputs)
    print("  Measuring CPU latency as well (simulating deployment without a GPU; this may take a while for SAM-Med2D) ...")
    peak_mem = measure_peak_memory_mb(model, inputs)
    ckpt_mb = checkpoint_size_mb(ckpt_path)

    if name.startswith("SAM-Med2D"):
        n_trainable = count_sam_finetune_trainable(sam_model)
    else:
        n_trainable = count_params(model, only_trainable=True)
    n_frozen = max(n_params_total - n_trainable, 0)
    if name.startswith("PGA-UNet (256x256)"):
        input_side = 256
    elif name.startswith("PGA-UNet (512x512)"):
        input_side = 512
    else:
        input_side = 256
    input_megapixels = (input_side * input_side) / 1e6
    current_latency = measure_latency(model, inputs)
    cpu_latency = measure_latency_cpu(model, inputs)
    ms_per_mp = _safe_div(current_latency["mean_ms"], input_megapixels)
    pixels_per_second_mp = _safe_div(input_megapixels, current_latency["mean_ms"] / 1000.0)
    cpu_ms_per_mp = _safe_div(cpu_latency["mean_ms"], input_megapixels)
    cpu_pixels_per_second_mp = _safe_div(input_megapixels, cpu_latency["mean_ms"] / 1000.0)

    rows.append(dict(
        model=name,
        input_side_px=input_side,
        input_megapixels=input_megapixels,
        params_total_M=n_params_total / 1e6,
        params_trainable_M=n_trainable / 1e6,
        params_frozen_M=n_frozen / 1e6,
        trainable_ratio_pct=_safe_div(n_trainable, n_params_total) * 100.0,
        gflops=gflops,
        gmacs=gmacs,
        checkpoint_MB=ckpt_mb,
        peak_mem_MB=peak_mem,
        latency_ms_mean=current_latency["mean_ms"],
        latency_ms_std=current_latency["std_ms"],
        latency_ms_p50=current_latency["p50_ms"],
        latency_ms_p95=current_latency["p95_ms"],
        latency_ms_min=current_latency["min_ms"],
        latency_ms_max=current_latency["max_ms"],
        latency_cv_pct=current_latency["cv_pct"],
        fps=current_latency["fps"],
        ms_per_megapixel=ms_per_mp,
        megapixels_per_second=pixels_per_second_mp,
        latency_ms_mean_cpu=cpu_latency["mean_ms"],
        latency_ms_std_cpu=cpu_latency["std_ms"],
        latency_ms_p50_cpu=cpu_latency["p50_ms"],
        latency_ms_p95_cpu=cpu_latency["p95_ms"],
        latency_ms_min_cpu=cpu_latency["min_ms"],
        latency_ms_max_cpu=cpu_latency["max_ms"],
        latency_cv_pct_cpu=cpu_latency["cv_pct"],
        fps_cpu=cpu_latency["fps"],
        ms_per_megapixel_cpu=cpu_ms_per_mp,
        megapixels_per_second_cpu=cpu_pixels_per_second_mp,
    ))
    print(f"  Parameters: {n_params_total/1e6:.3f}M total / {n_trainable/1e6:.3f}M trainable")
    print(f"  FLOPs:   {gflops:.3f} GFLOPs ({gmacs:.3f} GMACs)")
    print(f"  Peak GPU memory: {peak_mem:.1f} MB" if DEVICE.type == "cuda" else "  Peak memory: N/A (CPU)")
    print(
        f"  Latency (current device: {DEVICE.type}): "
        f"{current_latency['mean_ms']:.2f} ± {current_latency['std_ms']:.2f} ms/image  "
        f"(p50={current_latency['p50_ms']:.2f}, p95={current_latency['p95_ms']:.2f}, "
        f"{current_latency['fps']:.1f} images/s)"
    )
    print(
        f"  Latency (forced CPU): {cpu_latency['mean_ms']:.2f} ± {cpu_latency['std_ms']:.2f} ms/image  "
        f"(p50={cpu_latency['p50_ms']:.2f}, p95={cpu_latency['p95_ms']:.2f}, "
        f"{cpu_latency['fps']:.1f} images/s)"
    )
    print(f"  Checkpoint size on disk: {ckpt_mb:.1f} MB")

df = pd.DataFrame(rows)
csv_path = f"{RESULTS_DIR}/efficiency_comparison.csv"
df.to_csv(csv_path, index=False, float_format="%.4f")

print("\n" + "=" * 70)
print("SUMMARY TABLE")
print("=" * 70)
_num_cols = ["input_megapixels", "params_total_M", "params_trainable_M", "params_frozen_M",
             "trainable_ratio_pct", "gflops", "gmacs", "checkpoint_MB", "peak_mem_MB",
             "latency_ms_mean", "latency_ms_std", "latency_ms_p50", "latency_ms_p95",
             "latency_ms_min", "latency_ms_max", "latency_cv_pct", "fps",
             "ms_per_megapixel", "megapixels_per_second",
             "latency_ms_mean_cpu", "latency_ms_std_cpu", "latency_ms_p50_cpu",
             "latency_ms_p95_cpu", "latency_ms_min_cpu", "latency_ms_max_cpu",
             "latency_cv_pct_cpu", "fps_cpu", "ms_per_megapixel_cpu",
             "megapixels_per_second_cpu"]
print(df.to_string(index=False, formatters={c: (lambda x: f"{x:.3f}") for c in _num_cols}))
print(f"\n→ CSV: {csv_path}")

# Ratio summary against PGA-UNet at the same 256x256 resolution, ready to cite in the manuscript
try:
    r_pga = df[df["model"] == "PGA-UNet (256x256)"].iloc[0]
    r_sam = df[df["model"] == "SAM-Med2D (256x256)"].iloc[0]
    print("\n" + "-" * 70)
    print("SAM-Med2D / PGA-UNet comparison at the same 256x256 resolution:")
    print(f"  Parameter count:        {r_sam['params_total_M']/r_pga['params_total_M']:.1f}x "
          f"({r_sam['params_total_M']:.2f}M vs {r_pga['params_total_M']:.2f}M)")
    print(f"  Trainable parameters:   {r_sam['params_trainable_M']/r_pga['params_trainable_M']:.1f}x")
    print(f"  GFLOPs:            {r_sam['gflops']/r_pga['gflops']:.1f}x")
    print(f"  Checkpoint size (MB):   {r_sam['checkpoint_MB']/r_pga['checkpoint_MB']:.1f}x")
    if DEVICE.type == "cuda":
        print(f"  GPU latency:        {r_sam['latency_ms_mean']/r_pga['latency_ms_mean']:.1f}x")
        print(f"  GPU p95 latency:    {r_sam['latency_ms_p95']/r_pga['latency_ms_p95']:.1f}x")
    print(f"  CPU latency:        {r_sam['latency_ms_mean_cpu']/r_pga['latency_ms_mean_cpu']:.1f}x")
    print(f"  Pixels/s throughput:    {r_sam['megapixels_per_second']/r_pga['megapixels_per_second']:.1f}x")
    print("-" * 70)
except (IndexError, KeyError, ZeroDivisionError):
    pass

# ──────────────────────────────────────────────────────────────────────
# 6. Comparison plots (using the same color palette as the other thesis figures: PGA-UNet = blue `#2a78d6`, SAM-Med2D = orange `#eb6834`)
# ──────────────────────────────────────────────────────────────────────
COLORS = {"PGA-UNet (256x256)": "#8ec2ef",
          "PGA-UNet (512x512)": "#2a78d6",
          "SAM-Med2D (256x256)": "#eb6834"}

fig, axes = plt.subplots(2, 3, figsize=(16, 9))
axes = axes.flatten()
metrics = [
    ("params_total_M", "Parameter count (millions)", axes[0]),
    ("gflops", "GFLOPs", axes[1]),
    ("checkpoint_MB", "Checkpoint size on disk (MB)", axes[2]),
    ("peak_mem_MB", "Peak GPU memory (MB)", axes[3]),
    ("latency_ms_mean", f"Inference latency on {DEVICE.type.upper()} (ms/image)", axes[4]),
    ("latency_ms_mean_cpu", "Forced CPU inference latency (ms/image)", axes[5]),
]
for col, label, ax in metrics:
    vals = df[col].tolist()
    names = df["model"].tolist()
    bars = ax.bar(names, vals, color=[COLORS.get(n, "#888888") for n in names])
    for b, v in zip(bars, vals):
        txt = "N/A" if (isinstance(v, float) and v != v) else f"{v:.2f}"
        ax.text(b.get_x() + b.get_width() / 2, b.get_height(), txt,
                ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_title(label, fontsize=11, fontweight="bold")
    ax.set_xticklabels(names, rotation=20, ha="right", fontsize=8)
    ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
png_path = f"{RESULTS_DIR}/efficiency_comparison.png"
plt.savefig(png_path, dpi=150, bbox_inches="tight")
print(f"→ Figure: {png_path}")

if DEVICE.type != "cuda":
    print("\nReminder: run this script on Kaggle/Colab with GPU support before reporting "
          "memory/latency numbers, so the hardware setting matches the Tesla T4 used "
          "throughout the thesis.")
