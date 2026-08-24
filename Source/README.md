# PGA-Unet2D Source Layout

This directory contains the current source tree for the PGA-UNet thesis experiments after consolidation to the `PGA_Unet2D` repository structure.

## Active Structure

```text
Source/
├── Prompt-Guided-XRay-Segmentation/
│   ├── dataset.py
│   ├── train.py
│   ├── README.md
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

**PGA-UNet-{128,256,512}** (`pga-train-{128,256,512}.ipynb` for both BTXRD and FracAtlas) train on a center-scaled protocol (see `Prompt-Guided-XRay-Segmentation/README.md`, Step 2): `center_mixed`, box scaled from the GT center by `scale_factor=3.0`, off-center displacement `shift_ratio=0.5`, weighted 80% `center_shift` / 20% `center_zoom` per sample (a clinician rarely centers a box exactly on the lesion), plus a `QualityHead` no-GT confidence signal. The segmentation loss defaults to plain Dice + BCE. The loss investigation has exactly three configurations: the default, size-conditioned Tversky replacing Dice, and Focal Dice replacing Dice. The two alternatives remain separately selectable through `USE_SIZE_TVERSKY` and `USE_FOCAL_DICE`; enabling both is intentionally invalid because they replace the same loss term. Each test cell derives `MODEL_PATH` and its report/CSV loss label automatically from the selected configuration.

**SAM-Med2D** (`Finetune_SAMMed2D_test_robust.ipynb`) trains and tests on the same center-scaled protocol, so the comparison against PGA-UNet stays apples-to-apples: `center_zoom`/`center_shift`, `scale_factor=3.0`, `shift_ratio=0.5`, weighted 80/20 during training (own `DataLoader.py` cell, mirrors `dataset.py`'s math exactly), and `epochs=150`. Validation reports both scenarios and checkpoint selection uses `center_shift`. All models use early-stopping patience 15 except SAM-Med2D, which deliberately uses 30 because its adapter fine-tuning converges more slowly. This is not the original authors' box-noise protocol (`get_boxes_from_mask`, small pixel-level jitter). Training is box-only: the point-prompt branch and the `iter_point` point-refinement loop from the original authors' code are disabled (`iter_point=0`). Checkpoints are named `sam_center_mixed_x3_shift05_{best,last}.pth`.

**Attention U-Net** is unaffected: it has no prompt/box concept at all (plain image-only baseline). The 10 remaining architecture-ablation notebooks use thin dataset adapters around `PromptSegmentationDataset`, so box generation, Gaussian heatmap construction in original-image coordinates, resize-and-padding, deterministic test shifts, and synchronized augmentation exactly match PGA-UNet. The binary-prompt ablation overrides only heatmap construction and uses nearest-neighbor interpolation. Training uses `center_mixed`; testing reports `center_zoom` and `center_shift` separately.

**Prompt-matched conventional baselines**: two Attention U-Net variants, promoted out of the architecture-ablation set into standalone baselines, give a plain Attention U-Net the same box prompt PGA-UNet gets, without any of PGA-UNet's Gaussian-prior/PSG/CAD machinery, so the comparison isolates "does the architecture matter, or just having the box at all":
- `concat-prompt-attunet-r512.ipynb`: box heatmap concatenated as a 2nd input channel (`in_channels=2`), plain skip decoder.
- `crop-prompt-attunet-r512.ipynb`: trained and evaluated on the image cropped to the prompt box instead of the full image, prediction pasted back into the full frame for a fair comparison.

Both baselines train in their own dedicated notebook above, but are tested inside `test-pga-vs-attunet-variants-r512-{btxrd,fracatlas}.ipynb` alongside PGA-UNet and plain Attention U-Net, not in a separate test notebook: all four models are evaluated on the exact same balanced set of test images so their qualitative panels line up row-by-row.

Both use the same center-scaled protocol (`scale_factor=3.0`, `shift_ratio=0.5`) as PGA-UNet.

> **Pending retrain:** no checkpoint has been trained under the current center-scaled and standardized evaluation protocol yet for either PGA-UNet or the affected baselines. The obsolete `Results/` tree was removed. The paper's existing numeric tables still come from the previous protocol and must be refreshed after retraining. Training checkpoint selection now uses image-level merged validation metrics, matching the reported test aggregation.

## Dataset-Specific Notebook Folders

The active notebooks are dataset-specific, under `File_Train/{btxrd,fracatlas}/` and `File_Test/{btxrd,fracatlas}/`. There is no shared or template folder; every notebook is a real, dataset-specific entry point.

`File_Train/{btxrd,fracatlas}/` contains:

- `pga-train-128.ipynb`, `pga-train-256.ipynb`, `pga-train-512.ipynb`: official PGA-UNet training entry points at all three resolutions for both datasets. Environment variables `PROMPT_DATASET_ROOT` and `PROMPT_IMG_SIZE` select the dataset and resolution. All use the center-scaled `center_mixed` protocol, followed by image-level merged evaluation for the `center_zoom` and `center_shift` scenarios, no-GT confidence reporting, and sample visualizations.
- `Attention_Unet2D.ipynb`: Attention U-Net baseline training.
- `Finetune_SAMMed2D_test_robust.ipynb`: SAM-Med2D finetuning and its own center_zoom/center_shift test cells.
- `concat-prompt-attunet-r512.ipynb`: Attention U-Net + prompt channel, a prompt-matched conventional baseline (box heatmap concatenated as a 2nd input channel, no PSG, no CAD).
- `crop-prompt-attunet-r512.ipynb`: Attention U-Net trained on prompt-box crops instead of the full image, the other prompt-matched conventional baseline.
- `Ablation/`: the 5 remaining architecture-ablation training notebooks (`cad-only`, `psg-only`, `psg-attention`, `full-binary-prompt`, `full-heatmap-prompt`). `no-psg-attention-concat` (original attention gate, no PSG, prompt via concatenation) and `no-psg-no-cad-binary` (no PSG, no CAD, binary prompt via concatenation) were removed at the author's request.

`File_Test/{btxrd,fracatlas}/` contains:

- `test-pga-vs-attunet-variants-r512-{btxrd,fracatlas}.ipynb`: PGA-UNet vs Attention U-Net vs both prompt-matched conventional baselines (`concat-prompt-attunet-r512`, `crop-prompt-attunet-r512`) at `512`, all four on the same balanced set of test images. There is no separate standalone test notebook for Attention U-Net or the two baselines; this is the only place they are tested.
- `test-subcat-pga-vs-attunet-variants-r512-{btxrd,fracatlas}.ipynb`: plain Attention U-Net defines the post-hoc top-Dice 50 and bottom-Dice 50 image subsets. PGA-UNet, Attention U-Net + prompt channel, and Attention U-Net + prompt crop are then evaluated on those exact same stems at `512`; the three prompt-guided models report both `center_zoom` and `center_shift` for this focused subset comparison.
- `test-pga-samzs-samft-r256-{btxrd,fracatlas}.ipynb`: PGA-UNet vs SAM-Med2D (zero-shot and finetuned) at `256`.
- `test-subcat-small-r256-{btxrd,fracatlas}.ipynb`: GT-area-defined small-lesion analysis at 256, comparing PGA-UNet with SAM-Med2D zero-shot and fine-tuned.
- `test-subcat-small-r512-{btxrd,fracatlas}.ipynb`: the same type of GT-area-defined analysis for the four R512 architecture models. PGA-256 remains in the R256 file; resolution comparisons are assembled from the two result files when writing the paper.
- `test-pga-dataset-1234-{btxrd,fracatlas}.ipynb`: Monte Carlo cross-validation (4 repeated random image-level splits).
- `test-Demo_Interactive_PGA_Unet-{btxrd,fracatlas}.ipynb`: interactive Gradio demo (click two points, draw a box, get a mask).
- `Ablation/`: the matching 5 remaining ablation test notebooks.

Reusable model and training implementations live under `Prompt-Guided-XRay-Segmentation/` and are imported by the notebooks. In particular, `train_attunet.py`, `train_attunet_crop.py`, `models/networks/attunet_concat_prompt.py`, `models/networks/prompt_unet_psg_only.py`, and `models/networks/prompt_unet_psg_attention.py` are source files on `main`; notebooks do not create them with `%%writefile`. Remaining `%%writefile` cells only patch files that already exist in the separately cloned SAM-Med2D repository.

There is no single dedicated PGA-only test notebook; PGA-UNet is evaluated inside the comparison notebooks above. Efficiency analysis (parameter count, FLOPs, latency, checkpoint size, peak memory) is measured by `File_Test/test-measure_efficiency_btxrd.ipynb`. These numbers depend only on model architecture and input resolution, not on which dataset the checkpoint was trained on, so a single BTXRD-based notebook covers both datasets.

For comparisons across PGA input resolutions, the per-resolution CSVs retain native-pixel `hd95` and also report `hd95_normalized = hd95 / (sqrt(2) * IMG_SIZE)`. Use the normalized value when comparing 128, 256, and 512. Comparisons evaluated in one shared 512 frame may continue to report HD95 in pixels.

The active comparison story is:

1. PGA-UNet across BTXRD and FracAtlas at `128`, `256`, and `512`
2. Monte Carlo cross-validation for stability
3. PGA-UNet vs Attention U-Net at `512`
4. Attention U-Net-defined top-Dice and bottom-Dice subsets, with PGA-UNet and all three Attention U-Net variants evaluated on the same images
5. PGA-UNet vs SAM-Med2D at `256`
6. Small-lesion subset analysis
7. PGA-UNet vs the two prompt-matched conventional baselines (Attention U-Net + prompt channel, Attention U-Net on prompt crops)
8. Efficiency analysis
9. Ablation analysis

## Current Baselines

The current main baselines are:

- `Attention U-Net` as the automatic baseline
- `SAM-Med2D` as the prompt-based foundation baseline

Two additional prompt-matched conventional baselines give a plain Attention U-Net the same box prompt PGA-UNet gets, without PGA-UNet's Gaussian-prior/PSG/CAD machinery, for a fairer box-matched comparison:

- Attention U-Net + prompt channel (box heatmap concatenated as a 2nd input channel)
- Attention U-Net on prompt crops (trained and evaluated on the image cropped to the prompt box)

Plain `U-Net` is not trained or evaluated anywhere in this source tree. The paper mentions it only as prior architectural lineage when introducing Attention U-Net (Related Work table, `access.tex`), with no quantitative results to defend, so there is nothing to reconcile if it happens to outperform Attention U-Net on some metric.

## Split Terminology

The repeated stability experiment should be described as:

`Monte Carlo cross-validation (repeated random image-level splits)`

It should not be described as strict non-overlapping `k`-fold cross-validation.

All main and ablation training runs use the fixed training seed `22120196`. The four Monte Carlo runs use split seeds `1`, `2`, `3`, and `4` while keeping the training seed fixed at `22120196`. This isolates variation due to dataset membership from variation due to model initialization, shuffling, prompt sampling, and augmentation.

## Notes

- Dataset links have already been separated by folder for `BTXRD` and `FracAtlas`.
- The paper narrative now uses `Attention U-Net`, `SAM-Med2D`, `small-lesion subset`, and the full `Gaussian prompt + PSG + CAD` ablation story.
- All notebooks were audited for syntax errors, missing local-module imports, and cross-dataset ID mix-ups (see `CLAUDE.md` at the repo root for the conventions this branch follows).
- Several notebooks migrated to the center-scaled protocol this session still have their checkpoint download replaced with a `TODO_CHECKPOINT_ID_...` placeholder, since no checkpoint has actually been retrained under it yet (see "Pending retrain" above): `pga512`, `pga256`, `sam256`, `fold1`-`fold4` (in the main comparison notebooks), `attunet_concat_prompt`, `crop_attunet512`, and one per remaining ablation variant (`cad_only`, `psg_only`, `psg_attention`, `full_binary_prompt`, `full_pga_heatmap_reference`). Fill these in with real Drive IDs after training; everything else already has real IDs.
- Executed notebooks and image-level merged CSVs will be added to a new `Results/` tree only after the affected models have been retrained under the current protocol.
