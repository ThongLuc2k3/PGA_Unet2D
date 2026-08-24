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

**PGA-UNet-{128,256,512}** (`pga-train-{128,256,512}.ipynb`, both datasets where they exist) train on a center-scaled protocol (see `Prompt-Guided-XRay-Segmentation/README.md`, Step 2): `center_mixed`, box scaled from the GT center by `scale_factor=3.0`, off-center displacement `shift_ratio=0.5`, weighted 80% `center_shift` / 20% `center_zoom` per sample (a clinician rarely centers a box exactly on the lesion), plus a `QualityHead` no-GT confidence signal. The segmentation loss defaults to plain Dice + BCE; two candidate replacements (size-conditioned Tversky, Focal Dice) were tried and neither beat the default (see that README for the numbers), but both stay available as opt-in `train.py` flags (`USE_SIZE_TVERSKY`/`USE_FOCAL_DICE`) so PGA-UNet can be compared with either, both, or neither for further paper discussion. Each test cell derives `MODEL_PATH` and its report/CSV loss label automatically from the same flags.

**SAM-Med2D** (`Finetune_SAMMed2D_test_robust.ipynb`) trains and tests on the same center-scaled protocol, so the comparison against PGA-UNet stays apples-to-apples: `center_zoom`/`center_shift`, `scale_factor=3.0`, `shift_ratio=0.5`, weighted 80/20 during training (own `DataLoader.py` cell, mirrors `dataset.py`'s math exactly), `epochs=150`, default test/validation scenario `center_shift`. Not the original authors' box-noise protocol (`get_boxes_from_mask`, small pixel-level jitter). Training is box-only: the point-prompt branch and the `iter_point` point-refinement loop from the original authors' code are disabled (`iter_point=0`). Checkpoints are named `sam_center_mixed_x3_shift05_{best,last}.pth`.

**Attention U-Net** is unaffected: it has no prompt/box concept at all (plain image-only baseline). The 10 remaining architecture-ablation notebooks (each defining its own fully self-contained inline dataset class, no dependency on `dataset.py`) were migrated to the center-scaled `center_zoom`/`center_shift` protocol (and `center_mixed` for training), matching PGA-UNet and SAM-Med2D.

**Prompt-matched conventional baselines**: two Attention U-Net variants, promoted out of the architecture-ablation set into standalone baselines, give a plain Attention U-Net the same box prompt PGA-UNet gets, without any of PGA-UNet's Gaussian-prior/PSG/CAD machinery, so the comparison isolates "does the architecture matter, or just having the box at all":
- `concat-prompt-attunet-r512.ipynb`: box heatmap concatenated as a 2nd input channel (`in_channels=2`), plain skip decoder.
- `crop-prompt-attunet-r512.ipynb`: trained and evaluated on the image cropped to the prompt box instead of the full image, prediction pasted back into the full frame for a fair comparison.

Both baselines train in their own dedicated notebook above, but are tested inside `test-pga-vs-attention-unet-r512-{btxrd,fracatlas}.ipynb` alongside PGA-UNet and plain Attention U-Net, not in a separate test notebook: all four models are evaluated on the exact same balanced set of test images so their qualitative panels line up row-by-row.

Both use the same center-scaled protocol (`scale_factor=3.0`, `shift_ratio=0.5`) as PGA-UNet.

> **Pending retrain:** no checkpoint has been trained under the center-scaled protocol yet for either PGA-UNet or SAM-Med2D, so every tracked `Results/` notebook, CSV, and the paper's numeric tables were produced by the previous protocol (independent-per-side zoom/shift, no `QualityHead`). Until the `pga-train-*.ipynb`/`Finetune_SAMMed2D_test_robust.ipynb` notebooks are actually run and the tables refreshed, do not assume tracked numbers reflect this new protocol.

## Dataset-Specific Notebook Folders

The active notebooks are dataset-specific, under `File_Train/{btxrd,fracatlas}/` and `File_Test/{btxrd,fracatlas}/`. There is no shared or template folder; every notebook is a real, dataset-specific entry point.

`File_Train/{btxrd,fracatlas}/` contains:

- `pga-train-128.ipynb` (btxrd only, no fracatlas counterpart), `pga-train-256.ipynb`, `pga-train-512.ipynb`: PGA-UNet training at each resolution (env vars `PROMPT_DATASET_ROOT` selects the dataset, `PROMPT_IMG_SIZE` selects the resolution for `train.py`), all on the center-scaled `center_mixed` protocol (see "current prompt protocol" above), plus an inline post-train evaluation cell for the center_zoom/center_shift scenarios with no-GT confidence and sample visualizations for both scenarios.
- `Attention_Unet2D.ipynb`: Attention U-Net baseline training.
- `Finetune_SAMMed2D_test_robust.ipynb`: SAM-Med2D finetuning and its own center_zoom/center_shift test cells.
- `concat-prompt-attunet-r512.ipynb`: Attention U-Net + prompt channel, a prompt-matched conventional baseline (box heatmap concatenated as a 2nd input channel, no PSG, no CAD).
- `crop-prompt-attunet-r512.ipynb`: Attention U-Net trained on prompt-box crops instead of the full image, the other prompt-matched conventional baseline.
- `Ablation/`: the 5 remaining architecture-ablation training notebooks (`cad-only`, `psg-only`, `psg-attention`, `full-binary-prompt`, `full-heatmap-prompt`). `no-psg-attention-concat` (original attention gate, no PSG, prompt via concatenation) and `no-psg-no-cad-binary` (no PSG, no CAD, binary prompt via concatenation) were removed at the author's request.

`File_Test/{btxrd,fracatlas}/` contains:

- `test-pga-vs-attention-unet-r512-{btxrd,fracatlas}.ipynb`: PGA-UNet vs Attention U-Net vs both prompt-matched conventional baselines (`concat-prompt-attunet-r512`, `crop-prompt-attunet-r512`) at `512`, all four on the same balanced set of test images. There is no separate standalone test notebook for Attention U-Net or the two baselines; this is the only place they are tested.
- `test-subcat-pga-vs-attention-unet-{btxrd,fracatlas}.ipynb`: Attention U-Net top-Dice and bottom-Dice subsets, PGA-UNet on the same subsets.
- `test-pga-samzs-samft-r256-{btxrd,fracatlas}.ipynb`: PGA-UNet vs SAM-Med2D (zero-shot and finetuned) at `256`.
- `test-subcat-pga-vs-sam-r256-r512-{btxrd,fracatlas}.ipynb`: small-lesion subset analysis, SAM-256 vs PGA-256 vs PGA-512.
- `test-pga-dataset-1234-{btxrd,fracatlas}.ipynb`: Monte Carlo cross-validation (4 repeated random image-level splits).
- `test-Demo_Interactive_PGA_Unet-{btxrd,fracatlas}.ipynb`: interactive Gradio demo (click two points, draw a box, get a mask).
- `Ablation/`: the matching 5 remaining ablation test notebooks.

There is no single dedicated PGA-only test notebook; PGA-UNet is evaluated inside the comparison notebooks above. Efficiency analysis (parameter count, FLOPs, latency, checkpoint size, peak memory) is measured by `File_Test/test-measure_efficiency_btxrd.ipynb`. These numbers depend only on model architecture and input resolution, not on which dataset the checkpoint was trained on, so a single BTXRD-based notebook covers both datasets.

The active comparison story is:

1. PGA-UNet across BTXRD and FracAtlas at `256` and `512`
2. Monte Carlo cross-validation for stability
3. PGA-UNet vs Attention U-Net at `512`
4. Attention U-Net top-Dice and bottom-Dice subsets
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

## Notes

- Dataset links have already been separated by folder for `BTXRD` and `FracAtlas`.
- The paper narrative now uses `Attention U-Net`, `SAM-Med2D`, `small-lesion subset`, and the full `Gaussian prompt + PSG + CAD` ablation story.
- All notebooks were audited for syntax errors, missing local-module imports, and cross-dataset ID mix-ups (see `CLAUDE.md` at the repo root for the conventions this branch follows).
- Several notebooks migrated to the center-scaled protocol this session still have their checkpoint download replaced with a `TODO_CHECKPOINT_ID_...` placeholder, since no checkpoint has actually been retrained under it yet (see "Pending retrain" above): `pga512`, `pga256`, `sam256`, `fold1`-`fold4` (in the main comparison notebooks), `attunet_concat_prompt`, `crop_attunet512`, and one per remaining ablation variant (`cad_only`, `psg_only`, `psg_attention`, `full_binary_prompt`, `full_pga_heatmap_reference`). Fill these in with real Drive IDs after training; everything else already has real IDs.
- Executed copies of these test notebooks, plus their per-image CSVs, live under `../Results/Result_{BTXRD,FracAtlas}/`; see the root `README.md` for what is and isn't committed there.
