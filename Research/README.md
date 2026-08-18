# PGA-UNet follow-up research

This branch (`prompt-scale-protocol`) tracks the three follow-up research directions raised in advisor discussions, worked on one at a time in the priority order below. Each stage is trained and evaluated multiple times before moving to the next; nothing here is merged back into the paper on `main` until it is validated.

1. **`01_prompt_scale_protocol/`** (current stage): replace the current independent-per-side random box expansion with a box centered on the tight lesion box and scaled outward by a fixed multiplier, to better match how a clinician would draw a box.
2. **Loss function changes** (after stage 1): add a loss term that pays more attention to small lesions and to centroid accuracy, informed by whichever box protocol stage 1 settles on.
3. **Uncertainty / confidence estimation** (after stage 2): a score for how much to trust a prediction when no ground truth is available, and eventually a box-suggestion module.

Numbers and code changes only land here once real experiments back them up. Illustrations that are conceptual mockups rather than model output are labeled as such in their own folder.
