# ==============================================================================
# 1_unet.py — U-Net 2D (Baseline)
# ==============================================================================
# Kiến trúc Encoder-Decoder với skip connections, không có Attention/Prompt.
# Dataset đã được chuẩn bị (resize, split train/val) từ bước tiền xử lý ngoài.
# ==============================================================================

import os
import datetime
import logging
import random

import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.nn import init
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms.functional as TF
from tqdm import tqdm


# ==============================================================================
# TIỆN ÍCH: KHỞI TẠO TRỌNG SỐ
# ==============================================================================

def init_weights(net, init_type='kaiming'):
    def _kaiming(m):
        cls = m.__class__.__name__
        if 'Conv' in cls:
            init.kaiming_normal_(m.weight.data, a=0, mode='fan_in')
        elif 'Linear' in cls:
            init.kaiming_normal_(m.weight.data, a=0, mode='fan_in')
        elif 'BatchNorm' in cls:
            init.normal_(m.weight.data, 1.0, 0.02)
            init.constant_(m.bias.data, 0.0)
    net.apply(_kaiming)


# ==============================================================================
# KHỐI CƠ BẢN
# ==============================================================================

class unetConv2(nn.Module):
    """Hai lớp [Conv 3×3 → BN → ReLU] liên tiếp."""
    def __init__(self, in_size, out_size, is_batchnorm=True):
        super().__init__()
        if is_batchnorm:
            self.conv1 = nn.Sequential(
                nn.Conv2d(in_size,  out_size, 3, 1, 1),
                nn.BatchNorm2d(out_size), nn.ReLU(inplace=True))
            self.conv2 = nn.Sequential(
                nn.Conv2d(out_size, out_size, 3, 1, 1),
                nn.BatchNorm2d(out_size), nn.ReLU(inplace=True))
        else:
            self.conv1 = nn.Sequential(
                nn.Conv2d(in_size,  out_size, 3, 1, 1), nn.ReLU(inplace=True))
            self.conv2 = nn.Sequential(
                nn.Conv2d(out_size, out_size, 3, 1, 1), nn.ReLU(inplace=True))
        init_weights(self)

    def forward(self, x):
        return self.conv2(self.conv1(x))


class unetUp(nn.Module):
    """
    Khối giải mã chuẩn của U-Net:
      gating  → ConvTranspose2d (upsample ×2)
      skip    → căn chỉnh kích thước
      Concat(skip, up) → unetConv2
    """
    def __init__(self, in_size, out_size, is_deconv=True):
        super().__init__()
        self.conv = unetConv2(in_size, out_size, is_batchnorm=False)
        self.up   = (nn.ConvTranspose2d(in_size, out_size, kernel_size=4, stride=2, padding=1)
                     if is_deconv else nn.UpsamplingBilinear2d(scale_factor=2))
        init_weights(self.up)

    def forward(self, skip, gating):
        up     = self.up(gating)
        offset = up.size(2) - skip.size(2)
        pad    = 2 * [offset // 2, offset // 2]
        skip   = F.pad(skip, pad)
        return self.conv(torch.cat([skip, up], dim=1))


# ==============================================================================
# MÔ HÌNH U-NET 2D
# ==============================================================================

class UNet2D(nn.Module):
    """
    U-Net 2D tiêu chuẩn.

    Luồng dữ liệu:
        Input (B,1,H,W)
          ↓ Encoder (4 tầng): conv + MaxPool — feature maps c1..c4
          ↓ Bottleneck: center
          ↑ Decoder (4 tầng): unetUp(skip=ci, gating=prev) — lần lượt up4..up1
          ↓ Conv 1×1 → logit đầu ra (B,1,H,W)

    feature_scale=4  →  filters = [16, 32, 64, 128, 256]
    """
    def __init__(self, in_channels=1, n_classes=1,
                 feature_scale=4, is_batchnorm=True, is_deconv=True):
        super().__init__()
        f = [int(x / feature_scale) for x in [64, 128, 256, 512, 1024]]

        # Encoder
        self.conv1 = unetConv2(in_channels, f[0], is_batchnorm)
        self.pool1 = nn.MaxPool2d(2)
        self.conv2 = unetConv2(f[0], f[1], is_batchnorm)
        self.pool2 = nn.MaxPool2d(2)
        self.conv3 = unetConv2(f[1], f[2], is_batchnorm)
        self.pool3 = nn.MaxPool2d(2)
        self.conv4 = unetConv2(f[2], f[3], is_batchnorm)
        self.pool4 = nn.MaxPool2d(2)

        # Bottleneck
        self.center = unetConv2(f[3], f[4], is_batchnorm)

        # Decoder
        self.up4 = unetUp(f[4], f[3], is_deconv)
        self.up3 = unetUp(f[3], f[2], is_deconv)
        self.up2 = unetUp(f[2], f[1], is_deconv)
        self.up1 = unetUp(f[1], f[0], is_deconv)

        # Đầu ra
        self.final = nn.Conv2d(f[0], n_classes, kernel_size=1)

        for m in self.modules():
            if isinstance(m, (nn.Conv2d, nn.BatchNorm2d)):
                init_weights(m)

    def forward(self, x):
        c1 = self.conv1(x);       p1 = self.pool1(c1)
        c2 = self.conv2(p1);      p2 = self.pool2(c2)
        c3 = self.conv3(p2);      p3 = self.pool3(c3)
        c4 = self.conv4(p3);      p4 = self.pool4(c4)
        cn = self.center(p4)
        u4 = self.up4(c4, cn)
        u3 = self.up3(c3, u4)
        u2 = self.up2(c2, u3)
        u1 = self.up1(c1, u2)
        return self.final(u1)


# ==============================================================================
# DATASET
# Giả định: ảnh grayscale (.png/.jpg) và mask nhị phân cùng tên đã chuẩn bị sẵn.
# ==============================================================================

class BTXRD_Dataset(Dataset):
    def __init__(self, image_dir, mask_dir, img_size=256, is_train=True):
        self.image_dir = image_dir
        self.mask_dir  = mask_dir
        self.img_size  = img_size
        self.is_train  = is_train
        self.files = sorted(f for f in os.listdir(image_dir)
                            if f.endswith(('.png', '.jpg')))

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        name = self.files[idx]
        img  = cv2.imread(os.path.join(self.image_dir, name), cv2.IMREAD_GRAYSCALE)
        mask = cv2.imread(os.path.join(self.mask_dir,  name), cv2.IMREAD_GRAYSCALE)

        img  = cv2.resize(img,  (self.img_size, self.img_size))
        mask = cv2.resize(mask, (self.img_size, self.img_size),
                          interpolation=cv2.INTER_NEAREST)

        img  = img.astype(np.float32) / 255.0
        mask = (mask.astype(np.float32) / 255.0 > 0.5).astype(np.float32)

        img  = torch.from_numpy(img).unsqueeze(0)   # [1, H, W]
        mask = torch.from_numpy(mask).unsqueeze(0)  # [1, H, W]

        if self.is_train and random.random() > 0.5:
            img, mask = TF.hflip(img), TF.hflip(mask)

        return img, mask


# ==============================================================================
# LOSS & METRICS
# ==============================================================================

def dice_loss(pred, target, smooth=1e-5):
    prob  = torch.sigmoid(pred)
    inter = (prob * target).sum(dim=(1, 2, 3))
    union = prob.sum(dim=(1, 2, 3)) + target.sum(dim=(1, 2, 3))
    return (1 - (2. * inter + smooth) / (union + smooth)).mean()


def batch_metrics(pred, target, smooth=1e-5):
    """Trả về (sum_dice, sum_iou, sum_prec, sum_rec) trên cả batch."""
    pred_bin = (torch.sigmoid(pred) > 0.5).float()
    tp = (pred_bin * target).sum(dim=(1, 2, 3))
    fp = (pred_bin * (1 - target)).sum(dim=(1, 2, 3))
    fn = ((1 - pred_bin) * target).sum(dim=(1, 2, 3))
    dice = (2*tp + smooth) / (2*tp + fp + fn + smooth)
    iou  = (tp + smooth) / (tp + fp + fn + smooth)
    prec = (tp + smooth) / (tp + fp + smooth)
    rec  = (tp + smooth) / (tp + fn + smooth)
    return dice.sum().item(), iou.sum().item(), prec.sum().item(), rec.sum().item()


# ==============================================================================
# CẤU HÌNH HUẤN LUYỆN
# ==============================================================================

DEVICE     = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BATCH_SIZE = 8
EPOCHS     = 50
LR         = 1e-4
IMG_SIZE   = 256


def setup_logger(name):
    os.makedirs("logs", exist_ok=True)
    t = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    logging.basicConfig(
        level=logging.INFO, format='%(message)s',
        handlers=[logging.FileHandler(f"logs/{name}_{t}.log", encoding='utf-8'),
                  logging.StreamHandler()])
    return logging.getLogger()


# ==============================================================================
# VÒNG LẶP HUẤN LUYỆN
# ==============================================================================

def main():
    logger = setup_logger("unet")
    logger.info(f"{'='*70}")
    logger.info(f"TRAIN U-Net 2D (Baseline) | Device: {DEVICE}")
    logger.info(f"Batch: {BATCH_SIZE} | Epochs: {EPOCHS} | LR: {LR} | ImgSize: {IMG_SIZE}")
    logger.info(f"{'='*70}")

    train_ds = BTXRD_Dataset("dataset_BTXRD/train/images",
                             "dataset_BTXRD/train/masks", IMG_SIZE, is_train=True)
    val_ds   = BTXRD_Dataset("dataset_BTXRD/val/images",
                             "dataset_BTXRD/val/masks",   IMG_SIZE, is_train=False)
    train_loader = DataLoader(train_ds, BATCH_SIZE, shuffle=True,  num_workers=2, pin_memory=True)
    val_loader   = DataLoader(val_ds,   BATCH_SIZE, shuffle=False, num_workers=2, pin_memory=True)

    model     = UNet2D(in_channels=1, n_classes=1).to(DEVICE)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.AdamW(model.parameters(), lr=LR)

    os.makedirs("checkpoints", exist_ok=True)
    best_dice = 0.0

    for epoch in range(EPOCHS):
        # --- Train ---
        model.train()
        train_loss = 0.0
        loop = tqdm(train_loader, desc=f"Epoch {epoch+1}/{EPOCHS} [Train]")
        for imgs, masks in loop:
            imgs, masks = imgs.to(DEVICE), masks.to(DEVICE)
            preds = model(imgs)
            loss  = criterion(preds, masks) + dice_loss(preds, masks)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
            loop.set_postfix(loss=f"{loss.item():.4f}")

        # --- Validate ---
        model.eval()
        s_d = s_i = s_p = s_r = total = 0
        with torch.no_grad():
            for vi, vm in val_loader:
                vi, vm = vi.to(DEVICE), vm.to(DEVICE)
                d, i, p, r = batch_metrics(model(vi), vm)
                s_d += d; s_i += i; s_p += p; s_r += r
                total += vi.size(0)

        vdice = s_d / total
        log = (f"Epoch {epoch+1:3d} | Loss: {train_loss/len(train_loader):.4f} | "
               f"Dice: {vdice:.4f} | IoU: {s_i/total:.4f} | "
               f"Prec: {s_p/total:.4f} | Rec: {s_r/total:.4f}")

        torch.save(model.state_dict(), "checkpoints/unet_last.pth")
        if vdice > best_dice:
            best_dice = vdice
            torch.save(model.state_dict(), "checkpoints/unet_best.pth")
            log = "[BEST] " + log
        logger.info(log)

    logger.info(f"\nBest Dice: {best_dice:.4f}")
    logger.info("Checkpoint: checkpoints/unet_best.pth")


if __name__ == "__main__":
    main()
