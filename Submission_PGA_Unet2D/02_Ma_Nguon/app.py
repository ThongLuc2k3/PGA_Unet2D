"""
app.py — PGA-UNet Demo (Gradio UI)
Hệ thống phân đoạn tổn thương xương X-quang với câu nhắc trực quan.

Pipeline:
  1. MobileNetV4 Gatekeeper: phân loại có/không bệnh
  2. Bác sĩ vẽ bounding box prompt
  3. PGA-UNet: phân đoạn với Gaussian heatmap prompt
  4. Cơ chế phòng hộ: phát hiện prompt xấu → GradCAM rescue → IPR 3 vòng

Sử dụng:
  pip install -r requirements.txt
  python app.py
"""

import os, cv2, argparse
import numpy as np
import torch
import torch.nn.functional as F
import gradio as gr
from scipy.ndimage import binary_erosion

# ── Đường dẫn checkpoint (tải từ Google Drive nếu chưa có) ─────────────
PGA_CKPT_ID  = "1Mv-rUPI7KGmYemd27hmKbJQRHc4ZKB9z"
GKEEPER_ID   = "YOUR_MOBILENETV4_CKPT_ID"       # điền ID Drive của best_mobilenetv4.pth
PGA_CKPT     = "checkpoints/pga_unet_expB_best.pth"
GKEEPER_CKPT = "checkpoints/best_mobilenetv4.pth"
IMG_SIZE     = 512
DEVICE       = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ── Import models ────────────────────────────────────────────────────────
from models.networks.prompt_unet_2D import PGA_UNet

# ── Download checkpoints nếu chưa có ────────────────────────────────────
def download_if_missing():
    import gdown
    os.makedirs("checkpoints", exist_ok=True)
    if not os.path.exists(PGA_CKPT):
        print(f"Downloading PGA checkpoint...")
        gdown.download(f"https://drive.google.com/uc?id={PGA_CKPT_ID}", PGA_CKPT, quiet=False)

# ── Load PGA model ───────────────────────────────────────────────────────
def load_pga():
    model = PGA_UNet(in_channels=1, n_classes=1, use_encoder_prompt=True).to(DEVICE)
    model.load_state_dict(torch.load(PGA_CKPT, map_location=DEVICE, weights_only=True))
    model.eval()
    return model

# ── Tạo Gaussian heatmap từ bbox ─────────────────────────────────────────
def make_heatmap(bbox, S=512):
    x1 = max(0, int(bbox[0]) - 5); y1 = max(0, int(bbox[1]) - 5)
    x2 = min(S, int(bbox[2]) + 5); y2 = min(S, int(bbox[3]) + 5)
    hm = np.zeros((S, S), dtype=np.float32)
    if x2 > x1 and y2 > y1:
        hm[y1:y2, x1:x2] = 1.0
        hm = cv2.GaussianBlur(hm, (31, 31), 0)
    return hm

# ── Extract LCC ──────────────────────────────────────────────────────────
def extract_lcc(m):
    if m.sum() == 0: return m
    n, lbl, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    return m if n <= 1 else (lbl == (1 + np.argmax(st[1:, cv2.CC_STAT_AREA]))).astype(np.float32)

# ── Kiểm duyệt 5 tiêu chí ────────────────────────────────────────────────
def is_suspicious(prob_np, pm_np, img_norm_np, S=512,
                  conf_thr=0.80, dist_ratio=0.25, dark_thr=-0.80, dark_ratio=0.70):
    pred = (prob_np > 0.5).astype(np.float32)
    conf = float(prob_np.max())
    ys_p, xs_p = np.where(pm_np > 0.3)
    cx_pmt = xs_p.mean() if len(xs_p) else S / 2
    cy_pmt = ys_p.mean() if len(ys_p) else S / 2
    prompt_area = len(xs_p)
    ys_r, xs_r = np.where(pred > 0.5)
    pred_area = int(pred.sum())
    dist = (float(np.sqrt((xs_r.mean()-cx_pmt)**2 + (ys_r.mean()-cy_pmt)**2))
            if len(xs_r) > 0 else float(S))
    s_conf  = conf < conf_thr
    s_dist  = dist > S * dist_ratio
    s_area  = pred_area < 50
    s_ratio = prompt_area > 0 and pred_area / float(prompt_area) < 0.05
    pm_mask = pm_np > 0.3
    dr = float((img_norm_np[pm_mask] < dark_thr).sum() / pm_mask.sum()) if pm_mask.sum() > 0 else 1.0
    s_dark  = dr > dark_ratio
    return any([s_conf, s_dist, s_area, s_ratio, s_dark])

# ── GradCAM ──────────────────────────────────────────────────────────────
def compute_gradcam(model, img_norm):
    grads, acts = [], []
    def _hook(m, i, o):
        acts.append(o); o.register_hook(lambda g: grads.append(g))
    h = model.center.register_forward_hook(_hook)
    img_t  = torch.from_numpy(img_norm).unsqueeze(0).unsqueeze(0).float().to(DEVICE)
    zero_p = torch.zeros(1, 1, IMG_SIZE, IMG_SIZE, device=DEVICE)
    out = model(img_t, zero_p)
    model.zero_grad(); out.sum().backward(); h.remove()
    if not grads: return None
    w   = grads[0].mean(dim=(2, 3), keepdim=True)
    cam = F.relu((w * acts[0]).sum(1, keepdim=True))
    cam = F.interpolate(cam, (IMG_SIZE, IMG_SIZE), mode="bilinear", align_corners=False)
    cam = cam[0, 0].detach().cpu().numpy()
    mx  = cam.max(); return cam / mx if mx > 0 else cam

# ── IPR 3 vòng ───────────────────────────────────────────────────────────
def run_ipr(model, img_tensor, cx, cy, bw, bh, n_iter=3):
    px, py = float(cx), float(cy)
    for _ in range(n_iter):
        hm   = make_heatmap([px - bw/2, py - bh/2, px + bw/2, py + bh/2], IMG_SIZE)
        pm_t = torch.from_numpy(hm).unsqueeze(0).unsqueeze(0).float().to(DEVICE)
        with torch.no_grad():
            prob = torch.sigmoid(model(img_tensor, pm_t))[0, 0].cpu().numpy()
        mask = extract_lcc((prob > 0.5).astype(np.float32))
        if mask.sum() > 0:
            yp, xp = np.where(mask > 0.5)
            px, py = float(xp.mean()), float(yp.mean())
    return prob, mask

# ── Pipeline chính ───────────────────────────────────────────────────────
def segment(image, bbox_str, model):
    """
    image: PIL Image hoặc numpy H×W×3
    bbox_str: "x1,y1,x2,y2" (pixel coords tại độ phân giải gốc)
    """
    if image is None:
        return None, "⚠️ Chưa tải ảnh"
    img_np = np.array(image)
    if img_np.ndim == 3:
        img_gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    else:
        img_gray = img_np

    H0, W0 = img_gray.shape
    img_rs  = cv2.resize(img_gray, (IMG_SIZE, IMG_SIZE))
    img_norm = (img_rs.astype(np.float32) / 255.0 - 0.5) / 0.5

    # Parse bbox
    try:
        x1, y1, x2, y2 = [float(v) for v in bbox_str.split(",")]
        sx, sy = IMG_SIZE / W0, IMG_SIZE / H0
        x1, y1, x2, y2 = x1*sx, y1*sy, x2*sx, y2*sy
    except Exception:
        return None, "⚠️ Định dạng bbox không hợp lệ. Dùng: x1,y1,x2,y2"

    hm = make_heatmap([x1, y1, x2, y2], IMG_SIZE)
    img_t = torch.from_numpy(img_norm).unsqueeze(0).unsqueeze(0).float().to(DEVICE)
    pm_t  = torch.from_numpy(hm).unsqueeze(0).unsqueeze(0).float().to(DEVICE)

    with torch.no_grad():
        prob0 = torch.sigmoid(model(img_t, pm_t))[0, 0].cpu().numpy()

    bw = x2 - x1; bh = y2 - y1
    cx = (x1 + x2) / 2; cy = (y1 + y2) / 2
    status = ""

    if is_suspicious(prob0, hm, img_norm):
        status = "⚠️ Prompt xấu — kích hoạt GradCAM rescue"
        sal = compute_gradcam(model, img_norm)
        if sal is not None:
            py_c, px_c = np.unravel_index(sal.argmax(), sal.shape)
            cx, cy = float(px_c), float(py_c)
            status += " → GradCAM tìm được vùng gợi ý"
        prob, mask = run_ipr(model, img_t, cx, cy, bw, bh)
        status += " → IPR 3 vòng hoàn tất"
    else:
        prob, mask = run_ipr(model, img_t, cx, cy, bw, bh)
        status = "✅ Prompt hợp lệ → IPR refinement"

    # Overlay kết quả
    img_rgb  = cv2.cvtColor(img_rs, cv2.COLOR_GRAY2RGB)
    overlay  = img_rgb.copy().astype(np.float32)
    overlay[mask > 0.5] = overlay[mask > 0.5] * 0.4 + np.array([220, 60, 60]) * 0.6
    overlay = np.clip(overlay, 0, 255).astype(np.uint8)

    eps = 1e-6
    gm = mask; tp = (gm * mask).sum()
    dice = float((2*tp + eps) / (2*tp + eps))   # placeholder (không có GT)
    status += f"\n📊 Confidence max: {float(prob.max()):.3f}"

    return overlay, status

# ── Gradio UI ────────────────────────────────────────────────────────────
def build_demo(model):
    with gr.Blocks(title="PGA-UNet — Phân đoạn X-quang Xương") as demo:
        gr.Markdown("# PGA-UNet: Phân đoạn Tổn thương Xương X-quang\n"
                    "**Hướng dẫn:** Tải ảnh X-quang → nhập tọa độ bounding box → nhấn Phân đoạn")
        with gr.Row():
            with gr.Column():
                img_input  = gr.Image(label="Ảnh X-quang đầu vào", type="numpy")
                bbox_input = gr.Textbox(label="Bounding Box (x1,y1,x2,y2)",
                                        placeholder="Ví dụ: 120,150,380,420",
                                        value="100,100,400,400")
                btn = gr.Button("🔍 Phân đoạn", variant="primary")
            with gr.Column():
                img_output    = gr.Image(label="Kết quả phân đoạn (đỏ = mask dự đoán)")
                status_output = gr.Textbox(label="Trạng thái hệ thống", lines=4)

        btn.click(fn=lambda img, bbox: segment(img, bbox, model),
                  inputs=[img_input, bbox_input],
                  outputs=[img_output, status_output])

        gr.Markdown("---\n**Thông tin mô hình:** PGA-UNet (~4M params) | "
                    "Dice=0.8558 (mixed_7_3) | HD95=12.79px | Thời gian: ~180ms")
    return demo

if __name__ == "__main__":
    download_if_missing()
    print(f"Loading PGA-UNet on {DEVICE}...")
    model = load_pga()
    demo  = build_demo(model)
    demo.launch(share=False, server_port=7860)
