# Stage 2: loss function additions

## Motivation

The current loss is BCE + Dice, which only scores pixel overlap. Two known weak spots this does not address directly: (1) a prediction can have decent Dice while its centroid still drifts from the true lesion center, which is exactly what CBL measures separately in evaluation but never feeds back into training; (2) Dice is dominated by pixel count, so on a very small lesion a handful of missed pixels can swing Dice sharply, giving the network little gradient signal to prioritize recall on small targets.

## Proposed additions

Both are implemented in `Source/Prompt-Guided-XRay-Segmentation/train.py`, added on top of BCE + Dice, each gated by an environment variable that defaults to `0.0` (off), so an unconfigured run reproduces the exact loss stage 1 was trained with.

1. **Centroid loss** (`centroid_loss`, weight `LOSS_CENTROID_WEIGHT`): a differentiable L2 distance between the predicted soft mask's centroid and the GT mask's centroid, normalized by the GT bounding-box diagonal. This is the same formula `calculate_cbl` already uses for evaluation, just computed on the soft (sigmoid) prediction instead of the thresholded one so it is differentiable. It directly optimizes what CBL measures, rather than leaving centroid accuracy as a side effect of Dice.
2. **Tversky loss** (`tversky_loss`, weight `LOSS_TVERSKY_WEIGHT`, false-negative weight `LOSS_TVERSKY_BETA`, default `0.7`): a generalization of Dice with independent false-positive/false-negative weights. `beta > alpha` (`alpha` fixed at `0.3`) penalizes missed lesion pixels more than extra predicted pixels, which should help recall on very small lesions specifically.

Total training loss: `BCE + Dice + LOSS_CENTROID_WEIGHT * centroid_loss + LOSS_TVERSKY_WEIGHT * tversky_loss`.

Both functions were sanity-checked standalone (NumPy re-implementation): centroid loss is 0 for a perfect prediction and grows with distance; Tversky loss is 0 for a perfect prediction and approaches 1 for no overlap.

Checkpoints are tagged with the active loss weights (e.g. `pga_unet_center_zoom_x2_centroid05_512_best.pth`), so loss-variant runs never overwrite the stage 1 winner checkpoint (`pga_unet_center_zoom_x2_512_best.pth`, from `PROMPT_MODE=center_zoom PROMPT_SCALE_FACTOR=2.0 PROMPT_SHIFT_RATIO=0.3`).

## Which one to try first

**Tversky, not centroid, is the recommended first experiment.** Reasoning from the numbers already collected: the x2/shift0.3 winner already reaches CBL 0.9245-0.9592 (Zoom and Zoom+shift), so centroid accuracy is close to ceiling already and a centroid loss has little room to help. The demonstrated weak point, from the paper's SAM-Med2D comparison, the Bottom-Dice subgroup, and small-lesion HD95, is recall on small/faint lesions, missed pixels, not off-center predictions. Tversky with `beta=0.7` targets exactly that.

Suggested order once training resumes, all on top of the x2/shift0.3 box protocol from stage 1:

1. `LOSS_TVERSKY_WEIGHT=0.5 LOSS_TVERSKY_BETA=0.7` alone. Compare Dice/CBL/HD95 against the stage 1 x2/shift0.3 baseline, with particular attention to recall and to performance on the smallest lesions.
2. Only if step 1 helps, try `LOSS_CENTROID_WEIGHT=0.5` on top of it, to see whether there is any remaining centroid-accuracy headroom once recall improves.
3. Centroid loss alone is a reasonable control experiment (to isolate its effect) but is not expected to move the numbers much given how high CBL already is.

Weights above 0.5 are unexplored; start small since both terms are new and could destabilize training if too large relative to BCE + Dice.

## Status

Code is written and unit-checked; no training has happened yet.
