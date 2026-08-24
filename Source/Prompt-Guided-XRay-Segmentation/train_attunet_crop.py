import os
import cv2
import json
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader
from tqdm.auto import tqdm
import logging
import datetime
import numpy as np
import torchvision.transforms.functional as TF
from torchvision.transforms import InterpolationMode
import random

from dataset import PromptSegmentationDataset
from models.networks.attention_unet_2D import Attention_UNet_2D

DEVICE            = torch.device("cuda" if torch.cuda.is_available() else "cpu")
TRAINING_SEED = 22120196
random.seed(TRAINING_SEED)
np.random.seed(TRAINING_SEED)
torch.manual_seed(TRAINING_SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(TRAINING_SEED)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

BATCH_SIZE        = 4
EPOCHS            = 150
LR                = 1e-4
WEIGHT_DECAY      = 1e-4
IMG_SIZE          = 512
PATIENCE          = 15
SCHED_PATIENCE    = 5
TRAIN_PROMPT_MODE = "center_mixed"


class CroppedPromptDataset(PromptSegmentationDataset):
    """Per-polygon prompt dataset that crops the image to the prompt box
    before letterboxing, instead of building a heatmap over the whole
    image. Reuses the parent class's sample indexing and bbox helpers
    unchanged; only __getitem__ is overridden.
    """

    @staticmethod
    def _bbox_to_int_bounds(bx_min, by_min, bx_max, by_max, orig_h, orig_w):
        ix_min = int(np.floor(bx_min))
        iy_min = int(np.floor(by_min))
        ix_max = int(np.ceil(bx_max))
        iy_max = int(np.ceil(by_max))
        ix_min = max(0, min(ix_min, orig_w - 1))
        iy_min = max(0, min(iy_min, orig_h - 1))
        ix_max = max(ix_min + 1, min(ix_max, orig_w))
        iy_max = max(iy_min + 1, min(iy_max, orig_h))
        return ix_min, iy_min, ix_max, iy_max

    def __getitem__(self, idx):
        img_name, shape_idx = self.all_samples[idx]
        base = os.path.splitext(img_name)[0]

        image = cv2.imread(os.path.join(self.image_dir, img_name), cv2.IMREAD_GRAYSCALE)
        orig_h, orig_w = image.shape

        with open(os.path.join(self.json_dir, base + '.json'), 'r', encoding='utf-8') as f:
            data = json.load(f)
        points = np.array(data['shapes'][shape_idx]['points'])

        mask = np.zeros((orig_h, orig_w), dtype=np.uint8)
        cv2.fillPoly(mask, [points.astype(np.int32)], 255)

        x_min, y_min = np.min(points, axis=0)
        x_max, y_max = np.max(points, axis=0)

        if self.prompt_mode == 'center_zoom':
            bx_min, bx_max, by_min, by_max = self._center_zoom_bbox(
                x_min, x_max, y_min, y_max, orig_h, orig_w)
        elif self.prompt_mode == 'center_shift':
            bx_min, bx_max, by_min, by_max = self._center_shift_bbox(
                x_min, x_max, y_min, y_max, orig_h, orig_w, seed_idx=idx)
        elif self.prompt_mode == 'center_mixed':
            # Not a method on the parent class: mirrors the parent's own
            # 'center_mixed' dispatch (same self.mixed_shift_prob weighting),
            # since the parent's version is inline in its own __getitem__
            # and returns image/mask/prompt rather than a box, so it cannot
            # be called directly here.
            if random.random() < self.mixed_shift_prob:
                bx_min, bx_max, by_min, by_max = self._center_shift_bbox(
                    x_min, x_max, y_min, y_max, orig_h, orig_w, seed_idx=idx)
            else:
                bx_min, bx_max, by_min, by_max = self._center_zoom_bbox(
                    x_min, x_max, y_min, y_max, orig_h, orig_w)
        else:
            raise ValueError(f"Unknown prompt_mode: {self.prompt_mode}")

        ix_min, iy_min, ix_max, iy_max = self._bbox_to_int_bounds(
            bx_min, by_min, bx_max, by_max, orig_h, orig_w)

        image_crop = image[iy_min:iy_max, ix_min:ix_max]
        mask_crop = mask[iy_min:iy_max, ix_min:ix_max]

        image_crop = self._resize_and_pad(image_crop, cv2.INTER_LINEAR, pad_value=0)
        mask_crop = self._resize_and_pad(mask_crop, cv2.INTER_NEAREST, pad_value=0)

        image_crop = (image_crop.astype(np.float32) / 255.0 - 0.5) / 0.5
        mask_crop = (mask_crop > 127).astype(np.float32)

        image_t = torch.from_numpy(image_crop).unsqueeze(0)
        mask_t = torch.from_numpy(mask_crop).unsqueeze(0)

        if self.is_train:
            if random.random() >= 0.5:
                image_t, mask_t = TF.hflip(image_t), TF.hflip(mask_t)
            if random.random() >= 0.5:
                angle = random.uniform(-15, 15)
                image_t = TF.rotate(image_t, angle, interpolation=InterpolationMode.BILINEAR)
                mask_t = TF.rotate(mask_t, angle, interpolation=InterpolationMode.NEAREST)
        mask_t = (mask_t > 0.5).float()

        bbox_t = torch.tensor([ix_min, iy_min, ix_max, iy_max], dtype=torch.long)
        orig_hw_t = torch.tensor([orig_h, orig_w], dtype=torch.long)
        return image_t, mask_t, bbox_t, orig_hw_t


def dice_loss(pred, target, smooth=1e-5):
    pred_soft = torch.sigmoid(pred)
    intersection = (pred_soft * target).sum(dim=(1, 2, 3))
    union = pred_soft.sum(dim=(1, 2, 3)) + target.sum(dim=(1, 2, 3))
    return (1 - (2. * intersection + smooth) / (union + smooth)).mean()


def batch_metrics_sum(pred, target, smooth=1e-5):
    pred_bin = (torch.sigmoid(pred) > 0.5).float()
    tp = (pred_bin * target).sum(dim=(1, 2, 3))
    fp = (pred_bin * (1 - target)).sum(dim=(1, 2, 3))
    fn = ((1 - pred_bin) * target).sum(dim=(1, 2, 3))
    dice = (2. * tp + smooth) / (2. * tp + fp + fn + smooth)
    iou = (tp + smooth) / (tp + fp + fn + smooth)
    precision = tp / (tp + fp + smooth)
    recall = tp / (tp + fn + smooth)
    return dice.sum().item(), iou.sum().item(), precision.sum().item(), recall.sum().item()


def setup_logger():
    os.makedirs("logs", exist_ok=True)
    t = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    logging.basicConfig(
        level=logging.INFO, format='%(message)s',
        handlers=[logging.FileHandler(f"logs/train_attunet_crop_{t}.log", encoding='utf-8'), logging.StreamHandler()]
    )
    return logging.getLogger()


def main():
    logger = setup_logger()
    logger.info("=" * 90)
    logger.info(f"TRAIN CROP-PROMPT ATTENTION U-NET 2D | Device: {DEVICE}")
    logger.info(f"Batch: {BATCH_SIZE} | MaxEpochs: {EPOCHS} | LR: {LR} | ImgSize: {IMG_SIZE}")
    logger.info(f"WeightDecay: {WEIGHT_DECAY} | EarlyStop patience: {PATIENCE} | TrainPromptMode: {TRAIN_PROMPT_MODE}")
    logger.info("=" * 90)

    dataset_root = os.environ.get("DATASET_ROOT", "dataset_BTXRD")
    train_ds = CroppedPromptDataset(
        image_dir=f"{dataset_root}/train/images", json_dir=f"{dataset_root}/train/annotations",
        img_size=IMG_SIZE, is_train=True, prompt_mode=TRAIN_PROMPT_MODE)
    val_datasets = {
        mode: CroppedPromptDataset(
            image_dir=f"{dataset_root}/val/images",
            json_dir=f"{dataset_root}/val/annotations",
            img_size=IMG_SIZE,
            is_train=False,
            prompt_mode=mode,
        )
        for mode in ("center_zoom", "center_shift")
    }
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, num_workers=2, pin_memory=True)
    val_loaders = {
        mode: DataLoader(ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=2, pin_memory=True)
        for mode, ds in val_datasets.items()
    }

    model = Attention_UNet_2D(in_channels=1, n_classes=1).to(DEVICE)
    criterion_bce = nn.BCEWithLogitsLoss()
    optimizer = optim.AdamW(model.parameters(), lr=LR, weight_decay=WEIGHT_DECAY)
    scheduler = ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=SCHED_PATIENCE, min_lr=1e-7)

    os.makedirs("checkpoints", exist_ok=True)
    best_val_dice = 0.0
    no_improve = 0

    for epoch in range(EPOCHS):
        model.train()
        train_loss = 0.0
        loop = tqdm(train_loader, desc=f"Epoch {epoch+1}/{EPOCHS} [Train]")
        for images, masks, _, _ in loop:
            images, masks = images.to(DEVICE), masks.to(DEVICE)
            preds = model(images)
            loss = criterion_bce(preds, masks) + dice_loss(preds, masks)
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            train_loss += loss.item()
            loop.set_postfix(loss=f"{loss.item():.4f}")

        model.eval()
        val_results = {}
        with torch.no_grad():
            for mode, val_loader in val_loaders.items():
                sum_dice = sum_iou = sum_pre = sum_rec = 0.0
                total = 0
                for vi, vm, _, _ in val_loader:
                    vi, vm = vi.to(DEVICE), vm.to(DEVICE)
                    vout = model(vi)
                    d, i, p, r = batch_metrics_sum(vout, vm)
                    sum_dice += d; sum_iou += i; sum_pre += p; sum_rec += r
                    total += vi.size(0)
                val_results[mode] = {
                    "dice": sum_dice / total,
                    "iou": sum_iou / total,
                    "precision": sum_pre / total,
                    "recall": sum_rec / total,
                }

        primary = val_results["center_shift"]
        val_dice = primary["dice"]
        scheduler.step(val_dice)
        zoom = val_results["center_zoom"]
        log_str = (f"Epoch {epoch+1:3d} | Loss: {train_loss/len(train_loader):.4f} | "
                   f"ZoomDice: {zoom['dice']:.4f} | ShiftDice: {primary['dice']:.4f} | "
                   f"ShiftIoU: {primary['iou']:.4f} | ShiftPre: {primary['precision']:.4f} | "
                   f"ShiftRec: {primary['recall']:.4f} | LR: {optimizer.param_groups[0]['lr']:.2e}")
        torch.save(model.state_dict(), "checkpoints/attunet_crop_last.pth")
        if val_dice > best_val_dice:
            best_val_dice = val_dice
            no_improve = 0
            torch.save(model.state_dict(), "checkpoints/attunet_crop_best.pth")
            log_str = "[BEST] " + log_str
        else:
            no_improve += 1
        logger.info(log_str)
        if no_improve >= PATIENCE:
            logger.info(f"Early stopping at epoch {epoch+1}.")
            break

    logger.info(f"\nBest center_shift crop-frame Dice: {best_val_dice:.4f}")
    logger.info("Checkpoint: checkpoints/attunet_crop_best.pth")

if __name__ == "__main__":
    main()
