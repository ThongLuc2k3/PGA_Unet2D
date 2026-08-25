# PGA-UNet Claim Register

This file records the claims currently planned for the IEEE Access manuscript. It separates the scientific question, the required training and test files, and the conditions required before a quantitative claim can be reported.

## Shared Experimental Rules

- All main, baseline, and ablation training runs use the fixed training seed `22120196`.
- The main prompt protocol is `center_mixed` with `scale_factor=3.0`, `shift_ratio=0.5`, and `mixed_shift_prob=0.8`.
- Training therefore uses 80% `center_shift` and 20% `center_zoom`.
- Test evaluation reports `center_zoom` and `center_shift` separately.
- Image-level evaluation groups lesion polygons by source image, merges ground-truth masks by union, merges predicted probability maps by pixelwise maximum, thresholds at 0.5, and then computes the metrics.
- Main segmentation metrics are Dice, IoU, precision, recall, CBL, and HD95. Resolution comparisons should also report normalized HD95.
- BTXRD and FracAtlas are trained and evaluated independently. The experiments do not claim cross-dataset generalization unless a cross-dataset test is added.
- The task scope assumes that the user has identified the suspicious lesion region and provides a box intended to cover that lesion. It is a prompted segmentation task, not an unconstrained detector or a prompt-generation task.
- The current main protocol does not include partial-coverage boxes, negative boxes, or boxes placed on an unrelated normal region. Those settings are outside the defined task scope and must not be used to claim performance or failure in those settings.
- The values `31`, `scale_factor=3.0`, `shift_ratio=0.5`, and CAD depth weights `(1.0, 0.7, 0.4, 0.2)` are fixed protocol choices selected through preliminary experiments. They are not claimed to be globally optimal, and no additional sensitivity experiment is required for the current claim scope.
- `full-heatmap-prompt.ipynb` was removed from both training ablation folders because it duplicates the full Gaussian PGA-UNet configuration represented by `pga-train-512.ipynb`. The corresponding full-heatmap test notebooks remain available for ablation evaluation.
- Any quantitative claim that depends on notebooks still carrying `TODO_CHECKPOINT_ID_...` placeholders remains pending until the matching checkpoints are retrained, uploaded, and referenced with real IDs.

## Claim 1: PGA-UNet Versus Automatic and Prompt-Matched AttUNet

### Scientific question

What is the role of external localization, and does PGA-UNet exploit the provided box beyond simple prompt access?

### Models

1. PGA-UNet.
2. Image-only AttUNet.
3. AttUNet with the binary box prompt concatenated as a second input channel.
4. AttUNet trained on the prompt-box crop.

### Training files

For each dataset, train the four models with:

- `Source/File_Train/{btxrd,fracatlas}/pga-train-512.ipynb`
- `Source/File_Train/{btxrd,fracatlas}/Attention_Unet2D.ipynb`
- `Source/File_Train/{btxrd,fracatlas}/concat-prompt-attunet-r512.ipynb`
- `Source/File_Train/{btxrd,fracatlas}/crop-prompt-attunet-r512.ipynb`

### Test files

- `Source/File_Test/btxrd/test-pga-vs-attunet-variants-r512-btxrd.ipynb`
- `Source/File_Test/fracatlas/test-pga-vs-attunet-variants-r512-fracatlas.ipynb`

The prompt-guided models are evaluated under both `center_zoom` and `center_shift`. This comparison supports both the architecture claim and the associated prompt-displacement robustness claim.

### Claim wording

> PGA-UNet is compared with an image-only AttUNet and two prompt-matched AttUNet baselines to distinguish the contribution of prompt access from the contribution of prompt-conditioned processing.

Do not claim that the automatic AttUNet comparison is a fully matched architecture comparison.

### Localization interpretation

AttUNet without a prompt must localize and segment from the full image. The prompt-channel and prompt-crop variants receive the same type of lesion box as PGA-UNet. Comparing these three settings separates the localization burden of the automatic baseline from the question of how a model consumes an already identified region. The evidence supports the claim that external localization is an important difficulty in this task and that prompt access and prompt-conditioned processing should be discussed separately. It does not prove that localization is the only or universal bottleneck.

## Claim 2: AttUNet Top-Dice and Bottom-Dice Subsets

### Scientific question

Does prompt-guided segmentation remain useful on cases where automatic localization is relatively successful or unsuccessful?

### Procedure

1. Run image-only AttUNet on the full test set.
2. Rank test images by AttUNet Dice.
3. Select the top 50 and bottom 50 image stems.
4. Evaluate PGA-UNet, prompt-channel AttUNet, and prompt-crop AttUNet on the same stems.
5. Report both `center_zoom` and `center_shift` for the prompt-guided models.

### Test files

- `Source/File_Test/btxrd/test-subcat-pga-vs-attunet-variants-r512-btxrd.ipynb`
- `Source/File_Test/fracatlas/test-subcat-pga-vs-attunet-variants-r512-fracatlas.ipynb`

The required checkpoints come from the four training files listed in Claim 1.

### Claim wording

> The top-Dice and bottom-Dice analyses examine whether prompt-guided models retain an advantage on cases where automatic localization is relatively strong or weak, using identical image stems for all compared models.

The subsets are induced by AttUNet performance. They must not be described as intrinsic clinical difficulty groups.

## Claim 3: PGA-UNet Versus SAM-Med2D at 256

### Scientific question

When both models receive the same box prompt and resolution, how effectively does the lightweight PGA-UNet exploit that prompt compared with SAM-Med2D?

### Training files

- PGA-UNet: `Source/File_Train/{btxrd,fracatlas}/pga-train-256.ipynb`
- SAM-Med2D fine-tuning: `Source/File_Train/{btxrd,fracatlas}/Finetune_SAMMed2D_test_robust.ipynb`
- SAM-Med2D zero-shot requires no training.

### Test files

- `Source/File_Test/btxrd/test-pga-samzs-samft-r256-btxrd.ipynb`
- `Source/File_Test/fracatlas/test-pga-samzs-samft-r256-fracatlas.ipynb`

Both `center_zoom` and `center_shift` must be reported.

### Claim wording

> Under the matched box-prompt protocol, PGA-UNet and SAM-Med2D are compared at the same input resolution under both centered and off-center prompts.

A claim that PGA-UNet outperforms SAM-Med2D can be reported only after the affected models are retrained under the current protocol.

## Claim 4: Small PGA-UNet 256 Versus SAM-Med2D 256

### Scientific question

Is prompt-conditioned processing particularly useful for very small lesions?

### Training files

- PGA-UNet 256: `Source/File_Train/{btxrd,fracatlas}/pga-train-256.ipynb`
- SAM-Med2D fine-tuned 256: `Source/File_Train/{btxrd,fracatlas}/Finetune_SAMMed2D_test_robust.ipynb`
- SAM-Med2D zero-shot requires no training.

### Test files

- `Source/File_Test/btxrd/test-subcat-small-r256-btxrd.ipynb`
- `Source/File_Test/fracatlas/test-subcat-small-r256-fracatlas.ipynb`

### Primary metrics

Dice, CBL, and HD95. Dice is the primary overlap metric for this subset because very small regions make IoU highly sensitive to boundary changes.

### Claim wording

> On the GT-area-defined small-lesion subset, PGA-UNet is compared with zero-shot and fine-tuned SAM-Med2D at the matched 256 resolution.

## Claim 5: Small PGA-UNet 512 Versus Prompt-Channel and Prompt-Crop AttUNet

### Scientific question

Does PGA-UNet exploit the prompt more effectively than simple prompt-channel concatenation or prompt-box cropping on small lesions?

### Training files

- `Source/File_Train/{btxrd,fracatlas}/pga-train-512.ipynb`
- `Source/File_Train/{btxrd,fracatlas}/concat-prompt-attunet-r512.ipynb`
- `Source/File_Train/{btxrd,fracatlas}/crop-prompt-attunet-r512.ipynb`
- Image-only AttUNet is used where the subset notebook requires it.

### Test files

- `Source/File_Test/btxrd/test-subcat-small-r512-btxrd.ipynb`
- `Source/File_Test/fracatlas/test-subcat-small-r512-fracatlas.ipynb`

These files evaluate the R512 prompt-guided models on the same small-lesion stems. Both prompt scenarios should remain visible in the reported results.

### Claim wording

> On the small-lesion subset, PGA-UNet is compared with prompt-matched conventional baselines that either concatenate the binary box prompt or restrict the input to the prompt crop.

## Claim 6: Ablation of Gaussian Prompt, PSG, and CAD

### Scientific question

Which components contribute to the full PGA-UNet design?

### Configurations

- CAD-only.
- PSG-only.
- PSG with the original unconditioned attention gate.
- Full architecture with a binary prompt.
- Full PGA-UNet with Gaussian prompt, PSG, and CAD.

The full Gaussian configuration is trained by `pga-train-512.ipynb`. It is not a separate additional model from the deleted `full-heatmap-prompt.ipynb` trainer.

### Training files

- `Source/File_Train/{btxrd,fracatlas}/Ablation/cad-only.ipynb`
- `Source/File_Train/{btxrd,fracatlas}/Ablation/psg-only.ipynb`
- `Source/File_Train/{btxrd,fracatlas}/Ablation/psg-attention.ipynb`
- `Source/File_Train/{btxrd,fracatlas}/Ablation/full-binary-prompt.ipynb`
- `Source/File_Train/{btxrd,fracatlas}/pga-train-512.ipynb` for full PGA-UNet

### Test files

The corresponding files are in:

- `Source/File_Test/btxrd/Ablation/`
- `Source/File_Test/fracatlas/Ablation/`

The full-heatmap test files remain:

- `test-full-pga-heatmap-reference-btxrd.ipynb`
- `test-full-pga-heatmap-reference-fracatlas.ipynb`

### Smaller claims

- CAD-only may outperform the no-prompt-conditioning baseline in some settings.
- PSG-only is not necessarily sufficient.
- PSG and CAD may provide complementary contributions.
- Gaussian prompt encoding may outperform binary prompt encoding within the full architecture.
- The full configuration may achieve the best Dice among the evaluated configurations.
- The difference between `center_zoom` and `center_shift` measures sensitivity to prompt displacement.

Use `consistent with complementary contributions` instead of `proves synergy` unless a suitable factorial statistical analysis is added.

## Claim 7: Monte Carlo Cross-Validation

### Scientific question

Are the main trends stable across repeated random image-level splits?

### Training

Train four independent PGA-UNet checkpoints per dataset using split seeds `1`, `2`, `3`, and `4`, while keeping the training seed fixed at `22120196`.

### Test files

- `Source/File_Test/btxrd/test-pga-dataset-1234-btxrd.ipynb`
- `Source/File_Test/fracatlas/test-pga-dataset-1234-fracatlas.ipynb`

### Claim wording

> Monte Carlo cross-validation evaluates the stability of PGA-UNet across repeated random image-level splits.

Use `shows stability across the evaluated splits` rather than `proves generalization`. This claim concerns PGA-UNet stability, not superiority over a baseline. The current checkpoint IDs are placeholders, so this claim is pending retraining.

## Claim 8: Computational Efficiency

### Scientific question

Can the lightweight architecture support low-cost repeated inference?

### Training

No new training is required for architecture-only measurements.

### Test file

- `Source/File_Test/test-measure_efficiency_btxrd.ipynb`

### Measurements

- Total parameter count.
- Trainable parameter count.
- Frozen parameter count where applicable.
- FLOPs and MACs.
- Checkpoint size.
- Peak GPU memory.
- Mean, standard deviation, minimum, maximum, p50, and p95 latency.
- Latency coefficient of variation.
- Frames per second.
- Milliseconds per megapixel.
- Pixels processed per second.
- GPU and forced CPU latency.

### Claim wording

> PGA-UNet has a lower computational cost and measured latency than SAM-Med2D in the tested hardware, implementation, and input-resolution settings.

Do not extend this to clinical deployment or clinician usability without a dedicated study.

## Claim 9: Polygon-Level Estimated Mask Quality

### Scientific question

Can PGA-UNet provide a no-ground-truth score that helps a clinician review an individual prompt result?

### Training files

- `Source/File_Train/{btxrd,fracatlas}/pga-train-128.ipynb`
- `Source/File_Train/{btxrd,fracatlas}/pga-train-256.ipynb`
- `Source/File_Train/{btxrd,fracatlas}/pga-train-512.ipynb`

QualityHead is trained against the thresholded Dice of the corresponding polygon prompt. It is an auxiliary observer and does not improve the segmentation branch because its inputs are detached before the quality loss.

### Offline evaluation

- `Source/Prompt-Guided-XRay-Segmentation/evaluate_quality_head.py`

The evaluator reports predicted quality, true Dice, absolute error, MAE, RMSE, Pearson correlation, Spearman correlation, and the fraction of masks reaching the selected Dice threshold in each quality bin.

### Demo

- `Source/File_Test/btxrd/test-Demo_Interactive_PGA_Unet-btxrd.ipynb`
- `Source/File_Test/fracatlas/test-Demo_Interactive_PGA_Unet-fracatlas.ipynb`

### Claim wording

> PGA-UNet provides a polygon-level estimated mask-quality score intended to encourage clinician review.

Do not call the score a calibrated probability or interpret `0.80` as an 80% probability of a correct mask without calibration evidence.

The CAD decoder score is a separate `prompt-use score`, not a mask-correctness score.

## Claim 10: Candidate Prompt Suggestion

### Scientific question

Can PGA-UNet rank candidate boxes to assist clinician localization?

### Implementation

The demo samples candidate boxes, runs PGA-UNet for each candidate, scores each result using the QualityHead when available, and returns the top candidates. No separate prompt-suggestion network is trained.

### Files

- `Source/File_Test/btxrd/test-Demo_Interactive_PGA_Unet-btxrd.ipynb`
- `Source/File_Test/fracatlas/test-Demo_Interactive_PGA_Unet-fracatlas.ipynb`

### Claim wording

> The demo ranks candidate prompt boxes using PGA-UNet-generated scores for clinician review.

The clinician remains responsible for selecting or correcting the suspicious region and accepting or rejecting the resulting mask. Do not claim automatic lesion detection.

## Claim 11: PGA-UNet at 128, 256, and 512

### Scientific question

How does input resolution affect prompt-guided segmentation?

### Training and test files

For each dataset, train and evaluate using:

- `Source/File_Train/{btxrd,fracatlas}/pga-train-128.ipynb`
- `Source/File_Train/{btxrd,fracatlas}/pga-train-256.ipynb`
- `Source/File_Train/{btxrd,fracatlas}/pga-train-512.ipynb`

The test cells are embedded in these training notebooks.

### Claim wording

> Higher input resolution preserves more spatial evidence for small-lesion segmentation under the evaluated prompt protocol.

This is an empirical claim and requires the three retrained checkpoints and both prompt scenarios.

## Claim 12: Small-Lesion PGA-UNet at 128, 256, and 512

### Scientific question

Is the resolution effect more visible when the lesion is very small?

### New dedicated test files

- `Source/File_Test/btxrd/test-subcat-pga-small-r128-256-512-btxrd.ipynb`
- `Source/File_Test/fracatlas/test-subcat-pga-small-r128-256-512-fracatlas.ipynb`

### Required protocol

- Use the same GT-area-defined small-lesion stems at all three resolutions.
- Keep the subset definition fixed within each dataset.
- Evaluate `center_zoom` and `center_shift` separately.
- Merge predictions and GT masks at image level.
- Report Dice, IoU, precision, recall, CBL, native HD95, normalized HD95, mean, standard deviation, and paired degradation relative to 512.
- Use the fixed training seed `22120196` for the three model families.

### Claim wording

> The resolution effect is more pronounced on small lesions, where aggressive downsampling can remove a larger fraction of the available lesion evidence.

This claim requires a completed evaluator and all three retrained PGA checkpoints for each dataset.

## Claim 13: Evaluation on Two Datasets

### Scientific question

Does the method show the same general trend on two distinct bone X-ray datasets?

### Scope

Every main claim above should be evaluated independently on both BTXRD and FracAtlas where the corresponding experiment exists. The dataset-specific models are trained separately, and each model is primarily evaluated on its own dataset.

### Claim wording

> The proposed method is evaluated independently on BTXRD and FracAtlas, with the same experimental logic applied to both datasets.

If the results show the same direction across datasets, report that as a replicated trend within the two evaluated datasets. Do not call it external-domain generalization.

## Cross-Cutting Prompt-Robustness Claim

The `center_zoom` and `center_shift` results are not only implementation details. Across Claims 1 through 6 and Claims 9 through 12, the difference between these two scenarios provides evidence about sensitivity to imperfect prompt placement.

Recommended wording:

> The evaluation explicitly measures sensitivity to prompt displacement by reporting separate results for centered covering and controlled off-center prompts.

A stronger robustness claim requires reporting the Dice, CBL, HD95, and relative degradation between the two scenarios. Do not infer clinical robustness from simulated prompts alone.

## Claims Not Yet Supported

The following statements must not be used as established results without additional evidence:

- A QualityHead value of 0.80 is an 80% probability that the mask is correct.
- CAD prompt-use score is the probability that the mask is correct.
- Candidate prompt ranking is automatic lesion detection.
- PGA-UNet is clinically validated or ready for clinical deployment.
- Simulated prompts are equivalent to radiologist-drawn prompts.
- The method generalizes across institutions or external domains.
- Monte Carlo cross-validation proves generalization.
- PSG and CAD causally prove feature preservation without feature-level analysis.
- SAM-Med2D uses the prompt only as a positional cue unless its internal behavior is directly analyzed.
- A single representative qualitative image proves a general performance trend.
