## Step 1: Environment setup
- pip install torch torchvision opencv-python scipy matplotlib tqdm

## Input preprocessing
- Image, mask, and prompt map all use the `resize + padding` pipeline, never a direct stretch to a square frame.
- The long edge is scaled down to `img_size`, then the background is padded to form a square `img_size x img_size` image.
- `image` uses `cv2.INTER_LINEAR`, `mask` uses `cv2.INTER_NEAREST`, `prompt_map` uses `cv2.INTER_LINEAR`.
- Three prompt modes: `zoom_out`, `shift`, and `mixed` (independently picks `zoom_out` or `shift` per training sample with 50/50 probability, matching the SAM-Med2D finetuning protocol).
- `zoom_out` is sampled randomly in `0.15-0.45` during training, and fixed at `0.30` during testing.
- `shift` uses a fixed relative offset of `0.30`.
- No minimum context margin is enforced around the GT: the covering box only guarantees
  full coverage of the GT, nothing more (the `shift` mode already could not guarantee a
  minimum gap either, since it snaps back to the GT boundary to preserve coverage).
- The Gaussian kernel is fixed regardless of resolution: `31`, the same for
  `img_size=256` and `img_size=512`. It is applied to heatmap coordinates in
  original-image pixel space before the resize-and-pad step, so keeping it constant
  (rather than scaling with `img_size`) is what keeps the effective blur consistent
  relative to the final `img_size x img_size` frame the network sees.

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

## Step 2: Train on the mixed covering/off-center prompt (main protocol)
# In train.py: TRAIN_PROMPT_MODE='mixed', USE_ENCODER_PROMPT=True
- set `PROMPT_DATASET_ROOT=dataset_<DATASET_NAME>` and `PROMPT_IMG_SIZE=256` or `512` (defaults to `512` if unset)
- python train.py
# produces checkpoints/pga_unet_mixed_256_best.pth or _512_best.pth depending on PROMPT_IMG_SIZE
# validation reports zoom_out and shift separately; checkpoint selection uses zoom_out val Dice
- run the matching test notebook under File_Test/ to get the 2-scenario table (`zoom_out` and `shift`), the 6-metric summary, and sample visualizations

## Step 3 (optional, single-condition ablation): Train with the covering prompt only
# In train.py: TRAIN_PROMPT_MODE='zoom_out', USE_ENCODER_PROMPT=True or False
- python train.py
# produces checkpoints/pga_unet_zoom_out_256_best.pth or _512_best.pth
- run the matching test notebook under File_Test/
# compare against step 2 to see whether mixed-prompt training changes covering-condition performance

## Step 4 (optional, single-condition ablation): Train with the off-center prompt only
# In train.py: TRAIN_PROMPT_MODE='shift', USE_ENCODER_PROMPT=True
- python train.py
# produces checkpoints/pga_unet_shift_256_best.pth or _512_best.pth
- run the matching test notebook under File_Test/
# produces the 2-scenario table (`zoom_out` and `shift`) plus sample visualizations
