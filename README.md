# PGA-UNet

Prompt-guided, lightweight Attention U-Net for interactive bone X-ray lesion segmentation. A coarse bounding-box prompt is turned into a Gaussian-smoothed plateau heatmap, injected into encoder features through a **Prompt Spatial Gate (PSG)**, and reused in decoder skip-attention through a **Conditional Attention Decoder (CAD)**.

This branch (`main`) is the source for an IEEE Access journal submission. See `Paper_IEEE_Access/access.tex` for the manuscript. The `graduation-project` branch holds the original Vietnamese undergraduate thesis this work grew out of, and the two branches are separate deliverables that do not share content.

## Headline results

On BTXRD and FracAtlas, under covering box prompts at `512x512`, PGA-UNet reaches Dice `0.8788` and `0.8286` respectively, ahead of the Attention U-Net baseline and of fine-tuned SAM-Med2D at the matched `256x256` resolution, including on the 50 smallest lesions per dataset. The model has `2.95M` parameters, about `92x` fewer than SAM-Med2D. Full tables are in the paper (`Paper_IEEE_Access/access.tex`, Section V).

## Repository layout

```text
PGA_Unet2D/
├── Source/
│   ├── Prompt-Guided-XRay-Segmentation/   # shared model + dataset package (dataset.py, train.py, models/)
│   ├── File_Train/{btxrd,fracatlas}/      # training notebooks, incl. Ablation/
│   └── File_Test/{btxrd,fracatlas}/       # evaluation notebooks, incl. Ablation/
├── Results/                                # executed test notebooks + per-image CSVs (checkpoints excluded, see below)
└── Paper_IEEE_Access/                      # IEEE Access manuscript (access.tex, split into sections/, images/, vietnam/)
```

See `Source/README.md` for the full notebook inventory, the covering/off-center prompt protocol, and which checkpoints each notebook needs.

## Results/

Executed notebooks and metric CSVs from the runs reported in the paper, organized as `Results/Result_{BTXRD,FracAtlas}/<notebook-name>/`. Trained checkpoints (`best.pth`) are intentionally not committed: they are large binaries, re-downloadable from the Google Drive IDs already saved in the corresponding training/test notebook.

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

Plain U-Net is not trained or evaluated on this branch; it appears in the paper only as background in the Related Work discussion.
