# Manuscript Writing Guardrails for `main`

## Quick Start

Read this block first when resuming work.

1. This paper is a controlled prompted-segmentation study, not an unconstrained detector study.
2. The core question is: after a coarse lesion-covering box is given, does prompt-conditioned processing help more than simple prompt access alone?
3. Keep two comparison layers separate: Attention U-Net is the automatic reference; SAM-Med2D and the prompt-matched Attention U-Net variants are the matched prompt baselines.
4. The current protocol is `center_mixed` with 80% `center_shift`, 20% `center_zoom`, `scale_factor=3.0`, `shift_ratio=0.5`, Gaussian kernel `31`, `150` epochs, and image-level merged validation and test evaluation.
5. Never let the manuscript drift back to old wording such as `50/50`, `100 epochs`, polygon-level checkpoint selection, or outdated Precision wording.
6. Before editing any claim, check `README.md`, `Source/README.md`, `Paper_IEEE_Access/claims_to_validate.md`, and the target section in `sections/`.
7. Before writing a subsection, decide whether it is in pending-retrain mode or refreshed-results mode; do not mix the two.
8. Small-lesion, top-Dice and bottom-Dice, ablation, and Monte Carlo are focused analyses with narrower claim scope; do not inflate them into broad clinical claims.
9. QualityHead is an auxiliary estimate, not a calibrated probability, unless dedicated calibration evidence is added later.
10. If a paragraph sounds stronger than the exact notebook or table that supports it, weaken the paragraph, not the evidence standard.

This file is the working writing frame for the IEEE Access manuscript on the `main` branch. It is not a results file. Its purpose is to keep the paper aligned with the current repository scope, the implemented protocol, and the level of evidence that the repository actually supports.

Use this file before editing `access.tex` or any section under `Paper_IEEE_Access/sections/`.

## 1. Paper Scope

The paper studies interactive prompt-guided lesion segmentation on bone radiographs.

The task definition is:

`image -> user provides a coarse lesion-covering box -> model predicts lesion mask`

The paper does not study:

- unconstrained lesion detection
- free-form prompt suggestion as a validated standalone task
- negative-box behavior
- partial-coverage-box behavior
- unrelated-region-box behavior
- cross-dataset transfer from one dataset-trained model to another dataset
- radiologist-collected real prompts
- calibrated confidence as a probability claim

The safest one-line scope statement is:

`This is a controlled prompted-segmentation study under simulated lesion-covering boxes, not an unconstrained detector study.`

## 2. Core Scientific Question

The paper should keep returning to one central question:

`Once a suspicious region has already been identified coarsely by a box prompt, does prompt-conditioned processing help more than simple prompt access alone?`

This question has two comparison layers:

1. Automatic-reference layer:
   Attention U-Net without a prompt shows how difficult localization is when the model must find the lesion by itself.
2. Prompt-matched layer:
   SAM-Med2D, Attention U-Net + prompt channel, and Attention U-Net + prompt crop test how well PGA-UNet uses the same box prompt after localization has already been externally provided.

Do not collapse these two layers into one sentence that implies they answer the same question.

## 3. What the Paper Is Allowed to Claim

Claims that are currently in scope:

- PGA-UNet is a lightweight prompt-guided CNN for interactive bone X-ray lesion segmentation.
- The method uses a Gaussian-smoothed plateau prompt, Prompt Spatial Gate (PSG), and Conditional Attention Decoder (CAD).
- Attention U-Net acts as an automatic reference, not a fully matched prompt-guided baseline.
- The current protocol evaluates two controlled prompt conditions: `center_zoom` and `center_shift`.
- Monte Carlo cross-validation is used to assess split-level stability of PGA-UNet.
- BTXRD and FracAtlas are evaluated independently, not as a single cross-dataset model.
- The current protocol values were selected in preliminary experiments and then fixed.
- The exploratory loss comparison can be reported as a negative or near-neutral research finding if it is clearly framed as such.

Claims that require refreshed current-protocol results before they can be stated quantitatively:

- PGA-UNet is better than SAM-Med2D on the current protocol.
- PGA-UNet is better than prompt-channel or prompt-crop Attention U-Net on the current protocol.
- The refreshed resolution ordering at 128, 256, and 512.
- The refreshed ablation ordering under the standardized protocol.
- The refreshed Monte Carlo mean and variance.
- Any table value in the paper body other than architecture-only measurements.

Claims that should stay out unless new evidence is added:

- clinically robust to realistic radiologist prompts
- robust to arbitrary prompt errors
- confidence score is a calibrated probability
- localization is definitively the only or universal bottleneck
- cross-dataset generalization
- statistically significant superiority, unless paired testing is actually run and reported
- globally optimal hyperparameters
- stronger loss-design claims such as `the proposed replacement loss is necessary` or `the default loss is universally optimal`

## 4. Protocol That the Paper Must Describe

The current protocol is:

- prompt mode: `center_mixed`
- train prompt mixture: 80% `center_shift`, 20% `center_zoom`
- `scale_factor=3.0`
- `shift_ratio=0.5`
- Gaussian kernel size: `31`
- training seed: `22120196`
- this fixed training seed controls Python, NumPy, PyTorch CPU, and PyTorch CUDA randomness
- max training epochs: `150`
- early stopping patience: `15` for PGA-UNet and Attention U-Net variants
- SAM-Med2D patience: `30`
- model selection: image-level merged validation Dice under `center_shift`
- image-level merged evaluation for validation and test
- training uses `center_mixed`; test reporting should keep `center_zoom` and `center_shift` separate rather than merging them into one prompt condition
- `center_shift` is random during training but deterministic and reproducible per sample at test time
- the covering box guarantees GT coverage but does not enforce any extra minimum context margin around the lesion
- the Gaussian prompt is built in original-image coordinates before resize-and-pad
- image, mask, and prompt all use resize-and-pad rather than direct square stretching
- image-level merging means GT masks are union-merged by image, predicted probability maps are merged by pixelwise maximum, and the final binary mask is thresholded at `0.5`
- across 128, 256, and 512 comparisons, report normalized HD95 as `hd95 / (sqrt(2) * IMG_SIZE)`, not only raw pixels
- the default segmentation objective is Dice + BCE; the size-conditioned Tversky and Focal Dice options are exploratory alternatives and are mutually exclusive
- the current default also uses `USE_QUALITY_HEAD=1`
- architecture-only efficiency measurements are not blocked by retraining in the same way segmentation tables are
- several notebook comparisons intentionally reuse the exact same image stems across models; preserve that fairness statement when writing qualitative or subgroup comparisons
- some R256-versus-R512 subgroup notebooks report metrics in a shared `512x512` metric frame; do not describe them as if every model were scored only in its own native frame
- the prompt-crop baseline may report crop-frame diagnostics such as `dice_crop`, but manuscript comparisons should use the pasted-back full-frame image-level metrics for cross-model claims

The paper must not revert to older wording such as:

- `50/50 zoom/shift`
- `100 epochs`
- polygon-level selection as the main checkpoint rule
- legacy Precision wording if the implementation has changed

## 5. How to Frame the Prompt

Prompt generation is GT-derived and simulated. That is acceptable within the current task definition.

What this supports:

- segmentation quality after coarse localization has been supplied
- sensitivity to controlled prompt displacement
- comparison among models under the same simulated prompt protocol

What this does not support:

- free detection ability
- radiologist workflow validation
- robustness to wrong-region prompts
- negative prompt specificity

Recommended wording:

`The prompts are simulated from lesion annotations to provide a controlled prompted-segmentation protocol.`

Avoid wording like:

`The model localizes lesions automatically from box-free radiographs.`

## 6. Hyperparameter Framing

The protocol values `31`, `x3`, `shift_ratio=0.5`, and CAD depth weights `(1.0, 0.7, 0.4, 0.2)` should be described as fixed study protocol values chosen from preliminary experiments.

Recommended wording:

`These values were selected through preliminary experiments and then fixed as part of the controlled protocol.`

Do not write:

- `optimal`
- `best possible`
- `globally tuned`
- `proven superior across settings`

No extra sensitivity study is required for the current claim scope if the paper does not overclaim.

## 7. Section-by-Section Writing Guide

### Abstract

Must include:

- task = interactive prompted segmentation
- prompt = coarse lesion-covering box
- method = Gaussian prompt + PSG + CAD
- baselines = Attention U-Net as automatic reference, SAM-Med2D as prompt-matched baseline
- protocol limitation = simulated lesion-covering boxes
- caution = no claim of unconstrained detection, clinical robustness, or calibrated confidence

Must avoid:

- final numeric claims until refreshed results are inserted
- wording that suggests real clinician prompt collection happened

### Introduction

Must do:

- motivate why localization is hard for small lesions
- explain why prompt guidance is a practical narrowing of the search space
- distinguish automatic-reference comparison from prompt-matched comparison
- end with contributions that match the actual experiments

Must avoid:

- saying Attention U-Net is a fair prompt-matched baseline
- implying all prompt-based models answer the same scientific question

### Related Work

Keep three groups visible:

- automatic medical segmentation and Attention U-Net lineage
- interactive segmentation and prompt-based supervision
- promptable medical foundation models such as SAM-Med2D, MedSAM, Med-SA, EMedSAM, ScribblePrompt-style work

Do not promise experimental baselines that are not actually run.

### Method

Must define:

- problem setting
- prompt representation
- `center_zoom`, `center_shift`, `center_mixed`
- simulated lesion-covering-box scope
- PSG and CAD mathematically

Must avoid:

- claiming realistic radiologist prompts were used
- claiming protocol values are optimal

### Experimental Setup

Must include:

- dataset sizes and image-level split handling
- patient-level separation limitation
- training seed and Monte Carlo split seeds
- the fact that Monte Carlo changes split membership while keeping the training seed fixed at `22120196`
- 80/20 `center_mixed` training
- 150 epochs
- image-level merged validation/test evaluation
- baseline definitions
- primary metrics in the paper body
- the fact that prompts are box-only in the current SAM-Med2D comparison; point-prompt refinement is disabled there
- the fact that the SAM-Med2D comparison does not use the original small-jitter `get_boxes_from_mask` protocol from the source authors
- when relevant, the fact that some focused comparisons reuse the same exact image stems across all compared models
- when relevant, the fact that some R256 small-lesion comparisons are reported in a shared `512x512` metric frame

Recommended metric wording:

`The main paper emphasizes Dice, CBL, and HD95, while the code also records IoU, precision, and recall in the exported reports.`

Recommended confidence wording:

`The code exposes two different no-GT signals: a CAD prompt-use score and a QualityHead estimated mask-quality score. They should not be described as the same quantity.`

### Results

Treat each subsection as serving one specific claim:

- main comparison across datasets and resolutions
- resolution effect
- Monte Carlo stability
- automatic-reference comparison with Attention U-Net
- top-Dice and bottom-Dice subsets
- prompt-matched SAM-Med2D comparison
- small-lesion analysis
- exploratory loss comparison
- efficiency
- ablation

Rules for wording:

- if numbers are still legacy placeholders, say so
- Monte Carlo supports stability, not superiority
- Attention U-Net comparison supports localization-difficulty framing, not a matched architecture win
- SAM comparison should report both absolute values and prompt-condition drop
- the loss comparison may be reported as a null or near-null result if the tested alternatives do not materially improve the default
- if a notebook exposes both manuscript-facing metrics and debug or diagnostic metrics, only the manuscript-facing metrics should drive cross-model claims
- ablation should use `consistent with complementary contributions`, not `proves synergy`

### Discussion

The discussion should interpret only what the evidence actually covers.

Include:

- localization difficulty as a major challenge in this setting
- controlled prompted-segmentation scope
- separate-dataset training limitation
- patient-level separation limitation
- simulated-prompt limitation
- heuristic-but-fixed protocol limitation
- the possibility that the default Dice + BCE objective is already strong enough under the current protocol, so extra loss complexity may not translate into measurable gains
- ablation variance limitation if repeated multi-seed ablation is still missing
- confidence not yet calibrated

Avoid:

- new results not shown earlier
- stronger clinical claims than the Results section supports

### Conclusion

Keep it narrow:

- what PGA-UNet is
- what was evaluated
- what the conclusions do not establish
- what future work should validate

## 8. Claim-Specific Evidence Map

### Claim A: PGA-UNet vs Attention U-Net and prompt-matched Attention U-Net variants

Purpose:

- separate automatic localization burden from prompt-conditioned processing

Needed files:

- `Source/File_Train/{btxrd,fracatlas}/pga-train-512.ipynb`
- `Source/File_Train/{btxrd,fracatlas}/Attention_Unet2D.ipynb`
- `Source/File_Train/{btxrd,fracatlas}/concat-prompt-attunet-r512.ipynb`
- `Source/File_Train/{btxrd,fracatlas}/crop-prompt-attunet-r512.ipynb`
- `Source/File_Test/{btxrd,fracatlas}/test-pga-vs-attunet-variants-r512-*.ipynb`

Safe wording:

`This comparison distinguishes the role of prompt access from the role of prompt-conditioned processing.`

### Claim B: Top-Dice and bottom-Dice subsets

Purpose:

- see whether prompt-guided models stay useful on image stems where the automatic baseline is relatively stronger or weaker

Safe wording:

`These subsets are induced by Attention U-Net performance and do not define intrinsic clinical difficulty groups.`

### Claim C: PGA-UNet vs SAM-Med2D

Purpose:

- matched prompt-based comparison

Safe wording before retrain:

`This subsection defines the matched prompt-based comparison to be refreshed after retraining.`

Safe wording after retrain:

`PGA-UNet achieved higher absolute Dice under the tested prompt conditions, while relative degradation should be interpreted separately.`

### Claim D: Small-lesion subset

Purpose:

- evaluate the stress case where lesion evidence is weakest

Safe wording:

`The small-lesion subset is defined by GT lesion area and is used as a focused subgroup analysis rather than a claim of broader clinical stratification.`

### Claim E: Ablation

Purpose:

- test whether the evaluated configuration of Gaussian prompt, PSG, and CAD is useful

Safe wording:

`The evaluated results are consistent with complementary contributions from PSG, CAD, and Gaussian prompt encoding.`

Unsafe wording:

`The ablation proves synergy.`

### Claim F: Monte Carlo

Purpose:

- split-level stability of PGA-UNet

Safe wording:

`Monte Carlo cross-validation shows stability across the evaluated repeated image-level splits.`

Unsafe wording:

`Monte Carlo proves superiority over baselines.`

## 9. Current Pending Items Before Submission

### Results and checkpoints

- retrain all affected checkpoints under the current protocol
- refresh the manuscript tables from current-protocol CSVs
- complete the dedicated small-lesion `128/256/512` evaluator notebooks
- re-check all SAM, ablation, resolution, and Monte Carlo claims against refreshed outputs

### Manuscript cleanup

- fill the second author affiliation
- replace the biography placeholder for Ly Quoc Ngoc
- fill DOI if available at the submission stage
- remove checkpoint placeholders from notebooks intended for release
- remove any redline-only or author-action traces from the submission package
- verify that the Vietnamese self-check translation is not misleading after further English edits

### Optional but out of current required scope

- partial-box experiments
- negative-box experiments
- wrong-region-box experiments
- real radiologist prompt collection
- paired statistical testing against baselines
- confidence calibration study
- cross-dataset transfer evaluation

## 10. Final Writing Checklist

Before treating the paper as submission-ready, verify all of the following:

- every claim is backed by the current protocol, not by legacy numbers
- no section still says `50/50` if the protocol is 80/20
- no section still says `100 epochs` if the protocol is 150
- Attention U-Net is described as an automatic reference, not a fully matched prompt-guided baseline
- SAM-Med2D is described as the prompt-matched baseline
- partial and negative boxes are described as out of scope, not as failed experiments
- GT-derived prompts are described as controlled simulated prompts
- hyperparameters are described as fixed protocol values, not as optimal
- no confidence score is described as a calibrated probability
- no cross-dataset generalization is claimed
- no patient-level split claim exceeds the available metadata
- all placeholders are removed or explicitly marked as pending in internal drafts only

If any item above fails, fix the wording before editing figures or polishing style.

## 11. Practical Read-Then-Write Workflow

Use this sequence when resuming manuscript work after new runs, new CSVs, or new notebook outputs.

### Step 1. Re-anchor the scope before reading any numbers

Read these files first:

- `README.md`
- `Source/README.md`
- `Paper_IEEE_Access/claims_to_validate.md`
- `Paper_IEEE_Access/sections/05-results.tex`

Confirm the following before touching wording:

- whether the paper is still in the pre-retrain state or has refreshed current-protocol results
- which claims are still blocked by `TODO_CHECKPOINT_ID_...`
- which comparisons are architecture-only and therefore not blocked by retraining

If this check is skipped, it is easy to accidentally write old protocol logic into a new paragraph.

### Step 2. Read evidence by claim, not by notebook name alone

Use the claim structure, not the folder structure, as the reading order.

Recommended order:

1. main comparison against Attention U-Net and prompt-matched Attention U-Net variants
2. top-Dice and bottom-Dice subsets
3. matched SAM-Med2D comparison
4. small-lesion subset
5. ablation
6. Monte Carlo
7. efficiency
8. QualityHead or demo material, only if explicitly needed

For each claim, write down:

- exact notebooks used
- whether the results are image-level merged
- which prompt conditions are reported
- whether the numbers are current-protocol outputs or legacy placeholders
- one safe interpretation
- one interpretation that must be avoided

### Step 3. Extract the minimum facts needed for the subsection

Before writing any subsection, reduce the evidence to five items only:

- scientific question of the subsection
- compared models or conditions
- prompt condition or subset definition
- main metric pattern
- scope limit

If a paragraph needs facts outside these five items, check whether the paragraph is drifting into unsupported interpretation.

### Step 4. Use the correct writing mode

There are two allowed modes.

Mode A, pending retrain:

- describe the comparison structure
- describe what the subsection is meant to test
- explicitly mark legacy tables as reference only
- avoid final performance wording

Mode B, refreshed current-protocol results available:

- report the direction of the updated result
- state prompt conditions separately where relevant
- keep absolute values and degradation patterns distinct
- keep the same scope limits as before

Do not mix these two modes inside one subsection.

### Step 5. Subsection template

For most Results subsections, use this internal template:

1. one sentence for the scientific question
2. one sentence for the matched comparison setup
3. one sentence for the reported conditions or subset rule
4. one sentence for the main pattern in the numbers
5. one sentence for the narrow interpretation limit

Example skeleton:

`This subsection tests [question]. The comparison uses [models] under [matched condition]. Results are reported for [prompt condition / subset rule]. The main pattern is [safe factual summary]. This should be interpreted as [narrow claim], not as [forbidden broader claim].`

### Step 6. Reading guide for each major subsection

#### Main Attention U-Net comparison

Read:

- `test-pga-vs-attunet-variants-r512-*`

Write only:

- localization is hard without external prompt guidance
- prompt access and prompt-conditioned processing are different questions

Do not write:

- Attention U-Net is a fully matched prompt baseline

#### Top-Dice and bottom-Dice subsets

Read:

- `test-subcat-pga-vs-attunet-variants-r512-*`

Write only:

- the subsets are induced by Attention U-Net ranking
- the subsets test whether prompt-guided models remain useful where the automatic baseline is relatively stronger or weaker
- the prompt-guided models are re-evaluated on the same exact stems defined by the Attention U-Net ranking

Do not write:

- these are objective clinical difficulty strata

#### SAM-Med2D comparison

Read:

- `test-pga-samzs-samft-r256-*`

Write only:

- matched prompt-based comparison at the same resolution
- absolute Dice and prompt-condition drop must be read separately

Do not write:

- robustness is established from these two simulated prompt conditions alone

#### Small-lesion subset

Read:

- `test-subcat-small-r256-*`
- `test-subcat-small-r512-*`
- `test-subcat-pga-small-r128-256-512-*`

Write only:

- this is a GT-area-defined stress case
- explicit prompt conditioning and resolution may matter more strongly here
- if the notebook uses a shared `512x512` metric frame, say so instead of implying native-frame scoring

Do not write:

- this subgroup alone proves broad clinical utility

#### Ablation

Read:

- `Source/File_Test/{btxrd,fracatlas}/Ablation/`

Write only:

- results are consistent with complementary contributions
- matched qualitative stems matter when the notebook is designed to compare variants row by row

Do not write:

- the ablation proves synergy or a unique mechanism

#### Monte Carlo

Read:

- `test-pga-dataset-1234-*`

Write only:

- split-level stability across repeated random image-level splits

Do not write:

- superiority over baselines

### Step 7. How to read a table before editing its paragraph

For each manuscript table:

- identify whether the values are legacy or refreshed
- identify whether prompt conditions are merged, separated, or missing
- identify whether the table supports a direction claim, a robustness claim, or only a setup claim
- identify one sentence the table can support safely
- identify whether the displayed metric is the manuscript-facing full-frame image-level metric or only an auxiliary diagnostic

If the table does not cleanly support one safe sentence, do not write a stronger sentence to compensate.

### Step 8. Figure-reading rules

When writing from qualitative figures:

- state what the figure illustrates, not what it proves
- check whether the rows come from the same image stems across models
- check whether prompt-guided rows use `center_zoom`, `center_shift`, or both
- mention merged prompt overlays only if they are actually shown in the figure
- if the notebook explicitly reuses shared balanced stems, say that when the figure's fairness depends on it

Safe phrasing:

`The figure illustrates a representative pattern consistent with the quantitative comparison.`

Unsafe phrasing:

`The figure demonstrates that the model is clinically reliable.`

### Step 9. Fast sanity check before saving edits

Before saving a rewritten section, verify:

- every paragraph has one identifiable claim only
- every claim maps to a notebook or table already named in `claims_to_validate.md`
- every prompt-guided comparison states the prompt condition if it matters
- every subgroup paragraph states how the subgroup was defined
- every caution sentence still matches the current protocol

### Step 10. What to do when results are still missing

If refreshed results are still missing, do not block writing completely. Instead:

- keep the scientific question
- keep the comparison structure
- keep the scope limit
- replace final numeric interpretation with a pending-results sentence

Recommended placeholder sentence:

`This subsection defines the comparison structure and claim scope; final quantitative wording will be refreshed after the current-protocol checkpoints and CSVs are updated.`

## 12. Common Failure Patterns to Avoid

These are the mistakes most likely to reappear in later writing sessions.

### Failure Pattern A: mixing two different scientific questions

Wrong move:

- compare PGA-UNet with Attention U-Net and SAM-Med2D in one breath as if they answer one identical question

Why it is wrong:

- Attention U-Net tests automatic localization difficulty
- SAM-Med2D and the prompt-matched Attention U-Net variants test prompt-conditioned processing under matched prompt access

Safe correction:

- split the paragraph into an automatic-reference sentence and a prompt-matched sentence

### Failure Pattern B: turning a controlled prompt study into a detector paper

Wrong move:

- writing as if the model finds lesions on its own
- writing as if prompt suggestion is already a validated detection module

Why it is wrong:

- the present task assumes the suspicious region has already been identified coarsely by the user

Safe correction:

- say that the box narrows the search space and the model segments within that prompted setting

### Failure Pattern C: turning a subgroup into a universal conclusion

Wrong move:

- reading the small-lesion subset as if it proves overall clinical superiority
- reading top-Dice and bottom-Dice groups as intrinsic difficulty strata

Why it is wrong:

- those subsets are constructed for focused analysis, not for universal population claims

Safe correction:

- restate how the subgroup was defined in the same paragraph that interprets it

### Failure Pattern D: letting legacy numbers silently drive new wording

Wrong move:

- keeping old interpretation text after the protocol changed
- forgetting that current tables may still be placeholders

Why it is wrong:

- wording can become stronger than the evidence that currently exists in the repo

Safe correction:

- verify whether the subsection is in pending-retrain mode or refreshed-results mode before editing

### Failure Pattern E: confusing mechanism-level proof with system-level evidence

Wrong move:

- writing that PSG, CAD, or Gaussian prompts are proven to work through one unique internal mechanism

Why it is wrong:

- the current ablation supports useful system-level design choices, not definitive internal causal proof

Safe correction:

- use phrasing such as `consistent with`, `supports`, or `suggests`

### Failure Pattern F: collapsing two different confidence signals into one

Wrong move:

- writing as if the CAD prompt-confidence score and the QualityHead mask-quality score are interchangeable

Why it is wrong:

- the CAD score reflects prompt use inside the decoder
- the QualityHead score is a separate estimated mask-quality signal

Safe correction:

- name which score is being discussed and keep its interpretation narrow

### Failure Pattern G: forgetting that some comparisons must stay image-level and prompt-condition-specific

Wrong move:

- writing one pooled result across `center_zoom` and `center_shift` when the notebooks report them separately
- comparing 128, 256, and 512 using only raw-pixel HD95

Why it is wrong:

- prompt displacement sensitivity is part of the experimental question
- raw HD95 in pixels is not directly comparable across different input resolutions

Safe correction:

- keep the two prompt conditions visible where relevant
- use normalized HD95 for cross-resolution claims

### Failure Pattern H: using the wrong metric variant or wrong evaluation frame in a manuscript claim

Wrong move:

- comparing the prompt-crop baseline with other models using `dice_crop` instead of the pasted-back full-frame result
- describing an R256 small-lesion comparison as if every model were scored only in its own native frame

Why it is wrong:

- some notebooks expose diagnostic metrics for analysis, not for the main manuscript claim
- several subset notebooks are intentionally normalized into one shared metric frame

Safe correction:

- check whether the manuscript-facing metric is `dice_full` or an equivalent full-frame image-level measure
- state the shared metric frame explicitly when it matters

### Failure Pattern I: forgetting that figure fairness in some notebooks comes from shared stems

Wrong move:

- discussing a qualitative panel without noting that all models were shown on the same exact image stems

Why it is wrong:

- several notebook panels are meaningful specifically because they are aligned row by row on identical cases

Safe correction:

- mention shared stems when the figure or subgroup logic depends on them

## 13. Safe Wording Bank

Use these sentence patterns when you need wording that is strong enough to be useful but still defensible.

### For scope

- `The study is framed as a controlled prompted-segmentation task under simulated lesion-covering boxes.`
- `The current evidence does not address unconstrained detection or arbitrary prompt failures.`

### For automatic-reference comparisons

- `The Attention U-Net comparison clarifies how much of the task difficulty lies in localization when no external prompt is provided.`
- `This comparison should be interpreted as an automatic-reference analysis rather than a fully prompt-matched architecture comparison.`

### For prompt-matched comparisons

- `Under matched prompt access, the comparison isolates how the models consume prompt information after coarse localization has already been supplied.`
- `The result should be read as evidence about prompt-conditioned processing, not about free detection ability.`

### For prompt robustness

- `The two prompt conditions measure sensitivity to the controlled displacement defined in this protocol.`
- `These results do not by themselves establish robustness to arbitrary real-world clinician prompts.`

### For small lesions

- `The small-lesion subset is a focused stress case defined directly by GT lesion area.`
- `This subgroup suggests where prompt-conditioned processing may matter most strongly within the evaluated scope.`
- `Where stated in the notebook, the comparison is scored in a shared 512-frame metric space so the models are evaluated against the same final masks.`

### For ablation

- `The ablation results are consistent with complementary contributions from the evaluated components.`
- `The ablation supports the usefulness of the tested design choices at the system level.`

### For Monte Carlo

- `The repeated image-level splits show stability across the evaluated Monte Carlo runs.`
- `This experiment addresses split-level stability, not baseline superiority.`

### For confidence or QualityHead

- `The QualityHead score is an auxiliary model estimate and should not be interpreted as a calibrated probability without dedicated calibration evidence.`
- `The CAD prompt-confidence score reflects prompt use inside the model and is distinct from the QualityHead estimated mask-quality score.`

### For notebook-specific fairness or metric details

- `These qualitative panels use the same exact image stems across models, so the comparison is row-aligned case by case.`
- `For prompt-crop baselines, the manuscript comparison uses the pasted-back full-frame metric rather than the crop-frame diagnostic alone.`

### For protocol details that are easy to forget

- `The test-time off-center prompt is deterministic per sample, whereas the training-time off-center prompt is sampled randomly.`
- `The prompt heatmap is constructed in original-image coordinates and then resized with the image through the same resize-and-pad pipeline.`
- `The comparison with SAM-Med2D is box-only under the current protocol; point-refinement behavior is out of scope here.`
- `Some subgroup notebooks report R256 predictions in a shared 512-frame metric space to keep all compared masks on the same final reference frame.`

## 14. Session Restart Checklist

When opening the repo again after a long break or a lost conversation, do this before writing anything new.

### Minimal restart sequence

1. Read `README.md`.
2. Read `Source/README.md`.
3. Read `Paper_IEEE_Access/claims_to_validate.md`.
4. Read this file from the top.
5. Read `Paper_IEEE_Access/sections/05-results.tex`, `06-discussion.tex`, and `07-conclusion.tex`.
6. Check whether the needed notebooks still contain `TODO_CHECKPOINT_ID_...`.
7. Decide whether you are writing in pending-retrain mode or refreshed-results mode.

### Questions to answer explicitly

- What exact claim am I editing?
- Which notebook or table supports it?
- Is the comparison automatic-reference or prompt-matched?
- Are the results image-level merged?
- Are both `center_zoom` and `center_shift` supposed to be reported here?
- Is the current text still talking about legacy numbers?

If any answer is unclear, stop and resolve it before editing prose.

## 15. Final Self-Check Before Ending a Writing Session

Before closing a session, leave the manuscript in a state that is easy to resume later.

### Leave-behind checklist

- update any paragraph that still mixes automatic-reference and prompt-matched logic
- mark any still-pending quantitative subsection explicitly
- remove any sentence that sounds stronger than the underlying notebook evidence
- check that `80/20`, `150 epochs`, and image-level merged evaluation are still described correctly
- make sure any temporary note clearly says whether it is a writing note, a results note, or a pending retrain note

### Good stopping-point note format

When leaving a note for later, prefer a short line like:

`Pending: refresh this subsection after current-protocol CSVs from [notebook name] are available; keep the existing scope paragraph unchanged.`

This is much safer than leaving vague notes such as `fix later` or `update results`.
