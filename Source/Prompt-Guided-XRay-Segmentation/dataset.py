import os
import cv2
import json
import torch
import numpy as np
from torch.utils.data import Dataset
import torchvision.transforms.functional as TF
from torchvision.transforms import InterpolationMode
import random


class PromptSegmentationDataset(Dataset):
    """
    Generic polygon-to-prompt dataset for prompt-guided lesion segmentation.
    Each sample corresponds to one GT polygon inside one image.

    prompt_mode:
        'zoom_out'   – covering prompt expanded around the GT
        'shift'      – covering prompt with an off-center displacement
    """

    def __init__(self, image_dir, json_dir, img_size=512, is_train=True,
                 prompt_mode='zoom_out',
                 zoom_ratio=(0.15, 0.45),
                 shift_ratio=0.30):
        self.image_dir   = image_dir
        self.json_dir    = json_dir
        self.img_size    = img_size
        self.is_train    = is_train
        self.prompt_mode = prompt_mode
        self.zoom_ratio  = zoom_ratio
        self.shift_ratio = shift_ratio
        self.min_prompt_margin_px = max(1, int(round(5 * (self.img_size / 256.0))))

        kernel = int(round(31 * (self.img_size / 256.0)))
        self.prompt_kernel = kernel if kernel % 2 == 1 else kernel - 1
        self.prompt_kernel = max(3, self.prompt_kernel)

        self.all_samples = []
        for img_name in sorted(os.listdir(image_dir)):
            if not img_name.endswith(('.png', '.jpg')):
                continue
            base = os.path.splitext(img_name)[0]
            json_path = os.path.join(json_dir, base + '.json')
            if not os.path.exists(json_path):
                continue
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for i, s in enumerate(data.get('shapes', [])):
                if s.get('shape_type') == 'polygon':
                    self.all_samples.append((img_name, i))

    def __len__(self):
        return len(self.all_samples)

    # ── Prompt helpers ────────────────────────────────────────────────

    def _ensure_min_prompt_margin(self, bx_min, bx_max, by_min, by_max,
                                  x_min, x_max, y_min, y_max, orig_h, orig_w):
        """
        Ensure the prompt box does not hug the GT boundary too tightly when
        image space is still available. The minimum context margin is enforced
        at box generation time rather than as a post-hoc heatmap expansion.
        """
        margin = float(self.min_prompt_margin_px)

        left_gap = x_min - bx_min
        right_gap = bx_max - x_max
        top_gap = y_min - by_min
        bottom_gap = by_max - y_max

        if left_gap < margin:
            bx_min = max(0.0, min(bx_min, x_min - margin))
        if right_gap < margin:
            bx_max = min(float(orig_w), max(bx_max, x_max + margin))
        if top_gap < margin:
            by_min = max(0.0, min(by_min, y_min - margin))
        if bottom_gap < margin:
            by_max = min(float(orig_h), max(by_max, y_max + margin))

        return bx_min, bx_max, by_min, by_max

    def _zoom_out_bbox(self, x_min, x_max, y_min, y_max, orig_h, orig_w):
        """Expand the prompt box outside the GT. Train: asymmetric random. Test: fixed."""
        gt_w, gt_h = x_max - x_min, y_max - y_min
        lo, hi = self.zoom_ratio
        if self.is_train:
            r_l, r_r = random.uniform(lo, hi), random.uniform(lo, hi)
            r_t, r_b = random.uniform(lo, hi), random.uniform(lo, hi)
        else:
            r = 0.30
            r_l = r_r = r_t = r_b = r
        bx_min = max(0,       x_min - gt_w * r_l)
        bx_max = min(orig_w,  x_max + gt_w * r_r)
        by_min = max(0,       y_min - gt_h * r_t)
        by_max = min(orig_h,  y_max + gt_h * r_b)
        bx_min, bx_max, by_min, by_max = self._ensure_min_prompt_margin(
            bx_min, bx_max, by_min, by_max,
            x_min, x_max, y_min, y_max, orig_h, orig_w,
        )
        return bx_min, bx_max, by_min, by_max

    def _shift_bbox(self, x_min, x_max, y_min, y_max, orig_h, orig_w, seed_idx=None):
        """Create an off-center covering box that still fully contains the GT."""
        gt_w, gt_h = x_max - x_min, y_max - y_min
        bx_min, bx_max, by_min, by_max = self._zoom_out_bbox(
            x_min, x_max, y_min, y_max, orig_h, orig_w)

        if self.is_train:
            dx = random.uniform(-gt_w * self.shift_ratio, gt_w * self.shift_ratio)
            dy = random.uniform(-gt_h * self.shift_ratio, gt_h * self.shift_ratio)
        else:
            rng = random.Random(seed_idx or 0)
            dx = rng.uniform(gt_w * 0.4, gt_w * 0.7) * self.shift_ratio
            dy = rng.uniform(gt_h * 0.1, gt_h * 0.3) * self.shift_ratio

        bx_min = max(0,       bx_min + dx)
        bx_max = min(orig_w,  bx_max + dx)
        by_min = max(0,       by_min + dy)
        by_max = min(orig_h,  by_max + dy)

        # Shift mode must still cover the full GT, only changing its relative position inside the box.
        box_w = bx_max - bx_min
        box_h = by_max - by_min
        bx_min = min(bx_min, x_min)
        by_min = min(by_min, y_min)
        bx_max = max(bx_max, x_max)
        by_max = max(by_max, y_max)

        # If clamping to image borders shrinks the shifted box, try to preserve the original box size.
        if bx_max - bx_min < box_w:
            if bx_min <= 0:
                bx_max = min(orig_w, bx_min + box_w)
            elif bx_max >= orig_w:
                bx_min = max(0, bx_max - box_w)
        if by_max - by_min < box_h:
            if by_min <= 0:
                by_max = min(orig_h, by_min + box_h)
            elif by_max >= orig_h:
                by_min = max(0, by_max - box_h)

        return bx_min, bx_max, by_min, by_max

    def create_plateau_heatmap(self, bbox, orig_h, orig_w):
        heatmap = np.zeros((orig_h, orig_w), dtype=np.float32)
        x_min, y_min, x_max, y_max = bbox
        x_min = max(0, int(x_min))
        y_min = max(0, int(y_min))
        x_max = min(orig_w, int(x_max))
        y_max = min(orig_h, int(y_max))
        if x_max > x_min and y_max > y_min:
            heatmap[y_min:y_max, x_min:x_max] = 1.0
            heatmap = cv2.GaussianBlur(
                heatmap,
                (self.prompt_kernel, self.prompt_kernel),
                0,
            )
        return heatmap

    def _resize_and_pad(self, array, interpolation, pad_value=0):
        """Resize isotropically to fit the target square, then pad the rest."""
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

    # ── Main ──────────────────────────────────────────────────────────

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

        # Select the prompt box according to the configured prompt mode.
        if self.prompt_mode == 'zoom_out':
            bx_min, bx_max, by_min, by_max = self._zoom_out_bbox(
                x_min, x_max, y_min, y_max, orig_h, orig_w)

        elif self.prompt_mode == 'shift':
            bx_min, bx_max, by_min, by_max = self._shift_bbox(
                x_min, x_max, y_min, y_max, orig_h, orig_w, seed_idx=idx)

        else:
            raise ValueError(f"Unknown prompt_mode: {self.prompt_mode}")

        prompt_map = self.create_plateau_heatmap(
            [bx_min, by_min, bx_max, by_max], orig_h, orig_w)

        # Preserve aspect ratio before padding so anatomy is not distorted.
        image = self._resize_and_pad(image, cv2.INTER_LINEAR, pad_value=0)
        mask = self._resize_and_pad(mask, cv2.INTER_NEAREST, pad_value=0)
        prompt_map = self._resize_and_pad(prompt_map, cv2.INTER_LINEAR, pad_value=0.0)

        image = (image.astype(np.float32) / 255.0 - 0.5) / 0.5
        mask  = (mask > 127).astype(np.float32)

        image  = torch.from_numpy(image).unsqueeze(0)
        mask   = torch.from_numpy(mask).unsqueeze(0)
        prompt = torch.from_numpy(prompt_map).unsqueeze(0)

        # Synchronized augmentation (train only).
        if self.is_train:
            if random.random() >= 0.5:
                image, mask, prompt = TF.hflip(image), TF.hflip(mask), TF.hflip(prompt)
            if random.random() >= 0.5:
                angle  = random.uniform(-15, 15)
                image  = TF.rotate(image,  angle, interpolation=InterpolationMode.BILINEAR)
                mask   = TF.rotate(mask,   angle, interpolation=InterpolationMode.NEAREST)
                prompt = TF.rotate(prompt, angle, interpolation=InterpolationMode.BILINEAR)

        mask = (mask > 0.5).float()
        return image, mask, prompt


# Backward-compatible aliases used by older notebooks/scripts.
BTXRD_Dataset = PromptSegmentationDataset
FracAtlas_Dataset = PromptSegmentationDataset

__all__ = [
    "PromptSegmentationDataset",
    "BTXRD_Dataset",
    "FracAtlas_Dataset",
]
