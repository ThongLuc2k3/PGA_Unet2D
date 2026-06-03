# Đóng Góp Của Đề Tài

**Đề tài:** Phát triển hệ thống phân đoạn ảnh X-quang xương dựa vào câu nhắc trực quan  
**Tác giả:** Lục Tố Thông | **GVHD:** [Tên thầy/cô] | **Năm:** 2026

---

## Đóng Góp 1 — Nghiên Cứu: Kiến Trúc PGA-UNet

Đề xuất mô hình **PGA-UNet (Prompt-Guided Attention U-Net)** — kiến trúc phân đoạn ảnh y khoa có hướng dẫn từ bác sĩ qua hộp giới hạn (bounding box). Hai thành phần mới được tích hợp vào nền tảng U-Net, không kế thừa từ bài báo nào:

### 1.1 Cổng không gian tại bộ mã hóa (Prompt Spatial Gate — PSG)

Bản đồ nhiệt câu nhắc được nhân có chọn lọc vào từng lớp đặc trưng của bộ mã hóa:

$$\tilde{\mathbf{x}}^l = \mathbf{x}^l \odot \bigl(1 + \alpha \cdot \sigma(\mathbf{W}_{gate} \ast \mathbf{H}^l)\bigr)$$

Thiết kế **tăng cường** (không ức chế): vùng trong câu nhắc được khuếch đại, vùng ngoài giữ nguyên. Nhờ đó, bộ mã hóa tập trung học đặc trưng tổn thương ngay từ đầu mà không mất thông tin toàn cục.

### 1.2 Cơ chế chú ý có điều kiện tại bộ giải mã (Conditioned Attention Decoder — CAD)

Tín hiệu gating được điều kiện hóa bởi câu nhắc với **trọng số tin cậy giảm dần** theo độ sâu tầng giải mã:

$$\mathbf{g}' = \mathbf{g} + c \cdot \alpha \cdot w \cdot \mathbf{p}_{\text{enc}}, \quad w \in \{1.0,\, 0.7,\, 0.4,\, 0.2\}$$

Câu nhắc dẫn hướng từ ngữ nghĩa (tầng sâu) đến chi tiết đường biên (tầng nông), phù hợp với vai trò hướng dẫn giảm dần.

### 1.3 Mã hóa câu nhắc Plateau Heatmap

Hộp giới hạn được chuyển thành bản đồ nhiệt 2D: gán giá trị 1.0 đồng đều bên trong, sau đó làm mờ viền bằng bộ lọc Gaussian (kernel 31×31):

$$\mathbf{H}_{prompt} = \text{GaussianBlur}(\mathbf{B}_{mask},\; k=31)$$

**Tại sao không dùng mặt nạ nhị phân:** đường biên sắc nét tạo gradient giả tạo khiến mạng học cạnh hộp thay vì đặc trưng tổn thương.  
**Tại sao không dùng Gaussian thuần:** mô hình SAM dùng positional embedding rời rạc (2 vector 256 chiều) phù hợp Transformer; PGA dùng heatmap 2D phù hợp trực tiếp với feature map U-Net qua phép nhân theo phần tử.

---

## Đóng Góp 2 — Sản Phẩm: Pipeline Lâm Sàng End-to-End

Tích hợp 3 thành phần thành hệ thống phần mềm triển khai được:

### 2.1 Gác cổng sàng lọc (MobileNetV4 Gatekeeper)

Phân loại tự động ảnh X-quang "có bệnh / bình thường" trước khi phân đoạn. PGA-UNet chỉ nhận ảnh bệnh lý, tránh phân đoạn sai trên ảnh lành. Sử dụng MobileNetV4-Hybrid-Medium fine-tune 2 giai đoạn trên BTXRD.

### 2.2 Cơ chế phòng vệ câu nhắc (GradCAM + IPR)

**Vấn đề cần giải quyết:** bác sĩ có thể đặt câu nhắc sai vị trí — SAM-Med2D không có cơ chế nào xử lý tình huống này.

**Giải pháp của đề tài (đóng góp gốc):**
1. Bộ kiểm duyệt 3 tiêu chí phát hiện câu nhắc sai (độ tin cậy < 0.25 / mặt nạ rỗng / vùng câu nhắc > 70% tối)
2. GradCAM trích xuất điểm kích hoạt cực đại làm tâm câu nhắc cứu hộ
3. IPR (Iterative Prompt Refinement) tinh chỉnh tối đa 3 vòng dùng tâm hình học mặt nạ dự đoán

Tỷ lệ phát hiện đạt **174/174 = 100%**; cứu hộ thành công (Dice ≥ 0.70): **21.8%**.

### 2.3 Ứng dụng tích hợp (app.py)

Giao diện Gradio đóng gói toàn bộ pipeline — bác sĩ tải ảnh, vẽ hộp giới hạn, nhận kết quả phân đoạn và bản đồ nhiệt GradCAM.

---

## Tóm Tắt Điểm Khác Biệt So Với SAM-Med2D

| Tiêu chí | PGA-UNet (đề xuất) | SAM-Med2D (so sánh) |
|---|---|---|
| Tham số | ~4 triệu | ~100 triệu |
| Chiến lược huấn luyện | Từ đầu trên BTXRD | Fine-tune từ ViT-B pretrained |
| Mã hóa câu nhắc | Plateau Heatmap 2D | Positional embedding rời rạc |
| Xử lý câu nhắc sai | Có (GradCAM + IPR) | Không có |
| Kết quả Dice (Mixed 70/30) | **0.8558** | 0.7554 |
