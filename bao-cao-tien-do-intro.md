# Báo cáo tiến độ — Chương 3 & 4

## Đang làm gì?

Xây dựng hệ thống **phân đoạn vùng tổn thương xương** trên ảnh X-quang, dẫn hướng bằng câu nhắc trực quan (visual prompt) thay vì để mô hình tự đoán hoàn toàn.

---

## Tại sao cần làm?

Ảnh X-quang xương có nền phức tạp — mô mềm, khớp, cạnh xương dễ gây nhầm lẫn.  
Các mô hình phân đoạn tự động (U-Net, Attention U-Net) **không biết bác sĩ đang quan tâm vùng nào**, dẫn đến kết quả sai hoặc thiếu nhất quán giữa các ca.

---

## Điểm khác biệt so với các mô hình thông thường

| Vấn đề | Cách tiếp cận thông thường | Cách tiếp cận của đề tài |
|--------|--------------------------|--------------------------|
| Không có hướng dẫn đầu vào | Chỉ nhận ảnh, tự phân đoạn | Nhận thêm **visual prompt** (bounding box) từ bác sĩ |
| Mô hình chỉ train ảnh bệnh | Bị nhầm ảnh bình thường là bệnh | Thêm **Gatekeeper** (MobileNetV4) — lọc trước, chỉ phân đoạn khi thực sự phát hiện tổn thương |
| Prompt ban đầu có thể chưa chính xác | Giữ nguyên kết quả | **IPR Pipeline** — lặp tự tinh chỉnh prompt 3 lần, kết quả hội tụ tốt hơn |
| Mô hình không tự giải thích | Hộp đen | **GradCAM Rescue** — khi prompt sai hoàn toàn, dùng heat map để tìm lại vùng tổn thương |

---

## Kết quả nổi bật (so sánh thực nghiệm, N=248 mẫu)

| Mô hình | Dice ↑ | IoU ↑ | HD95 ↓ | Ghi chú |
|---------|--------|-------|--------|---------|
| U-Net (baseline) | 0.509 | 0.413 | 125 px | Tự động, không prompt |
| Attention U-Net | 0.411 | 0.321 | 141 px | Tự động, kém hơn U-Net |
| SAM-Med2D (SOTA) | 0.762 | 0.642 | 52 px | Prompt-based, ~100M params |
| **PGA-UNet (đề tài)** | **0.866** | **0.769** | **12 px** | Prompt-based, ~4M params |

> SAM-Med2D là mô hình SOTA được fine-tune từ 4M+ ảnh y tế (~100M tham số). PGA-UNet vượt trội với kiến trúc nhẹ hơn **25 lần**, được thiết kế đặc thù cho X-quang xương.

Gatekeeper (MobileNetV4): Accuracy 88.08%, F1 87.75%  
YOLOv11s (lọc nhiễu ảnh đầu vào): mAP50 98.6%

---

## Tóm tắt pipeline hoàn chỉnh

```
Ảnh X-quang đầu vào
    → YOLOv11s: loại bỏ nhiễu (nhãn, ký tự R/L)
    → MobileNetV4 Gatekeeper: phân loại bình thường / bất thường
    → PGA-UNet + IPR (3 vòng lặp): phân đoạn có dẫn hướng
    → GradCAM Rescue: bổ sung nếu prompt sai hoàn toàn
    → Kết quả mask + Gradio UI (phản hồi ~180ms)
```

---

---

## Chương 3 — Mô hình và hệ thống đề xuất

### 3.1 Kiến trúc tổng thể

Hệ thống hoạt động theo **4 giai đoạn liên hoàn**:

1. **Tiền xử lý** — làm sạch ảnh X-quang thô (loại ký tự R/L, chuẩn hóa pixel)
2. **Gatekeeper sàng lọc** — phân loại bình thường/bất thường, chỉ chuyển tiếp khi có bệnh lý
3. **PGA-UNet phân đoạn** — bác sĩ vẽ bounding box → hệ thống tạo prompt heatmap → mô hình phân đoạn có dẫn hướng
4. **IPR & GradCAM thẩm định** — tự tinh chỉnh prompt lệch nhẹ; từ chối + cứu hộ khi prompt sai hoàn toàn

### 3.2 Tiền xử lý dữ liệu

Dữ liệu BTXRD (Nature Scientific Data 2024) chứa nhiều loại nhiễu kỹ thuật:
- **ICC Profile lỗi** trong file PNG → gây crash OpenCV → xử lý bằng script `clean_data.py`
- **Ký tự R/L cản quang** (độ tương phản cao, dễ bị nhầm là tổn thương) → **YOLOv11s** detect và xóa (mAP50 = 98.6%)
- **Annotation** bằng LabelMe, lưu polygon JSON → chuyển thành PNG mask pixel-level
- **Augmentation đồng bộ** (hflip + xoay ±15°) — ảnh và mask biến đổi cùng nhau, không lệch nhau

### 3.3 PGA-UNet

Kiến trúc U-Net mở rộng với 2 cơ chế mới:
- **Prompt Spatial Gate** — nhận bounding box → tạo Gaussian heatmap → "khóa" vùng attention vào khu vực bác sĩ chỉ định, chặn nhiễu từ xương và mô mềm xung quanh
- **Conditioned Attention** — attention gate ở mỗi skip connection được điều kiện hóa bởi prompt, đảm bảo đặc trưng decoder luôn "nhớ" ngữ cảnh vị trí

### 3.4 IPR Pipeline (Iterative Prompt Refinement)

Khi prompt lệch nhẹ, mô hình vẫn ra mask nhưng lệch tâm. IPR tự tinh chỉnh:
- Lấy **centroid của mask** vừa ra → làm tâm prompt mới → chạy lại
- Lặp tối đa **k=3** lần (tổng ~180ms < giới hạn 200ms)
- Tại k=2 đã bão hòa: Dice tăng từ 0.837 → 0.852, HD95 giảm từ 14.4 → 12.7 px

### 3.5 Mô hình Gatekeeper (MobileNetV4-Hybrid-Medium)

Lý do cần có: PGA-UNet **chỉ được train trên ảnh có bệnh** → nếu nhận ảnh bình thường sẽ tạo mask sai.  
Giải pháp: thêm một bước phân loại trước.
- **MobileNetV4-Hybrid-Medium** (~11M params, 37.88 MB) — fine-tune 2 giai đoạn trên BTXRD
- Giai đoạn 1: đóng băng backbone, chỉ train head
- Giai đoạn 2: mở toàn bộ, học rate nhỏ hơn 10 lần

---

## Chương 4 — Thực nghiệm và đánh giá kết quả

### 4.1 Thiết lập thực nghiệm

**Dataset BTXRD:**

| Tập | Số ảnh | Số mẫu polygon |
|-----|--------|----------------|
| Train | ~1,495 | 1,859 |
| Validation | ~159 | 211 |
| Test | 187 | **248** (28 ảnh có 2 khối u) |

Hai luồng dữ liệu song song:
- Phân đoạn: chỉ ảnh có bệnh + mask pixel
- Phân lớp (Gatekeeper): cả ảnh bệnh lẫn ảnh bình thường, split 70/15/15

**Cài đặt huấn luyện** (đồng nhất cho U-Net, AttUNet, PGA-UNet):  
Batch=4, img=512×512, AdamW lr=1e-4, ReduceLROnPlateau, Early Stop patience=15, Loss = BCE + Dice

### 4.2 So sánh baseline

PGA-UNet (prompt-based) vs các mô hình tự động:

| Mô hình | Dice | IoU | HD95 | Epoch dừng |
|---------|------|-----|------|-----------|
| U-Net | 0.509 | 0.413 | 125 px | ep. 82 |
| Attention U-Net | 0.411 | 0.321 | 141 px | ep. 47 |
| **PGA-UNet** | **0.866** | **0.769** | **12 px** | ep. 60 |

*Attention U-Net kém hơn U-Net gốc vì attention gate khi không có prompt sẽ bị kích hoạt nhầm vào cạnh xương/thiết bị cố định — khuếch đại nhiễu thay vì ức chế.*

### 4.3 Tính bền bỉ (Robustness) của PGA-UNet

| Kịch bản prompt | Dice | CBL |
|-----------------|------|-----|
| Zoom-out (lý tưởng) | 0.866 | 0.958 |
| Shift (lệch tâm) | 0.828 | 0.932 |
| Mixed 70/30 (thực tế) | 0.855 | 0.953 |

Khi prompt lệch hoàn toàn: Dice chỉ giảm **4.4%** — chứng minh mô hình dùng prompt như "ngọn hải đăng", không phụ thuộc mù quáng vào tọa độ.

### 4.4 So sánh với SAM-Med2D (SOTA prompt-based)

| Mô hình | Kịch bản | Dice | IoU | HD95 |
|---------|----------|------|-----|------|
| **PGA-UNet** | Zoom-out | **0.866** | **0.769** | **12.1** |
| **PGA-UNet** | Shift | **0.828** | **0.716** | **15.3** |
| **PGA-UNet** | Mixed | **0.855** | **0.754** | **13.1** |
| SAM-Med2D | Zoom-out | 0.762 | 0.642 | 52.1* |
| SAM-Med2D | Shift | 0.727 | 0.598 | 54.4* |
| SAM-Med2D | Mixed | 0.755 | 0.633 | 51.8* |

*HD95 của SAM-Med2D tính trên ảnh 256×256; sau chuẩn hóa theo kích thước ảnh, PGA chính xác về biên hơn **~8 lần**.*

PGA (~4M params) vượt SAM-Med2D (~15M trainable, ~100M tổng) — kiến trúc nhẹ chuyên biệt hiệu quả hơn foundation model đa mục đích trên bài toán cụ thể này.

### 4.5 Ablation Study: IPR & GradCAM Rescue

**GradCAM Rescue** — khi prompt sai hoàn toàn:

| Tình huống | Dice trước | Dice sau | Tỷ lệ cứu thành công |
|------------|-----------|---------|----------------------|
| Prompt lệch ra rìa xương | 0.125 | 0.783 | **92.5%** |
| Prompt vào vùng nền | 0.000 | 0.710 | **85.3%** |

**IPR convergence** (kịch bản Shift):

| Vòng lặp | Dice | HD95 | Thời gian |
|----------|------|------|-----------|
| k=0 (raw) | 0.837 | 14.4 px | ~45 ms |
| k=1 | 0.849 | 13.1 px | ~90 ms |
| **k=2** | **0.852** | **12.8 px** | ~135 ms |
| k=3 | 0.853 | 12.7 px | ~180 ms |

Bão hòa tại k=2; chọn k=3 vì vẫn trong giới hạn 200ms và có giá trị khi điểm GradCAM khởi tạo xa.

### 4.6 Kết quả Gatekeeper (MobileNetV4)

| Metric | Kết quả |
|--------|---------|
| Accuracy | 88.08% |
| Precision | 89.89% |
| Recall (Sensitivity) | 85.71% |
| F1-Score | 87.75% |

Recall 85.71% đảm bảo hầu hết bệnh nhân có u không bị bỏ sót (false negative thấp) — tiêu chí quan trọng nhất trong sàng lọc y tế.

### 4.7 Ứng dụng thực tiễn (app.py)

Toàn bộ pipeline tích hợp vào Gradio UI:
- Tải ảnh → auto phân lớp (~50ms) → bác sĩ vẽ bounding box → phân đoạn (~45ms)
- Kịch bản cứu hộ phức tạp nhất: tổng ~180ms — đạt tiêu chuẩn real-time (<200ms)
- Triết lý **Human-in-the-loop**: AI hỗ trợ, bác sĩ quyết định cuối cùng
