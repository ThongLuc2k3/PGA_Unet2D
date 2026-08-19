# Stage 1: center-scaled box prompt protocol

## Motivation

The current prompt protocol (`dataset.py`, `_zoom_out_bbox` / covering-prompt path) expands the tight lesion box independently on each of the four sides, by a random fraction in `[0.15, 0.45]` of lesion width or height at training time, and by a fixed 0.30 at test time. Because each side is expanded independently, the resulting box can come out oddly shaped and elongated in a way a clinician would not naturally draw. A radiologist marking a suspicious region tends to draw a single box loosely centered on the lesion rather than stretching each edge by a different, uncorrelated amount.

## Proposed protocol

1. Start from the tight box around the lesion (the polygon's bounding box).
2. Compute its center.
3. Scale the box outward from that center by a multiplier (e.g. x2, x3), so all sides grow together instead of independently.
4. Optionally add an off-center shift (e.g. up to 30-50% of the scaled box size) while still fully containing the lesion, to keep testing robustness to imperfect centering.

This keeps the "box always covers the lesion" guarantee, but produces a more natural, roughly-square, centered box instead of the current independently-jittered rectangle.

## Illustrations

Conceptual mockups, not model output: all use the same BTXRD example (IMG000184, the femur lesion also used in the paper's Top-Dice qualitative figure). They visualize the geometric idea before/alongside implementation; none use `dataset.py`'s actual letterbox/heatmap pipeline or real prompt heatmaps.

- `illustration_prompt_scale.png`: six panels, the original image, the tight box (x1), and the same box scaled x2 through x5 from its center, no shift. At x4/x5 the box is clipped to the image border, showing how large multipliers saturate against the frame.
- `illustration_prompt_scale_{tag}.png`, one per real training configuration (`x2_shift03`, `x2_shift05`, `x2.5_shift03`, `x2.5_shift05`, `x3_shift03`, `x3_shift05`): four panels, the original image, the tight box (x1), the `center_zoom` box at that configuration's `scale_factor`, and the `center_shift` box at that same `scale_factor` and `shift_ratio`. Box coordinates use the exact `_center_zoom_bbox`/`_center_shift_bbox` formulas from `dataset.py` (with `seed_idx=0` for the shift, matching the deterministic test-time shift), evaluated directly on the illustration canvas rather than a real dataset sample, so the drawn boxes are geometrically faithful even though the canvas itself is a cropped mockup image.

## Implementation

Training, validation, and testing all follow the exact same methodology as the original PGA-UNet protocol: train only on the covering condition, validate each epoch on both the covering and off-center conditions, select the best checkpoint by validation Dice on the covering condition, and test on both conditions. The only thing that changes is the covering-box formula itself.

Added as two new prompt modes in `Source/Prompt-Guided-XRay-Segmentation/dataset.py`, alongside the existing `zoom_out`/`shift` modes, which are unchanged:

- `'center_zoom'` (`_center_zoom_bbox`): the tight GT box scaled outward from its own center by a fixed `scale_factor`, so all sides grow together instead of independently. Deterministic, no randomness. This is the direct replacement for `zoom_out`, and is the only mode training ever samples from.
- `'center_shift'` (`_center_shift_bbox`): `center_zoom` as the base box, with the exact same random off-center displacement mechanism `shift` applies on top of `zoom_out` (train: random each sample; test: fixed per sample via `seed_idx`), always re-clamped to still fully cover the GT and stay within the image. Evaluation-only, never used for training or checkpoint selection.

`train.py` reads `PROMPT_MODE`, `PROMPT_SCALE_FACTOR`, `PROMPT_SHIFT_RATIO`, and `PROMPT_EPOCHS` from the environment. `PROMPT_MODE=center_zoom` trains covering-only and validates each epoch on both `center_zoom` and `center_shift`, exactly mirroring how the existing code trains on `zoom_out` and validates on `zoom_out` and `shift`. Checkpoints are named `pga_unet_center_zoom_x{scale}_512_best.pth`, by `scale_factor` alone: since training itself never depends on `shift_ratio`, the two files that share a scale (e.g. x2/shift0.3 and x2/shift0.5) train an equivalent model and only differ in which shift value the test cell evaluates under.

The qualitative visualization section shows both test scenarios (Zoom, then Zoom + shift) as two separate 10-sample grids, not just the covering condition, so the off-center behavior is visible directly rather than only in the summary table.

## Training + test notebooks (BTXRD, 512x512)

One notebook per (scale, shift) combination in this folder, each self-contained: clone the `research/prompt-scale-protocol` branch, download BTXRD, train with `train.py` under `PROMPT_MODE=center_zoom` and the matching `scale_factor`/`shift_ratio`/`epochs`, then evaluate the resulting checkpoint under two scenarios, mirroring the original paper's Covering/Off-center dual-condition test: "Zoom" (`center_zoom` only) and "Zoom + shift" (`center_shift`, same scale and shift the file was configured for). No legacy `zoom_out`/`shift` comparison anywhere.

| Notebook | scale_factor | shift_ratio | epochs | status |
|---|---|---|---|---|
| `train_scale_x2_shift03_btxrd.ipynb` | 2.0 | 0.3 | 150 | retraining (first 100-epoch run did not early-stop; best Dice 0.8661 at epoch 88) |
| `train_scale_x2_shift05_btxrd.ipynb` | 2.0 | 0.5 | 150 | retraining (first 100-epoch run early-stopped at epoch 56, best at epoch 41) |
| `train_scale_x2.5_shift03_btxrd.ipynb` | 2.5 | 0.3 | 150 | not yet run |
| `train_scale_x2.5_shift05_btxrd.ipynb` | 2.5 | 0.5 | 150 | not yet run |
| `train_scale_x3_shift03_btxrd.ipynb` | 3.0 | 0.3 | 100 | trained: best Dice 0.8249 at epoch 73, early-stopped at epoch 88 |
| `train_scale_x3_shift05_btxrd.ipynb` | 3.0 | 0.5 | 100 | trained: best Dice 0.8264 at epoch 69, early-stopped at epoch 84 |

**Before running any of these in Colab/Kaggle, this branch must be pushed to `origin`** (the setup cell clones `-b research/prompt-scale-protocol` from GitHub; a local-only branch cannot be cloned from there).

## Status

x2/shift0.3, x2/shift0.5, x3/shift0.3, x3/shift0.5 have each been trained once for real on BTXRD/512 and evaluated on both Zoom and Zoom + shift. The two x2 runs did not clearly converge within 100 epochs (x2/shift0.3 never triggered early stopping; the Dice/IoU/HD95/CBL trend was still improving at epoch 100), so both are being retrained at 150 epochs. Two new x2.5 configurations were added alongside them to fill in the gap between x2 and x3. x3's two runs are considered done for this round; their notebooks and checkpoints are unchanged.

Across the first-round results, x2 reached higher absolute Dice/CBL under both test conditions than x3, but was noticeably more sensitive to the off-center shift (a much larger Zoom-to-Zoom+shift Dice drop at shift0.5 than x3 shows at the same shift ratio). x2.5 is meant to help tell whether that sensitivity is a smooth function of scale_factor or a sharper break somewhere between x2 and x3.

Next steps:

- Run the four pending notebooks (x2/0.3, x2/0.5 retrain; x2.5/0.3, x2.5/0.5 new) and record Dice/IoU/Pre/Rec/HD95/CBL under both scenarios.
- Compare all six (scale, shift) configurations against each other and against the current `zoom_out` protocol's existing numbers (Table 2/4 in the paper: BTXRD Dice 0.8788, CBL 0.9619 at 512x512).
- Decide a winning (scale, shift) setting, then repeat only that configuration on FracAtlas before considering loss-function changes (stage 2).
