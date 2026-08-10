# Project notes for AI assistants

## Branches: read this first

This repo has two branches with different purposes. Do not mix content, numbers, or checkpoint IDs between them.

- `main` (this branch): source for an IEEE Access journal paper submission. The paper draft is at `ACCESS_latex_template_20260513-1-1/ACCESS_latex_template_20260513/access.tex`. Experiments here use a cleaned-up, revised prompt protocol.
- `graduation-project`: the original undergraduate thesis, in Vietnamese, already submitted (full LaTeX report under `Report/`). Read it with `git show graduation-project:<path>` or a separate worktree; do not check it out over uncommitted work on `main`.

## Language rule (main branch only)

This rule is about file content, not conversation. Everything committed to files on `main` must be in English: code comments, docstrings, print/log/assert messages, notebook markdown cells, variable and function names. Do not add or leave Vietnamese text in any file on this branch. Vietnamese content belongs only on `graduation-project`.

Talking with the user is a separate matter: reply in whatever language the user writes in (this user writes in Vietnamese). Never switch the conversation itself to English just because the repo's file-content rule says English.

## Writing style

Do not use an em dash or a double hyphen as sentence-connecting punctuation in comments, docstrings, print statements, or markdown. It reads as AI-generated prose. Use a period, comma, or colon instead, or just restructure the sentence.

This does not apply to:
- decorative section-divider lines made of repeated dash or box-drawing characters, for example `# --------------------------------`, which are fine to keep as visual separators,
- functional code that legitimately manipulates that character, for example sanitizing a string for use in a filename,
- a single hyphen used as a plain title separator in a heading or comment, for example `# Ablation - CAD only`, which is a normal, human-natural convention and not the AI-writing tell this rule targets.

## Scope discipline

- Do only what was asked. Do not refactor, rename, delete files, or clean up unrelated code without asking first.
- Never invent placeholder values that look real: Google Drive IDs, checkpoint paths, credentials. If a value is genuinely missing, leave a clearly marked `TODO_...` placeholder and say so out loud.
- Before any destructive or broad action (deleting files, rewriting many notebooks at once, force git operations), state the exact list of files or changes first.
- If you notice something already broken, missing, or changed that you did not touch yourself, say so explicitly instead of silently fixing it or staying quiet about it.

## Known structure

- `Source/README.md`: current active notebook layout (BTXRD and FracAtlas datasets, `File_Train/`/`File_Test/`, dataset-specific subfolders).
- `Source/Prompt-Guided-XRay-Segmentation/`: shared PGA-UNet package (`dataset.py`, `train.py`, `models/`).
- Prompt protocol: the covering-box prompt keeps a minimum margin of 5px from the true lesion boundary (`_ensure_min_prompt_margin` in `dataset.py`). Training zoom range is 0.15 to 0.45, test-time zoom is fixed at 0.30, shift ratio is 0.30.
- Baselines compared in the paper: Attention U-Net as the automatic baseline, SAM-Med2D as the prompt-based foundation model baseline. Plain U-Net is kept for reference only, not a primary comparison.
- SAM-Med2D finetuning uses the original authors' training-time box-noise protocol (`get_boxes_from_mask`, small pixel-level jitter). Validation during training and the test split both use the same covering-prompt protocol as PGA-UNet, so evaluation is apples-to-apples across baselines even though each model trains its own way.
