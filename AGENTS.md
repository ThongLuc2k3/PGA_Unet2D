# Repository Agent Rules

## Repository Scope

- `main` contains the English IEEE Access submission and current experiments.
- `graduation-project` contains the submitted Vietnamese thesis. Do not mix files, results, checkpoints, or claims between branches.
- Read `README.md`, `Source/README.md`, `Source/Prompt-Guided-XRay-Segmentation/README.md`, and `Paper_IEEE_Access/claims_to_validate.md` before making assumptions about the current protocol or experiment status.

## File Language

- Files committed on `main` must be in English, including code comments, docstrings, logs, assertions, notebook markdown, names, and documentation.
- The only intentional exception is `Paper_IEEE_Access/vietnam/access_vietnam.tex`, which is a Vietnamese self-check translation.
- Reply to the user in the language they use. The file-language rule does not control conversation language.

## Writing Style

- Do not use em dashes, en dashes, or double hyphens as sentence-connecting punctuation.
- Prefer short, direct prose. Avoid empty comments and repeated explanations.
- Do not add copyright or license headers unless requested.
- Use ASCII by default. Preserve the existing character set when editing the Vietnamese translation.

## Safe Editing

- Make the smallest change that satisfies the request. Do not refactor, rename, delete, or revert unrelated work.
- Never invent checkpoint IDs, Drive IDs, credentials, metrics, or experimental results. Use an explicit `TODO_...` placeholder when a value is missing.
- Before destructive or broad changes, state the exact scope and affected files.
- Do not commit or create branches unless requested. Never force-push unless explicitly requested.
- Do not add AI attribution trailers or hidden watermarks, invisible Unicode markers, steganographic text, or covert metadata to any file.

## Investigation and Validation

- Match investigation depth to the request. For a short question, inspect the nearest relevant file or symbol only.
- Before editing, form one local hypothesis and identify one cheap check that could disconfirm it.
- After the first substantive edit, run the narrowest available validation before expanding the scope.
- Prefer existing README files, claim registers, neighboring tests, and call sites over broad repository scans.
- Use `apply_patch` for text files. Use notebook-aware editing for `.ipynb` files and validate their JSON after changes.
- Run syntax, type, lint, or focused tests when available. Do not claim a test passed if it was not run.
- Do not run training, large notebook cells, downloads, GPU benchmarks, or other expensive jobs unless the user explicitly requests execution.

## Notebook Rules

- Preserve notebook cell order, metadata, dataset-specific paths, and execution intent.
- Keep dataset names, resolutions, prompt modes, seeds, checkpoint names, and model input or output signatures consistent with the shared source code.
- Treat unexecuted cells and placeholder checkpoints as pending work, not as experimental evidence.
- Keep model capabilities scoped to their implementation. QualityHead and prompt suggestion belong to PGA-UNet unless another model has an explicit implementation and trained checkpoint.
- Distinguish polygon-level metrics from image-level merged metrics.

## Claims and Results

- Separate implementation claims from empirical claims.
- Do not infer performance, robustness, calibration, clinical validity, generalization, or causal mechanism from architecture code or notebook names.
- Report prompt conditions separately when relevant, especially `center_zoom` and `center_shift`.
- Treat a confidence score as an auxiliary estimate unless held-out calibration evidence supports a probability interpretation.
- Keep the final decision with the clinician. Do not describe prompt suggestion as automatic lesion detection without dedicated evidence.

## Token and Response Efficiency

- For short questions, give a short direct answer. Do not start a full repository audit unless requested or required by a concrete dependency.
- Do not reread files or repeat plans that are already established in the current conversation.
- Use targeted searches and small line ranges first. Read broader context only when the local evidence is ambiguous.
- Parallelize independent read-only checks, then summarize only the findings that affect the decision.
- Stop searching when the requested local fix passes focused validation. Ask before broadening into unrelated cleanup.
- Prefer reporting the changed files, validation result, blocker, or next decision instead of restating project background.

## Persistent Project Notes

- Current layout, protocol, baselines, and pending retraining: `Source/README.md`.
- Claim-to-evidence mapping: `Paper_IEEE_Access/claims_to_validate.md`.
- Shared package usage: `Source/Prompt-Guided-XRay-Segmentation/README.md`.
- Manuscript entry point: `Paper_IEEE_Access/access.tex`.
