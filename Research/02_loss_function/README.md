# Stage 2: loss function additions

## Status: implemented, ready to run, not yet trained

An earlier attempt (centroid loss, recall-weighted Tversky with beta > alpha) was implemented, then removed after re-checking against the real x2/shift0.3 numbers: on the full test set, precision and recall were already balanced (Zoom: 0.8558/0.8930, Zoom + shift: 0.8241/0.8309) and CBL was already 0.9245-0.9592, so neither term had a deficiency to target. That removed code is documented in git history (`git log -- Research/02_loss_function/README.md` and the `train.py` history around commit `03a606b`).

## What changed since then

A size-based breakdown of the small-lesion subset (`Results/*/test-subcat-pga-vs-sam-r256-r512/`, using the paper's zoom_out checkpoints) surfaced a gap the full-test-set average hides: on the 50 test images with the smallest GT area, precision trails recall noticeably (BTXRD @256: 0.7308/0.8293; @512: 0.8430/0.8638; FracAtlas @256: 0.7070/0.9356; @512: 0.8037/0.8895), i.e. the model over-segments small lesions specifically. This is the opposite direction from the earlier recall-weighted Tversky attempt, and only shows up on the small subset, not the aggregate, so it does not contradict the earlier "no deficiency" finding, it identifies a different, narrower one.

That subcat breakdown used the paper's zoom_out checkpoints (`main`), not this branch's `center_zoom` x2/shift0.3 protocol, so the gap has not yet been confirmed on the checkpoint this stage actually trains.

## Implementation: size-conditioned Tversky loss

Added to `Source/Prompt-Guided-XRay-Segmentation/train.py`:

- `size_weighted_tversky_loss(pred, target, area_ref, alpha_max)`: a per-sample Tversky loss whose alpha (false-positive weight) is interpolated from each sample's own GT pixel area. At or above `area_ref`, alpha=beta=0.5, mathematically identical to `dice_loss`, so large, already-well-segmented lesions are unaffected. Below `area_ref`, alpha rises toward `alpha_max`, penalizing false positives more than false negatives, targeting the over-segmentation above.
- `compute_area_reference(dataset, percentile)`: a one-time scan of the training set's per-sample GT area, used as `area_ref`. Percentile-based (default `SIZE_TVERSKY_AREA_PCTL=25`) rather than a fixed pixel count, so it self-calibrates to whatever dataset/resolution is in use.
- Toggled by `USE_SIZE_TVERSKY=1` (default off, existing checkpoints and training runs are unaffected). `SIZE_TVERSKY_ALPHA_MAX` (default 0.7) and `SIZE_TVERSKY_AREA_PCTL` (default 25) are also environment-variable configurable.

```bash
PROMPT_DATASET_ROOT=dataset_BTXRD PROMPT_IMG_SIZE=512 \
PROMPT_MODE=center_zoom PROMPT_SCALE_FACTOR=2.0 PROMPT_SHIFT_RATIO=0.3 PROMPT_EPOCHS=150 \
USE_SIZE_TVERSKY=1 SIZE_TVERSKY_ALPHA_MAX=0.7 SIZE_TVERSKY_AREA_PCTL=25 \
python train.py
```

Unlike stage 3's `QualityHead`, this loss changes the segmentation term itself, so it needs a full retrain, not a cheap fine-tune on top of an existing checkpoint.

## Validating it

`train-size-tversky-x2-shift03-btxrd.ipynb` in this folder trains only the size-conditioned Tversky variant under the center_zoom x2/shift0.3 protocol (no baseline retrain, since one already exists), then tests it on: (1) the usual Zoom / Zoom + shift scenarios over the full test set, all six metrics; (2) the 50 test images with the smallest unioned GT area under the Zoom scenario, grouped per source image exactly like `Results/*/test-subcat-pga-vs-sam-r256-r512/`. Not yet run.

Comparing these numbers against the baseline (same protocol, `Research/03_uncertainty_confidence/train-quality-head-x2-shift03-btxrd.ipynb`: Zoom Dice 0.8667/IoU 0.7726/Pre 0.8597/Rec 0.8875/HD95 9.49/CBL 0.9592; Zoom + shift Dice 0.8101/IoU 0.6906/Pre 0.8228/Rec 0.8175/HD95 12.20/CBL 0.9217) or against the earlier zoom_out-protocol small-lesion breakdown (`Results/*/test-subcat-pga-vs-sam-r256-r512/subcat_3model_small_lesion.csv`, `PGA-UNet 512` row: Dice 0.8483/IoU 0.7462/Pre 0.8430/Rec 0.8638/HD95 2.32/CBL 0.9451, a different checkpoint/protocol so only a rough scale reference for the small-lesion side) is done by reading both files side by side, not duplicated into this notebook.

If the small-lesion Dice/Precision gain is real and the full-test-set numbers do not regress, this becomes the segmentation loss for this branch going forward. If the gap does not reproduce on this checkpoint, or the fix does not help, the size-conditioned version stays documented here as a checked-and-not-needed finding, the same way the earlier attempt is.
