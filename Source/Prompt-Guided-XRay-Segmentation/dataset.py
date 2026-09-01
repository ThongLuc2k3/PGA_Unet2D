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
        'center_zoom': the tight GT box scaled outward from its own center by
            a fixed scale_factor (all sides together)
        'center_shift': 'center_zoom' with an added off-center displacement
            (see shift_ratio below)
        'center_mixed': independently picks 'center_zoom' or 'center_shift'
            per sample, with P(center_shift) = mixed_shift_prob (default
            0.8). Weighted toward 'center_shift' reflects that a clinician
            drawing a box freehand rarely centers it exactly on the lesion.
            Intended for training only; testing should still use
            'center_zoom' and 'center_shift' as two separate, fixed
            scenarios rather than 'center_mixed'.
    """

    def __init__(self, image_dir, json_dir, img_size=512, is_train=True,
                 prompt_mode='center_mixed',
                 shift_ratio=0.5,
                 scale_factor=3.0,
                 mixed_shift_prob=0.8,
                 binary_prompt=False):
        self.image_dir   = image_dir
        self.json_dir    = json_dir
        self.img_size    = img_size
        self.is_train    = is_train
        self.prompt_mode = prompt_mode
        self.shift_ratio = shift_ratio
        # Only used by prompt_mode='center_zoom'/'center_shift'/'center_mixed':
        # how many times larger than the tight GT box the covering box is,
        # measured from the GT center.
        self.scale_factor = scale_factor
        # Only used by prompt_mode='center_mixed': probability of picking
        # 'center_shift' over 'center_zoom' for a given sample.
        self.mixed_shift_prob = mixed_shift_prob
        # Fixed regardless of img_size: applied to heatmap coordinates in
        # original-image pixel space, before the resize-and-pad step. Scaling
        # it with img_size would change the effective blur relative to the
        # final img_size x img_size frame the network sees, so it stays
        # constant across resolutions instead.
        self.prompt_kernel = 31
        # binary_prompt=True is the ablation that feeds a hard box instead of
        # the Gaussian-smoothed plateau: create_plateau_heatmap skips the blur
        # and prompt resizing switches to nearest neighbor so the box stays
        # hard through resize-and-pad and rotation. Gaussian heatmaps keep
        # linear/bilinear interpolation.
        self.binary_prompt = binary_prompt
        if binary_prompt:
            self.prompt_interpolation = cv2.INTER_NEAREST
            self.prompt_augmentation_interpolation = InterpolationMode.NEAREST
        else:
            self.prompt_interpolation = cv2.INTER_LINEAR
            self.prompt_augmentation_interpolation = InterpolationMode.BILINEAR

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

    def _center_zoom_bbox(self, x_min, x_max, y_min, y_max, orig_h, orig_w):
        """Expand the tight GT box outward from its own center by a fixed
        scale_factor (all four sides together). Meant to look closer to how a
        clinician would actually draw a box: loosely centered on the
        lesion rather than stretched unevenly per edge. No randomness here
        (train and test use the same formula); scale_factor is a fixed
        experiment setting, not sampled per example.
        """
        cx = (x_min + x_max) / 2.0
        cy = (y_min + y_max) / 2.0
        half_w = (x_max - x_min) / 2.0 * self.scale_factor
        half_h = (y_max - y_min) / 2.0 * self.scale_factor
        bx_min = max(0,       cx - half_w)
        bx_max = min(orig_w,  cx + half_w)
        by_min = max(0,       cy - half_h)
        by_max = min(orig_h,  cy + half_h)
        return bx_min, bx_max, by_min, by_max

    def _center_shift_bbox(self, x_min, x_max, y_min, y_max, orig_h, orig_w, seed_idx=None):
        """Displaces _center_zoom_bbox off-center: train picks a random
        offset each sample, test uses a fixed, reproducible offset per
        sample (seeded by seed_idx)."""
        gt_w, gt_h = x_max - x_min, y_max - y_min
        bx_min, bx_max, by_min, by_max = self._center_zoom_bbox(
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

        # Shift must still cover the full GT, only changing its relative position inside the box.
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
            if not self.binary_prompt:
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
        if self.prompt_mode == 'center_zoom':
            bx_min, bx_max, by_min, by_max = self._center_zoom_bbox(
                x_min, x_max, y_min, y_max, orig_h, orig_w)

        elif self.prompt_mode == 'center_shift':
            bx_min, bx_max, by_min, by_max = self._center_shift_bbox(
                x_min, x_max, y_min, y_max, orig_h, orig_w, seed_idx=idx)

        elif self.prompt_mode == 'center_mixed':
            if random.random() < self.mixed_shift_prob:
                bx_min, bx_max, by_min, by_max = self._center_shift_bbox(
                    x_min, x_max, y_min, y_max, orig_h, orig_w, seed_idx=idx)
            else:
                bx_min, bx_max, by_min, by_max = self._center_zoom_bbox(
                    x_min, x_max, y_min, y_max, orig_h, orig_w)

        else:
            raise ValueError(f"Unknown prompt_mode: {self.prompt_mode}")

        prompt_map = self.create_plateau_heatmap(
            [bx_min, by_min, bx_max, by_max], orig_h, orig_w)

        # Preserve aspect ratio before padding so anatomy is not distorted.
        image = self._resize_and_pad(image, cv2.INTER_LINEAR, pad_value=0)
        mask = self._resize_and_pad(mask, cv2.INTER_NEAREST, pad_value=0)
        prompt_map = self._resize_and_pad(prompt_map, self.prompt_interpolation, pad_value=0.0)

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
                prompt = TF.rotate(
                    prompt,
                    angle,
                    interpolation=self.prompt_augmentation_interpolation,
                )

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
