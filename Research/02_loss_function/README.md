# Stage 2: loss function additions (shelved for now)

## Status: not implemented in code

Two loss additions (centroid loss, Tversky loss) were implemented, then removed from `train.py` after re-checking them against the real x2/shift0.3 numbers and finding neither is justified by anything currently measured. Kept here only as a documented idea to revisit if a real training run later shows the specific weakness each one targets.

## Why removed

`centroid_loss` was meant to directly optimize centroid alignment, but the x2/shift0.3 checkpoint already reaches CBL 0.9245-0.9592 (Zoom and Zoom+shift), so there is little room left for a centroid term to improve.

`tversky_loss` was meant to trade precision for recall on small lesions. Re-checking the actual x2/shift0.3 numbers: precision 0.8558 / recall 0.8930 under Zoom, precision 0.8241 / recall 0.8309 under Zoom+shift. Precision and recall are already reasonably balanced, not one lagging the other, so there is no clear evidence recall specifically needs a boost. The earlier reasoning ("recall is the weak point") leaned on a different, indirect comparison, SAM-Med2D's own recall collapse on small lesions, which does not establish that PGA-UNet's own recall is currently a bottleneck.

In short: no current metric is low enough to justify either loss term. Adding them now would be tuning against a problem that has not been shown to exist yet.

## If revisited later

Only add either loss back if a real training run surfaces the specific gap it targets, for example: recall trailing precision by a wide margin on a future checkpoint (motivates Tversky), or CBL noticeably lower than the current 0.92-0.96 on a future protocol/dataset (motivates centroid). The removed implementations (both unit-checked against a NumPy re-implementation before removal: correct 0-at-perfect-prediction behavior) can be recovered from git history (`git log -- Research/02_loss_function/README.md` and the `train.py` history around commit `03a606b`) rather than rewritten from scratch.
