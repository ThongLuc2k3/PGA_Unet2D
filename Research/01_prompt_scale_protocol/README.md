# Stage 1: center-scaled box prompt protocol

## Motivation

The current prompt protocol (`dataset.py`, `_zoom_out_bbox` / covering-prompt path) expands the tight lesion box independently on each of the four sides, by a random fraction in `[0.15, 0.45]` of lesion width or height at training time, and by a fixed 0.30 at test time. Because each side is expanded independently, the resulting box can come out oddly shaped and elongated in a way a clinician would not naturally draw. A radiologist marking a suspicious region tends to draw a single box loosely centered on the lesion rather than stretching each edge by a different, uncorrelated amount.

## Proposed protocol

1. Start from the tight box around the lesion (the polygon's bounding box).
2. Compute its center.
3. Scale the box outward from that center by a multiplier (e.g. x2, x3), so all sides grow together instead of independently.
4. Optionally add an off-center shift (e.g. up to 30-50% of the scaled box size) while still fully containing the lesion, to keep testing robustness to imperfect centering.

This keeps the "box always covers the lesion" guarantee, but produces a more natural, roughly-square, centered box instead of the current independently-jittered rectangle.

## `illustration_prompt_scale.png`

A conceptual mockup, not model output: one BTXRD example (IMG000184, the femur lesion also used in the paper's Top-Dice qualitative figure). Six panels: the original image, the tight box (x1), and the same box scaled x2 through x5 from its center. At x4/x5 the box is clipped to the image border, showing how large multipliers saturate against the frame. This is only meant to visualize the geometric idea before implementation; it does not use `dataset.py`'s actual letterbox/heatmap pipeline or real prompt heatmaps.

## Implementation

Added as a new `prompt_mode='center_scale'` in `Source/Prompt-Guided-XRay-Segmentation/dataset.py` (`_center_scale_bbox`), alongside the existing `zoom_out`/`shift` modes, which are unchanged. It scales the tight GT box outward from its own center by `scale_factor`, then applies a random off-center shift bounded by `shift_ratio` of the scaled half-size, always re-clamped to still fully cover the GT and to stay within the image. `train.py` reads `PROMPT_MODE`, `PROMPT_SCALE_FACTOR`, and `PROMPT_SHIFT_RATIO` from the environment, so each run below only differs in those three variables; checkpoints are named `pga_unet_center_scale_x{scale}_shiftNN_512_best.pth` so the four runs cannot overwrite each other.

## Training + test notebooks (BTXRD, 512x512)

Four notebooks in this folder, one per (scale, shift) combination, each self-contained: clone the `research/prompt-scale-protocol` branch, download BTXRD, train with `train.py` under the matching env vars, then evaluate the resulting checkpoint (Dice/IoU/Pre/Rec/HD95/CBL) under the same "zoom vs shift" pairing it was trained under: a zoom scenario (the trained scale, shift forced to 0, i.e. perfectly centered) and a shift scenario (the trained scale and shift ratio, i.e. in-distribution), plus the legacy `zoom_out`/`shift` protocols as a reference point against the existing paper baseline. Same qualitative visualization grid used by the existing `pga-train-512.ipynb` template.

| Notebook | scale_factor | shift_ratio |
|---|---|---|
| `train_scale_x2_shift03_btxrd.ipynb` | 2.0 | 0.3 |
| `train_scale_x2_shift05_btxrd.ipynb` | 2.0 | 0.5 |
| `train_scale_x3_shift03_btxrd.ipynb` | 3.0 | 0.3 |
| `train_scale_x3_shift05_btxrd.ipynb` | 3.0 | 0.5 |

**Before running any of these in Colab/Kaggle, this branch must be pushed to `origin`** (the setup cell clones `-b research/prompt-scale-protocol` from GitHub; a local-only branch cannot be cloned from there).

## Status

Code and notebooks are written and syntax-checked, with the box-generation logic unit-tested standalone (GT coverage and image-bound clamping hold across scale/shift/train-vs-test combinations). Not yet run for real: no GPU training has happened yet. Next steps:

- Push this branch, then run the four notebooks (a few repeats per config, per the user's plan) and record Dice/CBL/HD95.
- Compare against the current `zoom_out` protocol's existing numbers (Table 2/4 in the paper: BTXRD Dice 0.8788, CBL 0.9619 at 512x512).
- Decide a winning (scale, shift) setting, then repeat only that configuration on FracAtlas before considering loss-function changes (stage 2).
