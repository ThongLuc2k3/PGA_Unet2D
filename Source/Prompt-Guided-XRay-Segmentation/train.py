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
import random

from dataset import PromptSegmentationDataset
from models.networks.prompt_unet_2D import PGA_UNet

# =========================================================
# Experiment configuration
# =========================================================
# 'center_mixed' independently samples 'center_zoom' or 'center_shift' per
# training example, with P(center_shift) = PROMPT_MIXED_SHIFT_PROB. Weighted
# toward center_shift because a clinician drawing a box freehand rarely
# centers it exactly on the lesion.
TRAIN_PROMPT_MODE     = os.environ.get("PROMPT_MODE", "center_mixed")
PROMPT_SCALE_FACTOR   = float(os.environ.get("PROMPT_SCALE_FACTOR", "3.0"))
PROMPT_SHIFT_RATIO    = float(os.environ.get("PROMPT_SHIFT_RATIO", "0.5"))
PROMPT_MIXED_SHIFT_PROB = float(os.environ.get("PROMPT_MIXED_SHIFT_PROB", "0.8"))
# No-GT confidence: a small QualityHead learns to regress its own sample's
# real Dice during training (LOSS_CONFIDENCE_WEIGHT > 0); at inference it
# needs no ground truth at all. On by default now that this is the main
# protocol; set USE_QUALITY_HEAD=0 to fall back to a plain PGA_UNet.
USE_QUALITY_HEAD       = os.environ.get("USE_QUALITY_HEAD", "1") == "1"
LOSS_CONFIDENCE_WEIGHT = float(os.environ.get("LOSS_CONFIDENCE_WEIGHT", "1.0"))
# Stage 2 (loss function, Research/02_loss_function/): two candidate
# replacements for dice_loss, kept available (off by default) so PGA-UNet
# can be compared separately against the default for the paper. Enabling both is invalid because they replace the same term. Tested at
# center_mixed x3/shift0.5 (50/50 mix): size-conditioned Tversky measured
# worse Dice on the small-lesion subset than plain Dice (0.7561 vs. 0.7781),
# Focal Dice measured no real improvement (0.7786 vs. 0.7781, within noise).
# Neither is the default; both stay available for further comparison.
USE_SIZE_TVERSKY      = os.environ.get("USE_SIZE_TVERSKY", "0") == "1"
SIZE_TVERSKY_ALPHA_MAX = float(os.environ.get("SIZE_TVERSKY_ALPHA_MAX", "0.7"))
SIZE_TVERSKY_AREA_PCTL = float(os.environ.get("SIZE_TVERSKY_AREA_PCTL", "25"))
# Alternative to USE_SIZE_TVERSKY: size-conditioned Tversky only shifted the
# precision/recall balance on the small-lesion subset without raising Dice
# itself. Focal Dice stays symmetric (alpha=beta=0.5, no precision/recall
# bias) and instead raises (1 - Dice) to the focusing exponent 1/FOCAL_GAMMA,
# amplifying gradient on whichever samples are currently furthest from
# Dice=1, so it targets Dice directly rather than trading FP against FN.
# Mutually exclusive with USE_SIZE_TVERSKY (both replace dice_loss).
USE_FOCAL_DICE = os.environ.get("USE_FOCAL_DICE", "0") == "1"
FOCAL_GAMMA    = float(os.environ.get("FOCAL_GAMMA", "1.33"))
USE_ENCODER_PROMPT = True    # True enables PromptSpatialGate in the encoder
DEVICE     = torch.device("cuda" if torch.cuda.is_available() else "cpu")
SEED       = int(os.environ.get("PROMPT_SEED", "22120196"))
BATCH_SIZE = 4
EPOCHS     = int(os.environ.get("PROMPT_EPOCHS", "150"))
LR         = 1e-4
EARLY_STOP = 15
# Validate on both scenarios; 'center_mixed' has no matching validation
# loader (validation always reports the two pure scenarios separately), so
# checkpoint selection falls back to the harder, off-center scenario.
EVAL_PROMPT_MODES = ('center_zoom', 'center_shift')
PRIMARY_VAL_MODE  = 'center_shift' if TRAIN_PROMPT_MODE == 'center_mixed' else TRAIN_PROMPT_MODE
def resolve_img_size():
    return int(os.environ.get("PROMPT_IMG_SIZE", "512"))


def seed_everything(seed):
    """Fix training randomness for reproducible experiment reruns."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


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


def focal_dice_loss(pred, target, gamma=1.33, smooth=1e-5):
    """Focal Dice loss: the ordinary (symmetric) Dice score raised to the
    focusing exponent 1/gamma, so gradient is amplified on samples whose
    current Dice is furthest from 1.0, regardless of whether the gap comes
    from false positives or false negatives. gamma=1.0 makes this identical
    to dice_loss; gamma>1.0 increases the focusing effect. Unlike
    size_weighted_tversky_loss, alpha/beta are always 0.5, so there is no
    built-in precision/recall bias, only a per-sample difficulty weighting.
    """
    pred_soft    = torch.sigmoid(pred)
    intersection = (pred_soft * target).sum(dim=(1, 2, 3))
    union        = pred_soft.sum(dim=(1, 2, 3)) + target.sum(dim=(1, 2, 3))
    dice = (2. * intersection + smooth) / (union + smooth)
    return torch.pow(1 - dice, 1.0 / gamma).mean()


def compute_area_reference(dataset, percentile):
    """One-time scan of the training set's per-sample GT mask area (in
    pixels), used as size_weighted_tversky_loss's large/small boundary.
    Percentile-based rather than a fixed pixel count, so it self-calibrates
    to whatever dataset/resolution is in use.
    """
    areas = [dataset[i][1].sum().item() for i in range(len(dataset))]
    return float(np.percentile(areas, percentile))


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


def image_level_metrics(model, dataset):
    """Evaluate polygon prompts after merging predictions by source image."""
    loader = DataLoader(dataset, batch_size=1, shuffle=False, num_workers=2,
                        pin_memory=True)
    image_groups = {}
    with torch.no_grad():
        for sample_index, (images, masks, prompts) in enumerate(loader):
            images, masks, prompts = images.to(DEVICE), masks.to(DEVICE), prompts.to(DEVICE)
            probabilities = torch.sigmoid(model(images, prompts))[0, 0].cpu().numpy()
            ground_truth = masks[0, 0].cpu().numpy()
            image_name, _ = dataset.all_samples[sample_index]
            if image_name not in image_groups:
                image_groups[image_name] = {
                    'probability': probabilities.copy(),
                    'ground_truth': ground_truth.copy(),
                }
            else:
                group = image_groups[image_name]
                np.maximum(group['probability'], probabilities, out=group['probability'])
                np.maximum(group['ground_truth'], ground_truth, out=group['ground_truth'])

    metric_sums = {'dice': 0.0, 'iou': 0.0, 'pre': 0.0, 'rec': 0.0, 'cbl': 0.0}
    for group in image_groups.values():
        prediction = group['probability'] > 0.5
        target = group['ground_truth'] > 0.5
        tp = np.logical_and(prediction, target).sum()
        fp = np.logical_and(prediction, ~target).sum()
        fn = np.logical_and(~prediction, target).sum()
        smooth = 1e-5
        metric_sums['dice'] += (2 * tp + smooth) / (2 * tp + fp + fn + smooth)
        metric_sums['iou'] += (tp + smooth) / (tp + fp + fn + smooth)
        metric_sums['pre'] += tp / (tp + fp + smooth)
        metric_sums['rec'] += (tp + smooth) / (tp + fn + smooth)

        if target.any() and prediction.any():
            target_y, target_x = np.where(target)
            prediction_y, prediction_x = np.where(prediction)
            target_diagonal = np.sqrt(
                (target_y.max() - target_y.min()) ** 2
                + (target_x.max() - target_x.min()) ** 2
            ) + 1e-6
            distance = np.sqrt(
                (prediction_x.mean() - target_x.mean()) ** 2
                + (prediction_y.mean() - target_y.mean()) ** 2
            )
            metric_sums['cbl'] += max(0.0, 1.0 - distance / target_diagonal)

    image_count = len(image_groups)
    if image_count == 0:
        return {name: 0.0 for name in metric_sums}
    return {name: value / image_count for name, value in metric_sums.items()}


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
    """scale_factor/shift_ratio apply to every mode; mixed_shift_prob only
    applies to 'center_mixed'.
    """
    if mode == 'center_mixed':
        return dict(scale_factor=PROMPT_SCALE_FACTOR, shift_ratio=PROMPT_SHIFT_RATIO,
                    mixed_shift_prob=PROMPT_MIXED_SHIFT_PROB)
    return dict(scale_factor=PROMPT_SCALE_FACTOR, shift_ratio=PROMPT_SHIFT_RATIO)


def main():
    seed_everything(SEED)
    valid_modes = {'center_zoom', 'center_shift', 'center_mixed'}
    if TRAIN_PROMPT_MODE not in valid_modes:
        raise ValueError(f"TRAIN_PROMPT_MODE must be one of {sorted(valid_modes)}.")
    if PRIMARY_VAL_MODE not in EVAL_PROMPT_MODES:
        raise ValueError("PRIMARY_VAL_MODE must be one of EVAL_PROMPT_MODES.")
    if USE_SIZE_TVERSKY and USE_FOCAL_DICE:
        raise ValueError("USE_SIZE_TVERSKY and USE_FOCAL_DICE are mutually exclusive (both replace dice_loss).")

    logger = setup_logger(TRAIN_PROMPT_MODE)
    logger.info("=" * 90)
    logger.info(
        f"TrainPrompt: {TRAIN_PROMPT_MODE} | Device: {DEVICE} | "
        f"EncoderPrompt: {USE_ENCODER_PROMPT} | ImgSize: {IMG_SIZE} | "
        f"DatasetRoot: {DATASET_ROOT} | Seed: {SEED} | ScaleFactor: {PROMPT_SCALE_FACTOR} "
        f"| ShiftRatio: {PROMPT_SHIFT_RATIO} | MixedShiftProb: {PROMPT_MIXED_SHIFT_PROB}"
        + (f" | QualityHead: ConfidenceLossWeight={LOSS_CONFIDENCE_WEIGHT}" if USE_QUALITY_HEAD else "")
        + (f" | SizeTversky: AlphaMax={SIZE_TVERSKY_ALPHA_MAX}, AreaPercentile={SIZE_TVERSKY_AREA_PCTL}" if USE_SIZE_TVERSKY else "")
        + (f" | FocalDice: Gamma={FOCAL_GAMMA}" if USE_FOCAL_DICE else "")
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

    criterion_bce = nn.BCEWithLogitsLoss()
    optimizer     = optim.AdamW(model.parameters(), lr=LR, weight_decay=1e-4)
    scheduler     = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='max', factor=0.5, patience=5)

    os.makedirs("checkpoints", exist_ok=True)
    best_val_dice   = 0.0
    patience_counter = 0
    # scale_factor must be in the filename, otherwise the x2/x3 runs would
    # overwrite the same checkpoint. shift_ratio only matters (and is only
    # named) for the two modes that actually use it.
    scale_tag = str(PROMPT_SCALE_FACTOR).rstrip('0').rstrip('.') if '.' in str(PROMPT_SCALE_FACTOR) else str(PROMPT_SCALE_FACTOR)
    ckpt_tag = f"{TRAIN_PROMPT_MODE}_x{scale_tag}"
    if TRAIN_PROMPT_MODE in ('center_shift', 'center_mixed'):
        ckpt_tag += f"_shift{str(PROMPT_SHIFT_RATIO).replace('.', '')}"
    if USE_QUALITY_HEAD:
        ckpt_tag += "_qhead"
    if USE_SIZE_TVERSKY:
        ckpt_tag += "_sizetversky"
    if USE_FOCAL_DICE:
        gamma_tag = str(FOCAL_GAMMA).replace('.', '')
        ckpt_tag += f"_focaldice{gamma_tag}"
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
            elif USE_FOCAL_DICE:
                seg_loss = focal_dice_loss(preds, masks, FOCAL_GAMMA)
            else:
                seg_loss = dice_loss(preds, masks)
            loss = criterion_bce(preds, masks) + seg_loss
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
        for vname, vloader in val_loaders.items():
            merged = image_level_metrics(model, vloader.dataset)
            val_results[vname] = {
                'dice': merged['dice'],
                'iou':  merged['iou'],
                'pre':  merged['pre'],
                'rec':  merged['rec'],
                'cbl':  merged['cbl'],
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
