# PGA-UNet follow-up research

This branch (`prompt-scale-protocol`) tracks the three follow-up research directions raised in advisor discussions, worked on one at a time in the priority order below. Each stage is trained and evaluated multiple times before moving to the next; nothing here is merged back into the paper on `main` until it is validated.

1. **`01_prompt_scale_protocol/`** (decided): replace the independent-per-side random box expansion with a box centered on the tight lesion box and scaled outward by a fixed multiplier. Across the 6 trained (scale, shift) configurations, `center_zoom` x2 with `shift_ratio=0.3` gave the best Dice/CBL under both the Zoom and Zoom + shift test conditions (Zoom Dice 0.8700, Zoom + shift Dice 0.8195), so this is the box protocol carried into stages 2 and 3 below.
2. **`02_loss_function/`** (current stage): add a loss term that pays more attention to small lesions and to centroid accuracy, on top of the x2/shift0.3 box protocol.
3. **`03_uncertainty_confidence/`** (after stage 2): a score for how much to trust a prediction when no ground truth is available, and eventually a box-suggestion module.

Numbers and code changes only land here once real experiments back them up. Illustrations that are conceptual mockups rather than model output are labeled as such in their own folder.
