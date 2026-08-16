# Project notes for AI assistants

## Branches: read this first

This repo has two branches with different purposes. Do not mix content, numbers, or checkpoint IDs between them.

- `main` (this branch): source for an IEEE Access journal paper submission. The paper draft is at `Paper_IEEE_Access/access.tex`, split into `Paper_IEEE_Access/sections/*.tex` (one file per paper section), `references.tex`, and `biography.tex`; figures live under `Paper_IEEE_Access/images/<category>/`; a Vietnamese self-check translation (not for submission) lives in `Paper_IEEE_Access/vietnam/access_vietnam.tex`. Experiments here use a cleaned-up, revised prompt protocol.
- `graduation-project`: the original undergraduate thesis, in Vietnamese, already submitted (full LaTeX report under `Report/`). Read it with `git show graduation-project:<path>` or a separate worktree; do not check it out over uncommitted work on `main`.

## Language rule (main branch only)

This rule is about file content, not conversation. Everything committed to files on `main` must be in English: code comments, docstrings, print/log/assert messages, notebook markdown cells, variable and function names. Do not add or leave Vietnamese text in any file on this branch. Vietnamese content belongs only on `graduation-project`.

Talking with the user is a separate matter: reply in whatever language the user writes in (this user writes in Vietnamese). Never switch the conversation itself to English just because the repo's file-content rule says English.

The one deliberate, explicit exception: `Paper_IEEE_Access/vietnam/access_vietnam.tex` is a Vietnamese translation of the paper, kept only so the author can self-check the English manuscript. It exists on `main` at the user's explicit request, made after being told this contradicts the rule above. Do not treat its presence as license to add Vietnamese elsewhere; if it drifts out of sync with `access.tex`, that is a real staleness bug worth fixing, not something to leave because "there's already Vietnamese in the repo."

## Writing style

**Never use an em dash (—), an en dash (–), or a double/triple hyphen (`--`, `---`) as sentence-connecting punctuation, in any file, in any language, on this branch: code comments, docstrings, print/log/assert messages, notebook markdown cells, `.md` files, `.tex` prose (English or the Vietnamese self-check file), commit messages, everything.** It reads as AI-generated prose. Use a period, comma, colon, semicolon, or parentheses instead, or just restructure the sentence into two sentences. This has been violated repeatedly in past sessions (`README.md`, `access_vietnam.tex`, notebook markdown cells) despite being documented here; treat any new writing task as incomplete until you have grepped your own output for `—`, `–`, and `--` before considering it done.

This does not apply to:
- decorative section-divider lines made of repeated dash or box-drawing characters, for example `# --------------------------------`, which are fine to keep as visual separators,
- functional code that legitimately manipulates that character, for example sanitizing a string for use in a filename,
- a single hyphen used as a plain title separator in a heading or comment, for example `# Ablation - CAD only`, which is a normal, human-natural convention and not the AI-writing tell this rule targets,
- LaTeX's own `--` en-dash ligature inside numeric ranges, for example `15\%--45\%` or page ranges in `\bibitem` entries, which is TeX typesetting syntax, not prose punctuation.

## Scope discipline

- Do only what was asked. Do not refactor, rename, delete files, or clean up unrelated code without asking first.
- Never invent placeholder values that look real: Google Drive IDs, checkpoint paths, credentials. If a value is genuinely missing, leave a clearly marked `TODO_...` placeholder and say so out loud.
- Before any destructive or broad action (deleting files, rewriting many notebooks at once, force git operations), state the exact list of files or changes first.
- If you notice something already broken, missing, or changed that you did not touch yourself, say so explicitly instead of silently fixing it or staying quiet about it.

## Known structure

- `Source/README.md`: current active notebook layout (BTXRD and FracAtlas datasets, `File_Train/`/`File_Test/`, dataset-specific subfolders).
- `Results/`: executed test notebooks and per-image CSVs/xlsx are tracked in git; the `best.pth` checkpoints under it are gitignored (`Results/**/*.pth`, ~10-12MB each) and re-downloadable from the Google Drive IDs already in the matching notebook.
- `Source/Prompt-Guided-XRay-Segmentation/`: shared PGA-UNet package (`dataset.py`, `train.py`, `models/`).
- Prompt protocol: the covering-box prompt has no minimum margin, it only guarantees full coverage of the GT (`dataset.py` has no `_ensure_min_prompt_margin`, that helper does not exist in the current code). Training zoom range is 0.15 to 0.45, test-time zoom is fixed at 0.30, shift ratio is 0.30.
- Baselines compared in the paper: Attention U-Net as the automatic baseline, SAM-Med2D as the prompt-based foundation model baseline. Plain U-Net is kept for reference only, not a primary comparison.
- SAM-Med2D finetuning uses the PGA covering-prompt protocol for training too (50/50 per sample between zoom-out expansion, ratio 0.15-0.45, and off-center shift, ratio 0.30, via `prompt_box_from_mask` in `DataLoader.py`), not the original authors' `get_boxes_from_mask` box-noise: training SAM-Med2D only on the authors' tight-box jitter while testing it under PGA's wider zoom-out/shift prompts would confound the comparison, since PGA-UNet trains on the exact distribution it is tested on. Unlike PGA-UNet itself, which only trains on the zoom-out mode, SAM-Med2D trains on both zoom-out and shift so it is not undertrained relative to what it is tested on. Validation during training and the test split use the same covering-prompt protocol as well, so training and evaluation are apples-to-apples across baselines. Training is also box-only: the point-prompt branch and the `iter_point` point-refinement loop are disabled (`iter_point=0`), unlike the original authors' training which mixes box and point prompts.
