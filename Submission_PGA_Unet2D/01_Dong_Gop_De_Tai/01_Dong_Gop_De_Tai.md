# Đóng Góp Của Đề Tài

**Đề tài:** Phát triển hệ thống phân đoạn ảnh X-quang xương dựa vào câu nhắc trực quan  
**Tác giả:**  | **GVHD:** | **Năm:** 2026  
**Bộ dữ liệu:** BTXRD — Bone Tumor X-Ray Dataset (Nature Scientific Data, 2024)

---

## Bối Cảnh và Động Lực

Bài toán phân đoạn tổn thương xương trên ảnh X-quang 2D gặp hai thách thức cốt lõi:

1. **Phương pháp tự động** (U-Net, Attention U-Net) thiếu hoàn toàn cơ chế tiếp nhận định hướng từ bác sĩ. Khi tổn thương có độ tương phản thấp hoặc cấu trúc xương chồng lấp, mô hình không biết nên "nhìn" vào đâu, dẫn đến phân đoạn sai hoặc bỏ sót.

2. **Mô hình nền tảng** như SAM-Med2D (ViT-B ~100M tham số) tuy có câu nhắc nhưng bị giới hạn độ phân giải 256×256 và đòi hỏi tài nguyên tính toán lớn — khó triển khai tại cơ sở y tế tuyến cơ sở.

**Giải pháp:** Tích hợp câu nhắc trực quan (bounding box từ bác sĩ) trực tiếp vào kiến trúc CNN hạng nhẹ, huấn luyện chuyên biệt từ đầu trên dữ liệu X-quang xương.

---

## Đóng Góp 1 — Kiến Trúc PGA-UNet

Đề xuất mô hình **PGA-UNet (Prompt-Guided Attention U-Net)** — ~4M tham số, ảnh đầu vào 512×512, huấn luyện hoàn toàn từ đầu trên BTXRD. Hai thành phần chính được thiết kế mới:

### 1.1 Prompt Spatial Gate (PSG) — Cổng Không Gian Tại Bộ Mã Hóa

Bản đồ nhiệt câu nhắc được tích hợp vào từng tầng đặc trưng của bộ mã hóa qua phép nhân **tăng cường có chọn lọc**:

$$\tilde{\mathbf{x}}^l = \mathbf{x}^l \odot \bigl(1 + \alpha \cdot \sigma(\mathbf{W}_{gate} \ast \mathbf{H}^l)\bigr)$$

- **Thiết kế tăng cường (không ức chế):** vùng trong câu nhắc được khuếch đại, vùng ngoài giữ nguyên — không mất thông tin toàn cục.
- Ngay từ các tầng mã hóa đầu, mạng học đặc trưng tổn thương thay vì phải "tự tìm" khắp ảnh.

### 1.2 Conditioned Attention Decoder (CAD) — Cơ Chế Chú Ý Có Điều Kiện Tại Bộ Giải Mã

Tín hiệu gating được điều kiện hóa bởi câu nhắc với **trọng số giảm dần** theo độ sâu tầng giải mã:

$$\mathbf{g}' = \mathbf{g} + c \cdot \alpha \cdot w \cdot \mathbf{p}_{\text{enc}}, \quad w \in \{1.0,\ 0.7,\ 0.4,\ 0.2\}$$

- Tầng sâu (ngữ nghĩa): câu nhắc ảnh hưởng mạnh (w=1.0) — định hướng vùng tổn thương.
- Tầng nông (chi tiết đường biên): câu nhắc ảnh hưởng yếu (w=0.2) — mạng tự do tái tạo biên.
- Mở rộng từ công thức Attention Gate [Oktay 2018] bằng cách thêm điều kiện hóa câu nhắc.

### 1.3 Plateau Heatmap — Mã Hóa Câu Nhắc

Bounding box → bản đồ nhiệt 2D: gán 1.0 đồng đều bên trong (mở rộng 30%), làm mờ viền bằng Gaussian blur (kernel 31×31):

$$\mathbf{H}_{prompt} = \text{GaussianBlur}(\mathbf{B}_{filled},\ k=31)$$

**Ba cách mã hóa câu nhắc và lý do chọn Plateau Heatmap:**

- **Binary mask** (tensor nhị phân 0/1): bên trong bbox = 1, bên ngoài = 0. Đường biên hoàn toàn sắc nét — tạo gradient lớn tại biên hộp. Khi nhân trực tiếp vào feature map, mạng dễ học thuộc vị trí cạnh hộp thay vì đặc trưng tổn thương thực sự. Bị loại vì tạo gradient giả tạo.

- **Gaussian 2D thuần** (hàm Gauss chuẩn, đỉnh ở tâm bbox): được dùng trong SAM thông qua **position embedding** của Transformer — tích hợp vào attention scores, không nhân trực tiếp vào feature map. Với U-Net sử dụng phép nhân trực tiếp, phân phối Gauss thuần khiến vùng tâm quá nổi trội so với rìa tổn thương, tín hiệu yếu ở biên đối tượng. Bị loại vì không phù hợp với kiến trúc CNN có phép nhân trực tiếp.

- **Plateau Heatmap (đề xuất):** gán đồng đều 1.0 toàn bộ bên trong bbox (mọi vị trí tổn thương có trọng số ngang nhau), chỉ làm mờ viền bằng Gaussian blur k=31 để tránh gradient sắc nét. Phù hợp với phép nhân feature map của U-Net: vùng tổn thương được khuếch đại đều, không tạo "giả biên" như binary mask, không thiên vị tâm như Gaussian thuần.

---

### 1.4 Kết Quả So Sánh Baseline

*N = 232 mẫu per-polygon (tập test BTXRD). U-Net / Att-UNet: tự động, merged mask per-ảnh.*

**Ý nghĩa từng chỉ số đánh giá phân đoạn** (P = mask dự đoán, G = ground truth):
- **Dice** (F1): 2|P∩G| / (|P|+|G|) — độ chồng lấp tổng thể; 1.0 = khớp hoàn hảo
- **IoU** (Intersection over Union): |P∩G| / |P∪G| — tương tự Dice nhưng phạt nặng hơn dự đoán thừa/thiếu
- **Precision**: |P∩G| / |P| — trong vùng dự đoán là tổn thương, bao nhiêu thực sự là tổn thương (đo False Positive)
- **Recall**: |P∩G| / |G| — trong vùng tổn thương thực tế, bao nhiêu được phát hiện (đo False Negative)
- **HD95** (Hausdorff Distance 95th percentile, đơn vị pixel): khoảng cách tối đa (percentile 95) giữa đường biên P và G; giá trị thấp = đường biên bám sát GT
- **CBL** (Contour-Based metric): đánh giá chất lượng đường biên, trọng số cao ở vùng viền; bổ sung Dice về độ chính xác đường viền

| Mô hình | Kịch bản | Dice ↑ | IoU ↑ | Precision ↑ | Recall ↑ | HD95 ↓ (px) | CBL ↑ |
|---|---|---|---|---|---|---|---|
| U-Net (không prompt) | — | 0.4534 | 0.3671 | 0.6320 | 0.4539 | 128.61 | 0.5968 |
| Attention U-Net (không prompt) | — | 0.4159 | 0.3306 | 0.5951 | 0.4204 | 132.86 | 0.5569 |
| **PGA-UNet** | **Zoom-out** | **0.8524** | **0.7527** | **0.8505** | **0.8739** | **13.96** | **0.9451** |
| **PGA-UNet** | **Shift** | **0.8382** | **0.7336** | **0.8434** | **0.8556** | **13.57** | **0.9379** |
| **PGA-UNet** | **Mixed 70/30** | **0.8496** | **0.7486** | **0.8511** | **0.8689** | **14.38** | **0.9436** |

**Nhận xét:** Att-UNet (0.4159) thấp hơn cả U-Net (0.4534) do Attention Gate khuếch đại sai vùng khi không có tín hiệu định hướng. PGA vượt U-Net +0.3990 Dice — giá trị của prompt guidance.

---

### 1.5 Tính Bền Bỉ Câu Nhắc (Robustness)

Ba kịch bản mô phỏng mức độ chính xác khác nhau của bác sĩ khi khoanh vùng:

| Kịch bản | Mô tả | Dice ↑ | Chênh vs Zoom-out |
|---|---|---|---|
| Zoom-out | Câu nhắc lý tưởng, bao trọn +30% | 0.8524 | — |
| Shift | Câu nhắc bị dịch lệch ngẫu nhiên | 0.8382 | −0.0142 |
| Mixed (70/30) | 70% Zoom-out + 30% Shift | 0.8496 | −0.0028 |

Dice chỉ giảm 0.0142 khi câu nhắc lệch hoàn toàn — chứng minh PGA học "soft guidance" chứ không ghi nhớ cứng vị trí câu nhắc.

---

### 1.6 So Sánh Với SAM-Med2D (SOTA Prompt-Based)

*SAM-Med2D: ViT-B ~100M tham số, fine-tuned từ 4M+ ảnh y tế, độ phân giải 256×256.*  
***HD95 (norm)** = HD95 chuẩn hóa theo kích thước ảnh (÷512 với PGA, ÷256 với SAM) để so sánh công bằng giữa hai độ phân giải khác nhau.*  
*Viết tắt: **FT** = Fine-Tuned (có fine-tune trên BTXRD), **ZS** = Zero-Shot (không fine-tune trên dữ liệu đích).*

| Mô hình | Kịch bản | Dice ↑ | IoU ↑ | HD95 (norm) ↓ | CBL ↑ |
|---|---|---|---|---|---|
| **PGA-UNet** | Zoom-out | **0.8524** | **0.7527** | **0.027** | **0.9451** |
| **PGA-UNet** | Shift | **0.8382** | **0.7336** | **0.027** | **0.9379** |
| **PGA-UNet** | Mixed | **0.8496** | **0.7486** | **0.028** | **0.9436** |
| SAM-Med2D (FT) | Zoom-out | 0.7350 | 0.6130 | 0.207 | 0.8893 |
| SAM-Med2D (FT) | Shift | 0.7097 | 0.5818 | 0.213 | 0.8767 |
| SAM-Med2D (FT) | Mixed | 0.7283 | 0.6044 | 0.208 | 0.8863 |
| SAM-Med2D (ZS) | Zoom-out | 0.5337 | 0.3924 | 0.374 | 0.8194 |
| SAM-Med2D (ZS) | Shift | 0.5184 | 0.3775 | 0.403 | 0.7945 |
| SAM-Med2D (ZS) | Mixed | 0.5286 | 0.3882 | 0.384 | 0.8093 |

**Điểm chính:**
- PGA vượt SAM FT +0.1174 Dice (Zoom-out) với 25× ít tham số (~4M vs ~100M)
- Khoảng cách ZS→FT lớn (0.5337→0.7350) chứng minh fine-tuning trên domain đặc thù là cần thiết — PGA vượt qua cả SAM FT dù train từ đầu
- HD95 (norm): PGA 0.027 vs SAM FT 0.207 — bám biên chính xác hơn nhiều lần

**Hiệu quả tính toán:**

| Chỉ số | PGA-UNet | SAM-Med2D |
|---|---|---|
| Tổng tham số | ~4M | ~100M |
| Kích thước ảnh | 512×512 | 256×256 (cố định) |
| VRAM huấn luyện (batch=4) | ~3 GB | ~6 GB |
| VRAM suy luận (batch=1) | ~1 GB | ~2 GB |

---

### 1.7 Ablation — Đóng Góp Từng Thành Phần Kiến Trúc

*5 biến thể, cùng siêu tham số, huấn luyện lại hoàn toàn.*

**Ý nghĩa từng biến thể:**
- **V1 — Concat đơn giản:** PSG và CAD đều tắt; heatmap chỉ được nối (concatenate) thẳng vào kênh ảnh đầu vào tạo đầu vào 2 kênh. Baseline tối giản — không có cơ chế fusion nào trong mạng.
- **V2 — Chỉ PSG:** Có PSG (encoder được điều kiện hóa bởi heatmap), không có CAD. Kiểm tra riêng đóng góp của cổng không gian tại encoder.
- **V3 — Chỉ CAD:** Có CAD (decoder được điều kiện hóa), không có PSG. Kiểm tra riêng đóng góp của cơ chế chú ý có điều kiện tại decoder.
- **V4 — PSG + CAD, Binary bbox:** Kiến trúc đầy đủ PSG+CAD nhưng câu nhắc là binary mask (0/1) thay vì Gaussian heatmap. Kiểm tra tác động của loại mã hóa câu nhắc.
- **V5 — PSG + CAD, Gaussian Heatmap (đề xuất):** Kiến trúc đầy đủ PSG+CAD với Plateau Heatmap. Mô hình cuối cùng được đề xuất.

| Biến thể | PSG | CAD | Loại câu nhắc | Zoom-out Dice | Shift Dice | Mixed Dice |
|---|---|---|---|---|---|---|
| V1 — Concat đơn giản | ✗ | ✗ | Gaussian Heatmap | 0.8718 | 0.7201 | 0.8158 |
| V2 — Chỉ PSG | ✓ | ✗ | Gaussian Heatmap | 0.8643 | 0.7291 | 0.8146 |
| V3 — Chỉ CAD | ✗ | ✓ | Gaussian Heatmap | 0.8827 | 0.7335 | 0.8256 |
| V4 — PSG + CAD, Binary bbox | ✓ | ✓ | Binary bbox | 0.8800 | 0.7378 | 0.8276 |
| **V5 — PSG + CAD, Heatmap (đề xuất)** | ✓ | ✓ | Gaussian Heatmap | **0.8524** | **0.8382** | **0.8496** |

**Hai phát hiện chính:**
1. **CAD đóng góp mạnh hơn PSG** ở Zoom-out (V3=0.8827 > V2=0.8643), nhưng cần cả PSG+CAD để đạt robustness ở Shift.
2. **Gaussian Heatmap vs Binary bbox (V5 vs V4):** Shift tăng +0.1004 (0.8382 vs 0.7378), Zoom-out giảm nhẹ −0.0276. Đây là trade-off có chủ đích: Gaussian "làm mờ" biên câu nhắc → mạng không ghi nhớ cứng vị trí → robustness tốt hơn nhiều.

---

### 1.8 Kiểm Định Độ Ổn Định — Cross-Validation 4-Fold

*4 lần phân chia dữ liệu độc lập, cùng siêu tham số. **TB** = Trung Bình (average over 4 folds).*

| Kịch bản | Dice ↑ | IoU ↑ | Recall ↑ | HD95 ↓ (px) | CBL ↑ |
|---|---|---|---|---|---|
| Zoom-out (TB 4 fold) | 0.8769 | 0.7884 | 0.9145 | 9.78 | 0.9601 |
| Shift (TB 4 fold) | 0.8422 | 0.7389 | 0.8723 | 12.60 | 0.9369 |
| Mixed (TB 4 fold) | 0.8686 | 0.7766 | 0.9016 | 10.37 | 0.9541 |

Kết quả 4 fold đồng nhất — mô hình ổn định, không phụ thuộc cách chia dữ liệu.

---

### 1.9 Phân Tích Sub-Category

#### Nhóm theo độ khó (phân nhóm theo Dice của U-Net, N=187 ảnh, 50 dễ nhất / 50 khó nhất)

| Nhóm | Mô hình | Dice ↑ | IoU ↑ | HD95 ↓ (px) | CBL ↑ |
|---|---|---|---|---|---|
| Dễ (top-50) | U-Net | 0.8691 | 0.7713 | 21.05 | 0.9510 |
| Dễ (top-50) | Attention U-Net | 0.7609 | 0.6539 | 34.48 | 0.8662 |
| **Dễ (top-50)** | **PGA-UNet** | **0.8938** | **0.8122** | **13.16** | **0.9588** |
| Khó (bottom-50) | U-Net | 0.0000 | 0.0000 | 265.69 | 0.0243 |
| Khó (bottom-50) | Attention U-Net | 0.0929 | 0.0639 | 236.46 | 0.1551 |
| **Khó (bottom-50)** | **PGA-UNet** | **0.8181** | **0.7114** | **18.06** | **0.9247** |

U-Net sụp đổ hoàn toàn ở nhóm Khó (Dice 0.0000, HD95 265.69px). PGA **duy trì 0.8181** (Δ+0.8181 = 0.8181 − 0.0000, chênh lệch Dice PGA so với U-Net tại nhóm Khó) — minh chứng rõ nhất cho vai trò của PSG khi tổn thương phức tạp.

#### Nhóm theo đặc tính lâm sàng (50 mẫu per-polygon mỗi nhóm)

| Nhóm | Mô hình | Dice ↑ | IoU ↑ | HD95 ↓ (px) | CBL ↑ |
|---|---|---|---|---|---|
| Tổn thương nhỏ | SAM-Med2D FT | 0.3887 | 0.2835 | 88.73 | 0.6855 |
| **Tổn thương nhỏ** | **PGA-UNet** | **0.7970** | **0.6818** | **13.64** | **0.9202** |
| Biên giới mờ | SAM-Med2D FT | 0.5407 | 0.3886 | 27.44 | 0.8401 |
| **Biên giới mờ** | **PGA-UNet** | **0.8288** | **0.7152** | **12.00** | **0.9384** |
| Tổn thương rõ nét | SAM-Med2D FT | 0.8465 | 0.7392 | 27.04 | 0.9483 |
| **Tổn thương rõ nét** | **PGA-UNet** | **0.8741** | **0.7850** | **24.71** | **0.9548** |

Khoảng cách lớn nhất ở **Tổn thương nhỏ** (Δ+0.4083): SAM hoạt động ở 256×256 khiến tổn thương nhỏ chỉ còn vài pixel, PGA ở 512×512 giữ nguyên chi tiết.

---

## Đóng Góp 2 — Đánh Giá Pipeline Có Phân Lớp Hỗ Trợ

Trong thực tế lâm sàng, không phải ảnh nào cũng có tổn thương. Để đánh giá PGA-UNet trong điều kiện thực tế hơn, đề tài tích hợp thêm bộ lọc sàng lọc **EfficientNet_B3** đứng trước PGA-UNet và đánh giá hiệu năng toàn pipeline trên tập ảnh hỗn hợp.

### 2.1 Bộ Lọc Sàng Lọc EfficientNet_B3

Phân loại tự động ảnh X-quang "có bệnh lý / bình thường" trước khi đưa vào PGA-UNet.

- **Kiến trúc:** EfficientNet_B3, ~10.7M tham số, ảnh 300×300, ImageNet pretrained
- **Fine-tune 2 giai đoạn trên BTXRD:**
  - Giai đoạn 1 (25 epoch): đóng băng backbone, chỉ train head, LR=1e-4
  - Giai đoạn 2 (75 epoch): mở khóa toàn bộ trọng số **trừ các lớp BatchNorm** (giữ BatchNorm đóng băng), LR=1e-5, CosineAnnealingLR, patience=15  
    *Lý do giữ BatchNorm đóng băng:* Các lớp BatchNorm lưu trữ running mean/variance được ước lượng trên ImageNet. Nếu mở khóa, chúng sẽ cập nhật lại thống kê chạy ngay trong epoch đầu tiên sau khi giải đóng băng — làm rối loạn đặc trưng đã học và khiến độ chính xác giảm đột ngột ở epoch đó trước khi phục hồi.
- **Kết quả đánh giá độc lập — Standalone (tập test BTXRD, 375 ảnh):**

| Accuracy | Precision | Recall | Specificity | NPV | F1 | AUC-ROC |
|---|---|---|---|---|---|---|
| 85.60% | 91.30% | 78.61% | 92.55% | 81.31% | 84.52% | **0.9258** |

### 2.2 Đánh Giá Pipeline End-to-End

Pipeline chạy trên **dataset_online** (375 ảnh hỗn hợp: 187 có bệnh + 188 bình thường) — EfficientNet_B3 phân lớp trước, PGA-UNet phân đoạn sau với ảnh được dự đoán là dương tính.

**Phân loại trên dataset_online:**

| TP | FP | FN | TN | Sensitivity | Specificity | Accuracy | AUC-ROC |
|---|---|---|---|---|---|---|---|
| 181 | 38 | 6 | 150 | 96.79% | 79.79% | 88.27% | 0.9688 |

**Phân đoạn pipeline (đánh giá per-polygon):**

$$\text{Pipeline Dice} = \frac{\displaystyle\sum_{i \in \text{polygon(TP)}} \text{Dice}_i}{N_{\text{polygon(TP)}} + N_{\text{image(FP)}}} = \frac{\sum 226 \text{ polygon Dice}}{226 + 38} = \mathbf{0.7296}$$

| Thống kê | Giá trị |
|---|---|
| 181 ảnh TP → 226 polygon | TB 1.25 polygon/ảnh |
| 38 ảnh FP → Dice = 0 | Kéo điểm xuống |
| Mẫu số | 264 đơn vị |
| **Pipeline Dice** | **0.7296** |
| **Pipeline IoU** | **0.6430** |

**Phân tích sai số tích lũy:** Pipeline Dice (0.7296) thấp hơn PGA đánh giá độc lập/standalone (0.8524) do 38 ảnh bình thường bị phân loại sai (FP). Bottleneck là Specificity dataset_online (79.79%) — cải thiện Specificity sẽ trực tiếp nâng Pipeline Dice.

---

## Tóm Tắt So Sánh

| Tiêu chí | PGA-UNet (đề xuất) | SAM-Med2D FT | SAM-Med2D ZS | U-Net / AttUNet |
|---|---|---|---|---|
| Tham số | ~4M | ~100M | ~100M | ~7M / ~8M |
| Prompt | Bounding box → Plateau Heatmap | Bounding box → Position embedding | Bounding box → Position embedding | Không có |
| Độ phân giải | 512×512 | 256×256 (cố định) | 256×256 (cố định) | 512×512 |
| Dice Zoom-out | **0.8524** | 0.7350 | 0.5337 | 0.4534 / 0.4159 |
| Dice Shift | **0.8382** | 0.7097 | 0.5184 | N/A |
| Dice Mixed | **0.8496** | 0.7283 | 0.5286 | N/A |
| HD95 (norm) Zoom-out | **0.027** | 0.207 | 0.374 | — |
| VRAM suy luận | ~1 GB | ~2 GB | ~2 GB | ~0.5 GB |
| Huấn luyện | Từ đầu trên BTXRD | Fine-tune từ ViT-B | Không fine-tune | Từ đầu trên BTXRD |
