# Nháp III. Method (bản để duyệt)

Ngày 2026-09-04. Chưa đụng `.tex`. Bản polish + align cho `sections/03-method.tex`.
Giữ đúng 5 tiểu mục A..E và cả 3 phương trình. Không có tiểu mục QualityHead (III-F).

## Ghi chú thay đổi so với `.tex` hiện tại (và lý do)

1. **Bỏ III-F Auxiliary Outputs** (đã đề xuất trong `nhap_method_setup.md`). Theo chỉ đạo:
   QualityHead chỉ còn đúng một câu trung lập ở IV. Điểm prompt-use của CAD ($c^{l}$) vẫn được
   mô tả nhưng đóng khung rõ là cổng nội bộ trong CAD, không phải tín hiệu được báo cáo.
2. **III-C Prompt Representation**: làm rõ hành vi test so với train của `center_shift`:
   dịch chuyển ở test là tất định theo từng tổn thương (seed theo chỉ số mẫu), ở train là ngẫu
   nhiên mỗi vòng lặp; box luôn được kéo lại để vẫn bao trọn tổn thương. Thêm ý phạm vi:
   không bao gồm cả câu hỏi "bác sĩ có tự tìm đúng vùng hay không". Không đưa lại protocol cũ
   (tỉ lệ ngẫu nhiên `[0.15, 0.45]`).
3. **III-C / III-E hyperparameter**: nêu rõ các giá trị (scale, shift, kernel, trọng số độ sâu
   CAD) chọn từ thí nghiệm sơ bộ trên train/validation, **test split không dùng để tinh chỉnh**
   (đáp ứng tối thiểu AUTHOR ACTION của redline ở III-E, không thêm sensitivity study).
4. **III-E**: thêm một mệnh đề nói $c^{l}$ chỉ dùng bên trong cổng, không phải đầu ra riêng
   được phân tích trong bài.
5. **III-E**: thêm một dữ kiện kiến trúc: mô hình đầy đủ khoảng 2.95 triệu tham số.
6. Mọi câu khác giữ nguyên.

## Việc kèm theo

Không có `\ref{sec:results}` hợp lệ (mục Results chưa gắn label), nên các câu tham chiếu tránh
dùng `\ref` tới Results; dùng lời văn.

## Proposed English text for `sections/03-method.tex`

```latex
\section{Method}
\subsection{Offline and Online Framework}
The proposed system has two stages. In the offline stage, the model is trained on radiographs paired with lesion polygons. Each polygon is converted into a training prompt by generating a simulated bounding box and then transforming that box into a Gaussian-smoothed plateau heatmap. The network learns to map the image-prompt pair to the binary lesion mask. In the online stage, a user provides a coarse bounding box around a suspected lesion on a new radiograph. The same prompt-construction procedure is applied, and the trained model predicts the final lesion mask.

The scientific contribution of this framework is that the prompt is not treated as an optional side input used only at the first layer. Instead, the prompt is encoded as a dense spatial prior and made active at both encoder and decoder stages. The intended benefit is improved behavior when the prompt is coarse, mildly off-center, or applied to a very small lesion.

\subsection{Problem Setting}
Given a grayscale radiograph $\mathbf{I}\in\mathbb{R}^{H\times W}$ and a user-provided bounding box $\mathbf{B}$, the goal is to predict a binary lesion mask $\hat{\mathbf{M}}$. Let $\mathbf{H}(\mathbf{B})$ be the prompt heatmap derived from the box. PGA-UNet predicts
\begin{equation}
\hat{\mathbf{M}} = \mathbf{1}\left[f_{\mathrm{PGA}}\left(\mathbf{I},\mathbf{H}(\mathbf{B});\theta\right)\ge 0.5\right].
\end{equation}

\subsection{Prompt Representation}
The input prompt is not encoded as a hard binary rectangle. Instead, the box interior is rasterized into a plateau map at the original image resolution and its boundaries are softened with a fixed $31\times31$ Gaussian kernel, before the heatmap is resized and padded down to the target square resolution together with the image. The kernel size is not rescaled with the target resolution ($256\times256$ or $512\times512$): applying it once at the original resolution, prior to downsampling, keeps the effective blur consistent relative to whichever square frame the network ultimately sees. The plateau covers exactly the (possibly expanded) box with no additional minimum margin; coverage of the region of interest is guaranteed by the box expansion described below, not by a separate margin step.

During evaluation, prompts are tested in two fixed settings. The covering prompt (\texttt{center\_zoom}) scales the tight lesion box outward from its own center by a fixed factor of 3.0. The off-center prompt (\texttt{center\_shift}) applies the same scaling and then displaces the box by a fraction of the tight-box size bounded by \texttt{shift\_ratio}=0.5, after which the box is expanded back if needed so that it still fully contains the lesion. At test time this displacement is deterministic per lesion, seeded from the sample index, so every model is evaluated on exactly the same off-center boxes; during training the displacement is redrawn randomly at each iteration. A single model is trained per dataset and resolution with \texttt{center\_mixed}, which selects \texttt{center\_shift} with probability 0.8 and \texttt{center\_zoom} with probability 0.2, and the two conditions are scored separately at test time. The task scope assumes that the user has already identified the suspicious region and provides a box meant to cover that lesion; partial-coverage, negative, and unrelated-region boxes lie outside this controlled prompted-segmentation protocol, as does the separate question of whether a clinician can find the correct region in the first place.

Let $(x_1,y_1,x_2,y_2)$ denote the tight lesion box and let $w=x_2-x_1$ and $h=y_2-y_1$. The simulated covering box uses the fixed center scaling described above during training and evaluation. The off-center box uses the same scaled box and applies the deterministic test-time displacement rule implemented in \texttt{dataset.py}, while preserving lesion coverage. The scale factor, the displacement ratio, and the Gaussian kernel size were chosen from preliminary experiments on the training and validation data and then frozen; the test split was not used for any protocol or hyperparameter choice. They are reported as fixed protocol values, not as globally optimal settings. This simulation is not a substitute for radiologist-drawn prompts, but it provides a controlled way to measure sensitivity to the defined prompt displacement.

Algorithmically, prompt construction follows three steps: 1) derive a lesion box from the polygon annotation or user input and expand it as described above, 2) rasterize the expanded box into a plateau mask at the original image resolution, and 3) smooth the plateau boundary with the fixed Gaussian kernel before resizing to the target resolution. This sequence avoids the hard-edge dependence of a binary box while preserving a clear spatial prior.

\subsection{Prompt Spatial Gate}
Let $\mathbf{x}^{l}$ denote the encoder feature map at level $l$. PSG modulates it with a prompt-derived attention map $\mathbf{A}^{l}_{\mathrm{PSG}}$:
\begin{equation}
\widetilde{\mathbf{x}}^{l}
=
\mathbf{x}^{l}\odot
\left(1+\alpha^{l}_{\mathrm{PSG}}\mathbf{A}^{l}_{\mathrm{PSG}}\right),
\end{equation}
where $\odot$ is element-wise multiplication and $\alpha^{l}_{\mathrm{PSG}}$ is learnable. In the implementation, $\alpha^{l}_{\mathrm{PSG}}$ is initialized to 0.1 and clamped to $[0,1]$. The residual form keeps the original feature stream available while emphasizing prompt-relevant regions.

\subsection{Conditional Attention Decoder}
CAD extends decoder attention by conditioning the skip gate on prompt-encoded features. Let $\mathbf{g}^{l}$ be the decoder gating feature and $\mathbf{p}^{l}_{\mathrm{enc}}$ the prompt encoding at the same scale. The conditioned gate is
\begin{equation}
\mathbf{g}'^{\,l}=\mathbf{g}^{l}+c^{l}\alpha^{l}_{\mathrm{CAD}}w_{l}\mathbf{p}^{l}_{\mathrm{enc}},
\end{equation}
where $c^{l}$ is a decoder-derived prompt-use scalar, $\alpha^{l}_{\mathrm{CAD}}$ is learnable, and $w_{l}$ is a fixed depth coefficient. This design is intended to keep the decoder conditioned on the prompt when the box is not perfectly centered.

The prompt encoder in CAD uses two $3\times3$ convolutions with instance normalization and ReLU. The prompt-use scalar $c^{l}$ is produced by global average pooling followed by a $1\times1$ convolution and a sigmoid nonlinearity. It is computed inside the gate from the prompt encoding and is used only to scale the prompt term at that level; it is not exposed or analyzed as a separate model output in this article. The decoder depth coefficients are fixed to $\{1.0,0.7,0.4,0.2\}$ from deep to shallow layers. With feature scale 4, the channel widths are $\{16,32,64,128,256\}$ from the shallowest encoder stage to the bottleneck, and the complete model has approximately 2.95 million parameters. These protocol values were selected in preliminary experiments on the training and validation data and held fixed for the main evaluation, with the test split excluded from any tuning; no optimality claim is made. The CAD mixing coefficient is parameterized as a sigmoid-transformed scalar and initialized near 0.3.

Taken together, the method can be summarized as follows: 1) preprocess the image and prompt into a common square resolution, 2) encode prompt-relevant spatial priors with PSG in the encoder, 3) propagate prompt-conditioned context through CAD in the decoder, and 4) predict the final binary lesion mask. The scientific meaning of the contribution is that prompt information is both spatially softened and repeatedly reused, rather than being injected once and left to dissipate.

\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{images/architecture/architecture_pga_unet.png}
\caption{Overview of PGA-UNet. Prompt information derived from the bounding box is injected into encoder features through PSG and reused in decoder skip attention through CAD.}
\label{fig:arch}
\end{figure}
```
