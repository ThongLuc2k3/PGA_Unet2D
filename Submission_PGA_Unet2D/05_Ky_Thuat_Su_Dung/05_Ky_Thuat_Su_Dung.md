# Kỹ Thuật Sử Dụng Và Nguồn Gốc

> Phân biệt rõ kỹ thuật **kế thừa từ bài báo** vs **đề xuất mới của đề tài** để tránh đạo văn kỹ thuật.

---

## Kỹ Thuật Kế Thừa (Có Trích Dẫn Bài Báo Gốc)

| Kỹ thuật | Kế thừa từ | Cách sử dụng trong đề tài |
|---|---|---|
| **Kiến trúc U-Net** | Ronneberger 2015 [1] | Làm nền tảng encoder-decoder; không thay đổi cấu trúc cơ bản (4 cấp độ, skip connections, Max Pooling, UpConv) |
| **Attention Gate** | Oktay 2018 [2] | Kế thừa công thức tính hệ số chú ý α^l; mở rộng thành Conditioned Attention bằng cách thêm tín hiệu câu nhắc vào gating |
| **Kiến trúc SAM-Med2D** | Cheng 2023 [3] | Dùng làm mô hình đối sánh (benchmark); fine-tune trên BTXRD để so sánh công bằng; không tích hợp vào hệ thống đề xuất |
| **Backbone EfficientNet_B3** | Tan & Le 2019 [4] | Dùng trọng số pretrained ImageNet; fine-tune 2 giai đoạn trên BTXRD làm gatekeeper phân lớp |
| **Dataset BTXRD** | Nguyen 2024 [5] | Toàn bộ dữ liệu huấn luyện và đánh giá (ảnh X-quang xương có mask phân đoạn pixel-level) |
| **YOLOv11s** | Ultralytics 2024 [6] | Dùng pretrained COCO; fine-tune trên annotations nhiễu R/L của BTXRD để phát hiện và xóa ký tự nhiễu |

---

## Kỹ Thuật Đề Xuất Mới (Đóng Góp Gốc Của Đề Tài)

| Kỹ thuật | Mô tả | Cơ sở lý luận |
|---|---|---|
| **Prompt Spatial Gate (PSG)** | Tích hợp bản đồ nhiệt vào từng tầng bộ mã hóa qua phép nhân tăng cường có chọn lọc: x̃^l = x^l ⊙ (1 + α·σ(W_gate * H^l)) | Chưa có trong bài báo nào; lấy cảm hứng từ cơ chế gating nhưng thiết kế cho encoder U-Net, không ức chế mà chỉ khuếch đại vùng câu nhắc |
| **Conditioned Attention Decoder (CAD)** | Điều kiện hóa tín hiệu gating bằng câu nhắc với trọng số tin cậy giảm dần theo tầng: g' = g + c·α·w·p_enc, w ∈ {1.0, 0.7, 0.4, 0.2} | Mở rộng Attention Gate [2]; thêm cơ chế fusion câu nhắc với confidence score và trọng số w giảm dần — phản ánh vai trò hướng dẫn giảm dần từ ngữ nghĩa đến chi tiết |
| **Plateau Heatmap** | Gán 1.0 đồng đều bên trong bbox (mở rộng 30%) + Gaussian blur viền k=31 | Khác với Gaussian 2D thuần (dùng trong SAM qua position embedding Transformer); phù hợp với feature map U-Net qua phép nhân trực tiếp. Khác với binary mask: không tạo gradient giả tạo ở đường biên |
| **Chiến lược fine-tune 2 giai đoạn EfficientNet_B3** | Giai đoạn 1 (25 ep): đóng băng backbone, LR=1e-4; Giai đoạn 2 (75 ep): mở khóa, LR=1e-5, CosineAnnealingLR, patience=15 | Chiến lược fine-tuning tiêu chuẩn áp dụng cụ thể cho bài toán phân lớp X-quang xương BTXRD; không kế thừa từ bài báo cụ thể nào |

---

## Phân Biệt Rõ: Kế Thừa vs Đề Xuất Mới

```
KẾ THỪA TRỰC TIẾP (cite bài báo gốc):
  U-Net encoder-decoder architecture ─────────── [1]
  Attention Gate formula (α^l) ────────────────── [2]
  SAM-Med2D (dùng làm benchmark) ─────────────── [3]
  EfficientNet_B3 backbone ────────────────────── [4]

KẾ THỪA + MỞ RỘNG (dựa trên nhưng có sửa đổi):
  Attention Gate → Conditioned Attention
    (thêm câu nhắc vào gating signal) ──────── dựa trên [2]

ĐỀ XUẤT GỐC (không kế thừa từ bài báo nào):
  Prompt Spatial Gate (PSG)
  Plateau Heatmap (biến thể thực tiễn riêng)
  Kiến trúc tổng thể PGA-UNet (kết hợp PSG + CAD)
```

---

## Điều Kiện So Sánh Công Bằng

| Khía cạnh | Chi tiết |
|---|---|
| U-Net / Att-UNet vs PGA | Khác nhau về phương thức (tự động vs có prompt) — so sánh có chủ đích, minh chứng giá trị của prompt guidance |
| PGA vs SAM-Med2D | Cùng điều kiện: cùng tập test, cùng 3 kịch bản prompt (Zoom-out, Shift, Mixed), đánh giá per-polygon. SAM được fine-tune trên BTXRD để so sánh công bằng |
| Các biến thể ablation V1–V5 | Cùng siêu tham số, chỉ thay đổi cấu hình PSG/CAD và loại câu nhắc |
| Cross-validation | 4 lần phân chia dữ liệu độc lập, cùng siêu tham số |
