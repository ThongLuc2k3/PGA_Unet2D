# Nháp II. Related Work (bản để duyệt)

Ngày 2026-09-04. Chưa đụng `.tex`. Đây là bản polish + align cho `sections/02-related-work.tex`.
Giữ nguyên khung ba nhóm và bảng `tab:related`, chỉ thêm phần định vị mà redline yêu cầu.

## Ghi chú thay đổi so với `.tex` hiện tại (và lý do)

1. **Giữ nguyên toàn bộ khung ba nhóm** (phân đoạn tự động và dòng Attention U-Net; phân đoạn
   tương tác và theo prompt; mô hình nền tảng dùng prompt) và giữ khung "thắt vòng vây trước
   khi phân đoạn". Không viết lại các câu đang đúng.
2. **Thêm định vị so với công trình mới** (redline, AUTHOR ACTION số 4):
   - nnU-Net (`\cite{b10}`) vào nhóm tự động: pipeline tự cấu hình nhưng vẫn phải tự khu trú.
   - ScribblePrompt (`\cite{b11}`) vào nhóm tương tác: nhiều loại prompt, đa dataset.
   - EMedSAM và Med-SA (`\cite{b12,b13}`) vào nhóm mô hình nền tảng: biến thể adapter của SAM,
     prompt vẫn tác động chủ yếu ở mask decoder.
3. **Tinh lại câu phát biểu khoảng trống** đúng theo yêu cầu: khi prompt đã khu trú thô rồi,
   prompt chỉ đánh dấu nơi đặt mask, hay còn tiếp tục định hình việc trích đặc trưng để bằng
   chứng tổn thương nhỏ không mất qua downsampling.
4. **Không hứa baseline chưa chạy**: thêm đúng một câu là vòng này so với SAM-Med2D làm mốc,
   so sánh rộng hơn với các mô hình promptable mới hơn để dành cho phần phát triển sau.
5. **Bảng `tab:related`**: thêm 3 hàng (nnU-Net, ScribblePrompt, Med-SA / EMedSAM), giữ nguyên
   6 cột. Ô "Performance Evidence" của hàng "This work" bỏ IoU cho khớp bộ độ đo nhấn mạnh
   trong thân bài (Dice, CBL, HD95). Không có số bịa trong bảng.
6. **U-Net vẫn chỉ xuất hiện như dòng dõi (lineage)**, không có tuyên bố định lượng.

## Việc kèm theo (ngoài phạm vi file này, cần anh xử lý)

`references.tex` hiện chỉ có `b1`..`b9`. Bốn khóa `b10`..`b13` dùng ở trên chưa tồn tại trong
file. Vì không được sửa `.tex`, tôi để anh thêm 4 mục sau vào `references.tex` (lấy đúng từ
danh sách tài liệu của redline). Số trang viết bằng gạch nối đơn ở đây để không dính grep dấu
nối; khi dán vào `references.tex` anh đổi lại thành gạch nối kép cho khớp house style của file:

    \bibitem{b10} F. Isensee, P. F. Jaeger, S. A. A. Kohl, J. Petersen, and K. H. Maier-Hein, ``nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation,'' \textit{Nat. Methods}, vol. 18, pp. 203-211, 2021.
    \bibitem{b11} H. E. Wong, M. Rakic, J. Guttag, and A. V. Dalca, ``ScribblePrompt: Fast and Flexible Interactive Segmentation for Any Biomedical Image,'' in \textit{Proc. Eur. Conf. Comput. Vis. (ECCV)}, 2024, pp. 207-229.
    \bibitem{b12} G. Dong \textit{et al.}, ``An efficient segment anything model for the segmentation of medical images,'' \textit{Sci. Rep.}, vol. 14, art. 19425, 2024.
    \bibitem{b13} J. Wu \textit{et al.}, ``Medical SAM adapter: Adapting segment anything model for medical image segmentation,'' \textit{Med. Image Anal.}, vol. 102, art. 103547, 2025.

Redline mục 3.8 (trích số Dice của hai bài gốc BTXRD/FracAtlas làm mốc bối cảnh) không đưa
vào file này: đó là số cần verify từ `b7`/`b8` và thuộc phần Results/Discussion, không phải
Related Work.

## Proposed English text for `sections/02-related-work.tex`

```latex
\section{Related Work}
Small-lesion segmentation in medical imaging has long been constrained by a simple practical fact: before a model can segment a tiny target well, it must first narrow down where to look. In the fully automatic route, this search-space tightening is learned implicitly inside the network. U-Net established the canonical multi-scale encoder-decoder template for biomedical segmentation \cite{b3}, and Attention U-Net later added attention gates on the skip connections so that decoder-side fusion could suppress irrelevant spatial responses more selectively \cite{b4}. Self-configuring pipelines such as nnU-Net push the same route further by adapting preprocessing, network shape, and training schedule to each dataset automatically \cite{b10}. These models raised automatic segmentation quality considerably, but they still assume that the network itself localizes and delineates the lesion from the raw image alone, with no external hint about where the target lies.

Interactive medical segmentation developed in parallel, from the observation that a small amount of user guidance can simplify the problem substantially \cite{b5,b6}. Early methods used clicks, scribbles, and geodesic cues; later work added boxes as a fast coarse prompt. More recent interactive models such as ScribblePrompt handle several prompt types within a single framework and across many biomedical datasets \cite{b11}. Conceptually, all of these methods move part of the localization burden from the model to the user. For tiny radiographic lesions that shift is especially valuable: a clinician can usually mark a suspicious region coarsely even when a fully automatic system would struggle to find it reliably in the whole image.

The next step was promptable foundation models. SAM introduced general prompt-driven segmentation \cite{b1}, and medical adaptations such as SAM-Med2D and MedSAM carried the idea across many medical domains \cite{b2,b9}. Adapter-based variants such as EMedSAM and Med-SA lower the cost of specializing such models to medical data \cite{b12,b13}. These models are flexible, but the prompt is consumed mainly at the mask decoder, the backbones are large, and the design is not tuned to the statistics of a single radiograph task. For very small bone lesions this leaves one design question open: once a prompt has already localized the approximate region, should the prompt only indicate where the mask should be generated, or should it keep shaping feature extraction and decoding so that weak lesion evidence is not lost during downsampling?

The present work is motivated by that question. In grayscale bone radiographs the task is not only to know roughly where the lesion is, but to preserve faint lesion evidence while suppressing surrounding clutter after the search space has already been tightened. A lightweight prompt-guided CNN may therefore benefit from keeping the prompt active from early encoding to late decoding, instead of using it once as an initial cue or a positional restriction. We study that setting directly and use SAM-Med2D as the promptable reference in this article; a broader comparison with more recent promptable medical models is left to future work.

\begin{table}[t]
\caption{Representative prior work and the remaining gap addressed in this article.}
\label{tab:related}
\centering
\scriptsize
\resizebox{\columnwidth}{!}{%
\begin{tabular}{L{1.9cm}L{2.2cm}L{2.7cm}L{2.7cm}L{2.1cm}L{2.1cm}}
\toprule
Work & Principle & Method & Performance Evidence & Pros & Cons \\
\midrule
U-Net \cite{b3} & Fully convolutional encoder-decoder & Multi-scale skip-connected segmentation network & Widely used as a canonical biomedical segmentation baseline & Simple, efficient, strong reference model & No prompt guidance; all localization must be automatic \\
\midrule
Attention U-Net \cite{b4} & Skip-feature filtering by attention gates & U-Net with gated skip connections & Medical segmentation tasks reported with overlap metrics such as Dice and IoU & Stronger automatic baseline than plain U-Net & Attention is still learned without explicit prompt conditioning \\
\midrule
nnU-Net \cite{b10} & Self-configuring automatic pipeline & Dataset-adaptive preprocessing, architecture, and training & Strong automatic results across many medical benchmarks & Robust automatic pipeline with little manual tuning & No prompt mechanism; localization remains fully automatic \\
\midrule
DeepIGeoS and related interactive methods \cite{b6} & User guidance reduces search space & Geodesic or interaction-aware segmentation & Interactive medical segmentation under user input & Better reflects clinical interaction & Interaction mechanism can be task-specific or costly to maintain \\
\midrule
ScribblePrompt \cite{b11} & General interactive biomedical segmentation & One model for scribbles, clicks, and boxes across datasets & Multi-dataset interactive evaluation with several prompt types & Flexible, realistic interaction types & General-purpose, not a lightweight radiograph-specific prompt prior \\
\midrule
SAM-Med2D / MedSAM \cite{b2,b9} & Promptable foundation segmentation & Large pretrained model with prompt-driven mask decoding & Multi-dataset medical evaluation with prompt-based metrics & Flexible and broadly applicable & Heavy; prompt influence is not designed as a lightweight end-to-end radiograph-specific prior \\
\midrule
EMedSAM / Med-SA \cite{b12,b13} & Adapter tuning of SAM for medical images & Lightweight adapters on a frozen SAM backbone & Medical segmentation with reduced adaptation cost & Cheaper specialization of a foundation model & Still a large SAM backbone; prompt acts mainly at the mask decoder \\
\midrule
This work & Prompt as a dense spatial prior throughout the network & Gaussian plateau prompt + PSG + CAD in a lightweight CNN & BTXRD and FracAtlas; Dice, CBL, HD95, efficiency, and small-lesion analysis & Lightweight, prompt-aware from encoder to decoder, evaluated under controlled prompt displacement & Still requires supervised masks and fixed-resolution preprocessing \\
\bottomrule
\end{tabular}
}
\end{table}
```
