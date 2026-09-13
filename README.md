# PGA-UNet

Prompt-guided, lightweight Attention U-Net for interactive bone X-ray lesion segmentation. A coarse bounding-box prompt is turned into a Gaussian-smoothed plateau heatmap, injected into encoder features through a **Prompt Spatial Gate (PSG)**, and reused in decoder skip-attention through a **Conditional Attention Decoder (CAD)**.

This branch (`main`) is the source for an IEEE Access journal submission. See [`Paper_IEEE_Access/access.tex`](Paper_IEEE_Access/access.tex) (built PDF: [`Paper_IEEE_Access/access.pdf`](Paper_IEEE_Access/access.pdf)) for the manuscript. The `graduation-project` branch holds the original Vietnamese undergraduate thesis this work grew out of; the two branches are separate deliverables that do not share content.

## Headline results

At `512x512`, image-level merged Dice under the covering-prompt protocol, fixed test splits:

| Model | BTXRD | FracAtlas |
|---|---|---|
| Attention U-Net (no prompt) | 0.517 | 0.342 |
| U-Net + binary prompt channel | 0.760 | 0.593 |
| Attention U-Net + prompt crop | 0.741 | 0.590 |
| **PGA-UNet** | **0.782** | **0.727** |

PGA-UNet has about **2.96M parameters**, roughly 92x fewer than fine-tuned SAM-Med2D. It is also compared against fine-tuned SAM-Med2D (resolution-matched at `256x256`), MedSAM, and ScribblePrompt-UNet at their own native resolutions. These are descriptive point estimates on fixed test splits; see the manuscript for scope, ablations, off-center-prompt sensitivity, Monte Carlo split stability, and the exploratory training-free self-assessment score. Full numbers, protocol, and every table are in `Paper_IEEE_Access/access.tex`.

## Repository layout

```text
PGA_Unet2D/
├── Source/
│   ├── Prompt-Guided-XRay-Segmentation/   # shared model + dataset package (dataset.py, train.py, models/)
│   ├── File_Train/{btxrd,fracatlas}/      # training notebooks, incl. Ablation/
│   └── File_Test/{btxrd,fracatlas}/       # evaluation notebooks, incl. Ablation/
├── Paper_IEEE_Access/                     # IEEE Access manuscript (access.tex, split into sections/, images/, vietnam/)
└── Research/                              # standalone protocol-design notebooks (e.g. box scale/shift illustration)
```

`Result/` (executed notebooks, image-level merged CSVs) and `dataset_json/` (raw dataset annotations) are gitignored: large and re-derivable by re-running the notebooks on Kaggle. Trained checkpoints are likewise excluded; Google Drive IDs are saved in the corresponding notebooks.

See `Source/README.md` for the full notebook inventory, the covering/off-center prompt protocol, and which checkpoints each notebook needs. The repository uses the fixed training seed `22120196`; Monte Carlo split-stability experiments additionally use split seeds `1`, `2`, `3`, and `4`.

## Paper_IEEE_Access/

- `access.tex`: thin entry point that `\input`s everything below.
- `sections/00-frontmatter.tex` through `08-back-matter.tex`: one file per manuscript section, in submission order.
- `references.tex`, `biography.tex`: bibliography and author bios, kept out of the section files.
- `images/<category>/`: figures grouped by role (`architecture/`, `results/`, `ablation/`, `failure/`, `author/`, `demo/`).
- `vietnam/access_vietnam.tex`: a Vietnamese translation of the manuscript for the authors' own proofreading, not part of the submission, kept only for self-review.

Build with `latexmk -pdf access.tex` (or `pdflatex access.tex`, run twice to resolve references/figures; the bibliography is a manual `thebibliography`, not BibTeX). The `.cls`/`.bst`/`.sty`/font files alongside `access.tex` are IEEE Access template machinery that `pdflatex` expects in the same directory, so they are not further reorganized. `vietnam/access_vietnam.tex` builds separately with `xelatex` (needs the DejaVu Serif/Sans fonts for Vietnamese diacritics).

## Baselines

- **Attention U-Net**: automatic (no-prompt) baseline.
- **SAM-Med2D**: promptable foundation-model baseline, fine-tuned on the same covering/off-center prompt protocol PGA-UNet is evaluated on, resolution-matched at `256x256` for the main comparison.
- **MedSAM** and **ScribblePrompt-UNet**: additional fine-tuned promptable reference models, each reported at their own native resolution as configuration-specific results (not used to establish a cross-model ranking against differently-scored configurations).
- Two prompt-matched conventional baselines give a plain Attention U-Net the same box prompt PGA-UNet gets, without PGA-UNet's own machinery: the heatmap concatenated as a 2nd input channel (`U-Net + binary prompt channel`), or the image cropped to the prompt box before prediction (`Attention U-Net + prompt crop`). See `Source/README.md` for details.

Plain U-Net is not trained or evaluated on this branch; it appears in the paper only as background in the Related Work discussion.

The dedicated small-lesion resolution comparisons are `Source/File_Test/btxrd/test-subcat-pga-small-r128-256-512-btxrd.ipynb` and `Source/File_Test/fracatlas/test-subcat-pga-small-r128-256-512-fracatlas.ipynb`.
