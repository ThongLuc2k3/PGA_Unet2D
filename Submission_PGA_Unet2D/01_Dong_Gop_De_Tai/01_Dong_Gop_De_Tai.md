# Đóng Góp Của Đề Tài

**Đề tài:** Phát triển hệ thống phân đoạn ảnh X-quang xương dựa vào câu nhắc trực quan  
**Tác giả:** Lục Tố Thông | **GVHD:** | **Năm:** 2026  
**Bộ dữ liệu:** BTXRD — Bone Tumor X-Ray Dataset (Nature Scientific Data, 2024)

---

## Bối Cảnh và Động Lực

Bài toán phân đoạn tổn thương xương trên ảnh X-quang 2D gặp hai thách thức cốt lõi:

1. **Phương pháp tự động** (U-Net, Attention U-Net) thiếu hoàn toàn cơ chế tiếp nhận định hướng từ bác sĩ. Khi tổn thương có độ tương phản thấp hoặc cấu trúc xương chồng lấp, mô hình không biết nên "nhìn" vào đâu, dẫn đến phân đoạn sai hoặc bỏ sót.

2. **Mô hình nền tảng** như SAM-Med2D (ViT-B ~100M tham số) tuy có câu nhắc nhưng bị giới hạn độ phân giải 256×256 và đòi hỏi tài nguyên tính toán lớn — khó triển khai tại cơ sở y tế tuyến cơ sở.

**Giải pháp:** Tích hợp câu nhắc trực quan (bounding box từ bác sĩ) trực tiếp vào kiến trúc CNN hạng nhẹ, huấn luyện chuyên biệt từ đầu trên dữ liệu X-quang xương.

---

## Đóng Góp 1 — Nghiên Cứu: Kiến Trúc PGA-UNet

Đề xuất mô hình **PGA-UNet (Prompt-Guided Attention U-Net)** — ~4M tham số, ảnh đầu vào 512×512, huấn luyện hoàn toàn từ đầu trên BTXRD. Hai thành phần chính được thiết kế mới, không kế thừa trực tiếp từ bài báo nào:

### 1.1 Prompt Spatial Gate (PSG) — Cổng Không Gian Tại Bộ Mã Hóa

Bản đồ nhiệt câu nhắc được tích hợp vào từng tầng đặc trưng của bộ mã hóa qua phép nhân **tăng cường có chọn lọc**:

$$\tilde{\mathbf{x}}^l = \mathbf{x}^l \odot \bigl(1 + \alpha \cdot \sigma(\mathbf{W}_{gate} \ast \mathbf{H}^l)\bigr)$$

- **Thiết kế tăng cường (không ức chế):** vùng trong câu nhắc được khuếch đại, vùng ngoài giữ nguyên — không mất thông tin toàn cục.
- Ngay từ các tầng mã hóa đầu, mạng học đặc trưng tổn thương thay vì phải "tự tìm" khắp ảnh.

### 1.2 Conditioned Attention Decoder (CAD) — Cơ Chế Chú Ý Có Điều Kiện Tại Bộ Giải Mã

Tín hiệu gating được điều kiện hóa bởi câu nhắc với **trọng số tin cậy giảm dần** theo độ sâu tầng giải mã:

$$\mathbf{g}' = \mathbf{g} + c \cdot \alpha \cdot w \cdot \mathbf{p}_{\text{enc}}, \quad w \in \{1.0,\ 0.7,\ 0.4,\ 0.2\}$$

- Tầng sâu (ngữ nghĩa): câu nhắc ảnh hưởng mạnh (w=1.0) — định hướng vùng tổn thương.
- Tầng nông (chi tiết đường biên): câu nhắc ảnh hưởng yếu (w=0.2) — mạng tự do tái tạo biên.
- Mở rộng từ công thức Attention Gate [Oktay 2018] bằng cách thêm fusion câu nhắc.

### 1.3 Plateau Heatmap — Mã Hóa Câu Nhắc Trực Quan

Bounding box bác sĩ vẽ → bản đồ nhiệt 2D: gán 1.0 đồng đều bên trong (mở rộng 30%), làm mờ viền bằng Gaussian blur (kernel 31×31):

$$\mathbf{H}_{prompt} = \text{GaussianBlur}(\mathbf{B}_{filled},\ k=31)$$

- **Không dùng binary mask:** đường biên sắc nét tạo gradient giả — mạng học cạnh hộp thay vì đặc trưng tổn thương.
- **Không dùng Gaussian 2D thuần:** U-Net nhận heatmap qua phép nhân feature map (không qua position embedding như Transformer), nên phân phối đồng đều + làm mờ viền phù hợp hơn.

### 1.4 Kết Quả Thực Nghiệm (Đóng Góp 1)

| Mô hình | Kịch bản | Dice ↑ | IoU ↑ | HD95 ↓ | CBL ↑ |
|---|---|---|---|---|---|
| U-Net (tự động, không prompt) | — | 0.4534 | 0.3671 | 128.61 | 0.5968 |
| Attention U-Net (tự động) | — | 0.4159 | 0.3306 | 132.86 | 0.5569 |
| SAM-Med2D (zero-shot) | Zoom-out | 0.5337 | 0.3924 | HD95/256 | 0.8194 |
| SAM-Med2D (fine-tuned) | Zoom-out | 0.7350 | 0.6130 | HD95/256 | 0.8893 |
| **PGA-UNet (đề xuất)** | **Zoom-out** | **0.8524** | **0.7527** | **13.96** | **0.9451** |
| **PGA-UNet (đề xuất)** | **Shift (lệch tâm)** | **0.8382** | **0.7336** | **13.57** | **0.9379** |
| **PGA-UNet (đề xuất)** | **Mixed 70/30** | **0.8496** | **0.7486** | **14.38** | **0.9436** |

**Điểm nổi bật:**
- Vượt SAM-Med2D fine-tuned +0.1174 Dice (Zoom-out) với ít hơn 25× tham số (~4M vs ~100M)
- Robustness cao: Dice chỉ giảm 0.0142 khi câu nhắc bị lệch hoàn toàn (Zoom → Shift)
- VRAM suy luận ~1GB — có thể chạy trên GPU 4GB phổ thông

---

## Đóng Góp 2 — Sản Phẩm: Pipeline Lâm Sàng End-to-End

Tích hợp PGA-UNet vào hệ thống phần mềm hoàn chỉnh phục vụ sàng lọc lâm sàng thực tế:

### 2.1 Bộ Lọc Sàng Lọc EfficientNet_B3 (Gatekeeper)

Phân loại tự động ảnh X-quang "có bệnh lý / bình thường" trước khi đưa vào PGA-UNet. Điều này giải quyết thực tế: trong lâm sàng không phải ảnh nào cũng có tổn thương — PGA-UNet không nên nhận ảnh bình thường.

- **Kiến trúc:** EfficientNet_B3, ~10.7M tham số, ảnh 300×300, ImageNet pretrained
- **Chiến lược fine-tune 2 giai đoạn:**
  - Giai đoạn 1 (25 epoch): đóng băng toàn bộ backbone, chỉ train head, LR=1e-4
  - Giai đoạn 2 (75 epoch): mở khóa toàn bộ, LR=1e-5, CosineAnnealingLR, patience=15
- **Kết quả (standalone BTXRD):** Accuracy=85.60%, Recall=78.61%, Specificity=92.55%, AUC-ROC=0.9258

### 2.2 Đánh Giá Pipeline End-to-End (Cascading Error)

Pipeline đầy đủ được thử nghiệm trên tập **dataset_online** (375 ảnh hỗn hợp: 187 có bệnh + 188 bình thường):

| Chỉ số pipeline | Giá trị |
|---|---|
| TP / FP / FN / TN | 181 / 38 / 6 / 150 |
| Sensitivity (Recall) | 96.79% |
| Specificity | 79.79% |
| Accuracy | 88.27% |
| AUC-ROC | 0.9688 |
| 181 ảnh TP → 226 polygon (đánh giá per-polygon) | — |
| 38 ảnh FP → Dice = 0 | — |
| **Pipeline Dice** | **0.7296** |
| **Pipeline IoU** | **0.6430** |

**Phân tích sai số tích lũy:** Pipeline Dice (0.7296) thấp hơn PGA standalone (0.8524) do 38 ảnh bình thường bị phân loại sai (FP) kéo điểm xuống. Bottleneck là Specificity (79.79%) — cải thiện Specificity sẽ trực tiếp nâng Pipeline Dice.

---

## Tóm Tắt So Sánh

| Tiêu chí | PGA-UNet (đề xuất) | SAM-Med2D (fine-tuned) | U-Net / AttUNet |
|---|---|---|---|
| Tham số | ~4M | ~100M | ~7M / ~8M |
| Prompt | Bounding box → Plateau Heatmap | Bounding box → Position embedding | Không có |
| Độ phân giải | 512×512 | 256×256 (cố định) | 512×512 |
| Dice (Zoom-out) | **0.8524** | 0.7350 | 0.4534 / 0.4159 |
| Dice (Shift) | **0.8382** | 0.7097 | N/A |
| VRAM suy luận | ~1 GB | ~2 GB | ~0.5 GB |
| Huấn luyện | Từ đầu trên BTXRD | Fine-tune từ ViT-B pretrained | Từ đầu trên BTXRD |
