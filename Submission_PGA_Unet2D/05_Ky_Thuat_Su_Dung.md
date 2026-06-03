# Kỹ Thuật Sử Dụng Và Nguồn Gốc

> Mục đích: phân biệt rõ kỹ thuật **kế thừa từ bài báo** vs **đề xuất mới của đề tài** để tránh đạo văn.

---

## Kỹ Thuật Kế Thừa (Có Cite Bài Báo Gốc)

| Kỹ thuật | Kế thừa từ | Cách sử dụng trong đề tài |
|---|---|---|
| **Kiến trúc U-Net** | Ronneberger 2015 [1] | Làm nền tảng encoder-decoder; không thay đổi cấu trúc cơ bản |
| **Attention Gate** | Oktay 2018 [2] | Kế thừa công thức tính hệ số chú ý $\alpha^l$; mở rộng thành Conditioned Attention bằng cách thêm điều kiện hóa câu nhắc |
| **Kiến trúc SAM-Med2D** | Cheng 2023 [3] | Dùng làm mô hình đối sánh (benchmark); không tích hợp vào hệ thống đề xuất |
| **Backbone MobileNetV4** | Qin 2024 [4] | Dùng trọng số pretrained ImageNet-1K; fine-tune 2 giai đoạn trên BTXRD |
| **Thuật toán GradCAM** | Selvaraju 2019 [5] | Kế thừa công thức tính $\alpha_k^c$ và $L_\text{GradCAM}$; ứng dụng vào cơ chế cứu hộ câu nhắc (ứng dụng mới) |
| **Dataset BTXRD** | Nguyen 2024 [6] | Toàn bộ dữ liệu huấn luyện và đánh giá |
| **YOLOv11s** | Ultralytics 2024 | Dùng pretrained COCO; fine-tune trên annotations nhiễu R/L của BTXRD |
| **Roboflow** | Roboflow Inc. | Nền tảng gán nhãn bounding box; không có đóng góp kỹ thuật |

---

## Kỹ Thuật Đề Xuất Mới (Đóng Góp Gốc Của Đề Tài)

| Kỹ thuật | Mô tả | Cơ sở lý luận |
|---|---|---|
| **Prompt Spatial Gate (PSG)** | Tích hợp bản đồ nhiệt vào bộ mã hóa qua phép nhân tăng cường chọn lọc | Chưa có trong bài báo nào; lấy cảm hứng từ cơ chế gating nhưng thiết kế cho U-Net encoder |
| **Conditioned Attention Decoder (CAD)** | Điều kiện hóa tín hiệu gating bằng câu nhắc với trọng số tin cậy giảm dần theo tầng | Mở rộng Attention Gate [2]; thêm cơ chế fusion câu nhắc qua confidence score và trọng số w ∈ {1.0, 0.7, 0.4, 0.2} |
| **Plateau Heatmap** | Gán 1.0 đồng đều bên trong box + Gaussian blur viền k=31 | Lấy cảm hứng từ Gaussian 2D [lý thuyết] và bản đồ nhiệt GradCAM [5]; biến thể thực tiễn phù hợp U-Net |
| **IPR (Iterative Prompt Refinement)** | Vòng lặp tinh chỉnh câu nhắc dùng tâm hình học mặt nạ dự đoán, tối đa 3 vòng | Hoàn toàn mới; không kế thừa từ bài báo nào |
| **Pipeline GradCAM Rescue** | Bộ kiểm duyệt 3 tiêu chí → GradCAM trích điểm neo → IPR cứu hộ | Ứng dụng mới của GradCAM [5] trong ngữ cảnh sửa câu nhắc sai; kết hợp với IPR là đóng góp gốc |
| **Two-stage fine-tuning MobileNetV4** | Giai đoạn 1: đóng băng backbone 5 epoch; Giai đoạn 2: mở khóa toàn bộ | Chiến lược fine-tuning chuẩn; áp dụng cụ thể cho bài toán phân lớp BTXRD |

---

## Phân Biệt Kế Thừa Vs Đề Xuất Mới

```
Kế thừa nguyên si:
  U-Net architecture ────────────────── [1]
  Attention Gate formula ─────────────── [2]
  GradCAM formula (α_k, L_GradCAM) ──── [5]

Kế thừa + mở rộng:
  Attention Gate → Conditioned Attention (thêm câu nhắc) ── dựa trên [2]
  Gaussian heatmap → Plateau Heatmap (biến thể thực tiễn) ── cảm hứng từ lý thuyết

Đề xuất gốc (không kế thừa):
  Prompt Spatial Gate (PSG)
  IPR (Iterative Prompt Refinement)
  Pipeline GradCAM Rescue (ứng dụng GradCAM vào sửa câu nhắc sai)
```
