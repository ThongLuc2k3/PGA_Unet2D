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

| Notebook | scale_factor | shift_ratio | epochs | result |
|---|---|---|---|---|
| `train-scale-x2-shift03-btxrd.ipynb` | 2.0 | 0.3 | 150 | **winner.** Zoom Dice 0.8700 / CBL 0.9592, Zoom+shift Dice 0.8195 / CBL 0.9245 (best epoch 72, early-stopped at 87) |
| `train-scale-x2-shift05-btxrd.ipynb` | 2.0 | 0.5 | 150 | Zoom Dice 0.8687 / CBL 0.9544, Zoom+shift Dice 0.6998 / CBL 0.8640 (best epoch 85, early-stopped at 100) |
| `train-scale-x2-5-shift03-btxrd.ipynb` | 2.5 | 0.3 | 150 | Zoom Dice 0.8348 / CBL 0.9420, Zoom+shift Dice 0.7908 / CBL 0.9118 (best epoch 97, early-stopped at 112) |
| `train-scale-x2-5-shift05-btxrd.ipynb` | 2.5 | 0.5 | 150 | Zoom Dice 0.8302 / CBL 0.9394, Zoom+shift Dice 0.7357 / CBL 0.8799 (best epoch 84, early-stopped at 99) |
| `train-scale-x3-shift03-btxrd.ipynb` | 3.0 | 0.3 | 100 | Zoom Dice 0.8095 / CBL 0.9268, Zoom+shift Dice 0.7818 / CBL 0.9078 (best epoch 73, early-stopped at 88) |
| `train-scale-x3-shift05-btxrd.ipynb` | 3.0 | 0.5 | 100 | Zoom Dice 0.8088 / CBL 0.9288, Zoom+shift Dice 0.7173 / CBL 0.8776 (best epoch 69, early-stopped at 84) |

## Decision

**x2, shift_ratio=0.3 wins**, with the highest Dice and CBL of all six configurations under both test conditions. This is the box protocol stage 2 (loss function) and stage 3 (uncertainty/confidence) build on top of.

Two consistent patterns across all six real runs, useful context for later stages: (1) a smaller `scale_factor` gives higher absolute Dice/CBL, since a tighter box gives the network less irrelevant background to reason about; (2) a smaller `scale_factor` is also *more* sensitive to shift, not less (x2/shift0.5 drops 20.1% relative Dice under Zoom+shift, versus x3/shift0.5's 11.3%), because the same absolute shift distance covers a larger fraction of a smaller box. x2/shift0.3 sits at the good end of both trends: tight enough for high absolute accuracy, and only a mild 30% shift stress test rather than the more punishing 50%.

Still below the current paper's `zoom_out` protocol at BTXRD/512 (Dice 0.8788 covering / 0.8496 off-center, Table 2/4): not yet a proven improvement on raw Dice, so any write-up should present this as "a more clinician-realistic box shape at a comparable, slightly lower Dice" rather than a strict win, unless further tuning closes the gap.

Next steps:

- Repeat x2/shift0.3 on FracAtlas to confirm the winner is not BTXRD-specific.
- `02_loss_function/` was investigated and shelved (no evidence either loss term was needed); `03_uncertainty_confidence/` is the active stage, training `QualityHead` jointly on top of this x2/shift0.3 protocol.
