# Stage 3: confidence without ground truth

## Motivation

At real inference time there is no ground truth to compute Dice/CBL against, so the model has no way to flag a prediction it is likely wrong about. Three independent, no-GT signals are proposed here: a learned estimate of the model's own Dice trained with a dedicated auxiliary loss, how much the decoder trusts the prompt it was given, and how stable the prediction is under a harmless input transform.

## Proposed signals

### 1. Learned quality estimate (dedicated training loss, recommended primary signal)

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

### 2. Prompt confidence (already learned, just exposed)

The Conditional Attention Decoder (`unetUp_PromptAttention` in `models/networks/prompt_unet_2D.py`) already computes a per-level scalar, `self.prompt_confidence`, that gates how much the prompt encoding contributes to the decoder gate at that scale. This value is learned during ordinary training and needs no ground truth to compute at inference; it was simply never exposed outside the module before.

`PGA_UNet.forward` now accepts `return_confidence=False` (default, unchanged behavior). When `True`, it additionally returns a single scalar per sample in `[0, 1]`, the mean of the 4 decoder-level confidence gates:

```python
logits, prompt_confidence = model(images, prompts, return_confidence=True)
```

### 3. Result confidence (test-time augmentation agreement)

Training already includes horizontal flipping as an augmentation, so the model is expected to be roughly flip-invariant. At inference, running the same image and prompt through the model both as-is and horizontally flipped, then measuring the Dice agreement between the two (unflipped-back) binary predictions, gives a second no-GT confidence signal: low agreement suggests the prediction is unstable and less trustworthy.

```python
def estimate_confidence(model, image, prompt, device):
    """No-GT confidence for a single batch. Returns a dict of two (B,) tensors,
    neither of which uses ground truth:
      - prompt_confidence: mean CAD gate value, from the model itself.
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

Signal 2 (CAD gates) is free with any existing checkpoint. Signal 1 (QualityHead) requires training a new checkpoint with `USE_QUALITY_HEAD=1`. Signal 3 (TTA agreement) costs one extra forward pass and works with any checkpoint. All three need no ground truth to compute at inference.

## Validating the signals (once training resumes)

None of the three signals is useful until it is shown to actually correlate with real error. The natural check, using the existing test-set ground truth we do have: compute all three confidence signals and the real per-sample Dice on the test set, then look at the correlation (e.g. Spearman) between each signal and Dice. A useful confidence score should be low exactly on the samples where Dice is low. This validation still uses GT, but only to confirm the signal is meaningful; the signals themselves never need GT once validated.

## Status

`QualityHead`, `PGA_UNet.forward`'s `return_confidence`/`return_quality` flags, and the `estimate_confidence` helper above are written but not yet run against a real checkpoint or correlated against real test-set Dice. Suggested next steps: (1) train one x2/shift0.3 run with `USE_QUALITY_HEAD=1 LOSS_CONFIDENCE_WEIGHT=0.3` to get a checkpoint with a trained QualityHead, then (2) evaluate all three signals against real per-sample Dice on the BTXRD test set and check whether any of them actually track Dice before relying on them for anything downstream (e.g. a future box-suggestion module).
