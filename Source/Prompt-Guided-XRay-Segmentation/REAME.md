## Step 1: Environment setup
- pip install torch torchvision opencv-python scipy matplotlib tqdm

## Input preprocessing
- Image, mask, and prompt map all use the `resize + padding` pipeline, never a direct stretch to a square frame.
- The long edge is scaled down to `img_size`, then the background is padded to form a square `img_size x img_size` image.
- `image` uses `cv2.INTER_LINEAR`, `mask` uses `cv2.INTER_NEAREST`, `prompt_map` uses `cv2.INTER_LINEAR`.
- Only 2 prompt modes remain: `zoom_out` and `shift`.
- `zoom_out` is sampled randomly in `0.15-0.45` during training, and fixed at `0.30` during testing.
- `shift` uses a fixed relative offset of `0.30`.
- Prompt parameters scale with resolution:
  - `img_size=256`: minimum context margin around GT is `5 px`, Gaussian kernel `31`
  - `img_size=512`: minimum context margin around GT is `10 px`, Gaussian kernel `61`

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

## Step 2: Train with the covering prompt
# In train.py: TRAIN_PROMPT_MODE='zoom_out', USE_ENCODER_PROMPT=False
- set `PROMPT_DATASET_ROOT=dataset_<DATASET_NAME>`
- python train.py
# produces checkpoints/pga_unet_zoom_out_256_best.pth or _512_best.pth
- run the matching test notebook under File_Test/ to get the 6-metric table and sample visualizations

## Step 3: Train with the covering prompt plus encoder prompt
# In train.py: TRAIN_PROMPT_MODE='zoom_out', USE_ENCODER_PROMPT=True
- python train.py
- run the matching test notebook under File_Test/
# compare Dice/CBL against step 2

## Step 4: Train with the off-center prompt
# In train.py: TRAIN_PROMPT_MODE='shift', USE_ENCODER_PROMPT=True
- python train.py
# produces checkpoints/pga_unet_shift_256_best.pth or _512_best.pth
- run the matching test notebook under File_Test/
# produces the 2-scenario table (`zoom_out` and `shift`) plus sample visualizations
