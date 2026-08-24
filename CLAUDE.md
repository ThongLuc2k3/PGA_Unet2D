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

## Git commit conventions

**Never add a `Co-Authored-By: Claude ...` (or any AI-attribution) trailer to a commit message, on any branch.** This repo is public on GitHub, and that trailer makes GitHub list the AI as a repo contributor, which the author does not want. This was violated in early sessions on both `main` and `graduation-project`; both branches' histories were later rewritten (`git filter-branch --msg-filter`) to strip the trailer and force-pushed to origin, keeping a local-only `backup/<branch>-pre-claude-trailer-cleanup` branch for each in case anything needed to be recovered. Do not repeat the mistake, and do not force-push over anyone's work to "fix" this again without the user explicitly asking first, since it rewrites public commit hashes.

## No hidden watermarks or AI-identifying metadata

**Never embed any hidden marker of AI involvement in a file: invisible/zero-width Unicode characters (e.g. U+200B, U+200C, U+200D, U+FEFF, U+2060), steganographic text, hidden PDF metadata fields (Producer/Creator/Author/Keywords/XMP), PNG/JPEG metadata chunks (tEXt, EXIF, software tags), or any other covert signature identifying Claude, Anthropic, or AI generation, in any file on any branch.** This applies to `.tex` sources, generated `.pdf` files, and generated image files (e.g. the composite figures under `Paper_IEEE_Access/images/`) alike. The only acceptable place for a tool's own identity to appear is the ordinary, visible metadata a build tool writes about itself (e.g. `pdfTeX`/`xdvipdfmx` as PDF Producer), never anything referencing the AI assistant.

If asked to check for this, verify empirically rather than asserting from memory: grep source files for invisible Unicode ranges, inspect PDF metadata (`pdfinfo`, or search the raw `/Info` dictionary) and actual rendered text (`pdftotext`, not raw `strings`, which produces false positives from compressed binary streams), and check image files for metadata chunks (e.g. via Pillow's `Image.info`). Report findings plainly, including any coincidental false positives found and ruled out, rather than a bare "no."

## Scope discipline

- Do only what was asked. Do not refactor, rename, delete files, or clean up unrelated code without asking first.
- Never invent placeholder values that look real: Google Drive IDs, checkpoint paths, credentials. If a value is genuinely missing, leave a clearly marked `TODO_...` placeholder and say so out loud.
- Before any destructive or broad action (deleting files, rewriting many notebooks at once, force git operations), state the exact list of files or changes first.
- If you notice something already broken, missing, or changed that you did not touch yourself, say so explicitly instead of silently fixing it or staying quiet about it.

## Where to find current project state

This file holds durable rules only, not a snapshot of the codebase or current experiment status: those change too often to keep in sync here and belong in the docs that live next to the code they describe instead.

- Current notebook layout, prompt protocol, baselines, and pending-retrain status: `Source/README.md`.
- Shared PGA-UNet package usage (`dataset.py`, `train.py`, `models/`): `Source/Prompt-Guided-XRay-Segmentation/README.md`.
- Retraining status and the policy for regenerating `Results/`: the root `README.md`.

Read those before assuming anything about the current architecture, prompt protocol, or baseline set; if you find one of them out of date with the actual code, that is a staleness bug worth fixing, not something to silently work around.
