# Khung lập luận và bố cục viết lại bài IEEE Access (bản để duyệt)

Ngày 2026-09-03. Chưa đụng `.tex`. Đây là bản đọc hiểu, đánh giá hiện trạng, và đề xuất
bố cục để anh duyệt trước khi bắt đầu viết.

## A. Đã đọc những gì

- `Paper_IEEE_Access/manuscript_writing_guardrails.md` (toàn bộ 15 mục)
- `Paper_IEEE_Access/claims_to_validate.md` (13 claim + claim robustness xuyên suốt)
- `Paper_IEEE_Access/ke_hoach_chinh_sua_bai_bao.md`
- `PGA-UNet_IEEE_Access_Redline_Revision_VI.pdf` (13 trang + bảng ưu tiên + checklist biên tập)
- Toàn bộ `Paper_IEEE_Access/sections/00..08`
- `README.md` gốc + `Source/README.md`
- Số liệu mới trong `Result/` (train + test, BTXRD + FracAtlas, gồm ablation, Monte Carlo,
  và 3 nhánh loss `00` / `01` / `10`)

## B. Bài đang ở đâu

### B.1. Phần đã ổn định, chỉ cần rà nhỏ

Method, Related Work, Experimental Setup, và khung Discussion/Conclusion đã bám đúng guardrails:

- Logic hai tầng so sánh đã tách rõ: Attention U-Net là tham chiếu tự động (đo độ khó
  khu trú), SAM-Med2D là so sánh khớp prompt. Không còn câu nào đọc như "PGA-UNet thắng
  Attention U-Net nên kiến trúc tốt hơn".
- Khung "thắt vòng vây" đã có trong Introduction và Related Work.
- Protocol mô tả đúng: `center_mixed` 80/20, scale x3, shift 0.5, kernel 31, seed
  22120196, 150 epoch, chọn checkpoint theo image-level merged val Dice ở `center_shift`.
- Đã có 2 baseline prompt-matched (`concat-prompt-attunet`, `crop-prompt-attunet`), đúng
  AUTHOR ACTION số 1 của thầy.
- QualityHead và CAD prompt-confidence được tách rõ là 2 tín hiệu khác nhau, không cái nào
  bị gọi là xác suất hiệu chuẩn.

### B.2. Phần đang treo

- `sections/05-results.tex` vẫn để nguyên bảng số cũ (protocol trước) kèm "Status note".
  Toàn bộ bảng trong thân bài hiện là legacy.
- Theo quyết định của anh ngày 2026-09-01: train lại PGA cả 2 dataset để chọn checkpoint
  tốt nhất, chạy lại toàn bộ ablation multi-seed, chạy lại FracAtlas. Nên Claim
  1, 2, 3, 4, 5, 7, 11, 12 quay lại pending; mục Ablation chỉ nên ghi 1 câu "đang chạy lại".
- Efficiency (Claim 8) là số kiến trúc, không bị chặn, viết được ngay.

### B.3. Điểm cần anh chốt trước khi viết số

1. **FracAtlas 512 đã đổi số.** [Đã chốt 2026-09-03] Thư mục `Result/File_train/{btxrd,fracatlas}/pga 512/00/`
   là checkpoint PGA-512 chính thức mới nhất. Số canonical: BTXRD test zoom/shift
   0.7817 / 0.7740, FracAtlas 0.7271 / 0.7134. Bỏ hẳn số cũ 0.666 / 0.657.
2. **Ablation: full PGA không phải cấu hình tốt nhất** trên BTXRD trong đợt chạy hiện tại
   (vài biến thể hơn nhẹ, nằm trong độ lệch Monte Carlo). Đây là lý do anh quyết chạy lại
   multi-seed. Bài viết mục Ablation ở Mode A cho tới khi có số mới.
3. **Bảng Top/Bottom-Dice, SAM, small-lesion** trong `Result/` đã có số mới nhưng phụ thuộc
   checkpoint PGA "best" anh đang chọn lại. Nếu PGA chọn theo "best" thì AttUNet x2 và
   SAM-Med2D phải cùng cách chọn (cùng multi-seed hoặc cùng một seed cố định), nếu không sẽ
   dính AUTHOR ACTION số 3 của thầy.

## C. Bộ claim chính, gom gọn để khỏi lan man

13 claim quy về 4 trục. Bài nên bám đúng 4 trục này.

**Trục 1: Prompt là thiết yếu, không phải kiến trúc thắng kiến trúc.**
Bằng chứng: Attention U-Net tự động (Dice khoảng 0.52 BTXRD, 0.34 FracAtlas) so với
PGA-UNet có prompt; cộng subset Top-Dice / Bottom-Dice. Đọc đúng: bài toán không-prompt rất
khó, không phải PGA-UNet giỏi kiến trúc hơn.

**Trục 2: Đã có prompt rồi thì khai thác thế nào cho tốt.**
Bằng chứng: PGA-UNet vs SAM-Med2D @256 (cùng box, cùng độ phân giải); PGA-UNet vs 2 baseline
AttUNet prompt-matched @512. Đọc đúng: PSG và CAD giữ tín hiệu tổn thương nhỏ xuyên suốt
mạng, khác cách SAM chỉ dùng box để chỉ vùng ở mask decoder.

**Trục 3: Tổn thương nhỏ là nơi thiết kế này ăn tiền nhất.**
Bằng chứng: subset 50 ảnh diện tích tổn thương nhỏ nhất. SAM-Med2D-FT gần như không tạo
được mask (Dice khoảng 0.19 BTXRD), PGA-256 khoảng 0.76, PGA-512 khoảng 0.85. Đây là bằng
chứng mạnh nhất của bài. Cộng hiệu ứng độ phân giải 512 > 256 > 128.

**Trục 4: Ổn định và chi phí.**
Monte Carlo 4 split (std < 0.012) cho độ ổn định mức chia dữ liệu. Efficiency: 2.95M tham
số, khoảng 92x nhỏ hơn SAM-Med2D. Đọc đúng: ổn định không phải vượt trội thống kê; chi phí
thấp không phải sẵn sàng lâm sàng.

Ablation (Gaussian vs binary, PSG, CAD) là bằng chứng hỗ trợ Trục 2, viết theo "consistent
with complementary contributions".

## D. Khung lập luận xuyên suốt

Một câu: *Bài toán tổn thương nhỏ trên X-quang xương khó chủ yếu ở bước khu trú; PGA-UNet
nhảy cóc qua bước detection bằng box của bác sĩ, rồi thiết kế PSG và CAD để tín hiệu vùng
nhỏ không bị suy hao qua downsampling; đóng góp thật nằm ở cách khai thác prompt, rõ nhất
trên tập tổn thương nhỏ, chứ không phải ở việc thắng một baseline không-prompt.*

Mỗi mục Results phải quay về đúng một mắt xích của câu này.

## E. Sổ claim đầy đủ (mỗi claim ghi rõ MỤC TIÊU: chứng minh cho điều gì)

Cập nhật 2026-09-04: **C9 và C10 đã QUAY LẠI bài** (không còn gạt bỏ) vì điểm training-free
Q đạt ngưỡng trên cả 2 dataset. Cột "Số" là số hiện có; toàn bộ đã viết vào `05-results.tex`
(trừ Ablation C6 đang Mode A).

Câu chuyện xuyên suốt (spine): *bài toán tổn thương nhỏ khó chủ yếu ở bước khu trú; PGA-UNet
dùng box của bác sĩ để nhảy cóc qua detection, rồi PSG + CAD giữ tín hiệu vùng nhỏ xuyên
suốt mạng; đóng góp thật nằm ở cách khai thác prompt, rõ nhất ở tổn thương nhỏ.*

Ký hiệu tên mô hình:
- **PGA-UNet** = `Source/Prompt-Guided-XRay-Segmentation/models/networks/prompt_unet_2D.py` (class `PGA_UNet`),
  checkpoint `pga_unet_center_mixed_x3_shift05_qhead_{128,256,512}_best.pth`, train bằng
  `pga-train-{128,256,512}.ipynb`.
- **Attention U-Net** = `models/networks/attention_unet_2D.py` (class `Attention_UNet_2D`), train
  `Attention_Unet2D.ipynb`, checkpoint `attunet_best.pth` (không có box).
- **AttUNet + prompt-channel** = `models/networks/attunet_concat_prompt.py`, train
  `concat-prompt-attunet-r512.ipynb`, ckpt `attunet_concat_prompt_best.pth` (box nhị phân ghép kênh 2).
- **AttUNet + prompt-crop** = `train_attunet_crop.py`, train `crop-prompt-attunet-r512.ipynb`,
  ckpt `attunet_crop_best.pth` (cắt ảnh theo box, dán mask lại full-frame).
- **SAM-Med2D** = repo `OpenGVLab/SAM-Med2D`; zero-shot `sam_med2d.pth`, fine-tuned
  `sam_center_mixed_x3_shift05_best.pth`, train/test `Finetune_SAMMed2D_test_robust.ipynb`.
- **Q** = `mean(S_sharp, S_stab)`, tính trong `test-auxiliary-signals-r512-*` và trong demo;
  đầu học sẵn cũ = `QualityHead` trong `prompt_unet_2D.py` (không dùng).

---

## Nhóm 0. Nền tảng

### C13. Đánh giá độc lập trên hai dataset
So sánh: PGA-UNet chạy song song trên BTXRD (u xương) và FracAtlas (gãy xương).
Mục đích: xu hướng lặp lại được trên hai loại tổn thương rất khác nhau, không ăn may một dataset. KHÔNG phải tổng quát hóa chéo miền.
Bằng chứng: tất cả notebook trong `Result/File_test/{btxrd,fracatlas}/`.
Nằm ở: xuyên suốt V, chốt 1 câu ở VI.

### C11. Ảnh hưởng độ phân giải
So sánh: PGA-UNet @128 / 256 / 512, mỗi dataset, `center_zoom` và `center_shift`.
Mục đích: độ phân giải đầu vào là yếu tố quan trọng; giữ chi tiết không gian giúp phân đoạn tốt hơn (512 > 256 > 128 cả 2 dataset).
Bằng chứng: cell test nhúng trong `pga-train-128.ipynb`, `pga-train-256.ipynb`, `pga-train-512.ipynb` (`Result/File_train/*/pga 128,256,512/`).
Nằm ở: V-A.

---

## Nhóm 1. Prompt có thiết yếu không (tầng tham chiếu tự động)

### C1a. PGA-UNet vs Attention U-Net không prompt
So sánh: PGA-UNet vs `Attention U-Net` ảnh-only (không box) @512.
Mục đích: bài toán KHÔNG-prompt rất khó, phần lớn độ khó nằm ở bước tự khu trú (AttUNet chỉ 0.52 / 0.34) -> prompt của bác sĩ là thiết yếu. KHÔNG phải "kiến trúc PGA thắng kiến trúc AttUNet".
Bằng chứng: `test-pga-vs-attunet-variants-r512-{btxrd,fracatlas}.ipynb`.
Nằm ở: V-B đoạn 1.

### C1b. PGA-UNet vs Attention U-Net có prompt (prompt-matched)
So sánh: PGA-UNet vs `AttUNet + prompt-channel` vs `AttUNet + prompt-crop`, cùng box @512 (4 mô hình cùng tập ảnh).
Mục đích: chỉ "có box" chưa đủ; cách kiến trúc khai thác box (Gaussian + PSG + CAD) còn tạo thêm lợi thế so với ghép box thô vào input. Biên FracAtlas +0.13.
Bằng chứng: `test-pga-vs-attunet-variants-r512-{btxrd,fracatlas}.ipynb`.
Nằm ở: V-B đoạn 2.

### C2. Nhóm Top-Dice / Bottom-Dice của Attention U-Net
So sánh: Top-50 / Bottom-50 ảnh theo Dice của `Attention U-Net`; chạy lại PGA-UNet + prompt-channel + prompt-crop trên đúng các ảnh đó @512.
Mục đích: lợi thế của xử lý theo prompt tập trung đúng vào các ca khu trú tự động thất bại (bottom: AttUNet 0.03, PGA 0.71). Subset do AttUNet định nghĩa, không phải nhóm độ khó khách quan.
Bằng chứng: `test-subcat-pga-vs-attunet-variants-r512-{btxrd,fracatlas}.ipynb`.
Nằm ở: V-C.

---

## Nhóm 2. Đã có prompt thì khai thác thế nào cho tốt (tầng khớp prompt)

### C3. PGA-UNet vs SAM-Med2D
So sánh: PGA-UNet-256 vs `SAM-Med2D zero-shot` vs `SAM-Med2D fine-tuned`, cùng box @256.
Mục đích: so sánh công bằng nhất (cùng mô hình dùng prompt); PSG + CAD giữ tín hiệu xuyên suốt mạng hiệu quả hơn cách SAM chỉ dùng box ở mask decoder (PGA 0.762 vs SAM-FT 0.630).
Bằng chứng: `test-pga-samzs-samft-r256-{btxrd,fracatlas}.ipynb`.
Nằm ở: V-D.

### C6. Ablation Gaussian / PSG / CAD
So sánh: `cad-only`, `psg-only`, `psg-attention` (PSG + vanilla gate), `full-binary-prompt`, và full Gaussian PGA-UNet.
Mục đích: từng thành phần và tổ hợp đều đóng góp, không phải một phần gánh hết. Dùng "consistent with complementary contributions", cấm "proves synergy".
Bằng chứng: `Source/File_Test/{btxrd,fracatlas}/Ablation/*.ipynb` + `test-full-pga-heatmap-reference-*.ipynb`.
Nằm ở: V-H. **Mode A**: chờ multi-seed, chưa đưa số.

---

## Nhóm 3. Tổn thương nhỏ, nơi thiết kế ăn tiền nhất

### C4. Tổn thương nhỏ: PGA-UNet vs SAM-Med2D
So sánh: subset 50 ảnh diện tích tổn thương nhỏ nhất, PGA-UNet-256 vs SAM-Med2D ZS / FT @256, khung metric 512 chung.
Mục đích: ở ca khắc nghiệt nhất, khoảng cách PGA vs SAM giãn rất rộng (SAM-FT 0.26 / 0.37 vs PGA 0.71 / 0.65) -> bảo toàn tín hiệu vùng nhỏ là mấu chốt, prompt chỉ khoanh vùng chưa đủ.
Bằng chứng: `test-subcat-small-r256-{btxrd,fracatlas}.ipynb`.
Nằm ở: V-E.1.

### C5. Tổn thương nhỏ: PGA-UNet vs baseline prompt-matched thường
So sánh: cùng subset nhỏ, PGA-UNet-512 vs `AttUNet + prompt-channel` vs `AttUNet + prompt-crop` @512 (kèm AttUNet ảnh-only).
Mục đích: cùng ở tổn thương nhỏ, PGA vẫn hơn baseline prompt-matched thường -> lợi thế không phải chỉ do "có box".
Bằng chứng: `test-subcat-small-r512-{btxrd,fracatlas}.ipynb`.
Nằm ở: V-E.2.

### C12. Tổn thương nhỏ: hiệu ứng độ phân giải
So sánh: PGA-UNet @128 / 256 / 512 trên cùng 50 stem nhỏ, kèm mức tụt so với 512.
Mục đích: hiệu ứng độ phân giải rõ hơn khi tổn thương nhỏ (tụt từ 512 xuống 128 là 0.135 / 0.112, lớn hơn full set) -> downsampling ăn mòn bằng chứng vùng nhỏ.
Bằng chứng: `test-subcat-pga-small-r128-256-512-{btxrd,fracatlas}.ipynb`.
Nằm ở: V-E.3.

---

## Nhóm 4. Ổn định, chi phí, thử nghiệm phụ

### Cross-cutting. Nhạy cảm với dịch prompt
So sánh: chênh `center_zoom` vs `center_shift` cho mọi claim C1-C6, C11-C12.
Mục đích: PGA-UNet ít nhạy với dịch prompt trong protocol đã định (tụt < 0.015 Dice) -> box không cần chính xác tuyệt đối. KHÔNG suy ra robustness với box tuỳ ý của bác sĩ.
Bằng chứng: mọi notebook ở trên (đều báo 2 điều kiện riêng).
Nằm ở: V-F, và 2 cột trong mọi bảng.

### C7. Monte Carlo cross-validation
So sánh: 4 checkpoint PGA-UNet-512 với split seed 1, 2, 3, 4; seed train cố định `22120196`.
Mục đích: kết quả ổn định qua các lần chia ngẫu nhiên mức ảnh (std ≤ 0.011), không ăn may 1 lần chia. KHÔNG phải bằng chứng vượt trội baseline.
Bằng chứng: `test-pga-dataset-1234-{btxrd,fracatlas}.ipynb`.
Nằm ở: V-G.

### C8. Chi phí tính toán
So sánh: PGA-UNet 256/512 vs SAM-Med2D 256 (params, FLOPs, checkpoint size, latency GPU/CPU).
Mục đích: lợi thế đạt được với chi phí thấp (~92x nhẹ hơn SAM), phù hợp suy luận lặp lại nhiều lần trong quy trình tương tác. Chỉ giới hạn phần cứng / độ phân giải đã test.
Bằng chứng: `test-measure_efficiency_btxrd.ipynb`.
Nằm ở: V-I.

### E1. Thí nghiệm loss (gợi ý của thầy)
So sánh: PGA-UNet-512, `00` Dice+BCE (mặc định) vs `01` Focal Dice vs `10` size-conditioned Tversky.
Mục đích: (kết quả âm tính) loss Dice+BCE mặc định đã đủ tốt dưới protocol này; loss phức tạp hơn không cải thiện, Focal Dice còn làm hỏng FracAtlas.
Bằng chứng: `Result/File_train/{btxrd,fracatlas}/pga 512/{00,01,10}/pga-train-512.ipynb` (cell test nhúng).
Nằm ở: V-J.

---

## Nhóm 5. Tự đánh giá không cần đáp án và gợi ý vùng (ĐÃ QUAY LẠI BÀI)

### C9. Điểm tự đánh giá training-free Q
So sánh: `Q = mean(S_sharp, S_stab)` của PGA-UNet-512 vs Dice thật (Spearman + Pearson), 2 điều kiện prompt; đối chiếu với đầu học sẵn `QualityHead`.
Mục đích: mô hình tự cho một điểm tin cậy KHÔNG cần đáp án, dùng để bác sĩ biết ca nào nên xem lại (Spearman 0.48 đến 0.70). Điểm training-free tốt hơn đầu học sẵn (`QualityHead` sập về hằng số, Spearman < 0.2). Q là heuristic, KHÔNG phải xác suất hiệu chuẩn.
Bằng chứng: `test-auxiliary-signals-r512-{btxrd,fracatlas}.ipynb` Phần A (`Result/File_test/`).
Nằm ở: V-L đoạn 1.

### C10. Gợi ý vùng box theo Q
So sánh: PGA-UNet-512 chấm 50 box ngẫu nhiên bằng Q, giữ top-3/5, đo độ phủ tổn thương của box (không dùng mask).
Mục đích: Q lọc ra một danh sách ngắn vùng nghi ngờ cho bác sĩ (top-5 khoanh trọn 67% / 82%, độ phủ tốt nhất 0.84 / 0.90) -> tiền đề quy trình tương tác không bắt bác sĩ tự khoanh từ đầu. KHÔNG phải detection.
Bằng chứng: `test-auxiliary-signals-r512-{btxrd,fracatlas}.ipynb` Phần B + demo `test-Demo_Interactive_PGA_Unet-{btxrd,fracatlas}.ipynb`.
Nằm ở: V-L đoạn 2, hình `fig:demo-suggest`.

### C-fail. Failure modes
So sánh: PGA-UNet trên các ca tổn thương dài / phân nhánh, vùng giải phẫu chồng lấn, tương phản yếu.
Mục đích: giới hạn của phương pháp; prompt không cứu được ca mà bằng chứng ảnh cục bộ đã kém.
Bằng chứng: `Paper_IEEE_Access/images/failure/failure_case_overlap.png`.
Nằm ở: V-K.

### Thay đổi so với bản sổ claim trước

- **C9, C10 quay lại bài** (trước đây gạt bỏ vì QualityHead học sẵn sập). Nay dùng điểm
  **training-free Q**, đạt Spearman 0.48 đến 0.70 cả 2 dataset. Có mục V-L trở lại, có
  III-F mô tả công thức Q, có đóng góp trong Introduction, có 1 câu ở Discussion/Conclusion.
  QualityHead học sẵn chỉ còn 1 câu ở V-L như phương án thất bại đối chiếu.
- **Mỗi claim giờ có cột "Mục tiêu"** nói rõ nó chứng minh cho mắt xích nào của spine.
- Nhóm 0 đến 4: claim và số không đổi, chỉ thêm cột mục tiêu.

## F. Mục lục IEEE (mọi tiểu mục ghi rõ claim)

```
I.   INTRODUCTION
     nút thắt khu trú, 2 hướng giải, câu hỏi trung tâm, đóng góp
     [khớp C1, C3, C6, C7, C8, và nhóm nhỏ C4/C5/C12]

II.  RELATED WORK
     A. Automatic segmentation and the Attention U-Net lineage
     B. Interactive and prompt-based segmentation
     C. Promptable medical foundation models
     Bảng: prior work + khoảng trống
     [không mang claim, khung hoá gap]

III. METHOD
     A. Offline and online framework
     B. Problem setting
     C. Prompt representation (Gaussian plateau, center_zoom/shift/mixed, phạm vi box mô phỏng)
     D. Prompt Spatial Gate (PSG)
     E. Conditional Attention Decoder (CAD)
     F. Training-Free Self-Assessment Score
        [công thức Q = mean(S_sharp, S_stab), K=6, "không phải xác suất hiệu chuẩn";
         nền cho C9/C10 ở V-L]
     Hình 1: kiến trúc; Hình demo workflow (fig:demo-seg)

IV.  EXPERIMENTAL SETUP
     A. Datasets (BTXRD, FracAtlas; chia mức ảnh; hạn chế patient-level)   [C13]
     B. Training details (seed, 150 epoch, center_mixed 80/20, chọn checkpoint, fine-tune SAM-Med2D, split seed MC)
     C. Baselines and metrics (AttUNet tự động; SAM-Med2D; prompt-channel + prompt-crop AttUNet; Dice/CBL/HD95; công thức CBL; HD95 chuẩn hoá)
     D. Scope of analysis (box một phần / âm / vùng lạ nằm ngoài phạm vi)

V.   RESULTS
     Status note: mục nào Mode A pending, mục nào Mode B refreshed
     A. Main results across datasets and resolutions          [C11, C13]
     B. Comparison against automatic and prompt-matched Attention U-Net
        doan 1: vs image-only Attention U-Net                 [C1a]
        doan 2: vs prompt-channel va prompt-crop Attention U-Net   [C1b]
     C. Behavior on automatic-baseline top-Dice / bottom-Dice subsets   [C2]
     D. Matched comparison against SAM-Med2D                  [C3]
     E. Small-lesion analysis
        E.1 vs SAM-Med2D at 256                               [C4]
        E.2 vs prompt-channel and prompt-crop Attention U-Net at 512   [C5]
        E.3 PGA-UNet at 128 / 256 / 512                       [C12]
     F. Sensitivity to prompt displacement                    [cross-cutting robustness, tong hop C1-C6/C11-C12]
     G. Monte Carlo cross-validation                          [C7]
     H. Ablation study                                        [C6]  (Mode A vong nay)
     I. Efficiency analysis                                   [C8]  (Mode B)
     J. Exploratory comparison of segmentation losses         [E1]  (Mode B, ket qua am tinh)
     K. Failure modes                                         [C-fail]
     L. Training-free self-assessment and candidate suggestion [C9, C10]  + fig:demo-suggest

VI.  DISCUSSION
     cau hoi trung tam; 2 ket qua phu (loss am tinh, Q duong tinh); han che
     (do phan giai co dinh, prompt mo phong, train tach 2 dataset, patient-level,
      protocol heuristic, ablation mot split -> multi-seed, Monte Carlo = on dinh khong phai
      vuot troi, chua probing feature-level, chua them baseline prompt hien dai ngoai SAM-Med2D)
     + Q la positive vua phai: Spearman 0.5-0.7, tot hon dau hoc san (sap ve hang so);
       Q van la heuristic, chua hieu chuan.

VII. CONCLUSION
     PGA-UNet la gi, da danh gia gi, khong thiet lap dieu gi, future work
     + future work: hoan tat ablation multi-seed, them baseline promptable moi, prompt long
       hon, va bien Q thanh tin hieu hieu chuan roi dung de goi y vung.

BACK MATTER
     Data availability, Author contributions, Ethics statement,
     Acknowledgment (khai bao dung AI), References, Biographies
```

### Ghi chú phân bổ

- **C1 giữ nguyên 1 mục (V-B) nhưng 2 đoạn tách bạch**: đoạn tự động và đoạn prompt-matched,
  đúng guardrails "không gộp 2 tầng vào 1 câu", mà vẫn không giấu 2 baseline prompt-channel /
  prompt-crop.
- **prompt-channel và prompt-crop xuất hiện 3 lần**: toàn tập (V-B), subset top/bottom (V-C),
  subset nhỏ (V-E.2). Mỗi lần là một câu hỏi khác nhau.
- **Small-lesion tách 3 mục con** để C4, C5, C12 đều hiện rõ, không dồn thành 1 đoạn.
- **V-F** là mục mới gom claim robustness xuyên suốt lại một chỗ, đồng thời chuyển hình
  `fig:robust` (đang nằm nhầm dưới Monte Carlo) về đây.
- **V-J** là mục cho thí nghiệm loss (negative control).
- **V-L quay lại** cho C9/C10 với điểm training-free Q (đạt Spearman 0.48-0.70). III-F mô tả
  công thức Q. Đầu học sẵn QualityHead chỉ còn 1 câu ở V-L làm phương án thất bại đối chiếu.
- Discussion và Conclusion: 1 dòng loss âm tính + 1 dòng Q là positive vừa phải.

## F. Số liệu

### F.1. Dùng được ngay

- Efficiency: bảng đầy đủ (2.955M params, 7.74 GFLOPs @256 / 30.97 @512, ckpt 11.4 MB, GPU
  8.6ms @256 / 18.8ms @512, CPU 100ms / 335ms; SAM-Med2D 271.24M, 92 GFLOPs, 2443 MB).
- So sánh loss: xem mục G, kết quả âm tính sạch.
- Attention U-Net tự động: Dice 0.52 BTXRD / 0.34 FracAtlas (nếu anh chốt các `00` là chính thức).

### F.2. Pending tới khi anh chốt checkpoint

- Bảng chính resolution, Monte Carlo, baseline, top/bottom, SAM, small-lesion, ablation.

## G. So sánh loss (điểm anh nhờ rà, số 1)

3 nhánh đã chạy xong test nhúng trong chính notebook train, không cần chạy test riêng.

| Loss | BTXRD zoom / shift | FracAtlas zoom / shift |
|---|---|---|
| Dice + BCE (`00`, mặc định) | **0.7817 / 0.7740** | **0.7271 / 0.7134** |
| Focal Dice (`01`) | 0.7725 / 0.7653 | 0.6421 / 0.5784 |
| size Tversky (`10`) | 0.7776 / 0.7665 | 0.7086 / 0.6796 |

Kết luận: mặc định Dice + BCE tốt nhất hoặc ngang bằng ở cả 2 dataset và cả 2 điều kiện
prompt. Focal Dice làm hỏng nặng FracAtlas (HD95 nhảy lên khoảng 105 pixel). Đây là kết quả
âm tính sạch, khớp guardrails ("default có thể đã đủ mạnh dưới protocol hiện tại").

Đề xuất xử lý:

1. Gộp 3 số này vào notebook `00` (thêm 1 cell markdown + 1 bảng nhỏ), bỏ ý định làm
   notebook test loss riêng.
2. Trong bài: 1 đoạn ngắn nói rõ đã thử theo gợi ý của thầy (mục 3.5 redline), không cải
   thiện, nên giữ Dice + BCE. Vị trí cụ thể cần anh chọn (xem câu hỏi cuối file).

## H. File đuôi kép (điểm anh nhờ rà, số 2)

Lỗi: `Source/Prompt-Guided-XRay-Segmentation/qualitative_visualization.py`, hàm
`export_qualitative_rows`. Tên ảnh xuất ra bị `IMG000184.png.png` vì `_record_name` trả về
tên đã có đuôi `.png` rồi code còn nối thêm `.png`.

Trạng thái: đã có bản sửa trong cây làm việc (chưa commit), strip đuôi ảnh
(`png/jpg/jpeg/bmp/tif/tiff`) trước khi ghép `.png`. `re` đã import sẵn. Bản sửa đúng và đủ.
Chỉ cần anh xác nhận đây đúng là file anh nói, rồi commit chung khi commit `Source/`.

## I. Thông tin còn thiếu để viết IEEE

### I.1. C9 và C10: đã chạy, kết quả âm tính, gạt sang một bên (chốt 2026-09-04)

Notebook `test-auxiliary-signals-r512-{btxrd,fracatlas}.ipynb` đã chạy xong, output ở
`Result/File_test/{btxrd,fracatlas}/`.

**C9 (QualityHead):**

| dataset | prompt | MAE | RMSE | Pearson | Spearman |
|---|---|---|---|---|---|
| BTXRD | zoom | 0.148 | 0.186 | −0.046 | 0.060 |
| BTXRD | shift | 0.151 | 0.189 | −0.049 | 0.037 |
| FracAtlas | zoom | 0.103 | 0.133 | 0.160 | 0.186 |
| FracAtlas | shift | 0.112 | 0.152 | 0.060 | 0.097 |

QualityHead ra gần như hằng số (~0.69 BTXRD, ~0.72 FracAtlas) cho mọi ca. Tương quan gần 0.
Head học đoán về mức trung bình để tối thiểu MSE (đầu vào bị detach, head nhỏ, trọng số loss
nhỏ). Không phải bug test, không phải bug train, là điểm yếu thiết kế.

**C10 (gợi ý vùng box):** BTXRD top-5 độ phủ trung bình 0.223 / tốt nhất 0.688 / khoanh trọn
38%. FracAtlas 0.608 / 0.953 / 87.5%. Nhưng vì QualityHead hằng số nên top-5 = 5 box tùy
tiện; FracAtlas cao chỉ do hình học (vết gãy nhỏ nằm giữa + box ứng viên to). Không đo được
gì về phương pháp.

**Xử lý trong bài:**

- Bỏ mục V-L. Không trích số C9/C10.
- Method III-F: giữ định nghĩa QualityHead + điểm prompt-use của CAD (có thật trong kiến
  trúc). Câu cuối đổi thành "we find this head does not yet provide a usable signal, see
  Limitations".
- Discussion: thêm 1 câu "the auxiliary QualityHead collapsed toward a near-constant estimate
  and did not provide a discriminative per-prompt signal (Spearman 0.04 to 0.19); it should
  be treated as non-functional under the current training".
- Conclusion: thêm 1 câu kết mở, hướng nghiên cứu sau là một tín hiệu tự đánh giá đáng tin
  hơn và từ đó là gợi ý vùng.
- Làm nhẹ chỗ nhắc QualityHead ở abstract/introduction (abstract đã hedge "does not establish
  calibrated confidence", chỉ cần bỏ chỗ nào ngụ ý nó hoạt động).
- Demo Gradio giữ nguyên làm minh hoạ giao diện, đã cập nhật checkpoint sang `00`. User chụp
  1 ảnh luồng vẽ box -> mask (không chụp "Suggest prompts").

Notebook + số C9/C10 giữ lại trong repo làm bằng chứng, không đưa vào manuscript.

**Cập nhật 2026-09-04, thử cứu bằng điểm training-free Q (Cách A). ĐANG CÓ TRIỂN VỌNG.**

`test-auxiliary-signals-r512-*` viết lại: bỏ đọc QualityHead, thay bằng điểm `Q` tính
thẳng từ output suy luận, KHÔNG train lại.

- **Q chính thức = mean(S_sharp, S_stab)** (2 cue bền vững).
  - S_sharp = độ dứt khoát của mask (trung bình `2p-1` trên vùng mask).
  - S_stab = IoU trung bình giữa mask gốc và 6 mask khi nhích box (dịch 0.12, co giãn +-0.10).
- S_fill, S_size bị bỏ khỏi Q vì trên FracAtlas chúng ra hằng số (tổn thương quá nhỏ so với
  box 3x). Notebook vẫn in S_fill/S_size riêng và `Q4 = mean cả 4` để đối chiếu BTXRD.

**Kết quả FracAtlas Part A (đã chạy):** S_sharp Spearman 0.47/0.43 (zoom/shift), S_stab
0.63/0.45, **Q 0.65/0.48**. Đạt ngưỡng.

**Đang chờ:** BTXRD Part A + Part B cả 2 dataset (user chạy). Ngưỡng: BTXRD Q Spearman
>= ~0.4.
- Đạt -> C9/C10 **quay lại bài**: mục V-L sống lại dưới tên "training-free self-assessment
  score"; Method III-F mô tả công thức Q thay vì QualityHead; Experimental Setup thêm 1 câu
  "mô hình có nhánh QualityHead detach, không dùng đầu ra"; demo mới (Q) dùng để chụp ảnh.
- Không đạt -> giữ nguyên "gạt sang một bên" như phần trên.

**Demo:** `test-Demo_Interactive_PGA_Unet-*` đã đổi sang tính Q (2 cue) + sửa gallery
(`object_fit=contain`). User chạy, chụp ảnh luồng vẽ box -> mask. Ảnh cuối để sau khi chốt
Q qua BTXRD.

Commit: `b6f98f4` (notebook Q 4-cue) -> `1c5473d` (bỏ QualityHead) -> `e6aa2e5` (demo Q) ->
`f5767f4` (Q = 2 cue, cả notebook + demo).

### I.2. Các mục còn thiếu khác

1. **Số của 2 bài gốc BTXRD và FracAtlas** (thầy yêu cầu, mục 3.8 redline): cần trích
   Dice/segmentation từ `\cite{b7}` và `\cite{b8}` làm điểm đối chiếu bối cảnh. Chưa có
   trong bài.
2. **AUTHOR ACTION số 2 redline**: thêm ít nhất 1 baseline prompt hiện đại nữa (MedSAM /
   ScribblePrompt / Med-SA). [Đã chốt 2026-09-03] Đưa vào future work, không làm vòng này.
   Vòng này giữ SAM-Med2D + 2 baseline AttUNet prompt-matched, ghi rõ trong hạn chế +
   hướng phát triển.
3. **AUTHOR ACTION số 3 redline**: thống kê theo cặp (paired bootstrap / 95% CI) cho PGA vs
   baseline và cho ablation chính. Chưa làm.
4. **AUTHOR ACTION số 4/5 redline**: test prompt khó hơn (bao phủ một phần, box âm).
   Guardrails đã đặt ngoài phạm vi. Cần anh xác nhận giữ nguyên "ngoài phạm vi" trong bài.
5. **Placeholder**: affiliation tác giả 2, tiểu sử + ảnh Lý Quốc Ngọc, DOI, footer
   template. Thầy tự điền.

## J. Việc

**Đã xong:**
1. File đuôi kép (mục H): bản sửa `qualitative_visualization.py`, commit `cfef8ba`.
2. Notebook C9 + C10 `test-auxiliary-signals-r512-*`: viết lại theo điểm Q training-free
   (mục I.1). Commit `f5767f4`.
3. Demo `test-Demo_Interactive_PGA_Unet-*`: checkpoint `00`, tính điểm Q, sửa gallery.
   Commit `f5767f4`.

**Đang chờ user (Kaggle):**
4. Chạy 2 notebook `test-auxiliary-signals-r512-{btxrd,fracatlas}` -> gửi bảng Part A + Part B.
5. Chạy 2 demo -> gửi ảnh chụp luồng vẽ box -> mask.

**Chưa làm:**
6. Chốt C9/C10 dựa trên bảng BTXRD (mục I.1): quay lại bài hay giữ future work.
7. Gộp số loss vào notebook `00` (mục G).
8. Viết nháp `.md`: `nhap_method_setup.md` (III + IV) đã có, cần chỉnh theo kết quả Q.
   Tiếp: II Related Work, khung V/VI/VII. Mỗi mục `.md` nháp trước khi sửa `.tex`.

## K. Trạng thái quyết định

**2026-09-03**
- File đuôi kép: bug `qualitative_visualization.py`, giữ bản sửa. Commit `cfef8ba`.
- Checkpoint PGA-512: thư mục `00` là chính thức. BTXRD 0.782/0.774, FracAtlas 0.727/0.713.
- Baseline prompt hiện đại thêm (MedSAM/ScribblePrompt): future work, không làm vòng này.

**2026-09-04**
- QualityHead có sẵn trong mô hình: **hỏng** (sập về hằng số ~0.69, Spearman 0.04 đến 0.19).
  Không đọc nữa, không đưa vào bài.
- Thay bằng điểm training-free **Q = mean(S_sharp, S_stab)**, không train lại. FracAtlas
  Part A: Q Spearman 0.65/0.48 -> đạt. **Chờ BTXRD để chốt.**
- Nếu BTXRD cũng đạt: C9/C10 quay lại bài (mục V-L), tên "training-free self-assessment
  score", dùng demo Q để chụp ảnh.
- Nếu BTXRD không đạt: C9/C10 gạt sang một bên, chỉ 1 câu hạn chế + 1 câu kết mở.
- Gộp số loss vào `00`: chưa làm.

## L1. Nháp section đã có (2026-09-04, commit `cedd971`)

- `Paper_IEEE_Access/nhap/nhap_02_related_work.md` (II Related Work)
- `Paper_IEEE_Access/nhap/nhap_03_method.md` (III Method A..E, không có III-F)
- `Paper_IEEE_Access/nhap/nhap_04_experimental_setup.md` (IV Experimental Setup A..D)

Mỗi file: ghi chú thay đổi + text tiếng Anh đề xuất. Do agent soạn, đã verify (git diff sạch,
không dấu gạch ngang, không bịa số). Chờ user duyệt rồi mới ghép vào `.tex`.

Điểm cần user chốt khi ghép:
1. `references.tex` mới có `b1..b9`. Nháp II dùng `b10..b13` (nnU-Net, ScribblePrompt,
   EMedSAM, Med-SA) cho AUTHOR ACTION số 4. 4 `\bibitem` đã có sẵn trong ghi chú của
   `nhap_02_related_work.md`, cần thêm vào `references.tex`.
2. Nháp IV-D đổi câu "auxiliary screening pipeline" thành "self-assessment + prompt
   suggestion ngoài phạm vi". Bộ phân loại có/không tổn thương (thầy hỏi mục 3.10 ke_hoach,
   nhóm đã thử rồi bỏ) nên vẫn giữ 1 câu riêng. User quyết.
3. Chưa xử: redline 3.8 (số Dice 2 bài gốc BTXRD/FracAtlas làm mốc) thuộc Results/Discussion.

## L. Nếu chat bị ngắt, đọc để tiếp tục

1. Trạng thái mới nhất: mục I.1 (đoạn "Cập nhật 2026-09-04") + mục K "2026-09-04".
2. Việc kế tiếp: user gửi bảng số BTXRD từ `test-auxiliary-signals-r512-btxrd`. Nhìn dòng
   `Q` (headline, 2 cue) và `Q4` (4 cue) trong Part A. Spearman `Q` >= ~0.4 ở cả 2 prompt
   mode -> C9/C10 quay lại bài.
3. Số Q FracAtlas đã có: S_sharp 0.47/0.43, S_stab 0.63/0.45, Q 0.65/0.48 (zoom/shift).
4. 4 file liên quan đều ở `Source/File_Test/{btxrd,fracatlas}/`:
   `test-auxiliary-signals-r512-*` và `test-Demo_Interactive_PGA_Unet-*`. Commit hiện tại
   `f5767f4` trở về sau.
5. Memory `access-results-refresh-status` có toàn bộ số liệu Results mới + các quyết định.
6. Chưa đụng file `.tex` nào. `nhap_method_setup.md` là nháp chờ duyệt.
