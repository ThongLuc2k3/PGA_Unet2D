import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader
from tqdm.auto import tqdm
import logging
import datetime

from dataset_simple import BTXRD_Dataset
from models.networks.unet_2D import unet_2D

# =========================================================
# CAU HINH — CHOT CUOI (CONG BANG VOI ATTUNET & PGA)
# =========================================================
DEVICE        = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BATCH_SIZE    = 4
EPOCHS        = 100
LR            = 1e-4
WEIGHT_DECAY  = 1e-4
IMG_SIZE      = 512
PATIENCE      = 15
SCHED_PATIENCE = 5


# =========================================================
# LOSS & METRICS
# =========================================================
def dice_loss(pred, target, smooth=1e-5):
    pred_soft    = torch.sigmoid(pred)
    intersection = (pred_soft * target).sum(dim=(1, 2, 3))
    union        = pred_soft.sum(dim=(1, 2, 3)) + target.sum(dim=(1, 2, 3))
    return (1 - (2. * intersection + smooth) / (union + smooth)).mean()


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


def setup_logger():
    os.makedirs("logs", exist_ok=True)
    t = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    logging.basicConfig(
        level=logging.INFO, format='%(message)s',
        handlers=[
            logging.FileHandler(f"logs/train_unet_{t}.log", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger()


def main():
    logger = setup_logger()
    logger.info("=" * 90)
    logger.info(f"TRAIN U-NET 2D | Device: {DEVICE}")
    logger.info(f"Batch: {BATCH_SIZE} | MaxEpochs: {EPOCHS} | LR: {LR} | ImgSize: {IMG_SIZE}")
    logger.info(f"WeightDecay: {WEIGHT_DECAY} | EarlyStop patience: {PATIENCE}")
    logger.info("=" * 90)

    train_ds = BTXRD_Dataset(
        image_dir="dataset_BTXRD/train/images",
        mask_dir="dataset_BTXRD/train/masks",
        img_size=IMG_SIZE, is_train=True
    )
    val_ds = BTXRD_Dataset(
        image_dir="dataset_BTXRD/val/images",
        mask_dir="dataset_BTXRD/val/masks",
        img_size=IMG_SIZE, is_train=False
    )
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True,  num_workers=2, pin_memory=True)
    val_loader   = DataLoader(val_ds,   batch_size=BATCH_SIZE, shuffle=False, num_workers=2, pin_memory=True)

    model         = unet_2D(in_channels=1, n_classes=1).to(DEVICE)
    criterion_bce = nn.BCEWithLogitsLoss()
    optimizer     = optim.AdamW(model.parameters(), lr=LR, weight_decay=WEIGHT_DECAY)
    scheduler     = ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=SCHED_PATIENCE, min_lr=1e-7)

    os.makedirs("checkpoints", exist_ok=True)
    best_val_dice = 0.0
    no_improve    = 0

    for epoch in range(EPOCHS):
        model.train()
        train_loss = 0.0
        loop = tqdm(train_loader, desc=f"Epoch {epoch+1}/{EPOCHS} [Train]")
        for images, masks in loop:
            images, masks = images.to(DEVICE), masks.to(DEVICE)
            preds = model(images)
            loss  = criterion_bce(preds, masks) + dice_loss(preds, masks)
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            train_loss += loss.item()
            loop.set_postfix(loss=f"{loss.item():.4f}")

        model.eval()
        sum_dice, sum_iou, sum_pre, sum_rec = 0, 0, 0, 0
        total = 0
        with torch.no_grad():
            for vi, vm in val_loader:
                vi, vm = vi.to(DEVICE), vm.to(DEVICE)
                vout   = model(vi)
                d, i, p, r = batch_metrics_sum(vout, vm)
                sum_dice += d; sum_iou += i; sum_pre += p; sum_rec += r
                total += vi.size(0)

        val_dice = sum_dice / total
        scheduler.step(val_dice)

        log_str = (f"Epoch {epoch+1:3d} | Loss: {train_loss/len(train_loader):.4f} | "
                   f"Dice: {val_dice:.4f} | IoU: {sum_iou/total:.4f} | "
                   f"Pre: {sum_pre/total:.4f} | Rec: {sum_rec/total:.4f} | "
                   f"LR: {optimizer.param_groups[0]['lr']:.2e}")

        torch.save(model.state_dict(), "checkpoints/unet_last.pth")
        if val_dice > best_val_dice:
            best_val_dice = val_dice
            no_improve    = 0
            torch.save(model.state_dict(), "checkpoints/unet_best.pth")
            log_str = "[BEST] " + log_str
        else:
            no_improve += 1

        logger.info(log_str)

        if no_improve >= PATIENCE:
            logger.info(f"\nEarly stopping at epoch {epoch+1} (no improve for {PATIENCE} epochs)")
            break

    logger.info(f"\nBest Val Dice: {best_val_dice:.4f}")
    logger.info("Checkpoint: checkpoints/unet_best.pth")


if __name__ == "__main__":
    main()
