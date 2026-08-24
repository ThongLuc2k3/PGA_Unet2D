# Manuscript Writing Guardrails for `main`

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

## 4. Protocol That the Paper Must Describe

The current protocol is:

- prompt mode: `center_mixed`
- train prompt mixture: 80% `center_shift`, 20% `center_zoom`
- `scale_factor=3.0`
- `shift_ratio=0.5`
- Gaussian kernel size: `31`
- training seed: `22120196`
- max training epochs: `150`
- early stopping patience: `15` for PGA-UNet and Attention U-Net variants
- SAM-Med2D patience: `30`
- model selection: image-level merged validation Dice under `center_shift`
- image-level merged evaluation for validation and test

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
- 80/20 `center_mixed` training
- 150 epochs
- image-level merged validation/test evaluation
- baseline definitions
- primary metrics in the paper body

Recommended metric wording:

`The main paper emphasizes Dice, CBL, and HD95, while the code also records IoU, precision, and recall in the exported reports.`

### Results

Treat each subsection as serving one specific claim:

- main comparison across datasets and resolutions
- resolution effect
- Monte Carlo stability
- automatic-reference comparison with Attention U-Net
- top-Dice and bottom-Dice subsets
- prompt-matched SAM-Med2D comparison
- small-lesion analysis
- efficiency
- ablation

Rules for wording:

- if numbers are still legacy placeholders, say so
- Monte Carlo supports stability, not superiority
- Attention U-Net comparison supports localization-difficulty framing, not a matched architecture win
- SAM comparison should report both absolute values and prompt-condition drop
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
