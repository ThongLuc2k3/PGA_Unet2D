# Stage 3: confidence without ground truth

## Motivation

At real inference time there is no ground truth to compute Dice/CBL against, so the model has no way to flag a prediction it is likely wrong about. Two independent, no-GT signals are proposed here: how much the decoder trusts the prompt it was given, and how stable the prediction is under a harmless input transform.

## Proposed signals

### 1. Prompt confidence (already learned, just exposed)

The Conditional Attention Decoder (`unetUp_PromptAttention` in `models/networks/prompt_unet_2D.py`) already computes a per-level scalar, `self.prompt_confidence`, that gates how much the prompt encoding contributes to the decoder gate at that scale. This value is learned during ordinary training and needs no ground truth to compute at inference; it was simply never exposed outside the module before.

`PGA_UNet.forward` now accepts `return_confidence=False` (default, unchanged behavior). When `True`, it additionally returns a single scalar per sample in `[0, 1]`, the mean of the 4 decoder-level confidence gates:

```python
logits, prompt_confidence = model(images, prompts, return_confidence=True)
```

### 2. Result confidence (test-time augmentation agreement)

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

Both signals are cheap (no retraining, no extra parameters for signal 1; one extra forward pass for signal 2) and can be computed for every real inference, not just test-set images with ground truth.

## Validating the signals (once training resumes)

Neither signal is useful until it is shown to actually correlate with real error. The natural check, using the existing test-set ground truth we do have: compute both confidence signals and the real per-sample Dice on the test set, then look at the correlation (e.g. Spearman) between each signal and Dice. A useful confidence score should be low exactly on the samples where Dice is low. This validation still uses GT, but only to confirm the signal is meaningful; the signals themselves never need GT once validated.

## Status

`PGA_UNet.forward`'s `return_confidence` flag and the `estimate_confidence` helper above are written but not yet run against a real checkpoint or correlated against real test-set Dice. Suggested next step: run this against the stage 1 x2/shift0.3 checkpoint on the BTXRD test set and check whether either signal actually tracks Dice before relying on it for anything downstream (e.g. a future box-suggestion module).
