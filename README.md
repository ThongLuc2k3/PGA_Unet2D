# PGA-UNet

Prompt-guided, lightweight Attention U-Net for interactive bone X-ray lesion segmentation. A coarse bounding-box prompt is turned into a Gaussian-smoothed plateau heatmap, injected into encoder features through a **Prompt Spatial Gate (PSG)**, and reused in decoder skip-attention through a **Conditional Attention Decoder (CAD)**.

This branch (`main`) is the source for an IEEE Access journal submission. See `Paper_IEEE_Access/access.tex` for the manuscript. The `graduation-project` branch holds the original Vietnamese undergraduate thesis this work grew out of, and the two branches are separate deliverables that do not share content.

## Previous-protocol reference results

Reference only: Dice `0.8788` on BTXRD and `0.8286` on FracAtlas at `512x512` from the previous protocol. Do not reuse these as current results. Refresh the paper tables only after retraining under the current prompt pipeline, center-shift checkpoint selection, Precision definition, and image-level merged evaluation. The architecture has `2.95M` parameters, about `92x` fewer than SAM-Med2D; this architecture-only comparison is unchanged.

## Repository layout

```text
PGA_Unet2D/
├── Source/
│   ├── Prompt-Guided-XRay-Segmentation/   # shared model + dataset package (dataset.py, train.py, models/)
│   ├── File_Train/{btxrd,fracatlas}/      # training notebooks, incl. Ablation/
│   └── File_Test/{btxrd,fracatlas}/       # evaluation notebooks, incl. Ablation/
└── Paper_IEEE_Access/                      # IEEE Access manuscript (access.tex, split into sections/, images/, vietnam/)
```

See `Source/README.md` for the full notebook inventory, the covering/off-center prompt protocol, and which checkpoints each notebook needs.

The planned IEEE claims and the train/test evidence for each claim are recorded in [`Paper_IEEE_Access/claims_to_validate.md`](Paper_IEEE_Access/claims_to_validate.md). The repository uses the fixed training seed `22120196`; Monte Carlo split experiments additionally use split seeds `1`, `2`, `3`, and `4`.

## Experiment results

The obsolete `Results/` tree was removed because it contained outputs from the previous protocol. Add new executed notebooks and image-level merged CSVs only after retraining under the current source. Trained checkpoints remain excluded because they are large binaries; add their Google Drive IDs to the notebooks after retraining and upload.

## Paper_IEEE_Access/

- `access.tex`: thin entry point that `\input`s everything below.
- `sections/00-frontmatter.tex` through `08-back-matter.tex`: one file per manuscript section, in submission order.
- `references.tex`, `biography.tex`: bibliography and author bios, kept out of the section files.
- `images/<category>/`: figures grouped by role (`architecture/`, `results/`, `ablation/`, `failure/`, `author/`).
- `vietnam/access_vietnam.tex`: a Vietnamese translation of the manuscript for the author's own proofreading, not part of the submission, kept only for self-review.

Compile with `pdflatex access.tex` (run twice for references/figures to resolve). The `.cls`/`.bst`/`.sty`/font files alongside `access.tex` are IEEE Access template machinery; `pdflatex` only looks in that same directory for them, so they are not further reorganized.

## Baselines

- **Attention U-Net**: automatic (no-prompt) baseline.
- **SAM-Med2D**: prompt-based foundation-model baseline, fine-tuned on the same covering-prompt protocol PGA-UNet is evaluated on (see `Source/README.md` for why).
- Two prompt-matched conventional baselines give a plain Attention U-Net the same box prompt PGA-UNet gets, without PGA-UNet's own machinery: the heatmap concatenated as a 2nd input channel, or the image cropped to the prompt box before prediction. See `Source/README.md` for details.

The dedicated small-lesion resolution comparisons are `Source/File_Test/btxrd/test-subcat-pga-small-r128-256-512-btxrd.ipynb` and `Source/File_Test/fracatlas/test-subcat-pga-small-r128-256-512-fracatlas.ipynb`. The duplicate full-heatmap training notebooks were removed because the full Gaussian configuration is trained by `pga-train-512.ipynb`; the full-heatmap test notebooks remain for evaluation.

Plain U-Net is not trained or evaluated on this branch; it appears in the paper only as background in the Related Work discussion.
