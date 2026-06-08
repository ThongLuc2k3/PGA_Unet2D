# Minh Chứng Hình Ảnh

> Tất cả ảnh được trích xuất từ notebook thực nghiệm trong `Result/` và lưu tại thư mục `images/` (68 file PNG).  
> Xem số liệu chi tiết tương ứng tại **02_Minh_Chung_So_Lieu.md**.

---

## Tổng Quan Hình Ảnh (68 file)

| Nhóm | File | Số lượng |
|---|---|---|
| PGA-UNet kết quả chính | `pga-unet2d_01.png`, `vis_pga_01.png` | 2 |
| U-Net kết quả | `unet2d_01-10.png`, `vis_unet2d_01.png` (tham khảo) | 10 |
| Attention U-Net | `attention-unet2d_01-10.png`, `vis_attunet_01.png` | 11 |
| SAM-Med2D fine-tuned | `finetune-sammed2d-test-robust_01-10.png`, `vis_sam_ft_01.png` | 11 |
| SAM-Med2D zero-shot | `sammed2d-zeroshot_01-10.png` | 10 |
| Ablation V1–V4 | `ablation_v1..v4_01.png` | 4 |
| Cross-validation 4 fold | `cross-validation_pga-dataset-1..4_01.png` | 4 |
| Sub-category PGA vs Baseline | `subcat-pga-vs-baseline_01-07.png` | 7 |
| Sub-category PGA vs SAM | `subcat-pga-vs-sam_01-07.png` | 7 |
| EfficientNet_B3 phân lớp | `efficientnet_b3_01.png` | 1 |
| Pipeline end-to-end | `pipeline-evaluation_01.png` | 1 |

---

# PHẦN I — ĐÓNG GÓP 1: Kết Quả PGA-UNet

## A. PGA-UNet — Kết Quả Phân Đoạn Chính

### A.1 Kết quả tổng hợp trên tập test
**File:** `images/pga-unet2d_01.png` *(trích xuất từ Result/pga-unet2d.ipynb)*

Biểu đồ / bảng tổng hợp kết quả PGA-UNet trên 3 kịch bản prompt (Zoom-out, Shift, Mixed 70/30).  
Dice: 0.8524 / 0.8382 / 0.8496 — robustness cao, không sụt giảm đáng kể khi câu nhắc lệch.

![PGA-UNet kết quả tổng hợp](images/pga-unet2d_01.png)

### A.2 Minh họa trực quan định tính
**File:** `images/vis_pga_01.png` *(từ Report/images — mẫu đại diện được chọn thủ công)*

Hiển thị: ảnh gốc | ground truth mask | mask dự đoán PGA (kịch bản Zoom-out). Đường biên bám sát GT nhờ PSG + CAD.

![PGA-UNet visualization](images/vis_pga_01.png)

---

## B. U-Net — Baseline Tự Động (Không Có Prompt)

**Files:** `images/unet2d_01.png` đến `images/unet2d_10.png` *(10 mẫu test, từ Result/unet2d.ipynb)*

10 mẫu kiểm thử đại diện. Cột: ảnh gốc | ground truth | dự đoán | overlay.  
Dice trung bình = 0.4534. Hiện tượng: over-segmentation, nhầm bờ khớp xương, bỏ sót tổn thương độ tương phản thấp.

![U-Net mẫu 01](images/unet2d_01.png)
![U-Net mẫu 02](images/unet2d_02.png)
![U-Net mẫu 03](images/unet2d_03.png)
![U-Net mẫu 04](images/unet2d_04.png)
![U-Net mẫu 05](images/unet2d_05.png)
![U-Net mẫu 06](images/unet2d_06.png)
![U-Net mẫu 07](images/unet2d_07.png)
![U-Net mẫu 08](images/unet2d_08.png)
![U-Net mẫu 09](images/unet2d_09.png)
![U-Net mẫu 10](images/unet2d_10.png)

---

## C. Attention U-Net — Baseline Tự Động

**Files:** `images/attention-unet2d_01.png` đến `images/attention-unet2d_10.png`  
*(từ Result/attention-unet2d.ipynb)*

Dice trung bình = 0.4159 (thấp hơn cả U-Net). Attention Gate khuếch đại sai vùng (thiết bị cố định, bờ khớp) khi không có tín hiệu định hướng — thể hiện rõ ở các mẫu tổn thương mờ.

![Att-UNet mẫu 01](images/attention-unet2d_01.png)
![Att-UNet mẫu 02](images/attention-unet2d_02.png)
![Att-UNet mẫu 03](images/attention-unet2d_03.png)
![Att-UNet mẫu 04](images/attention-unet2d_04.png)
![Att-UNet mẫu 05](images/attention-unet2d_05.png)
![Att-UNet mẫu 06](images/attention-unet2d_06.png)
![Att-UNet mẫu 07](images/attention-unet2d_07.png)
![Att-UNet mẫu 08](images/attention-unet2d_08.png)
![Att-UNet mẫu 09](images/attention-unet2d_09.png)
![Att-UNet mẫu 10](images/attention-unet2d_10.png)

Minh họa định tính so sánh với PGA:

![Att-UNet vis](images/vis_attunet_01.png)

---

## D. SAM-Med2D Fine-Tuned — Mô Hình So Sánh

**Files:** `images/finetune-sammed2d-test-robust_01.png` đến `_10.png`  
*(từ Result/finetune-sammed2d-test-robust.ipynb — 3 kịch bản: Zoom-out, Shift, Mixed)*

Dice: 0.7350 / 0.7097 / 0.7283 — thấp hơn PGA +0.1174 (Zoom-out). Hạn chế rõ nhất: độ phân giải 256×256 khiến tổn thương nhỏ bị mờ (Dice chỉ 0.3887 ở nhóm tổn thương nhỏ).

![SAM-Med2D FT mẫu 01](images/finetune-sammed2d-test-robust_01.png)
![SAM-Med2D FT mẫu 02](images/finetune-sammed2d-test-robust_02.png)
![SAM-Med2D FT mẫu 03](images/finetune-sammed2d-test-robust_03.png)
![SAM-Med2D FT mẫu 04](images/finetune-sammed2d-test-robust_04.png)
![SAM-Med2D FT mẫu 05](images/finetune-sammed2d-test-robust_05.png)
![SAM-Med2D FT mẫu 06](images/finetune-sammed2d-test-robust_06.png)
![SAM-Med2D FT mẫu 07](images/finetune-sammed2d-test-robust_07.png)
![SAM-Med2D FT mẫu 08](images/finetune-sammed2d-test-robust_08.png)
![SAM-Med2D FT mẫu 09](images/finetune-sammed2d-test-robust_09.png)
![SAM-Med2D FT mẫu 10](images/finetune-sammed2d-test-robust_10.png)

Minh họa định tính:

![SAM-Med2D FT vis](images/vis_sam_ft_01.png)

---

## E. SAM-Med2D Zero-Shot — Đánh Giá Không Fine-Tune

**Files:** `images/sammed2d-zeroshot_01.png` đến `_10.png`  
*(từ Result/sammed2d-zeroshot.ipynb)*

Dice: 0.5337 / 0.5184 / 0.5286 — không fine-tune trên BTXRD, hiệu năng thấp hơn đáng kể so với fine-tuned. Chứng minh fine-tuning trên dữ liệu domain đặc thù là cần thiết.

![SAM-ZS mẫu 01](images/sammed2d-zeroshot_01.png)
![SAM-ZS mẫu 02](images/sammed2d-zeroshot_02.png)
![SAM-ZS mẫu 03](images/sammed2d-zeroshot_03.png)
![SAM-ZS mẫu 04](images/sammed2d-zeroshot_04.png)
![SAM-ZS mẫu 05](images/sammed2d-zeroshot_05.png)
![SAM-ZS mẫu 06](images/sammed2d-zeroshot_06.png)
![SAM-ZS mẫu 07](images/sammed2d-zeroshot_07.png)
![SAM-ZS mẫu 08](images/sammed2d-zeroshot_08.png)
![SAM-ZS mẫu 09](images/sammed2d-zeroshot_09.png)
![SAM-ZS mẫu 10](images/sammed2d-zeroshot_10.png)

---

## F. Ablation — Đóng Góp Từng Thành Phần Kiến Trúc

*Mỗi ảnh hiển thị kết quả trực quan của một biến thể trên tập test.*

### F.1 V1 — Concat đơn giản (không PSG, không CAD)
**File:** `images/ablation_v1-nopsg-nocad-concat_01.png`  
Dice Zoom-out=0.8718, Shift=0.7201. Không có PSG/CAD, chỉ nối heatmap vào ảnh. Zoom-out tốt nhưng Shift giảm mạnh — không có cơ chế "soft guidance".

![Ablation V1](images/ablation_v1-nopsg-nocad-concat_01.png)

### F.2 V2 — Chỉ PSG (không CAD)
**File:** `images/ablation_v2-psg-only_01.png`  
Dice Zoom-out=0.8643, Shift=0.7291. PSG encoder giúp tập trung đặc trưng, nhưng decoder chưa được điều kiện hóa.

![Ablation V2](images/ablation_v2-psg-only_01.png)

### F.3 V3 — Chỉ CAD (không PSG)
**File:** `images/ablation_v3-cad-only_01.png`  
Dice Zoom-out=0.8827 (cao nhất ablation), Shift=0.7335. CAD đóng góp mạnh hơn PSG ở Zoom-out, nhưng Shift vẫn thấp khi thiếu PSG.

![Ablation V3](images/ablation_v3-cad-only_01.png)

### F.4 V4 — PSG + CAD, Binary bbox
**File:** `images/ablation_v4-full-binaryprompt_01.png`  
Dice Zoom-out=0.8800, Shift=0.7378. Kiến trúc đầy đủ nhưng câu nhắc nhị phân — Shift vẫn thấp hơn V5 (Gaussian) đến 0.1004.

![Ablation V4](images/ablation_v4-full-binaryprompt_01.png)

*(V5 = PGA-UNet đề xuất — xem mục A)*

---

## G. Cross-Validation — Kiểm Định Độ Ổn Định 4 Fold

*Mỗi ảnh là kết quả của một fold phân chia dữ liệu khác nhau.*

**Files:** `images/cross-validation_pga-dataset-1_01.png` đến `_4_01.png`  
*(từ Result/Cross-validation/pga-dataset-1..4.ipynb)*

Dice trung bình 4 fold: Zoom-out=0.8769, Shift=0.8422, Mixed=0.8686 — kết quả đồng nhất, không phụ thuộc cách chia.

![CV Fold 1](images/cross-validation_pga-dataset-1_01.png)
![CV Fold 2](images/cross-validation_pga-dataset-2_01.png)
![CV Fold 3](images/cross-validation_pga-dataset-3_01.png)
![CV Fold 4](images/cross-validation_pga-dataset-4_01.png)

---

## H. Sub-Category — PGA vs Baseline (Nhóm Dễ / Khó)

**Files:** `images/subcat-pga-vs-baseline_01.png` đến `_07.png`  
*(từ Result/subcat-pga-vs-baseline.ipynb)*

Biểu đồ so sánh Dice, HD95, CBL theo nhóm Dễ (top-100) và Khó (bottom-100). Kết quả nổi bật: U-Net Dice=0.1539 ở nhóm Khó, PGA-UNet duy trì 0.8458.

![SubCat Baseline 01](images/subcat-pga-vs-baseline_01.png)
![SubCat Baseline 02](images/subcat-pga-vs-baseline_02.png)
![SubCat Baseline 03](images/subcat-pga-vs-baseline_03.png)
![SubCat Baseline 04](images/subcat-pga-vs-baseline_04.png)
![SubCat Baseline 05](images/subcat-pga-vs-baseline_05.png)
![SubCat Baseline 06](images/subcat-pga-vs-baseline_06.png)
![SubCat Baseline 07](images/subcat-pga-vs-baseline_07.png)

---

## I. Sub-Category — PGA vs SAM-Med2D (3 Nhóm Đặc Tính Lâm Sàng)

**Files:** `images/subcat-pga-vs-sam_01.png` đến `_07.png`  
*(từ Result/subcat-pga-vs-sam.ipynb)*

Biểu đồ so sánh 3 nhóm: Tổn thương nhỏ / Biên giới mờ / Tổn thương rõ nét. Khoảng cách lớn nhất ở nhóm nhỏ: PGA 0.7970 vs SAM 0.3887 (Δ+0.4083).

![SubCat SAM 01](images/subcat-pga-vs-sam_01.png)
![SubCat SAM 02](images/subcat-pga-vs-sam_02.png)
![SubCat SAM 03](images/subcat-pga-vs-sam_03.png)
![SubCat SAM 04](images/subcat-pga-vs-sam_04.png)
![SubCat SAM 05](images/subcat-pga-vs-sam_05.png)
![SubCat SAM 06](images/subcat-pga-vs-sam_06.png)
![SubCat SAM 07](images/subcat-pga-vs-sam_07.png)

---

# PHẦN II — ĐÓNG GÓP 2: Pipeline Lâm Sàng

## J. EfficientNet_B3 — Kết Quả Phân Lớp Sàng Lọc

**File:** `images/efficientnet_b3_01.png`  
*(từ Result/EfficientNet_B3.ipynb)*

Kết quả đánh giá EfficientNet_B3 trên tập test BTXRD: confusion matrix, đường cong ROC (AUC=0.9258), phân phối xác suất dự đoán. Accuracy=85.60%, Sensitivity=78.61%, Specificity=92.55%.

![EfficientNet_B3 kết quả](images/efficientnet_b3_01.png)

---

## K. Pipeline End-to-End — Đánh Giá Trên Dataset_Online

**File:** `images/pipeline-evaluation_01.png`  
*(từ Result/pipeline-evaluation.ipynb)*

Kết quả pipeline đầy đủ trên 375 ảnh hỗn hợp (187 có bệnh + 188 bình thường):  
- Phân loại: TP=181, FP=38, FN=6, TN=150 — Sensitivity=96.79%, Specificity=79.79%  
- Phân đoạn: 181 TP → 226 polygon, 38 FP → Dice=0; **Pipeline Dice=0.7296, IoU=0.6430**

![Pipeline evaluation](images/pipeline-evaluation_01.png)
