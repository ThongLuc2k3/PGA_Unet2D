# Nháp III Method + IV Experimental Setup (bản để duyệt)

Ngày 2026-09-03. Chưa đụng `.tex`. Đây là nháp phần viết mới/sửa cho `sections/03-method.tex`
và `sections/04-experimental-setup.tex`, không phụ thuộc kết quả C9/C10. Prose tiếng Anh là
văn sẽ đưa vào bài; ghi chú tiếng Việt là để anh duyệt.

Nguyên tắc: chỉ thêm phần còn thiếu, không viết lại phần đang đúng.

---

## A. III METHOD

### A.1. Giữ nguyên (đã đúng, không sửa)

- III-A Offline and Online Framework
- III-B Problem Setting
- III-C Prompt Representation. Công thức box hiện tại (scale cố định x3 từ tâm, off-center
  `shift_ratio=0.5`, kernel 31 dựng ở độ phân giải gốc rồi resize) khớp `dataset.py` và
  guardrails. Bản redline nhắc "tỉ lệ ngẫu nhiên [0.15, 0.45]" là protocol CŨ đã bị thay,
  không đưa lại.
- III-D Prompt Spatial Gate
- III-E Conditional Attention Decoder

### A.2. Thêm mới: III-F Auxiliary Outputs (nền cho C9 và C10)

Lý do thêm: abstract và introduction đã nhắc QualityHead, nhưng Method chưa định nghĩa
QualityHead lẫn điểm prompt-use của CAD. Mục này định nghĩa cả hai, khung rõ là tín hiệu
phụ, không phải xác suất hiệu chuẩn.

**Prose (English):**

> \subsection{Auxiliary Outputs: Prompt-Use Score and QualityHead}
>
> PGA-UNet exposes two scalar outputs that need no ground truth at inference and are kept
> separate from the segmentation mask.
>
> The first is a prompt-use score computed inside CAD. At decoder level $l$ the conditioned
> gate already forms a scalar $c^{l}\in[0,1]$ by global average pooling of the prompt
> encoding followed by a $1\times1$ convolution and a sigmoid; this is the same $c^{l}$ that
> scales the prompt term in the conditioned gate. The reported score is the depth-weighted
> mean of these per-level scalars, using the same fixed coefficients
> $w_{l}=\{1.0,0.7,0.4,0.2\}$ that weight the gating fusion, so levels with more influence on
> the output also weigh more in the score. This score reflects how strongly the decoder
> relies on the prompt for a given sample, not whether the resulting mask is correct.
>
> The second is QualityHead, a small auxiliary branch that estimates the model's own Dice
> for the current sample. It concatenates the final decoder feature map, the predicted
> probability map, and the prompt heatmap at full resolution, applies two $3\times3$
> convolutions so it can spatially compare the produced mask against the requested region,
> and then global-average-pools to a single sigmoid score. During training it is regressed
> against the thresholded Dice of the prediction with a mean squared error term. Every input
> to the branch is detached, so this term never propagates into the encoder or decoder and
> QualityHead cannot alter segmentation. At inference it requires no ground truth.
>
> Neither output is a calibrated probability. The two scores also answer different questions
> and are not interchangeable: the CAD score concerns prompt reliance inside the decoder,
> whereas QualityHead concerns the quality of the final mask. In our evaluation the
> QualityHead branch, as trained here, collapsed toward a near-constant estimate and did not
> track the true per-prompt Dice; we therefore treat it as non-functional under the current
> training and discuss it only as a limitation (Section~\ref{sec:discussion}).

**Ghi chú:**
- Cần trỏ đúng số phương trình của $c^{l}$ trong III-E khi ghép vào `.tex`.
- Câu cuối phản ánh quyết định 2026-09-04: C9/C10 gạt sang một bên. Nếu anh muốn nhẹ hơn
  thì bỏ cụm "did not track the true per-prompt Dice", chỉ giữ "we treat it as a limitation".

---

## B. IV EXPERIMENTAL SETUP

### B.1. Giữ nguyên (đã đúng)

- IV-A Datasets (kích thước split, hạn chế patient-level)
- IV-B Training Details phần lớn giữ nguyên (seed, 150 epoch, AdamW, center_mixed 80/20,
  chọn checkpoint image-level merged `center_shift`, fine-tune SAM-Med2D, Monte Carlo split seed)
- IV-C công thức CBL, quy ước HD95
- IV-D Scope of Analysis (box một phần/âm/vùng lạ ngoài phạm vi)

### B.2. Thêm 1 câu vào IV-B: cấu hình loss thí nghiệm (nền cho V-J)

Chỗ chèn: ngay sau câu "The loss was the sum of binary cross-entropy and Dice loss."

**Prose (English):**

> As an exploratory comparison motivated by the small size of the targets, we additionally
> trained PGA-UNet at $512\times512$ with the Dice term replaced by a size-conditioned
> Tversky loss and, in a separate run, by a Focal Dice loss, holding every other setting
> fixed. The two replacements are mutually exclusive and are reported only in
> Section~\ref{sec:results} as a negative control on the objective.

### B.3. (BỎ) IV-E Auxiliary-Signal Evaluation

Quyết định 2026-09-04: C9/C10 gạt sang một bên, không có mục Results, nên **không cần** mục
protocol đánh giá này. Chỉ giữ 1 câu hạn chế trong Discussion (xem `khung_va_bo_cuc_viet_access.md`
mục I.1). Nếu sau này quay lại làm QualityHead tử tế thì mới dựng lại mục này.

### B.4. Thêm 1 câu vào IV về protocol tổn thương nhỏ 3 độ phân giải (nền cho C12)

Chỗ chèn: IV-C hoặc IV-D, chỗ nói về subgroup.

**Prose (English):**

> For the three-resolution small-lesion comparison, the same $50$ smallest-lesion image
> stems are fixed per dataset and evaluated at $128$, $256$, and $512$; predictions and
> ground truth are merged at image level at each resolution, HD95 is reported both in native
> pixels and normalized by $\sqrt{2}\,\cdot\,\text{IMG\_SIZE}$, and degradation is reported
> relative to the $512$ result.

---

## C. Việc sau khi anh duyệt nháp này

1. Ghép III-F vào `sections/03-method.tex`, chèn `\eqref` đúng.
2. Ghép B.2 và B.4 vào `sections/04-experimental-setup.tex` (B.3 đã bỏ).
3. Discussion: thêm câu hạn chế QualityHead (xem `khung_va_bo_cuc_viet_access.md` I.1).
4. Conclusion: thêm câu kết mở.
5. Dịch các đoạn mới sang `vietnam/access_vietnam.tex`.
6. Build thử `latexmk` và `xelatex`, grep lại dấu gạch ngang.

Chưa làm gì cho tới khi anh duyệt.
