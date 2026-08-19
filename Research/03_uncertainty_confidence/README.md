# Stage 3: confidence without ground truth

## Motivation

At real inference time there is no ground truth to compute Dice/CBL against, so the model has no way to flag a prediction it is likely wrong about. Three independent, no-GT signals are proposed here: a learned estimate of the model's own Dice trained with a dedicated auxiliary loss, how much the decoder trusts the prompt it was given, and how stable the prediction is under a harmless input transform.

## Proposed signals

### 1. Learned quality estimate (dedicated training loss, recommended primary signal)

`QualityHead` (`models/networks/prompt_unet_2D.py`) is a small auxiliary head, global-average-pool over the final decoder features (`up1`) followed by two linear layers, that learns to regress this sample's own real Dice. It is trained jointly with the segmentation loss but with its own separate loss term, `LOSS_CONFIDENCE_WEIGHT * MSE(predicted_quality, real_dice.detach())`, in `train.py`. The `.detach()` on the target means gradients from this loss only update the quality head, never the segmentation output.

At training time, the real Dice is known (GT is available), so the head has a real target to learn from. At inference time, the head still outputs a prediction, using nothing but the image, prompt, and its own learned weights, so no ground truth is needed to produce the confidence score, only during training to teach it what to predict.

```python
model = PGA_UNet(..., use_quality_head=True)     # constructor flag, off by default
# training: PROMPT_MODE=... USE_QUALITY_HEAD=1 LOSS_CONFIDENCE_WEIGHT=0.3 python train.py
logits, predicted_quality = model(images, prompts, return_quality=True)  # inference, no GT needed
```

`use_quality_head` defaults to `False` so the model architecture, and therefore the state_dict keys, exactly matches every checkpoint already trained; only a run explicitly started with `USE_QUALITY_HEAD=1` builds and trains this head.

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
