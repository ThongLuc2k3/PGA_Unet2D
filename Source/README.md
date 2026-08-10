# PGA-Unet2D Source Layout

This directory contains the current source tree for the PGA-UNet thesis experiments after consolidation to the `PGA_Unet2D` repository structure.

## Active Structure

```text
Source/
├── Prompt-Guided-XRay-Segmentation/
│   ├── dataset.py
│   ├── train.py
│   ├── REAME.md
│   └── models/
├── File_Train/
│   ├── btxrd/
│   ├── fracatlas/
│   └── common/
└── File_Test/
    ├── btxrd/
    ├── fracatlas/
    └── common/
```

## Source Package

`Prompt-Guided-XRay-Segmentation/` is the shared runtime package for PGA-UNet.

- `dataset.py`: `PromptSegmentationDataset`, prompt generation, resize-and-padding, image-level split handling.
- `train.py`: main PGA-UNet training loop.
- `models/networks/prompt_unet_2D.py`: PGA-UNet architecture with Gaussian prompt input, Prompt Spatial Gate, and Conditional Attention Decoder.
- `models/layers/grid_attention_layer.py`: original attention gate inherited from Attention U-Net and reused in ablation variants.

The current prompt protocol is resolution-aware:

- `256 x 256`: minimum prompt margin `5 px`, Gaussian kernel `31`
- `512 x 512`: minimum prompt margin `10 px`, Gaussian kernel `61`
- covering prompt training range: `0.25-0.70`
- covering prompt test setting: `0.50`
- off-center shift setting: up to `0.50`, while still covering the lesion

## Dataset-Specific Notebook Folders

The active notebooks are dataset-specific:

- `File_Train/btxrd/`
- `File_Train/fracatlas/`
- `File_Test/btxrd/`
- `File_Test/fracatlas/`

Each dataset folder contains the current train or test notebooks for:

- `PGA_Unet2D.ipynb`
- `Attention_Unet2D.ipynb`
- `Unet2D.ipynb`
- `Finetune_SAMMed2D_test_robust.ipynb`
- ablation notebooks
- dataset-specific comparison notebooks

The active comparison story is:

1. PGA-UNet across BTXRD and FracAtlas at `256` and `512`
2. Monte Carlo cross-validation for stability
3. PGA-UNet vs Attention U-Net at `512`
4. Attention U-Net top-Dice and bottom-Dice subsets
5. PGA-UNet vs SAM-Med2D at `256`
6. Small-lesion subset analysis
7. Efficiency analysis
8. Ablation analysis

## Common Folders

`File_Train/common/` and `File_Test/common/` are shared templates and legacy intermediate notebooks retained for reference. They are not the primary entry points for reruns. When in doubt, prefer the dataset-specific folders first.

## Current Baselines

The current main baselines are:

- `Attention U-Net` as the automatic baseline
- `SAM-Med2D` as the prompt-based foundation baseline

`U-Net` is still kept in the source tree for reference and optional supplementary experiments, but it is no longer the main automatic baseline in the paper narrative.

## Split Terminology

The repeated stability experiment should be described as:

`Monte Carlo cross-validation (repeated random image-level splits)`

It should not be described as strict non-overlapping `k`-fold cross-validation.

## Notes

- Test notebooks intentionally keep some checkpoint placeholders because final reruns will produce new checkpoints.
- Dataset links have already been separated by folder for `BTXRD` and `FracAtlas`.
- The paper narrative now uses `Attention U-Net`, `SAM-Med2D`, `small-lesion subset`, and the full `Gaussian prompt + PSG + CAD` ablation story.
