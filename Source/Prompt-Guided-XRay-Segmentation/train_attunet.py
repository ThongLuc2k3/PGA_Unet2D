import os
import cv2
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader, Dataset
from tqdm.auto import tqdm
import logging
import datetime
import numpy as np
import torchvision.transforms.functional as TF
from torchvision.transforms import InterpolationMode
import random

from models.networks.attention_unet_2D import Attention_UNet_2D

DEVICE         = torch.device("cuda" if torch.cuda.is_available() else "cpu")
TRAINING_SEED = 22120196
random.seed(TRAINING_SEED)
np.random.seed(TRAINING_SEED)
torch.manual_seed(TRAINING_SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(TRAINING_SEED)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

BATCH_SIZE     = 4
EPOCHS         = 150
LR             = 1e-4
WEIGHT_DECAY   = 1e-4
IMG_SIZE       = 512
PATIENCE       = 15
SCHED_PATIENCE = 5

class ImageMaskDataset(Dataset):
    """Image-level dataset using the same resize and padding policy as PGA."""
    def __init__(self, image_dir, mask_dir, img_size=512, is_train=True):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.img_size = img_size
        self.is_train = is_train
        image_names = sorted(
            f for f in os.listdir(image_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        )
        mask_by_stem = {}
        for mask_name in sorted(os.listdir(mask_dir)):
            if not mask_name.lower().endswith((".png", ".jpg", ".jpeg")):
                continue
            stem = os.path.splitext(mask_name)[0]
            if stem in mask_by_stem:
                raise ValueError(f"Duplicate mask stem: {stem}")
            mask_by_stem[stem] = mask_name
        missing = [name for name in image_names if os.path.splitext(name)[0] not in mask_by_stem]
        if missing:
            raise FileNotFoundError(f"Missing masks for {len(missing)} images: {missing[:5]}")
        self.samples = [
            (image_name, mask_by_stem[os.path.splitext(image_name)[0]])
            for image_name in image_names
        ]

    def __len__(self):
        return len(self.samples)

    def _resize_and_pad(self, array, interpolation, pad_value=0):
        orig_h, orig_w = array.shape[:2]
        scale = min(self.img_size / orig_w, self.img_size / orig_h)
        new_w = max(1, int(round(orig_w * scale)))
        new_h = max(1, int(round(orig_h * scale)))
        resized = cv2.resize(array, (new_w, new_h), interpolation=interpolation)
        padded = np.full((self.img_size, self.img_size), pad_value, dtype=resized.dtype)
        pad_left = (self.img_size - new_w) // 2
        pad_top = (self.img_size - new_h) // 2
        padded[pad_top:pad_top + new_h, pad_left:pad_left + new_w] = resized
        return padded

    def __getitem__(self, idx):
        img_name, mask_name = self.samples[idx]
        image = cv2.imread(os.path.join(self.image_dir, img_name), cv2.IMREAD_GRAYSCALE)
        mask = cv2.imread(os.path.join(self.mask_dir, mask_name), cv2.IMREAD_GRAYSCALE)
        image = self._resize_and_pad(image, cv2.INTER_LINEAR, pad_value=0)
        mask = self._resize_and_pad(mask, cv2.INTER_NEAREST, pad_value=0)
        image = (image.astype(np.float32) / 255.0 - 0.5) / 0.5
        mask = (mask > 127).astype(np.float32)
        image = torch.from_numpy(image).unsqueeze(0)
        mask = torch.from_numpy(mask).unsqueeze(0)
        if self.is_train:
            if random.random() >= 0.5:
                image, mask = TF.hflip(image), TF.hflip(mask)
            if random.random() >= 0.5:
                angle = random.uniform(-15, 15)
                image = TF.rotate(image, angle, interpolation=InterpolationMode.BILINEAR)
                mask = TF.rotate(mask, angle, interpolation=InterpolationMode.NEAREST)
        mask = (mask > 0.5).float()
        return image, mask


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
        handlers=[logging.FileHandler(f"logs/train_attunet_{t}.log", encoding='utf-8'), logging.StreamHandler()]
    )
    return logging.getLogger()


def main():
    logger = setup_logger()
    logger.info("=" * 90)
    logger.info(f"TRAIN ATTENTION U-NET 2D | Device: {DEVICE}")
    logger.info(f"Batch: {BATCH_SIZE} | MaxEpochs: {EPOCHS} | LR: {LR} | ImgSize: {IMG_SIZE}")
    logger.info(f"WeightDecay: {WEIGHT_DECAY} | EarlyStop patience: {PATIENCE}")
    logger.info("=" * 90)

    dataset_root = os.environ.get("DATASET_ROOT", "dataset_BTXRD")
    train_ds = ImageMaskDataset(f"{dataset_root}/train/images", f"{dataset_root}/train/masks", img_size=IMG_SIZE, is_train=True)
    val_ds = ImageMaskDataset(f"{dataset_root}/val/images", f"{dataset_root}/val/masks", img_size=IMG_SIZE, is_train=False)
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, num_workers=2, pin_memory=True)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=2, pin_memory=True)

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
        for images, masks in loop:
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
        sum_dice = sum_iou = sum_pre = sum_rec = 0.0
        total = 0
        with torch.no_grad():
            for vi, vm in val_loader:
                vi, vm = vi.to(DEVICE), vm.to(DEVICE)
                vout = model(vi)
                d, i, p, r = batch_metrics_sum(vout, vm)
                sum_dice += d; sum_iou += i; sum_pre += p; sum_rec += r
                total += vi.size(0)

        val_dice = sum_dice / total
        scheduler.step(val_dice)
        log_str = (f"Epoch {epoch+1:3d} | Loss: {train_loss/len(train_loader):.4f} | "
                   f"Dice: {val_dice:.4f} | IoU: {sum_iou/total:.4f} | "
                   f"Pre: {sum_pre/total:.4f} | Rec: {sum_rec/total:.4f} | "
                   f"LR: {optimizer.param_groups[0]['lr']:.2e}")
        torch.save(model.state_dict(), "checkpoints/attunet_last.pth")
        if val_dice > best_val_dice:
            best_val_dice = val_dice
            no_improve = 0
            torch.save(model.state_dict(), "checkpoints/att_unet_best.pth")
            log_str = "[BEST] " + log_str
        else:
            no_improve += 1
        logger.info(log_str)
        if no_improve >= PATIENCE:
            logger.info(f"Early stopping at epoch {epoch+1}.")
            break

    logger.info(f"\nBest Dice: {best_val_dice:.4f}")
    logger.info("Checkpoint: checkpoints/att_unet_best.pth")

if __name__ == "__main__":
    main()
