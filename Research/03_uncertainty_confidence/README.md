# Stage 3: confidence without ground truth

## Motivation

At real inference time there is no ground truth to compute Dice/CBL against, so the model has no way to flag a prediction it is likely wrong about. Four independent, no-GT signals are proposed here, ordered from cheapest to most expensive: pixel-level prediction entropy, test-time-augmentation agreement, a hand-crafted-feature quality estimator, and a learned estimate of the model's own Dice trained with a dedicated auxiliary loss (`QualityHead`), plus one signal specific to this architecture (the CAD prompt-confidence gates).

## Scope: this stage stays a measurement problem, not a product feature

This stage only answers "how well does a no-GT signal track real Dice for a single prediction," validated by comparing the signal against real GT on the test set (correlation, Top-1/Top-K agreement between signal ranking and real Dice ranking). It does **not** include generating many candidate prompts for one image, ranking them, clustering for diversity, or presenting a Top-K shortlist to a clinician; that is a distinct downstream feature (a prompt-search / recommendation system) that belongs only in the interactive demo notebook, `Source/File_Test/btxrd/test-Demo_Interactive_PGA_Unet-btxrd.ipynb`, which already has the Gradio interface such a feature would need. Train/test research notebooks in this repo should stick to the narrower measurement question; any future "Top-K prompts for doctor review" flow should be prototyped in the demo notebook only, once a signal from this stage has been shown to actually correlate with real quality.

## Proposed signals, cheapest first

### 1. Pixel-wise prediction entropy (free, no training, weakest signal)

For each pixel, `sigmoid(logits)` close to 0.5 means the model is unsure; close to 0 or 1 means it is sure. Aggregating that over the mask (mean entropy, or restricted to the boundary region where segmentation errors concentrate) gives an immediate no-GT score with zero extra code beyond the model's existing output. No training, no extra model, works on any existing checkpoint today.

Weakest of the four: it measures how sure the model *feels*, not whether it is *right*. A model can be confidently wrong (this is exactly the Attention U-Net failure pattern already documented in the paper: high-confidence predictions that miss the lesion entirely), so entropy alone should be treated as one input signal, not a final answer.

### 2. Test-time-augmentation (TTA) agreement (free, no training)

Run the same image/prompt through the model as-is and lightly perturbed (currently just a horizontal flip, since that is what training augmentation already includes), and measure how much the two predictions agree. Also free, also works on any existing checkpoint, and a somewhat stronger signal than entropy since it tests actual stability rather than self-reported certainty, though it still cannot catch a consistent, repeatable mistake (wrong in the same way under every perturbation).

```python
def estimate_confidence(model, image, prompt, device):
    """No-GT confidence for a single batch. Returns a dict of two (B,) tensors,
    neither of which uses ground truth:
      - prompt_confidence: mean CAD gate value, from the model itself (see
        signal 5 below).
      - tta_agreement: Dice agreement between the prediction and its
        horizontally-flipped counterpart (flipped back before comparing).
    """
    model.eval()
    with torch.no_grad():
        logits, prompt_confidence = model(image, prompt, return_confidence=True)
        pred_a = (torch.sigmoid(logits) > 0.5).float()

        image_f  = torch.flip(image, dims=[3])
        prompt_f = torch.flip(prompt, dims=[3])
        logits_f, _ = model(image_f, prompt_f, return_confidence=True)
        pred_f = torch.flip((torch.sigmoid(logits_f) > 0.5).float(), dims=[3])

        inter = (pred_a * pred_f).sum(dim=(1, 2, 3))
        union = pred_a.sum(dim=(1, 2, 3)) + pred_f.sum(dim=(1, 2, 3))
        tta_agreement = (2 * inter + 1e-6) / (union + 1e-6)

    return {'prompt_confidence': prompt_confidence, 'tta_agreement': tta_agreement}
```

### 3. Hand-crafted-feature quality estimator (cheap to train, no GPU needed)

Not yet implemented. The idea: compute simple statistics that need no GT at inference, entropy (signal 1), TTA agreement (signal 2), predicted mask area, connected-component count, boundary irregularity, prompt size/position, then train a small classical model (logistic regression, or a small gradient-boosted tree model) to regress real Dice from those features, using the test set's real GT only during this small training step. At inference, only the statistics above are needed, no GT.

This sits between the free signals and `QualityHead` below: still needs a training step with GT, but the model being trained is tiny (seconds to minutes on CPU, no GPU), much easier to debug than a CNN, and lower risk of overfitting than a learned head with its own convolutions. Worth trying before `QualityHead`, not after: if this already tracks real Dice well, the more expensive CNN option may not be worth building.

### 4. Learned quality estimate (`QualityHead`, dedicated training loss, most expensive)

`QualityHead` (`models/networks/prompt_unet_2D.py`) is a small auxiliary head that learns to regress this sample's own real Dice. Its own parameters are trained normally by gradient descent; what makes it a "no-GT" signal is only that, once trained, it needs no GT at inference time, not that it is somehow trained without ever learning anything.

**What it actually looks at.** An earlier version only pooled the final decoder feature map (`up1`) into one vector, an abstract summary with no explicit view of the image, the prompt region, or the mask actually produced. That is a weak basis for a confidence estimate: a head should be able to compare what was asked for against what came out. `QualityHead` now takes three things concatenated at full spatial resolution, not pre-pooled: `up1` (decoder features, carrying image and prompt context), the predicted probability map (`sigmoid(logits)`, what the model actually produced), and the prompt heatmap (what region was asked for). Two 3x3 convolutions mix these spatially, so the head can pick up on things like the predicted mask extending outside the prompted region or not aligning with it, before pooling down to one score.

**How the "no influence on segmentation" property actually works, precisely:**

- `up1` and `logits` are the same tensors `self.final(up1)` uses to produce the segmentation output. Before `QualityHead` sees any of its three inputs, the model detaches all of them (`up1.detach()`, `sigmoid(logits).detach()`, `prompt.detach()`). Detaching cuts the autograd graph at that point, so gradients computed from the quality loss cannot flow backward into anything upstream (the whole encoder/decoder). `QualityHead` is a *pure observer*: whatever it learns can never change how the network segments, only how it self-assesses.
- The training loss is `LOSS_CONFIDENCE_WEIGHT * MSE(predicted_quality, real_dice)`, added in `train.py`, where `real_dice` is computed from the real prediction and GT for that same batch (`per_sample_dice`), then `.detach()`ed as a target (a defensive habit here; the thresholding inside `per_sample_dice` already blocks any gradient regardless).
- Net effect: this loss term only ever updates `QualityHead`'s own parameters (the two mixing convolutions and the two linear layers). It cannot make segmentation better or worse, no matter how large `LOSS_CONFIDENCE_WEIGHT` is set.

**Consequence: QualityHead does not require retraining segmentation from scratch.** Since it never influences the backbone, it can be trained as a cheap fine-tune on top of an already-trained checkpoint (like the stage 1 x2/shift0.3 winner) instead of a full 100+ epoch run:

```bash
PROMPT_DATASET_ROOT=dataset_BTXRD PROMPT_IMG_SIZE=512 \
PROMPT_MODE=center_zoom PROMPT_SCALE_FACTOR=2.0 PROMPT_SHIFT_RATIO=0.3 \
USE_QUALITY_HEAD=1 LOSS_CONFIDENCE_WEIGHT=0.3 \
INIT_CHECKPOINT=checkpoints/pga_unet_center_zoom_x2_512_best.pth \
FREEZE_BACKBONE=1 \
PROMPT_EPOCHS=15 \
python train.py
```

What each new flag does in `train.py`:

- `INIT_CHECKPOINT=<path>`: loads that checkpoint's weights into the model with `strict=False` (the old checkpoint has no `quality_head.*` keys, and the new model has no keys the old checkpoint lacks otherwise, so this always succeeds cleanly). The backbone starts from the already-trained x2/shift0.3 weights instead of random initialization.
- `FREEZE_BACKBONE=1`: sets `requires_grad=False` on every parameter except `quality_head.*`, and builds the optimizer over only those parameters. Only `QualityHead`'s few hundred parameters actually receive gradient updates; the rest of the ~2.95M-parameter model stays frozen at its already-trained values.
- `PROMPT_EPOCHS=15` (or similar, short): since only a tiny head is being trained and the backbone is fixed, this should converge much faster than a full segmentation run.

**A caveat with this cheap fine-tune mode**, since it affects which output file to actually use: with the backbone frozen and the val set deterministic, the segmentation-side validation Dice (`primary_dice`, used for the existing "is this the best epoch" bookkeeping) stays essentially constant every epoch, since predictions don't change once weights are fixed. That means the run's `_best.pth` checkpoint effectively just locks in at whichever epoch happened first, regardless of how much `QualityHead` improved afterward. **Use `{ckpt_prefix}_last.pth` (saved every epoch unconditionally) to get the fully fine-tuned `QualityHead`, not `_best.pth`.**

```python
model = PGA_UNet(use_encoder_prompt=True, use_quality_head=True)
model.load_state_dict(torch.load("checkpoints/pga_unet_center_zoom_x2_qhead_512_last.pth"))
logits, predicted_quality = model(images, prompts, return_quality=True)  # inference, no GT needed
```

`use_quality_head` defaults to `False` so the model architecture, and therefore the state_dict keys, exactly matches every checkpoint already trained; only a run explicitly started with `USE_QUALITY_HEAD=1` builds this head at all, and `return_quality=True` raises a clear error if called on a model that was not.

### 5. Prompt confidence (architecture-specific bonus signal, already learned, just exposed)

The Conditional Attention Decoder (`unetUp_PromptAttention` in `models/networks/prompt_unet_2D.py`) already computes a per-level scalar, `self.prompt_confidence`, that gates how much the prompt encoding contributes to the decoder gate at that scale. This value is learned during ordinary training and needs no ground truth to compute at inference; it was simply never exposed outside the module before. Free with any existing checkpoint, no retraining needed, and already included in the `estimate_confidence` helper above.

```python
logits, prompt_confidence = model(images, prompts, return_confidence=True)
```

## Decision: signal 4 (`QualityHead`) is primary, signal 3 is the fallback plan

Originally planned cheapest-first (try signal 3's hand-crafted-feature estimator before ever training `QualityHead`). Revisited once it became clear PGA-UNet itself will keep being retrained repeatedly (new scales, FracAtlas, etc.), which changes the cost-benefit:

- **Signal 3** structurally cannot train jointly with PGA-UNet: it always needs a finished PGA checkpoint's outputs as input features first. Every time PGA-UNet is retrained, signal 3's small model needs to be redone (cheap individually, but it compounds if PGA changes often).
- **Signal 4 (`QualityHead`)** is built into `PGA_UNet` itself and its loss is fully gradient-isolated (see below), so it can simply be turned on (`USE_QUALITY_HEAD=1`) from epoch 1 of any PGA-UNet training run, no separate step, automatically in sync with whichever checkpoint comes out.

Given PGA-UNet is expected to keep changing, **signal 4 is now the one being trained and evaluated**: `train_quality_head_x2_shift03_btxrd.ipynb` trains PGA-UNet fresh under the stage 1 winning protocol (center_zoom, scale_factor=2.0, shift_ratio=0.3) with `USE_QUALITY_HEAD=1 LOSS_CONFIDENCE_WEIGHT=1.0` active from the start, then validates whether `predicted_quality` (and, for free, the CAD `prompt_confidence` gate) actually correlates with real per-sample Dice on the BTXRD test set.

**Signal 3 remains the documented fallback**, to fall back on only if signal 4's correlation with real Dice turns out weak: cheaper, safer, easier to explain, but requires its own redo step each time PGA-UNet changes. Signals 1 (entropy) and 2 (TTA agreement) stay useful regardless of which of 3/4 wins, since they are free and can be added as extra input features to signal 3 later if needed.

## Validating the signals

None of the five signals is useful until it is shown to actually correlate with real error. The check, using the existing test-set ground truth: compute each no-GT signal and the real per-sample Dice on the test set, then look at the correlation (e.g. Spearman) between each signal and Dice. A useful confidence score should be low exactly on the samples where Dice is low. This validation still uses GT, but only to confirm the signal is meaningful; the signals themselves never need GT once validated. This validation, correlation against real per-sample Dice on the existing test set, is the extent of what belongs in the train/test research notebooks (see Scope above); ranking or shortlisting multiple candidate predictions for a clinician is a separate, later feature for the demo notebook only.

## Status

Signal 1 (entropy) and signal 3 (hand-crafted-feature estimator, the fallback plan) are not yet implemented. Signal 2 (TTA agreement) and signal 5 (CAD prompt confidence) are implemented via `estimate_confidence` above and also folded into the notebook below. Signal 4 (`QualityHead`) is implemented and ready to train.

**Ready to run:** `train_quality_head_x2_shift03_btxrd.ipynb` in this folder. Trains PGA-UNet from scratch on BTXRD/512 under `PROMPT_MODE=center_zoom PROMPT_SCALE_FACTOR=2.0 PROMPT_SHIFT_RATIO=0.3 PROMPT_EPOCHS=150` (the stage 1 x2/shift0.3 winner's exact protocol) with `USE_QUALITY_HEAD=1 LOSS_CONFIDENCE_WEIGHT=1.0` active from epoch 1, then: (1) confirms the Zoom/Zoom+shift segmentation numbers still match the stage 1 winner (sanity check that QualityHead did not affect segmentation), and (2) computes the Spearman correlation between `predicted_quality` (signal 4) and real per-sample Dice, and separately between `prompt_confidence` (signal 5) and real Dice, with a scatter plot of each. Needs this branch pushed to `origin` before it can be cloned from Colab/Kaggle.

Next steps after this run: if the printed `rho` for `predicted_quality` is not clearly positive and reasonably large (a weak or near-zero correlation means the signal does not track real quality and should not be trusted), fall back to signal 3 (hand-crafted-feature estimator) instead, reusing whichever of entropy/TTA/CAD-confidence turned out informative as its input features.
