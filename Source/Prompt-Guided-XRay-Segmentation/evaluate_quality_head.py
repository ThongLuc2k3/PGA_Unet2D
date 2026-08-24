"""Evaluate PGA-UNet QualityHead against held-out Dice targets."""

import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import torch
from torch.utils.data import DataLoader

from dataset import PromptSegmentationDataset
from models.networks.prompt_unet_2D import PGA_UNet


def per_sample_dice(logits, target, smooth=1e-5):
    prediction = (torch.sigmoid(logits) > 0.5).float()
    tp = (prediction * target).sum(dim=(1, 2, 3))
    fp = (prediction * (1 - target)).sum(dim=(1, 2, 3))
    fn = ((1 - prediction) * target).sum(dim=(1, 2, 3))
    return (2 * tp + smooth) / (2 * tp + fp + fn + smooth)


def rankdata(values):
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(len(values), dtype=np.float64)
    ranks[order] = np.arange(len(values), dtype=np.float64)
    return ranks


def correlation(values_a, values_b):
    if len(values_a) < 2 or np.std(values_a) == 0 or np.std(values_b) == 0:
        return float("nan")
    pearson = float(np.corrcoef(values_a, values_b)[0, 1])
    spearman = float(np.corrcoef(rankdata(values_a), rankdata(values_b))[0, 1])
    return pearson, spearman


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-root", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--split", default="val", choices=("val", "test"))
    parser.add_argument("--img-size", type=int, default=512)
    parser.add_argument("--prompt-mode", default="center_shift", choices=("center_zoom", "center_shift"))
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--dice-threshold", type=float, default=0.7)
    parser.add_argument("--output", default="quality_head_evaluation.csv")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dataset = PromptSegmentationDataset(
        os.path.join(args.dataset_root, args.split, "images"),
        os.path.join(args.dataset_root, args.split, "annotations"),
        img_size=args.img_size,
        is_train=False,
        prompt_mode=args.prompt_mode,
        scale_factor=3.0,
        shift_ratio=0.5,
    )
    loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=False, num_workers=0)

    model = PGA_UNet(use_quality_head=True).to(device)
    state = torch.load(args.checkpoint, map_location=device, weights_only=True)
    model.load_state_dict(state)
    model.eval()

    rows = []
    with torch.no_grad():
        offset = 0
        for images, masks, prompts in loader:
            images, masks, prompts = images.to(device), masks.to(device), prompts.to(device)
            logits, quality = model(images, prompts, return_quality=True)
            dice = per_sample_dice(logits, masks).cpu().numpy()
            quality = quality.cpu().numpy()
            for index, (predicted, actual) in enumerate(zip(quality, dice)):
                image_name, shape_index = dataset.all_samples[offset + index]
                rows.append({
                    "image": image_name,
                    "polygon_index": shape_index,
                    "quality_pred": float(predicted),
                    "true_dice": float(actual),
                    "absolute_error": float(abs(predicted - actual)),
                    "dice_usable": int(actual >= args.dice_threshold),
                })
            offset += len(dice)

    quality = np.array([row["quality_pred"] for row in rows])
    dice = np.array([row["true_dice"] for row in rows])
    pearson, spearman = correlation(quality, dice)
    print(f"Samples: {len(rows)} | split={args.split} | prompt={args.prompt_mode}")
    print(f"Quality MAE: {np.mean(np.abs(quality - dice)):.4f}")
    print(f"Quality RMSE: {np.sqrt(np.mean((quality - dice) ** 2)):.4f}")
    print(f"Pearson: {pearson:.4f} | Spearman: {spearman:.4f}")
    for lower, upper in zip(np.arange(0.0, 1.0, 0.1), np.arange(0.1, 1.1, 0.1)):
        selected = (quality >= lower) & ((quality < upper) if upper < 1.0 else (quality <= upper))
        if selected.any():
            usable = np.mean(dice[selected] >= args.dice_threshold)
            print(f"Quality [{lower:.1f}, {upper:.1f}]: n={selected.sum()} mean_Dice={dice[selected].mean():.4f} usable={usable:.1%}")

    with open(args.output, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
