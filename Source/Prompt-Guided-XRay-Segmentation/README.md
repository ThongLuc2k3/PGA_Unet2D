## Step 1: Environment setup
- pip install torch torchvision opencv-python scipy matplotlib tqdm

## Input preprocessing
- Image, mask, and prompt map all use the `resize + padding` pipeline, never a direct stretch to a square frame.
- The long edge is scaled down to `img_size`, then the background is padded to form a square `img_size x img_size` image.
- `image` uses `cv2.INTER_LINEAR`, `mask` uses `cv2.INTER_NEAREST`, `prompt_map` uses `cv2.INTER_LINEAR`.
- Three prompt modes, all box-scaled-from-center (no independent-per-side expansion): `center_zoom`, `center_shift`, `center_mixed`.
- `center_zoom` scales the tight GT box outward from its own center by a fixed `scale_factor` (all four sides together, no per-side randomness, no randomness at all: train and test use the same formula).
- `center_shift` adds an off-center displacement to `center_zoom`, using `shift_ratio` (train: random each sample; test: fixed, reproducible per sample), then re-clamps so the box still fully covers the GT.
- `center_mixed` independently picks `center_zoom` or `center_shift` per sample, with `P(center_shift) = mixed_shift_prob` (default `0.8`, i.e. 80% shift / 20% zoom): weighted toward `center_shift` because a clinician drawing a box freehand rarely centers it exactly on the lesion. Intended for training only; testing uses `center_zoom` and `center_shift` as two separate, fixed scenarios.
- No minimum context margin is enforced around the GT: the covering box only guarantees full coverage of the GT, nothing more (`center_shift` already cannot guarantee a minimum gap either, since it snaps back to the GT boundary to preserve coverage).
- The Gaussian kernel is fixed regardless of resolution: `31`, the same for `img_size=128`, `256`, and `512`. It is applied to heatmap coordinates in original-image pixel space before the resize-and-pad step, so keeping it constant (rather than scaling with `img_size`) is what keeps the effective blur consistent relative to the final `img_size x img_size` frame the network sees.

## Required directory structure:
# dataset_<DATASET_NAME>/
  - train/images/  train/annotations/
  - val/images/    val/annotations/
  - test/images/   test/annotations/
# models/
  - layers/grid_attention_layer.py
  - networks/prompt_unet_2D.py
  - networks_other.py
# dataset.py
# train.py

## Step 2: Train on the center-scaled mixed covering/off-center prompt (main protocol)
# In train.py: TRAIN_PROMPT_MODE='center_mixed' (default), USE_ENCODER_PROMPT=True, USE_QUALITY_HEAD=1 (default)
- set `PROMPT_DATASET_ROOT=dataset_<DATASET_NAME>` and `PROMPT_IMG_SIZE=128`, `256`, or `512` (defaults to `512` if unset)
- python train.py
# with no other env vars set, this already runs the current default recipe: center_mixed,
# scale_factor=3.0, shift_ratio=0.5, mixed_shift_prob=0.8 (80% shift / 20% zoom), QualityHead on
# produces checkpoints/pga_unet_center_mixed_x3_shift05_qhead_<128|256|512>_best.pth
# validation reports center_zoom and center_shift separately after image-level polygon merging; checkpoint selection uses image-level center_shift val Dice (the harder, off-center scenario)
- run the matching test notebook under File_Train/ (each `pga-train-*.ipynb` has its own inline test cell) to get the 2-scenario table (`center_zoom` and `center_shift`), the 6-metric summary, the no-GT confidence (CAD prompt-confidence gate + QualityHead), and sample visualizations for both scenarios

Two candidate segmentation-loss replacements remain available as reference options: size-conditioned Tversky and Focal Dice. Reference numbers from the earlier loss check are `0.7561` vs. `0.7781` on the small-lesion subset for size-conditioned Tversky versus plain Dice, and `0.7786` vs. `0.7781` for Focal Dice versus plain Dice. Keep these as reference only. The current default remains plain Dice + BCE unless one alternative is explicitly enabled. The three valid configurations are default Dice + BCE, size-conditioned Tversky + BCE, and Focal Dice + BCE. Enabling both alternatives together is intentionally invalid because they replace the same Dice term.

Environment variables for Step 2 (all optional, shown with their defaults):
- `PROMPT_MODE` (default `center_mixed`): `center_zoom`, `center_shift`, or `center_mixed`.
- `PROMPT_SCALE_FACTOR` (default `3.0`), `PROMPT_SHIFT_RATIO` (default `0.5`), `PROMPT_MIXED_SHIFT_PROB` (default `0.8`, only used by `center_mixed`).
- `PROMPT_EPOCHS` (default `150`).
- `PROMPT_SEED` (default `22120196`): fixed training seed used by the main experiments and architecture ablations. It controls Python, NumPy, PyTorch CPU, and PyTorch CUDA randomness. Monte Carlo experiments keep this training seed fixed while changing only the split seed (`1`, `2`, `3`, `4`).
- `USE_QUALITY_HEAD` (default `1`), `LOSS_CONFIDENCE_WEIGHT` (default `1.0`): set `USE_QUALITY_HEAD=0` to fall back to a plain `PGA_UNet` with no confidence head. `PGA_UNet`'s own constructor also defaults `use_quality_head=True`; pass `use_quality_head=False` there directly to load an older checkpoint trained without one.
- `USE_SIZE_TVERSKY=1` (default off), with `SIZE_TVERSKY_ALPHA_MAX` (default `0.7`) and `SIZE_TVERSKY_AREA_PCTL` (default `25`): replaces `dice_loss` with `size_weighted_tversky_loss`, penalizing false positives more on small-GT-area samples.
- `USE_FOCAL_DICE=1` (default off), with `FOCAL_GAMMA` (default `1.33`): replaces `dice_loss` with `focal_dice_loss`, `(1 - Dice)^(1/gamma)`. Mutually exclusive with `USE_SIZE_TVERSKY`.
- Checkpoint filenames record which loss was used (`_sizetversky` / `_focaldice<gamma>` suffix, nothing added for the plain-Dice default), so `File_Train/{btxrd,fracatlas}/pga-train-{128,256,512}.ipynb`'s test cell can derive `MODEL_PATH` and its report/CSV loss label automatically from the same `USE_SIZE_TVERSKY`/`USE_FOCAL_DICE` variables set in the train cell above it.

No-GT confidence: the CAD prompt-confidence gate (`PGA_UNet.forward(..., return_confidence=True)`)
combines its 4 decoder levels with a weighted mean using the same `prompt_weights`
(`1.0, 0.7, 0.4, 0.2`) that scale each level's gating fusion strength, rather than a plain
average, so levels with more influence on the output also weigh more in the reported
confidence.

QualityHead validation: `evaluate_quality_head.py` evaluates the PGA-UNet QualityHead at the
polygon-prompt level against held-out ground-truth Dice targets. Each score refers to the mask
generated from one lesion prompt, not to an image-level mask after merging multiple lesions. It
reports MAE, RMSE, Pearson and Spearman correlation, plus mean Dice and the fraction of usable
masks in each predicted-quality bin. The QualityHead score is an auxiliary model estimate, not a
calibrated probability, until this evaluation supports such an interpretation. Example:
`python3 evaluate_quality_head.py --dataset-root dataset_BTXRD
--checkpoint checkpoints/pga_unet_center_mixed_x3_shift05_qhead_512_best.pth --split val
--img-size 512 --prompt-mode center_shift`.

## Step 3 (optional, single-condition ablation): Train with the covering prompt only
# In train.py: PROMPT_MODE=center_zoom
- python train.py
# produces checkpoints/pga_unet_center_zoom_x3_qhead_256_best.pth or _512_best.pth
- run the matching test notebook under File_Train/
# compare against step 2 to see whether center_mixed training changes covering-condition performance

## Step 4 (optional, single-condition ablation): Train with the off-center prompt only
# In train.py: PROMPT_MODE=center_shift
- python train.py
# produces checkpoints/pga_unet_center_shift_x3_shift05_qhead_256_best.pth or _512_best.pth
- run the matching test notebook under File_Train/
# produces the 2-scenario table (`center_zoom` and `center_shift`) plus sample visualizations
