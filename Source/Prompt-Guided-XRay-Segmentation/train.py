import os
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm import tqdm
import logging
import datetime

from dataset import PromptSegmentationDataset
from models.networks.prompt_unet_2D import PGA_UNet

# =========================================================
# Experiment configuration
# =========================================================
# 'zoom_out'/'shift': legacy, independent-per-side random expansion.
# 'center_zoom'/'center_shift': tight box scaled from its center by
# PROMPT_SCALE_FACTOR; 'center_shift' additionally displaces it off-center
# by up to PROMPT_SHIFT_RATIO, exactly like 'shift' does to 'zoom_out'.
# 'center_mixed': independently samples 'center_zoom' or 'center_shift' per
# training example with 50/50 probability, so the model is not trained on a
# narrower prompt distribution than it is tested on. For 'zoom_out'/'shift'
# and plain 'center_zoom'/'center_shift', training only ever uses the
# "zoom" side of whichever pair is selected; the "shift" side is
# evaluation-only.
TRAIN_PROMPT_MODE   = os.environ.get("PROMPT_MODE", "zoom_out")
PROMPT_SCALE_FACTOR = float(os.environ.get("PROMPT_SCALE_FACTOR", "2.0"))
PROMPT_SHIFT_RATIO  = float(os.environ.get("PROMPT_SHIFT_RATIO", "0.30"))
# Stage 3 (no-GT confidence, Research/03_uncertainty_confidence/): a small
# QualityHead learns to regress its own sample's real Dice during training
# (LOSS_CONFIDENCE_WEIGHT > 0); at inference it needs no ground truth at all.
# Off by default so the model architecture matches every checkpoint trained
# so far (adding the head unconditionally would change the state_dict keys).
USE_QUALITY_HEAD       = os.environ.get("USE_QUALITY_HEAD", "0") == "1"
LOSS_CONFIDENCE_WEIGHT = float(os.environ.get("LOSS_CONFIDENCE_WEIGHT", "0.0"))
# Since QualityHead's input is detached inside the model (see
# prompt_unet_2D.py), its loss never reaches the encoder/decoder anyway, so
# training it does not require retraining segmentation from scratch. Set
# INIT_CHECKPOINT to an existing checkpoint (e.g. the stage 1 x2/shift0.3
# winner) to load its backbone weights (loaded non-strict: the checkpoint
# has no quality_head keys, and none of its keys are missing from the new
# model either way), and set FREEZE_BACKBONE=1 to train only QualityHead's
# own small MLP on top of it, a few cheap epochs instead of a full retrain.
INIT_CHECKPOINT = os.environ.get("INIT_CHECKPOINT", "")
FREEZE_BACKBONE = os.environ.get("FREEZE_BACKBONE", "0") == "1"
# Stage 2 (loss function, Research/02_loss_function/): a size-conditioned
# Tversky term, replacing dice_loss in the main segmentation loss when
# enabled. Unlike the earlier beta>alpha attempt (removed, see that folder's
# README), this only shifts weight toward penalizing false positives on
# small lesions, where a real x2/shift0.3 checkpoint was measured to
# over-segment (precision trailing recall); large lesions, already well
# segmented, get alpha=beta=0.5, mathematically identical to dice_loss.
USE_SIZE_TVERSKY      = os.environ.get("USE_SIZE_TVERSKY", "0") == "1"
SIZE_TVERSKY_ALPHA_MAX = float(os.environ.get("SIZE_TVERSKY_ALPHA_MAX", "0.7"))
SIZE_TVERSKY_AREA_PCTL = float(os.environ.get("SIZE_TVERSKY_AREA_PCTL", "25"))
USE_ENCODER_PROMPT = True    # True enables PromptSpatialGate in the encoder
DEVICE     = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BATCH_SIZE = 4
EPOCHS     = int(os.environ.get("PROMPT_EPOCHS", "100"))
LR         = 1e-4
EARLY_STOP = 15
# Validate on the same zoom/shift pair as the one being trained.
# 'center_mixed' has no matching validation loader (validation always
# reports the two pure scenarios separately); checkpoint selection then
# falls back to the covering-prompt ('center_zoom') validation Dice.
EVAL_PROMPT_MODES = ('zoom_out', 'shift') if TRAIN_PROMPT_MODE in ('zoom_out', 'shift') \
    else ('center_zoom', 'center_shift')
PRIMARY_VAL_MODE  = 'center_zoom' if TRAIN_PROMPT_MODE == 'center_mixed' else TRAIN_PROMPT_MODE
def resolve_img_size():
    return int(os.environ.get("PROMPT_IMG_SIZE", "512"))


def resolve_dataset_root():
    env_root = os.environ.get("PROMPT_DATASET_ROOT")
    if env_root:
        return env_root

    candidates = [
        "dataset",
        "dataset_BTXRD",
        "dataset_FracAtlas",
    ]
    for root in candidates:
        if os.path.isdir(os.path.join(root, "train", "images")):
            return root

    for name in sorted(os.listdir(".")):
        if os.path.isdir(os.path.join(name, "train", "images")):
            return name

    return "dataset"


DATASET_ROOT = resolve_dataset_root()
IMG_SIZE     = resolve_img_size()

# =========================================================
# METRICS
# =========================================================
def dice_loss(pred, target, smooth=1e-5):
    pred_soft    = torch.sigmoid(pred)
    intersection = (pred_soft * target).sum(dim=(1, 2, 3))
    union        = pred_soft.sum(dim=(1, 2, 3)) + target.sum(dim=(1, 2, 3))
    return (1 - ((2. * intersection + smooth) / (union + smooth))).mean()


def size_weighted_tversky_loss(pred, target, area_ref, alpha_max=0.7, smooth=1e-5):
    """Per-sample Tversky loss with alpha (false-positive weight)
    interpolated by each sample's own GT area, not fixed for the whole
    batch. Samples at or above area_ref get alpha=beta=0.5, mathematically
    identical to dice_loss, so lesions already segmented well are
    unaffected. Samples below area_ref get alpha up to alpha_max, so false
    positives are penalized more than false negatives, aimed at the
    over-segmentation measured on the small-lesion subset (see
    Research/02_loss_function/).
    """
    pred_soft = torch.sigmoid(pred)
    area = target.sum(dim=(1, 2, 3))
    shrink = (area_ref - area).clamp(min=0) / area_ref
    alpha = 0.5 + shrink * (alpha_max - 0.5)
    beta  = 1.0 - alpha

    tp = (pred_soft * target).sum(dim=(1, 2, 3))
    fp = (pred_soft * (1 - target)).sum(dim=(1, 2, 3))
    fn = ((1 - pred_soft) * target).sum(dim=(1, 2, 3))
    tversky = (tp + smooth) / (tp + alpha * fp + beta * fn + smooth)
    return (1 - tversky).mean()


def compute_area_reference(dataset, percentile):
    """One-time scan of the training set's per-sample GT mask area (in
    pixels), used as size_weighted_tversky_loss's large/small boundary.
    Percentile-based rather than a fixed pixel count, so it self-calibrates
    to whatever dataset/resolution is in use, instead of a constant tuned
    for one specific image size.
    """
    areas = [dataset[i][1].sum().item() for i in range(len(dataset))]
    return float(np.percentile(areas, percentile))


def per_sample_dice(pred, target, smooth=1e-5):
    """Real Dice per sample in the batch (not summed/averaged), used as the
    regression target for QualityHead. Always detached by the caller before
    use as a loss target, since the head should learn to predict this value,
    not backpropagate through the segmentation head to change it.
    """
    pred_bin = (torch.sigmoid(pred) > 0.5).float()
    tp = (pred_bin * target).sum(dim=(1, 2, 3))
    fp = (pred_bin * (1 - target)).sum(dim=(1, 2, 3))
    fn = ((1 - pred_bin) * target).sum(dim=(1, 2, 3))
    return (2. * tp + smooth) / (2. * tp + fp + fn + smooth)


def batch_metrics_sum(pred, target, smooth=1e-5):
    pred_bin = (torch.sigmoid(pred) > 0.5).float()
    tp = (pred_bin * target).sum(dim=(1, 2, 3))
    fp = (pred_bin * (1 - target)).sum(dim=(1, 2, 3))
    fn = ((1 - pred_bin) * target).sum(dim=(1, 2, 3))
    dice      = (2. * tp + smooth) / (2. * tp + fp + fn + smooth)
    iou       = (tp + smooth) / (tp + fp + fn + smooth)
    precision = tp / (tp + fp + smooth)
    recall    = tp / (tp + fn + smooth)
    return dice.sum().item(), iou.sum().item(), precision.sum().item(), recall.sum().item()


def calculate_cbl(pred, target, smooth=1e-6):
    """
    CBL, Center-Based Localization score in [0, 1].
    Measures how close the predicted mask's centroid is to the GT mask's centroid.
    Normalized by the GT bbox diagonal to stay scale-invariant.
    Returns (cbl_sum, valid_count).
    """
    B, _, H, W = pred.shape
    pred_bin = (torch.sigmoid(pred) > 0.5).float()

    ys = torch.arange(H, device=pred.device, dtype=torch.float32)
    xs = torch.arange(W, device=pred.device, dtype=torch.float32)
    grid_y, grid_x = torch.meshgrid(ys, xs, indexing='ij')  # (H, W)

    cbl_sum, valid_count = 0.0, 0

    for b in range(B):
        gt_m   = target[b, 0]
        pred_m = pred_bin[b, 0]
        gt_area = gt_m.sum()

        if gt_area < smooth:
            continue  # empty GT, skip

        # GT centroid
        cx_gt = (grid_x * gt_m).sum() / (gt_area + smooth)
        cy_gt = (grid_y * gt_m).sum() / (gt_area + smooth)

        # GT bbox diagonal
        nz    = gt_m.nonzero()
        gt_diag = torch.sqrt(
            ((nz[:, 0].max() - nz[:, 0].min()).float()) ** 2 +
            ((nz[:, 1].max() - nz[:, 1].min()).float()) ** 2
        ) + smooth

        pred_area = pred_m.sum()
        if pred_area < smooth:
            valid_count += 1  # CBL = 0 for this sample
            continue

        # Predicted mask centroid
        cx_p = (grid_x * pred_m).sum() / (pred_area + smooth)
        cy_p = (grid_y * pred_m).sum() / (pred_area + smooth)

        d   = torch.sqrt((cx_p - cx_gt) ** 2 + (cy_p - cy_gt) ** 2)
        cbl = torch.clamp(1.0 - d / gt_diag, min=0.0)
        cbl_sum += cbl.item()
        valid_count += 1

    return cbl_sum, valid_count


# =========================================================
# LOGGER
# =========================================================
def setup_logger(exp_name):
    os.makedirs("logs", exist_ok=True)
    t = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    logging.basicConfig(
        level=logging.INFO, format='%(message)s',
        handlers=[
            logging.FileHandler(f"logs/train_exp{exp_name}_{t}.log", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger()


# =========================================================
# MAIN
# =========================================================
def _dataset_kwargs(mode):
    """scale_factor/shift_ratio only apply to 'center_zoom'/'center_shift'/
    'center_mixed'; the legacy 'zoom_out'/'shift' modes keep their own
    defaults regardless of these env vars.
    """
    if mode in ('center_zoom', 'center_shift', 'center_mixed'):
        return dict(scale_factor=PROMPT_SCALE_FACTOR, shift_ratio=PROMPT_SHIFT_RATIO)
    return {}


def main():
    if TRAIN_PROMPT_MODE not in {'zoom_out', 'shift', 'center_zoom', 'center_shift', 'center_mixed'}:
        raise ValueError(
            "TRAIN_PROMPT_MODE must be 'zoom_out', 'shift', 'center_zoom', 'center_shift', or 'center_mixed'.")
    if PRIMARY_VAL_MODE not in EVAL_PROMPT_MODES:
        raise ValueError("PRIMARY_VAL_MODE must be one of EVAL_PROMPT_MODES.")

    logger = setup_logger(TRAIN_PROMPT_MODE)
    logger.info("=" * 90)
    logger.info(
        f"TrainPrompt: {TRAIN_PROMPT_MODE} | Device: {DEVICE} | "
        f"EncoderPrompt: {USE_ENCODER_PROMPT} | ImgSize: {IMG_SIZE} | "
        f"DatasetRoot: {DATASET_ROOT}"
        + (f" | ScaleFactor: {PROMPT_SCALE_FACTOR}"
           if TRAIN_PROMPT_MODE in ('center_zoom', 'center_shift', 'center_mixed') else "")
        + (f" | QualityHead: ConfidenceLossWeight={LOSS_CONFIDENCE_WEIGHT}" if USE_QUALITY_HEAD else "")
        + (f" | SizeTversky: AlphaMax={SIZE_TVERSKY_ALPHA_MAX}, AreaPercentile={SIZE_TVERSKY_AREA_PCTL}" if USE_SIZE_TVERSKY else "")
    )
    logger.info("=" * 90)

    # ── Dataset ──────────────────────────────────────────────────────
    train_ds = PromptSegmentationDataset(
        image_dir=os.path.join(DATASET_ROOT, "train", "images"),
        json_dir=os.path.join(DATASET_ROOT, "train", "annotations"),
        img_size=IMG_SIZE, is_train=True,
        prompt_mode=TRAIN_PROMPT_MODE,
        **_dataset_kwargs(TRAIN_PROMPT_MODE),
    )
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True,
                              num_workers=2, pin_memory=True)

    size_tversky_area_ref = None
    if USE_SIZE_TVERSKY:
        size_tversky_area_ref = compute_area_reference(train_ds, SIZE_TVERSKY_AREA_PCTL)
        logger.info(
            f"SizeTversky area reference (p{SIZE_TVERSKY_AREA_PCTL:.0f} of train GT area): "
            f"{size_tversky_area_ref:.1f} px"
        )

    val_loaders = {}
    for mode in EVAL_PROMPT_MODES:
        ds = PromptSegmentationDataset(
            image_dir=os.path.join(DATASET_ROOT, "val", "images"),
            json_dir=os.path.join(DATASET_ROOT, "val", "annotations"),
            img_size=IMG_SIZE, is_train=False,
            prompt_mode=mode,
            **_dataset_kwargs(mode),
        )
        val_loaders[mode] = DataLoader(
            ds,
            batch_size=BATCH_SIZE,
            shuffle=False,
            num_workers=2,
            pin_memory=True,
        )

    # ── Model ────────────────────────────────────────────────────────
    model = PGA_UNet(in_channels=1, n_classes=1,
                     use_encoder_prompt=USE_ENCODER_PROMPT,
                     use_quality_head=USE_QUALITY_HEAD).to(DEVICE)

    if INIT_CHECKPOINT:
        state = torch.load(INIT_CHECKPOINT, map_location=DEVICE)
        missing, unexpected = model.load_state_dict(state, strict=False)
        logger.info(
            f"Loaded INIT_CHECKPOINT={INIT_CHECKPOINT} "
            f"(missing={missing}, unexpected={unexpected})"
        )

    if FREEZE_BACKBONE:
        if not USE_QUALITY_HEAD:
            raise ValueError("FREEZE_BACKBONE=1 only makes sense with USE_QUALITY_HEAD=1.")
        for name, param in model.named_parameters():
            param.requires_grad = name.startswith("quality_head.")
        trainable_params = [p for p in model.parameters() if p.requires_grad]
        n_trainable = sum(p.numel() for p in trainable_params)
        logger.info(f"FREEZE_BACKBONE=1: training only quality_head ({n_trainable} parameters).")
    else:
        trainable_params = model.parameters()

    criterion_bce = nn.BCEWithLogitsLoss()
    optimizer     = optim.AdamW(trainable_params, lr=LR, weight_decay=1e-4)
    scheduler     = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='max', factor=0.5, patience=5)

    os.makedirs("checkpoints", exist_ok=True)
    best_val_dice   = 0.0
    patience_counter = 0
    ckpt_tag = TRAIN_PROMPT_MODE
    if TRAIN_PROMPT_MODE in ('center_zoom', 'center_shift', 'center_mixed'):
        # scale_factor must be in the filename, otherwise the x2/x3 runs
        # would overwrite the same checkpoint. 'center_zoom' training does
        # not depend on shift_ratio at all, so it is left out of the tag
        # unless TRAIN_PROMPT_MODE is 'center_shift' or 'center_mixed'.
        scale_tag = str(PROMPT_SCALE_FACTOR).rstrip('0').rstrip('.') if '.' in str(PROMPT_SCALE_FACTOR) else str(PROMPT_SCALE_FACTOR)
        ckpt_tag = f"center_zoom_x{scale_tag}"
        if TRAIN_PROMPT_MODE == 'center_shift':
            shift_tag = f"shift{str(PROMPT_SHIFT_RATIO).replace('.', '')}"
            ckpt_tag = f"center_shift_x{scale_tag}_{shift_tag}"
        elif TRAIN_PROMPT_MODE == 'center_mixed':
            shift_tag = f"shift{str(PROMPT_SHIFT_RATIO).replace('.', '')}"
            ckpt_tag = f"center_mixed_x{scale_tag}_{shift_tag}"
    if USE_QUALITY_HEAD:
        ckpt_tag += "_qhead"
    if USE_SIZE_TVERSKY:
        ckpt_tag += "_sizetversky"
    ckpt_prefix     = f"checkpoints/pga_unet_{ckpt_tag}_{IMG_SIZE}"

    for epoch in range(EPOCHS):
        # ── Train ────────────────────────────────────────────────────
        model.train()
        train_loss = 0.0
        loop = tqdm(train_loader, desc=f"Epoch {epoch+1}/{EPOCHS} [Train]")
        for images, masks, prompts in loop:
            images, masks, prompts = (images.to(DEVICE), masks.to(DEVICE), prompts.to(DEVICE))
            if USE_QUALITY_HEAD and LOSS_CONFIDENCE_WEIGHT > 0:
                preds, pred_quality = model(images, prompts, return_quality=True)
            else:
                preds = model(images, prompts)
            if USE_SIZE_TVERSKY:
                seg_loss = size_weighted_tversky_loss(
                    preds, masks, size_tversky_area_ref, SIZE_TVERSKY_ALPHA_MAX)
            else:
                seg_loss = dice_loss(preds, masks)
            loss  = criterion_bce(preds, masks) + seg_loss
            if USE_QUALITY_HEAD and LOSS_CONFIDENCE_WEIGHT > 0:
                # QualityHead learns to predict real Dice. Its input (up1)
                # is detached inside the model itself, so this loss only
                # ever updates the head's own small MLP, never the shared
                # encoder/decoder; detaching the target here too is just
                # for clarity, since per_sample_dice's thresholding already
                # blocks gradient from flowing through it either way.
                real_dice = per_sample_dice(preds, masks).detach()
                confidence_loss = F.mse_loss(pred_quality, real_dice)
                loss = loss + LOSS_CONFIDENCE_WEIGHT * confidence_loss
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            train_loss += loss.item()
            loop.set_postfix(loss=f"{loss.item():.4f}")

        train_loss_avg = train_loss / len(train_loader)

        # ── Validate (all loaders) ─────────────────────────────
        model.eval()
        val_results = {}
        with torch.no_grad():
            for vname, vloader in val_loaders.items():
                s_dice, s_iou, s_pre, s_rec = 0, 0, 0, 0
                s_cbl, n_cbl, n_total = 0, 0, 0
                for vi, vm, vp in vloader:
                    vi, vm, vp = vi.to(DEVICE), vm.to(DEVICE), vp.to(DEVICE)
                    vout = model(vi, vp)
                    d, i, p, r = batch_metrics_sum(vout, vm)
                    s_dice += d; s_iou += i; s_pre += p; s_rec += r
                    cb, ncb = calculate_cbl(vout, vm)
                    s_cbl += cb; n_cbl += ncb
                    n_total += vi.size(0)
                val_results[vname] = {
                    'dice': s_dice / n_total,
                    'iou':  s_iou  / n_total,
                    'pre':  s_pre  / n_total,
                    'rec':  s_rec  / n_total,
                    'cbl':  s_cbl  / n_cbl if n_cbl > 0 else 0.0,
                }

        primary_dice = val_results[PRIMARY_VAL_MODE]['dice']
        scheduler.step(primary_dice)

        # Log
        log_str = f"Epoch {epoch+1:3d} | T_Loss: {train_loss_avg:.4f}"
        for vname, vr in val_results.items():
            tag = vname.upper()[:7]
            log_str += (f" | [{tag}] Dice:{vr['dice']:.4f} IoU:{vr['iou']:.4f}"
                        f" CBL:{vr['cbl']:.4f}")
        log_str += f" | LR:{optimizer.param_groups[0]['lr']:.1e}"

        torch.save(model.state_dict(), f"{ckpt_prefix}_last.pth")

        # Note for FREEZE_BACKBONE=1 runs: primary_dice is a frozen-backbone
        # segmentation score, so with a deterministic val set it stays
        # constant every epoch and "best" effectively locks in after epoch 1
        # regardless of how quality_head training progresses. Use
        # {ckpt_prefix}_last.pth, not _best.pth, to get the fully-trained
        # quality_head in that case.
        if primary_dice > best_val_dice:
            best_val_dice = primary_dice
            torch.save(model.state_dict(), f"{ckpt_prefix}_best.pth")
            log_str = "🥇 [BEST] " + log_str
            patience_counter = 0
        else:
            patience_counter += 1

        logger.info(log_str)

        if patience_counter >= EARLY_STOP:
            logger.info(f"Early stopping at epoch {epoch+1}.")
            break

    logger.info(f"\nBest Dice ({PRIMARY_VAL_MODE}): {best_val_dice:.4f}")
    logger.info(f"Checkpoint: {ckpt_prefix}_best.pth")


if __name__ == "__main__":
    main()
