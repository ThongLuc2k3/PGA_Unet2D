# Minh Chứng Số Liệu

> Toàn bộ số liệu được thực nghiệm trên Google Colab (GPU). Kết quả có thể xem lại trong các notebook tại `Result/`.  
> **Đóng góp 1** đánh giá PGA-UNet thuần túy — số liệu sạch để so sánh công bằng với baseline.  
> **Đóng góp 2** đánh giá pipeline khi có EfficientNet_B3 hỗ trợ sàng lọc — thừa nhận sai số tích lũy từ bộ lọc.

---

# PHẦN I — ĐÓNG GÓP 1: Kiến Trúc PGA-UNet

## A. Thông Tin Bộ Dữ Liệu và Phân Chia

| Thông tin | Giá trị |
|---|---|
| Bộ dữ liệu phân đoạn | BTXRD (ảnh có bệnh lý kèm mask pixel-level) |
| Đơn vị đánh giá | **Per-polygon** (mỗi polygon = 1 mẫu độc lập) |
| Tập test phân đoạn | N = 232 mẫu per-polygon |
| Phân chia train/val/test | 70 / 15 / 15 (ảnh) |
| Bộ dữ liệu phân lớp | BTXRD toàn bộ (3.746 ảnh, cả lành và bệnh) |
| Phân chia phân lớp | 80 / 10 / 10 (~2.996 / 375 / 375 ảnh) |

**Lưu ý so sánh U-Net / Att-UNet vs PGA:**  
U-Net và Att-UNet hoạt động tự động (merged mask per-ảnh, N=250 ảnh). PGA-UNet hoạt động có câu nhắc (per-polygon, N=232 mẫu). Sự chênh lệch phản ánh giá trị của hướng tiếp cận prompt-guided.

---

## B. Cấu Hình Huấn Luyện

| Tham số | U-Net / Att-UNet / PGA-UNet | EfficientNet_B3 |
|---|---|---|
| Loss function | BCE + Dice Loss | BCE |
| Optimizer | AdamW (weight decay 1e-4) | AdamW |
| Batch size | 4 | 16 |
| Epoch tối đa | 100 | 25 (giai đoạn 1) + 75 (giai đoạn 2) |
| Learning Rate | 1e-4, ReduceLROnPlateau (×0.5 sau 5 ep.) | 1e-4 → 1e-5, CosineAnnealingLR |
| Early stopping | Patience = 15 | Patience = 15 |
| Kích thước ảnh | 512×512 | 300×300 |
| Augmentation | Flip, rotate, scale | Flip, rotate, color jitter |

---

## C. So Sánh Baseline — U-Net vs Att-UNet vs PGA-UNet

*Kịch bản Zoom-out (câu nhắc lý tưởng bao trọn tổn thương +30%)*

| Mô hình | Điều kiện | Dice ↑ | IoU ↑ | Precision ↑ | Recall ↑ | HD95 ↓ (px) | CBL ↑ |
|---|---|---|---|---|---|---|---|
| U-Net | Tự động, không prompt | 0.4534 | 0.3671 | 0.6320 | 0.4539 | 128.61 | 0.5968 |
| Attention U-Net | Tự động, không prompt | 0.4159 | 0.3306 | 0.5951 | 0.4204 | 132.86 | 0.5569 |
| **PGA-UNet** | **Có prompt (Zoom-out)** | **0.8524** | **0.7527** | **0.8505** | **0.8739** | **13.96** | **0.9451** |

**Nhận xét:** Attention U-Net thấp hơn cả U-Net (Dice 0.4159 vs 0.4534) do Attention Gate khuếch đại sai vùng (bờ khớp, thiết bị cố định) khi không có tín hiệu định hướng. PGA vượt +0.3990 so với U-Net, chứng minh giá trị của prompt guidance.

---

## D. Tính Bền Bỉ (Robustness) — 3 Kịch Bản Câu Nhắc

*N = 232 mẫu per-polygon*

| Kịch bản | Mô tả | Dice ↑ | IoU ↑ | Precision ↑ | Recall ↑ | HD95 ↓ (px) | CBL ↑ |
|---|---|---|---|---|---|---|---|
| Zoom-out | Câu nhắc lý tưởng, mở rộng +30% | 0.8524 | 0.7527 | 0.8505 | 0.8739 | 13.96 | 0.9451 |
| Shift | Câu nhắc bị dịch lệch ngẫu nhiên | 0.8382 | 0.7336 | 0.8434 | 0.8556 | 13.57 | 0.9379 |
| Mixed (70/30) | 70% Zoom-out + 30% Shift | 0.8496 | 0.7486 | 0.8511 | 0.8689 | 14.38 | 0.9436 |

**Nhận xét:** Dice chỉ giảm 0.0142 từ Zoom-out sang Shift — chứng minh PGA-UNet học "soft guidance" chứ không ghi nhớ cứng vị trí câu nhắc. Kịch bản Mixed mô phỏng thực tế lâm sàng đạt Dice = 0.8496.

---

## E. So Sánh Với SAM-Med2D (SOTA Prompt-Based)

*N = 232 mẫu per-polygon. **HD95 (norm)** = HD95 chuẩn hóa theo kích thước ảnh (÷512 với PGA, ÷256 với SAM) để so sánh công bằng giữa hai độ phân giải khác nhau.*  
*Viết tắt: **FT** = Fine-Tuned (có fine-tune trên BTXRD), **ZS** = Zero-Shot (không fine-tune trên dữ liệu đích).*

| Mô hình | Kịch bản | Dice ↑ | IoU ↑ | Pre ↑ | Rec ↑ | HD95 (norm) ↓ | CBL ↑ |
|---|---|---|---|---|---|---|---|
| **PGA-UNet** | Zoom-out | **0.8524** | **0.7527** | **0.8505** | **0.8739** | **0.027** | **0.9451** |
| **PGA-UNet** | Shift | **0.8382** | **0.7336** | **0.8434** | **0.8556** | **0.027** | **0.9379** |
| **PGA-UNet** | Mixed | **0.8496** | **0.7486** | **0.8511** | **0.8689** | **0.028** | **0.9436** |
| SAM-Med2D (FT) | Zoom-out | 0.7350 | 0.6130 | 0.7513 | 0.7478 | 0.207 | 0.8893 |
| SAM-Med2D (FT) | Shift | 0.7097 | 0.5818 | 0.7385 | 0.7117 | 0.213 | 0.8767 |
| SAM-Med2D (FT) | Mixed | 0.7283 | 0.6044 | 0.7491 | 0.7379 | 0.208 | 0.8863 |
| SAM-Med2D (ZS) | Zoom-out | 0.5337 | 0.3924 | 0.4743 | 0.6776 | 0.374 | 0.8194 |
| SAM-Med2D (ZS) | Shift | 0.5184 | 0.3775 | 0.4570 | 0.6559 | 0.403 | 0.7945 |
| SAM-Med2D (ZS) | Mixed | 0.5286 | 0.3882 | 0.4700 | 0.6670 | 0.384 | 0.8093 |

**So sánh tham số:** PGA ~4M vs SAM ~100M (tổng) / ~15M (trainable).  
**Điểm chính:** PGA vượt SAM FT +0.1174 Dice với 25× ít tham số hơn. HD95 (norm) của PGA (0.027) tốt hơn SAM (0.207) — bám biên chính xác hơn nhiều.

---

## F. Hiệu Quả Tính Toán

| Chỉ số | PGA-UNet | SAM-Med2D |
|---|---|---|
| Tổng tham số | ~4M | ~100M |
| Tham số huấn luyện được | ~4M (100%) | ~15M (Adapter + Decoder) |
| Kích thước ảnh đầu vào | 512×512 | 256×256 (cố định) |
| VRAM huấn luyện (batch=4) | ~3 GB | ~6 GB |
| VRAM suy luận (batch=1) | ~1 GB | ~2 GB |
| Chạy được trên GPU 4GB | Có | Hạn chế |

---

## G. Ablation — Đóng Góp Từng Thành Phần Kiến Trúc (V1–V5)

*Đánh giá trên 3 kịch bản. V5 là mô hình đề xuất.*

| Biến thể | PSG | CAD | Loại câu nhắc | Zoom-out Dice ↑ | Shift Dice ↑ | Mixed Dice ↑ |
|---|---|---|---|---|---|---|
| V1 — Concat đơn giản | ✗ | ✗ | Gaussian Heatmap | 0.8718 | 0.7201 | 0.8158 |
| V2 — Chỉ PSG | ✓ | ✗ | Gaussian Heatmap | 0.8643 | 0.7291 | 0.8146 |
| V3 — Chỉ CAD | ✗ | ✓ | Gaussian Heatmap | 0.8827 | 0.7335 | 0.8256 |
| V4 — PSG + CAD, Binary bbox | ✓ | ✓ | Binary bbox | 0.8800 | 0.7378 | 0.8276 |
| **V5 — PSG + CAD, Heatmap (đề xuất)** | **✓** | **✓** | **Gaussian Heatmap** | **0.8524** | **0.8382** | **0.8496** |

**Hai phát hiện quan trọng từ ablation:**

1. **CAD đóng góp nhiều hơn PSG trong kịch bản Zoom-out:** V3 (CAD only) = 0.8827 > V2 (PSG only) = 0.8643 > V1 = 0.8718. Tuy nhiên, cả hai đều thua V5 ở kịch bản Shift — cần kết hợp PSG+CAD để đạt robustness.

2. **Trade-off Gaussian vs Binary (V5 vs V4):** Gaussian heatmap giảm Dice Zoom-out nhẹ (0.8524 vs 0.8800, -0.0276) nhưng tăng Dice Shift mạnh (+0.1004: 0.8382 vs 0.7378). Gaussian "làm mờ" đường biên câu nhắc — mạng không thể ghi nhớ cứng vị trí hộp → robustness tốt hơn nhiều với câu nhắc lệch.

---

## H. Kiểm Định Độ Ổn Định — Cross-Validation 4-Fold

*4 lần phân chia dữ liệu khác nhau, kết quả nhất quán xác nhận mô hình ổn định. **TB** = Trung Bình (average over 4 folds).*

| Kịch bản | Dice ↑ | IoU ↑ | Precision ↑ | Recall ↑ | HD95 ↓ (px) | CBL ↑ |
|---|---|---|---|---|---|---|
| Zoom-out (TB 4 fold) | 0.8769 | 0.7884 | 0.8507 | 0.9145 | 9.78 | 0.9601 |
| Shift (TB 4 fold) | 0.8422 | 0.7389 | 0.8283 | 0.8723 | 12.60 | 0.9369 |
| Mixed (TB 4 fold) | 0.8686 | 0.7766 | 0.8481 | 0.9016 | 10.37 | 0.9541 |

**Nhận xét:** Các fold cho kết quả đồng nhất. Cross-validation nhỉnh hơn tập test chính một chút (0.8769 vs 0.8524) do sự khác biệt nhỏ về phân phối dữ liệu giữa các phân vùng — không phải overfitting.

---

## I. Đánh Giá Theo Đặc Tính Tổn Thương — Sub-Category

### I.1 PGA vs Baseline — Nhóm Dễ / Khó (phân nhóm theo Dice của U-Net, N=187 ảnh, 50 dễ nhất / 50 khó nhất)

| Nhóm | Mô hình | Dice ↑ | IoU ↑ | Pre ↑ | Rec ↑ | HD95 ↓ (px) | CBL ↑ |
|---|---|---|---|---|---|---|---|
| Dễ (top-50 U-Net Dice) | U-Net | 0.8691 | 0.7713 | 0.8711 | 0.8771 | 21.05 | 0.9510 |
| Dễ | Attention U-Net | 0.7609 | 0.6539 | 0.8055 | 0.7797 | 34.48 | 0.8662 |
| **Dễ** | **PGA-UNet** | **0.8938** | **0.8122** | **0.8704** | **0.9249** | **13.16** | **0.9588** |
| Khó (bottom-50 U-Net Dice) | U-Net | 0.0000 | 0.0000 | 0.2200 | 0.0000 | 265.69 | 0.0243 |
| Khó | Attention U-Net | 0.0929 | 0.0639 | 0.3397 | 0.1034 | 236.46 | 0.1551 |
| **Khó** | **PGA-UNet** | **0.8181** | **0.7114** | **0.8446** | **0.8274** | **18.06** | **0.9247** |

**Điểm quan trọng nhất:** Ở nhóm Khó, U-Net sụp đổ hoàn toàn (Dice 0.0000, HD95 265.69px). PGA-UNet **duy trì ổn định 0.8181** (Δ+0.8181 = 0.8181 − 0.0000, chênh lệch Dice PGA so với U-Net tại nhóm Khó). Đây là minh chứng mạnh nhất cho cơ chế PSG — thiếu tín hiệu định hướng, tự động hoàn toàn thất bại.

### I.2 PGA vs SAM-Med2D — 3 Nhóm Đặc Tính Lâm Sàng (50 mẫu per-polygon mỗi nhóm)

| Nhóm | Mô hình | Dice ↑ | IoU ↑ | Pre ↑ | Rec ↑ | HD95 ↓ (px) | CBL ↑ |
|---|---|---|---|---|---|---|---|
| Tổn thương nhỏ | SAM-Med2D (FT) | 0.3887 | 0.2835 | 0.7223 | 0.3335 | 88.73 | 0.6855 |
| **Tổn thương nhỏ** | **PGA-UNet** | **0.7970** | **0.6818** | **0.7906** | **0.8453** | **13.64** | **0.9202** |
| Biên giới mờ | SAM-Med2D (FT) | 0.5407 | 0.3886 | 0.7673 | 0.4610 | 27.44 | 0.8401 |
| **Biên giới mờ** | **PGA-UNet** | **0.8288** | **0.7152** | **0.8382** | **0.8413** | **12.00** | **0.9384** |
| Tổn thương rõ nét | SAM-Med2D (FT) | 0.8465 | 0.7392 | 0.8955 | 0.8129 | 27.04 | 0.9483 |
| **Tổn thương rõ nét** | **PGA-UNet** | **0.8741** | **0.7850** | **0.8638** | **0.8969** | **24.71** | **0.9548** |

**Khoảng cách lớn nhất:** Tổn thương nhỏ — PGA 0.7970 vs SAM 0.3887 (Δ+0.4083). Nguyên nhân: SAM hoạt động ở 256×256, tổn thương nhỏ chỉ còn vài pixel; PGA ở 512×512 giữ nguyên chi tiết.

---

# PHẦN II — ĐÓNG GÓP 2: Pipeline Lâm Sàng

## J. Mô Hình Phân Lớp Sàng Lọc — EfficientNet_B3 (Đánh Giá Độc Lập trên BTXRD)

*Đánh giá độc lập (standalone = chỉ đánh giá mô hình phân lớp riêng lẻ, chưa kết hợp vào pipeline) trên tập test BTXRD (375 ảnh hỗn hợp).*

**Ý nghĩa từng chỉ số:**
- **Accuracy**: tỉ lệ dự đoán đúng tổng thể (cả dương và âm)
- **Precision (PPV — Positive Predictive Value)**: trong số ảnh mô hình dự đoán là có bệnh, bao nhiêu phần trăm thực sự có bệnh (đo mức độ sai dương — FP)
- **Recall (Sensitivity)**: trong số ảnh thực sự có bệnh, bao nhiêu phần trăm được phát hiện đúng (đo mức độ bỏ sót — FN)
- **Specificity**: trong số ảnh thực sự bình thường, bao nhiêu phần trăm được phân loại đúng là âm tính (đo mức độ sai dương với lớp âm)
- **NPV (Negative Predictive Value)**: trong số ảnh mô hình dự đoán là bình thường, bao nhiêu phần trăm thực sự bình thường
- **F1-Score**: trung bình điều hòa của Precision và Recall — cân bằng giữa độ chính xác dự đoán dương và khả năng phát hiện bệnh
- **AUC-ROC**: diện tích dưới đường cong ROC, đo khả năng phân biệt hai lớp; 1.0 = phân biệt hoàn hảo, 0.5 = ngẫu nhiên

| Độ đo | Giá trị |
|---|---|
| Accuracy | 85.60% |
| Precision (PPV) | 91.30% |
| Recall (Sensitivity) | 78.61% |
| Specificity | 92.55% |
| NPV | 81.31% |
| F1-Score | 84.52% |
| **AUC-ROC** | **0.9258** |

**Nhận xét:** Precision 91.30% cao — khi báo dương tính, xác suất đúng cao (ít gửi ảnh lành xuống PGA). Recall 78.61% thấp hơn — điểm cần cải thiện (21.39% ca bệnh bị bỏ lọt). Trong bối cảnh Human-in-the-loop, bác sĩ vẫn là người quyết định cuối.

---

## K. Đánh Giá Pipeline End-to-End — Dataset_Online (375 Ảnh Hỗn Hợp)

*Chạy toàn bộ pipeline: EfficientNet_B3 → PGA-UNet trên dataset_online*

### K.1 Phân Loại (EfficientNet_B3 trên dataset_online)

| TP | FP | FN | TN | Sensitivity | Specificity | Accuracy | AUC-ROC |
|---|---|---|---|---|---|---|---|
| 181 | 38 | 6 | 150 | 96.79% | 79.79% | 88.27% | 0.9688 |

### K.2 Phân Đoạn Pipeline (PGA-UNet, đánh giá per-polygon)

| Thống kê | Giá trị |
|---|---|
| Ảnh TP đưa vào PGA | 181 ảnh → 226 polygon (TB 1.25 polygon/ảnh) |
| Ảnh FP (Dice = 0) | 38 ảnh |
| Mẫu số tổng | 226 + 38 = **264 đơn vị** |
| **Pipeline Dice** | **0.7296** |
| **Pipeline IoU** | **0.6430** |

**Công thức:**
$$
\text{Pipeline Dice} = \frac{\displaystyle\sum_{i \in \text{polygon(TP)}} \text{Dice}_{i}}{N_{\text{polygon(TP)}} + N_{\text{image(FP)}}} = \frac{\sum 226 \text{ polygon Dice}}{226 + 38} = \frac{...}{264} = \mathbf{0.7296}
$$

**Phân tích:** Pipeline Dice (0.7296) thấp hơn PGA standalone (0.8524) vì 38 ảnh FP kéo điểm xuống. Bottleneck là Specificity dataset_online (79.79%) — mỗi ảnh bình thường bị sai → 1 đơn vị Dice=0 trong mẫu số. Cải thiện Specificity sẽ trực tiếp nâng Pipeline Dice.

---

## L. Hướng Dẫn Xem Kết Quả Thực Nghiệm

| Notebook | Nội dung |
|---|---|
| `Result/pga-unet2d.ipynb` | Kết quả chính PGA-UNet (Zoom/Shift/Mixed) |
| `Result/unet2d.ipynb` | Kết quả U-Net baseline |
| `Result/attention-unet2d.ipynb` | Kết quả Attention U-Net |
| `Result/finetune-sammed2d-test-robust.ipynb` | Kết quả SAM-Med2D fine-tuned |
| `Result/sammed2d-zeroshot.ipynb` | Kết quả SAM-Med2D zero-shot |
| `Result/Ablation/v1-nopsg-nocad-concat.ipynb` | Ablation V1 |
| `Result/Ablation/v2-psg-only.ipynb` | Ablation V2 |
| `Result/Ablation/v3-cad-only.ipynb` | Ablation V3 |
| `Result/Ablation/v4-full-binaryprompt.ipynb` | Ablation V4 |
| `Result/Cross-validation/pga-dataset-1..4.ipynb` | 4-fold cross-validation |
| `Result/subcat-pga-vs-baseline.ipynb` | Sub-category PGA vs baseline |
| `Result/subcat-pga-vs-sam.ipynb` | Sub-category PGA vs SAM |
| `Result/EfficientNet_B3.ipynb` | Phân lớp sàng lọc |
| `Result/pipeline-evaluation.ipynb` | Pipeline end-to-end |
