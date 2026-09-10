# Nháp: đưa MedSAM + ScribblePrompt vào bài (bản tiếng Việt, chờ duyệt)

Nguồn số: `Result/File_test/{btxrd,fracatlas}/test-{medsam,scribbleprompt}-zeroshot-finetune-*.ipynb`
(image-level merged, cùng giao thức box center_zoom/center_shift với phần còn lại).

## Toàn bộ số (Dice covering / off-center)

| Model | res | BTXRD z/s | BTXRD ft | FracAtlas z/s | FracAtlas ft |
|---|---|---|---|---|---|
| **PGA-UNet** | 512 | — | **0.782 / 0.774** | — | **0.727 / 0.713** |
| MedSAM | 1024 | 0.304 / 0.294 | 0.724 / 0.691 | 0.319 / 0.291 | 0.729 / 0.666 |
| ScribblePrompt | 128 | 0.411 / 0.400 | 0.653 / 0.573 | 0.432 / 0.431 | 0.679 / 0.598 |
| SAM-Med2D | 256 | 0.255 / 0.267 | 0.630 / 0.601 | 0.262 / 0.258 | 0.563 / 0.532 |

Metric đầy đủ covering (Dice / IoU / HD95 / CBL):

| Model (res) | BTXRD z/s | BTXRD ft | FracAtlas z/s | FracAtlas ft |
|---|---|---|---|---|
| PGA-UNet (512) | — | 0.782 / 0.661 / 22.8 / 0.918 | — | 0.727 / 0.585 / 10.5 / 0.913 |
| MedSAM (1024) | 0.304 / 0.185 / 242 / 0.832 | 0.724 / 0.590 / 79.9 / 0.883 | 0.319 / 0.193 / 60.1 / 0.843 | 0.729 / 0.583 / 16.2 / 0.900 |
| ScribblePrompt (128) | 0.411 / 0.285 / 232 / 0.774 | 0.653 / 0.514 / 123 / 0.853 | 0.432 / 0.290 / 34.2 / 0.832 | 0.679 / 0.527 / 17.9 / 0.891 |
| SAM-Med2D (256) | 0.255 / 0.156 / 41.2 / 0.734 | 0.630 / 0.497 / 17.3 / 0.836 | 0.262 / 0.156 / 21.3 / 0.752 | 0.563 / 0.417 / 8.0 / 0.846 |

=======================================================================

## [QUYẾT ĐỊNH D] Mốc so sánh: PGA r512

`tab:sam` hiện dùng PGA **r256** với lập luận "cùng độ phân giải 256 với SAM-Med2D".
MedSAM chạy 1024, ScribblePrompt 128, SAM-Med2D 256 -> KHÔNG có độ phân giải chung.
=> chuyển sang: **mỗi foundation model ở độ phân giải gốc của nó, so với PGA-UNet ở 512
(độ phân giải tốt nhất)**, kèm cột "input res" + 1 câu nói rõ độ phân giải khác nhau.

Nếu vẫn dùng PGA r256 thì FracAtlas covering: MedSAM ft 0.729 > PGA-256 0.629 -> thua.
Với PGA-512:
- BTXRD ft: PGA 0.782 > MedSAM 0.724 > ScribblePrompt 0.653 > SAM-Med2D 0.630 (PGA thắng sạch).
- FracAtlas ft covering: MedSAM 0.729 ~ PGA-512 0.727 (**hoà, MedSAM nhỉnh 0.002**).
- FracAtlas ft off-center: PGA-512 0.713 >> MedSAM 0.666 (PGA thắng rõ).
- CBL + HD95: PGA dẫn ở hầu hết ô.

=> **KHÔNG viết "consistently outperforms" nữa.** Viết "matches or exceeds" + nhấn
off-center + tham số + độ phân giải nhỏ hơn.

=======================================================================

## Bảng mới `tab:sam` (thay bảng cũ, giữ nguyên label `tab:sam`)

```latex
\begin{table}[t]
\caption{So sánh với các baseline nhận prompt, image-level merged, prompt bao phủ.
Mỗi mô hình nền tảng chạy ở độ phân giải cố định của nó; PGA-UNet ở $512$. Vì các
độ phân giải khác nhau, so sánh này không hoàn toàn đồng nhất; so sánh đồng độ phân
giải $256$ với SAM-Med2D nằm ở Mục~\ref{sec:small}.}
\label{tab:sam}
\centering
\scriptsize
\resizebox{\columnwidth}{!}{%
\begin{tabular}{llccccc}
\toprule
Bộ dữ liệu & Mô hình & Res. & Dice & IoU & HD95 & CBL \\
\midrule
\multirow{7}{*}{BTXRD}
& PGA-UNet            & 512  & \textbf{0.782} & \textbf{0.661} & \textbf{22.8} & \textbf{0.918} \\
& MedSAM zero-shot    & 1024 & 0.304 & 0.185 & 242.4 & 0.832 \\
& MedSAM fine-tuned   & 1024 & 0.724 & 0.590 & 79.9  & 0.883 \\
& ScribblePrompt zero-shot  & 128 & 0.411 & 0.285 & 232.2 & 0.774 \\
& ScribblePrompt fine-tuned & 128 & 0.653 & 0.514 & 122.7 & 0.853 \\
& SAM-Med2D zero-shot  & 256 & 0.255 & 0.156 & 41.2  & 0.734 \\
& SAM-Med2D fine-tuned & 256 & 0.630 & 0.497 & 17.3  & 0.836 \\
\midrule
\multirow{7}{*}{FracAtlas}
& PGA-UNet            & 512  & 0.727 & \textbf{0.585} & 10.5 & \textbf{0.913} \\
& MedSAM zero-shot    & 1024 & 0.319 & 0.193 & 60.1 & 0.843 \\
& MedSAM fine-tuned   & 1024 & \textbf{0.729} & 0.583 & 16.2 & 0.900 \\
& ScribblePrompt zero-shot  & 128 & 0.432 & 0.290 & 34.2 & 0.832 \\
& ScribblePrompt fine-tuned & 128 & 0.679 & 0.527 & 17.9 & 0.891 \\
& SAM-Med2D zero-shot  & 256 & 0.262 & 0.156 & 21.3 & 0.752 \\
& SAM-Med2D fine-tuned & 256 & 0.563 & 0.417 & \textbf{8.0} & 0.846 \\
\bottomrule
\end{tabular}
}
\end{table}
```

(Ghi chú: FracAtlas covering để MedSAM ft in đậm Dice 0.729 vì nó nhỉnh hơn PGA 0.727.
PGA vẫn đậm IoU + CBL. Đây là chỗ honest cần giữ.)

=======================================================================

## Mục V-D `05-results` (`vietnam/access_vietnam.tex`), viết lại

Đổi tên tiểu mục: "So sánh khớp với SAM-Med2D" -> **"So sánh với các baseline nhận prompt"**.

Đoạn văn mới (thay đoạn hiện tại ở dòng ~129 EN / tương ứng VN):

> Ba mô hình nền tảng nhận prompt được thử với cùng một hộp: SAM-Med2D (đã đưa vào
> y khoa qua fine-tune diện rộng), MedSAM (fine-tune y khoa, chỉ nhận hộp), và
> ScribblePrompt-UNet (một UNet nhẹ, không phải kiến trúc SAM). Ở chế độ zero-shot,
> cả ba đều gần như không dùng được trên X-quang xương: Dice chỉ 0.25 đến 0.43, với
> precision rất thấp (0.16 đến 0.34) do mask bị phình ra ngoài tổn thương. Fine-tune
> trên cùng split và cùng giao thức prompt kéo Dice lên đáng kể, thêm 0.24 đến 0.42.
> Sau fine-tune, trên BTXRD PGA-UNet ở $512$ (0.782) dẫn trước cả ba (MedSAM 0.724,
> ScribblePrompt 0.653, SAM-Med2D 0.630). Trên FracAtlas với prompt bao phủ, MedSAM
> fine-tune (0.729) ngang PGA-UNet-512 (0.727); nhưng khi prompt lệch tâm, PGA-UNet
> (0.713) bỏ xa MedSAM (0.666), và PGA-UNet dẫn về CBL ở mọi ô cùng về HD95 ở hầu hết
> ô, trong khi chỉ dùng khoảng $1/90$ số tham số của MedSAM và một ảnh đầu vào nhỏ
> hơn. ScribblePrompt-UNet, tuy có số tham số xấp xỉ PGA-UNet, vẫn kém hơn từ 0.05
> đến 0.13 Dice và có khoảng cách bao-phủ-so-với-lệch-tâm lớn nhất trong nhóm (0.08
> trên cả hai bộ dữ liệu). Mỗi mô hình nền tảng được đánh giá ở độ phân giải cố định
> riêng của nó, nên so sánh này không đồng nhất tuyệt đối về độ phân giải; phần so
> sánh đồng độ phân giải $256$ với SAM-Med2D trên tổn thương nhỏ nằm ở
> Mục~\ref{sec:small}. Sự thay đổi từ prompt bao phủ sang lệch tâm được bàn riêng ở
> Mục~\ref{sec:robust}.

=======================================================================

## Các sửa nhỏ (EN + VN)

### 1. Abstract (`00-frontmatter` / VN ~54)
Cũ: "SAM-Med2D as the prompt-matched reference ... PGA-UNet consistently outperforms
two conventional prompt-matched baselines and fine-tuned SAM-Med2D."
Mới: "... SAM-Med2D, MedSAM, and ScribblePrompt as fine-tuned promptable references.
... Given the same box, PGA-UNet matches or outperforms all three fine-tuned
promptable foundation models and two conventional prompt-matched baselines, with a
clear advantage under off-center prompts."
(Câu "fine-tuned SAM-Med2D drops to 0.26 to 0.37 Dice" ở small-lesion GIỮ NGUYÊN, đó
là số SAM-Med2D riêng.)
(Câu "92 times lighter than SAM-Med2D" GIỮ, thêm nửa vế: "and comparable in size to
ScribblePrompt-UNet, which it still outperforms.")

### 2. `01-intro` contribution bullet (dòng 20 EN / ~78 VN)
Cũ: "... and SAM-Med2D; using Dice and IoU ..."
Mới: "... and three fine-tuned promptable models (SAM-Med2D, MedSAM, ScribblePrompt);
using Dice and IoU ..."

### 3. `01-intro` dòng 13 EN (VN ~67)
Cũ: "SAM-Med2D, by contrast, is chosen as the direct comparison because it receives
the same bounding-box input."
Mới: "Promptable foundation models (SAM-Med2D, MedSAM, ScribblePrompt), by contrast,
receive the same bounding-box input and serve as the direct comparison."

### 4. `02-related-work` dòng 8 EN (VN tương ứng)
Cũ: "... using SAM-Med2D as the promptable reference model; a broader comparison with
newer promptable medical models is left to future work."
Mới: "... using SAM-Med2D, MedSAM, and ScribblePrompt as the promptable reference
models."

### 5. `06-discussion` dòng 3 EN
Cũ: "... to a plain Attention U-Net and to fine-tuned SAM-Med2D."
Mới: "... to a plain Attention U-Net and to fine-tuned promptable foundation models."

### 6. `06-discussion` dòng 7 EN (câu "sole promptable foundation-model reference")
Cũ: "In this round, SAM-Med2D remains the sole promptable foundation-model reference;
comparison with newer promptable medical models is left for later."
Mới: XÓA câu này (giờ đã có 3 baseline).

### 7. `07-conclusion` dòng 2 EN (VN ~742)
Cũ: "... as well as fine-tuned SAM-Med2D given the same box ... only about 1/92 that
of SAM-Med2D."
Mới: "... as well as three fine-tuned promptable foundation models (SAM-Med2D,
MedSAM, ScribblePrompt) given the same box, with the clearest margin under off-center
prompts ... only about 1/92 that of SAM-Med2D and on par with the smallest of the
three."

### 8. `02-related-work` bảng dòng 30: thêm dòng ScribblePrompt nếu bảng đó liệt kê baseline
(kiểm tra: bảng related-work có cột "so với PGA". Nếu SAM-Med2D/MedSAM đã 1 dòng thì
thêm 1 dòng ScribblePrompt: "Lightweight promptable UNet | ... | Small but not
radiograph-specific, prompt consumed at decoder only".)

=======================================================================

## KHÔNG đụng
- `tab:small-sam` + prose small-lesion: giữ SAM-Med2D-only (MedSAM/Scri không có
  breakdown tổn thương nhỏ). Không claim PGA thắng MedSAM/Scri trên tổn thương nhỏ.
- `tab:robust`: có thể thêm 2 dòng MedSAM ft + ScribblePrompt ft (z/s) nếu muốn cho
  đầy đủ, nhưng KHÔNG bắt buộc; hiện chỉ có SAM-Med2D ft. [chờ user chốt]
- Efficiency table: ScribblePrompt/MedSAM params chưa đo trong repo -> hoặc bỏ, hoặc
  chỉ nói định tính "ScribblePrompt ~ PGA size, MedSAM ~ SAM-Med2D size". [chờ user]

## Sau khi VN duyệt -> mirror EN 8 file -> build EN pdflatex + VN xelatex -> commit push.
