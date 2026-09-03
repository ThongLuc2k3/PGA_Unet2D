# Nháp IV. Experimental Setup (bản để duyệt)

Ngày 2026-09-04. Chưa đụng `.tex`. Bản polish + align cho `sections/04-experimental-setup.tex`.
Giữ 4 tiểu mục A Datasets, B Training details, C Baselines and metrics, D Scope of analysis.
Không có tiểu mục IV-E (Auxiliary-Signal Evaluation đã hủy).

## Ghi chú thay đổi so với `.tex` hiện tại (và lý do)

1. **IV-A Datasets**: giữ nguyên kích thước split. Mở rộng một mệnh đề về hạn chế patient-level
   (redline mục 5): metadata công khai không đủ để tách theo bệnh nhân, nên về nguyên tắc các
   ảnh của cùng một bệnh nhân có thể rơi vào các split khác nhau.
2. **IV-B Training details**:
   - Nêu rõ seed `22120196` seed cho Python, NumPy, PyTorch (CPU và CUDA).
   - Thêm câu về thí nghiệm loss (nền cho mục Results V-J): huấn luyện thêm PGA-UNet 512 với
     size-conditioned Tversky và, ở lần chạy riêng, Focal Dice; hai lựa chọn loại trừ nhau,
     chỉ báo cáo sau như một negative control. Không đưa số.
   - SAM-Med2D: thêm một câu là cách dựng box này **khác** với small-jitter
     `get_boxes_from_mask` của nhóm tác giả gốc, ở đây không dùng.
   - Thêm **đúng một câu trung lập** về QualityHead: nhánh hồi quy chất lượng phụ trợ, bị
     detach, không ảnh hưởng phân đoạn, đầu ra không dùng trong bài.
3. **IV-C Baselines and metrics**:
   - Giữ câu "thân bài nhấn Dice, CBL, HD95; IoU, precision, recall nằm trong report" (đây là
     AUTHOR ACTION của redline, đã có sẵn, giữ nguyên).
   - Thêm HD95 chuẩn hóa `HD95 / (sqrt(2) * S)` cho so sánh xuyên độ phân giải.
   - Thêm câu về khung metric 512 chung khi trộn model R256 và R512 trong một số so sánh subset.
4. **IV-D Scope of analysis**:
   - Định nghĩa chính xác tập tổn thương nhỏ: "50 test images with the smallest total lesion
     area" (sửa cụm mơ hồ "50 smallest lesions" theo redline).
   - Thêm câu về protocol so sánh 3 độ phân giải: cố định cùng 50 stem đó cho mỗi dataset ở
     128 / 256 / 512, merge mức ảnh, báo HD95 native + chuẩn hóa, và mức tụt so với 512.
   - Đổi cụm "auxiliary screening pipeline explored separately outside the present manuscript"
     thành mô tả trung lập hơn (self-assessment và gợi ý prompt nằm ngoài phạm vi bài).
5. Không thêm hứa hẹn baseline promptable hiện đại hay paired-statistics vào mục này (thuộc
   Discussion/Conclusion, và vòng này để future work theo kế hoạch).

## Việc kèm theo

Redline mục 3.8 (số Dice của hai bài gốc BTXRD/FracAtlas) chưa đưa vào: cần số verify từ
`b7`/`b8`, thuộc Results/Discussion.

## Proposed English text for `sections/04-experimental-setup.tex`

```latex
\section{Experimental Setup}
\subsection{Datasets}
We evaluate on two public bone radiograph datasets. BTXRD is a primary bone tumor X-ray dataset with polygon annotations for classification, localization, and segmentation \cite{b7}. Our BTXRD split contains 1,493/187/187 images with 1,848/238/232 lesion polygons for training, validation, and testing, respectively. FracAtlas is a fracture radiograph dataset with classification, localization, and segmentation labels \cite{b8}. After data cleaning and polygon normalization, our FracAtlas split contains 573/72/72 images with 730/95/92 lesion polygons for training, validation, and testing, respectively.

Splits are performed at the image level, and all polygons from the same image are kept in the same split. The public metadata were insufficient to verify strict patient-level separation, so images from the same patient could in principle fall into different splits; we treat this as a limitation of the evaluation. Each polygon is treated as one promptable lesion sample during training. For image-level evaluation, if an image contains multiple lesions, the model is run once per lesion box and the probability maps are merged by pixelwise maximum before thresholding at 0.5. Ground-truth masks are merged by union in the same image.

Inputs are resized isotropically and padded to square resolutions of $256\times256$ or $512\times512$ to preserve aspect ratio. Images, masks, and prompt maps undergo the same geometric preprocessing.

\subsection{Training Details}
\label{sec:training}
All CNN models were implemented in PyTorch and trained on an NVIDIA Tesla T4 GPU with 16 GB memory. PGA-UNet and Attention U-Net were trained separately on each dataset and resolution. In other words, the article studies one shared architecture family instantiated as separate models with separate parameter sets for BTXRD and FracAtlas, rather than a single jointly trained cross-dataset model. The optimizer was AdamW with learning rate $10^{-4}$ and weight decay $10^{-4}$. The loss was the sum of binary cross-entropy and Dice loss. As an exploratory check motivated by the small size of the targets, PGA-UNet was additionally trained at $512\times512$ with the Dice term replaced by a size-conditioned Tversky loss and, in a separate run, by a Focal Dice loss, with every other setting held fixed; the two replacements are mutually exclusive and are reported later only as a negative control on the training objective. Batch size was 4, the maximum training budget was 150 epochs, and early stopping with patience 15 was used. All main and ablation training runs use the fixed training seed 22120196, which seeds Python, NumPy, and PyTorch randomness on both CPU and CUDA. The primary model-selection criterion was image-level merged validation Dice under the \texttt{center\_shift} condition.

Training-time augmentation included horizontal flipping and random rotation within $\pm15^\circ$. The implementation also applied prompt dropout or prompt noise to a subset of training iterations to reduce over-reliance on an ideal prompt. PGA-UNet is trained with \texttt{center\_mixed}, selecting \texttt{center\_shift} with probability 0.8 and \texttt{center\_zoom} with probability 0.2. The prompts are simulated from lesion annotations to provide a controlled prompted-segmentation protocol. The current article should therefore be read as a study under simulated lesion-covering boxes around user-identified lesions, not as an evaluation of unconstrained lesion detection or fully realistic radiologist-drawn boxes. For the fine-tuned SAM-Med2D comparison, the pretrained image encoder was frozen except for its lightweight Adapter layers, while the prompt encoder and mask decoder were fully updated on each dataset under the same split protocol. SAM-Med2D was fine-tuned with box prompts only, using the same center-scaled covering and off-center protocol as PGA-UNet; the point-prompt branch and iterative point refinement were disabled. This box construction differs from the small random-jitter \texttt{get\_boxes\_from\_mask} sampling used by the original SAM-Med2D authors, which was not applied here. Validation during SAM-Med2D fine-tuning and the final test split used both prompt scenarios, with batch size 4, a maximum of 150 epochs, early stopping patience 30, and learning rate $10^{-5}$. The matched protocol reduces differences caused by prompt distribution and resolution, but does not eliminate differences in model scale, initialization, or optimization. Additional stability experiments were performed using Monte Carlo cross-validation, that is, repeated random image-level splits rather than strict non-overlapping $k$-fold partitioning. The Monte Carlo experiments keep the training seed fixed at 22120196 and vary only the split seed across 1, 2, 3, and 4.

PGA-UNet also carries a small auxiliary quality-regression head. It is detached from the segmentation branch and does not affect the predicted mask, and its output is not used in this article.

Two evaluation details are important for interpreting the results. First, prompt generation itself is resolution-agnostic: the plateau heatmap is built and smoothed with a fixed $31\times31$ Gaussian kernel at the original image resolution, and only the resulting heatmap is resized and padded down to $256\times256$ or $512\times512$ together with the image, so the same absolute blur is compressed differently by the two target resolutions rather than being parameterized separately for each. Second, the Monte Carlo cross-validation experiments are auxiliary stability evidence rather than replacements for the fixed train/validation/test split used in the main tables.

\subsection{Baselines and Metrics}
PGA-UNet is compared with Attention U-Net \cite{b4} as the main automatic baseline and with SAM-Med2D \cite{b2} as the main prompt-based baseline. Attention U-Net is trained without prompts and is used to characterize how difficult the task is when localization must be solved automatically. SAM-Med2D is evaluated at $256\times256$ in fine-tuned form with the same dataset splits and the same box prompts as PGA-UNet, making it the primary prompt-matched comparison.

To further isolate whether PGA-UNet's advantage comes from its architecture or simply from having access to the box prompt at all, we add two prompt-matched conventional baselines built on the same Attention U-Net backbone, given the identical box prompt PGA-UNet receives but without PGA-UNet's Gaussian-prior heatmap, Prompt Spatial Gate, or Conditional Attention Decoder. Attention U-Net with a concatenated prompt channel appends the prompt heatmap as a second input channel and predicts on the full image through a plain skip-connection decoder. Attention U-Net on prompt crops instead restricts the network's field of view: the input image is cropped to the prompt box before resizing to the model's input resolution, the plain Attention U-Net predicts a mask on that crop alone, and the prediction is pasted back into the full frame for evaluation. Both baselines are trained under the same covering and off-center box protocol as PGA-UNet, so any remaining gap reflects the architecture rather than an unequal prompt. Cross-model comparisons use the pasted-back full-frame metrics for the prompt-crop baseline, not its crop-frame diagnostic values.

The main paper emphasizes Dice, CBL, and HD95, while the code and exported reports also record IoU, precision, and recall. For a predicted mask centroid $(x_p,y_p)$, a ground-truth centroid $(x_g,y_g)$, and the diagonal length $D_{\mathrm{GT}}$ of the ground-truth bounding box, CBL is defined as
\begin{equation}
\mathrm{CBL}=\max\left(0,1-\frac{\sqrt{(x_p-x_g)^2+(y_p-y_g)^2}}{D_{\mathrm{GT}}}\right).
\end{equation}
HD95 is computed from bidirectional boundary distances. If both masks are empty, HD95 is set to 0. If exactly one mask is empty, HD95 is set to the input side length $S$ (256 or 512 pixels). No samples are discarded. For comparisons that span input resolutions, HD95 is also reported in normalized form, $\mathrm{HD95}/(\sqrt{2}\,S)$, because a raw pixel distance is not comparable across the $128$, $256$, and $512$ frames. Some subgroup comparisons that mix models trained at $256\times256$ and $512\times512$ are scored in a shared $512\times512$ frame: the $256\times256$ predictions are upsampled before scoring, so every model is measured against identical ground-truth masks rather than in its own native frame.

\subsection{Scope of Analysis}
This article focuses on prompt-guided segmentation itself and excludes the auxiliary self-assessment and prompt-suggestion behavior, which addresses a different question and is outside the present scope. To keep the article compact, we retain only the subgroup analyses that most directly support the main claim: the role of prompt-guided localization, sensitivity to the controlled prompt displacement defined in this study, and effectiveness on very small lesions. The small-lesion subgroup is defined per dataset as the 50 test images with the smallest total lesion area. For the three-resolution small-lesion comparison, this same set of image stems is held fixed and evaluated at $128$, $256$, and $512$; predictions and ground truth are merged at image level at each resolution, HD95 is reported both in native pixels and in the normalized form above, and degradation is reported relative to the $512$ result. Partial-coverage boxes, negative boxes, and unrelated-region boxes are outside the present task scope and are therefore not used to support or reject the paper's claims.
```
