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

## Status

Not yet implemented in `dataset.py` or the training notebooks. Next steps:

- Decide a concrete multiplier range (e.g. x2-x3) and whether the multiplier itself should be randomized per sample or fixed.
- Implement it as a new prompt mode alongside the existing `zoom_out`/`shift` modes, without removing the current ones.
- Retrain PGA-UNet on this protocol and compare Dice, CBL, and HD95 against the current independent-side-expansion protocol, on both BTXRD and FracAtlas.
- Only then decide whether the more natural-looking box is worth keeping, especially if it costs some Dice relative to the current protocol.
