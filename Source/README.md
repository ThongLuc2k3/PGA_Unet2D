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
│       ├── networks_other.py
│       ├── layers/grid_attention_layer.py
│       └── networks/
│           ├── prompt_unet_2D.py
│           ├── attention_unet_2D.py
│           └── utils.py
├── File_Train/
│   ├── btxrd/
│   └── fracatlas/
└── File_Test/
    ├── btxrd/
    └── fracatlas/
```

## Source Package

`Prompt-Guided-XRay-Segmentation/` is the shared runtime package. Every notebook clones the `PGA_Unet2D` GitHub repo and imports from this package, so it must stay self-contained (no dependency on any other repo).

- `dataset.py`: `PromptSegmentationDataset`, prompt generation, resize-and-padding, image-level split handling.
- `train.py`: main PGA-UNet training loop.
- `models/networks/prompt_unet_2D.py`: PGA-UNet architecture with Gaussian prompt input, Prompt Spatial Gate, and Conditional Attention Decoder.
- `models/networks/attention_unet_2D.py`: the Attention U-Net baseline (`Attention_UNet_2D`), used by `Attention_Unet2D.ipynb` and the PGA-vs-Attention-U-Net comparison notebooks.
- `models/networks/utils.py`: shared building blocks (`unetConv2`, `unetUp`) used by the baseline above.
- `models/layers/grid_attention_layer.py`: original attention gate inherited from Attention U-Net and reused in ablation variants.

The current prompt protocol:

- no minimum prompt margin: the covering box only guarantees full coverage of the GT
- Gaussian kernel `31`, fixed for both `256 x 256` and `512 x 512` (applied in
  original-image pixel space before resize, so keeping it constant is what keeps it
  consistent relative to the network's final input frame)
- covering prompt training range: `0.15-0.45`
- covering prompt test setting: fixed at `0.30`
- off-center shift setting: fixed relative offset `0.30`, while still overlapping the lesion

SAM-Med2D finetuning is the one exception: training uses the original authors' box-noise protocol (`get_boxes_from_mask`, small pixel-level jitter), not the covering-prompt ranges above. Its validation split during training and its test notebooks do use the same covering-prompt protocol as PGA-UNet, so evaluation stays apples-to-apples across baselines even though each model trains its own way.

## Dataset-Specific Notebook Folders

The active notebooks are dataset-specific, under `File_Train/{btxrd,fracatlas}/` and `File_Test/{btxrd,fracatlas}/`. There is no shared or template folder; every notebook is a real, dataset-specific entry point.

`File_Train/{btxrd,fracatlas}/` contains:

- `pga-train-256.ipynb`, `pga-train-512.ipynb`: PGA-UNet training (env vars `PROMPT_DATASET_ROOT` selects the dataset and `PROMPT_IMG_SIZE` selects the resolution for `train.py`, defaults to `512` if unset), plus an inline post-train evaluation cell for the zoom-out/shift scenarios.
- `Attention_Unet2D.ipynb`: Attention U-Net baseline training.
- `Finetune_SAMMed2D_test_robust.ipynb`: SAM-Med2D finetuning and its own zoom-out/shift test cells.
- `Ablation/`: the 8 architecture-ablation training notebooks (`cad-only`, `psg-only`, `psg-attention`, `full-binary-prompt`, `full-heatmap-prompt`, `no-psg-attention-concat`, `no-psg-no-cad-binary`, `no-psg-no-cad-concat`).

`File_Test/{btxrd,fracatlas}/` contains:

- `pga-vs-attention-unet-r512.ipynb`: PGA-UNet vs Attention U-Net at `512`.
- `test-subcat-pga-vs-attention-unet.ipynb`: Attention U-Net top-Dice and bottom-Dice subsets, PGA-UNet on the same subsets.
- `test-pga-samzs-samft-r256.ipynb`: PGA-UNet vs SAM-Med2D (zero-shot and finetuned) at `256`.
- `test-subcat-pga-vs-sam-r256-r512.ipynb`: small-lesion subset analysis, SAM-256 vs PGA-256 vs PGA-512.
- `test-pga-dataset-1234.ipynb`: Monte Carlo cross-validation (4 repeated random image-level splits).
- `Attention_Unet2D.ipynb`: standalone Attention U-Net evaluation.
- `Demo_Interactive_PGA_Unet.ipynb`: interactive Gradio demo (click two points, draw a box, get a mask).
- `Ablation/`: the matching 8 ablation test notebooks.

There is no single dedicated PGA-only test notebook; PGA-UNet is evaluated inside the comparison notebooks above. Efficiency analysis is measured by `File_Test/measure_efficiency.py` (parameter count, FLOPs, latency), not a notebook.

The active comparison story is:

1. PGA-UNet across BTXRD and FracAtlas at `256` and `512`
2. Monte Carlo cross-validation for stability
3. PGA-UNet vs Attention U-Net at `512`
4. Attention U-Net top-Dice and bottom-Dice subsets
5. PGA-UNet vs SAM-Med2D at `256`
6. Small-lesion subset analysis
7. Efficiency analysis
8. Ablation analysis

## Current Baselines

The current main baselines are:

- `Attention U-Net` as the automatic baseline
- `SAM-Med2D` as the prompt-based foundation baseline

Plain `U-Net` is not trained or evaluated anywhere in this source tree. The paper mentions it only as prior architectural lineage when introducing Attention U-Net (Related Work table, `access.tex`), with no quantitative results to defend, so there is nothing to reconcile if it happens to outperform Attention U-Net on some metric.

## Split Terminology

The repeated stability experiment should be described as:

`Monte Carlo cross-validation (repeated random image-level splits)`

It should not be described as strict non-overlapping `k`-fold cross-validation.

## Notes

- Dataset links have already been separated by folder for `BTXRD` and `FracAtlas`.
- The paper narrative now uses `Attention U-Net`, `SAM-Med2D`, `small-lesion subset`, and the full `Gaussian prompt + PSG + CAD` ablation story.
- All notebooks were audited for syntax errors, missing local-module imports, and cross-dataset ID mix-ups (see `CLAUDE.md` at the repo root for the current known-good state and the conventions this branch follows).

### Checkpoints still pending (Google Drive ID not filled in yet)

These cells have a `TODO_..._DRIVE_ID` or an empty `''` in place of a real Google Drive file ID, because the corresponding checkpoint has not been retrained/reuploaded yet under the current protocol. Fill in the real ID once the checkpoint exists, do not leave a guessed value:

- `File_Test/{btxrd,fracatlas}/pga-vs-attention-unet-r512.ipynb`: Attention U-Net checkpoint (both datasets); PGA-UNet-512 checkpoint for FracAtlas.
- `File_Test/{btxrd,fracatlas}/test-subcat-pga-vs-attention-unet.ipynb`: Attention U-Net checkpoint and PGA-UNet-512 checkpoint (both datasets).
- `File_Test/{btxrd,fracatlas}/Demo_Interactive_PGA_Unet.ipynb`: PGA-UNet-512 checkpoint for BTXRD and for FracAtlas.
