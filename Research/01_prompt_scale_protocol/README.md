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

Training, validation, and testing all follow the exact same methodology as the original PGA-UNet protocol: train only on the covering condition, validate each epoch on both the covering and off-center conditions, select the best checkpoint by validation Dice on the covering condition, and test on both conditions. The only thing that changes is the covering-box formula itself.

Added as two new prompt modes in `Source/Prompt-Guided-XRay-Segmentation/dataset.py`, alongside the existing `zoom_out`/`shift` modes, which are unchanged:

- `'center_zoom'` (`_center_zoom_bbox`): the tight GT box scaled outward from its own center by a fixed `scale_factor`, so all sides grow together instead of independently. Deterministic, no randomness. This is the direct replacement for `zoom_out`, and is the only mode training ever samples from.
- `'center_shift'` (`_center_shift_bbox`): `center_zoom` as the base box, with the exact same random off-center displacement mechanism `shift` applies on top of `zoom_out` (train: random each sample; test: fixed per sample via `seed_idx`), always re-clamped to still fully cover the GT and stay within the image. Evaluation-only, never used for training or checkpoint selection.

`train.py` reads `PROMPT_MODE`, `PROMPT_SCALE_FACTOR`, and `PROMPT_SHIFT_RATIO` from the environment. `PROMPT_MODE=center_zoom` trains covering-only and validates each epoch on both `center_zoom` and `center_shift`, exactly mirroring how the existing code trains on `zoom_out` and validates on `zoom_out` and `shift`. Checkpoints are named `pga_unet_center_zoom_x{scale}_512_best.pth`, by `scale_factor` alone: since training itself never depends on `shift_ratio`, the two files that share a scale (x2/shift0.3 and x2/shift0.5, or x3/shift0.3 and x3/shift0.5) train an equivalent model and only differ in which shift value the test cell evaluates under.

## Training + test notebooks (BTXRD, 512x512)

Four notebooks in this folder, one per (scale, shift) combination, each self-contained: clone the `research/prompt-scale-protocol` branch, download BTXRD, train with `train.py` under `PROMPT_MODE=center_zoom` and the matching `scale_factor`/`shift_ratio`, then evaluate the resulting checkpoint under two scenarios, mirroring the original paper's Covering/Off-center dual-condition test: "Zoom" (`center_zoom` only) and "Zoom + shift" (`center_shift`, same scale and shift the file was configured for). No legacy `zoom_out`/`shift` comparison anywhere. Same qualitative visualization grid used by the existing `pga-train-512.ipynb` template.

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
