# Minh Chứng Số Liệu

> **Lưu ý:** Đề tài có hai đóng góp tách biệt. Số liệu Đóng góp 1 đánh giá PGA-UNet thuần túy (không qua MobileNetV4) — đây là số sạch để so sánh công bằng với SAM. Số liệu Đóng góp 2 đánh giá pipeline lâm sàng hoàn chỉnh và thừa nhận sai số tích lũy.
>
> ⏳ = chờ kết quả thực nghiệm (dataset đã đổi sang ID mới `1X1SY8T63pdBPIdrv_3P0gKVwoLxCa5sW`, chạy lại toàn bộ)

---

# PHẦN I — ĐÓNG GÓP 1: Kiến Trúc PGA-UNet

## A. Kết Quả Phân Đoạn Tổng Hợp (BTXRD)

| Mô hình | Kịch bản | Dice ↑ | IoU ↑ | Độ chính xác ↑ | Độ bao phủ ↑ | HD95 ↓ (px) | CBL ↑ |
|---|---|---|---|---|---|---|---|
| U-Net (không có câu nhắc) | — | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| Attention U-Net (không có câu nhắc) | — | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| SAM-Med2D (zero-shot) | Zoom-out | ⏳ | ⏳ | ⏳ | ⏳ | ⏳* | ⏳ |
| SAM-Med2D (zero-shot) | **Shift** | ⏳ | ⏳ | ⏳ | ⏳ | ⏳* | ⏳ |
| SAM-Med2D (zero-shot) | Mixed 70/30 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳* | ⏳ |
| SAM-Med2D (fine-tuned) | Zoom-out | ⏳ | ⏳ | ⏳ | ⏳ | ⏳* | ⏳ |
| SAM-Med2D (fine-tuned) | **Shift** | ⏳ | ⏳ | ⏳ | ⏳ | ⏳* | ⏳ |
| SAM-Med2D (fine-tuned) | Mixed 70/30 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳* | ⏳ |
| **PGA-UNet (đề xuất)** | Zoom-out | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| **PGA-UNet (đề xuất)** | Shift | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| **PGA-UNet (đề xuất)** | Mixed 70/30 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |

> `*` HD95 của SAM-Med2D tính trên không gian ảnh 256×256 px.  
> U-Net/Att-UNet: merged mask (per-ảnh). PGA/SAM: per-polygon.

**Ba kịch bản câu nhắc:**
- **Zoom-out**: câu nhắc lý tưởng bao quanh hoàn toàn tổn thương (+30%)
- **Shift**: câu nhắc bị dịch lệch ngẫu nhiên — mô phỏng thao tác không chính xác
- **Mixed 70/30**: 70% Zoom-out + 30% Shift — **kịch bản thực tế nhất**

---

## B. Ablation — Đóng Góp Từng Loại Câu Nhắc

> Giữ nguyên kiến trúc PGA-UNet đầy đủ, chỉ thay đổi loại câu nhắc đầu vào tại suy luận.

| Cấu hình câu nhắc | Dice ↑ | IoU ↑ | HD95 ↓ (px) | CBL ↑ |
|---|---|---|---|---|
| PGA + Câu nhắc rỗng | ⏳ | ⏳ | ⏳ | ⏳ |
| PGA + Câu nhắc nhiễu ngẫu nhiên | ⏳ | ⏳ | ⏳ | ⏳ |
| SAM-Med2D (fine-tuned, hard bbox) | ⏳ | ⏳ | ⏳* | ⏳ |
| PGA + Hard binary bbox | ⏳ | ⏳ | ⏳ | ⏳ |
| **PGA + Plateau Heatmap (triển khai)** | ⏳ | ⏳ | ⏳ | ⏳ |
| PGA + Oracle (GT mask làm câu nhắc) | ⏳ | ⏳ | ⏳ | ⏳ |

---

## C. Ablation — Đóng Góp Từng Thành Phần Kiến Trúc (V1–V5)

> Đánh giá trên kịch bản **Zoom-out**. Chạy lại toàn bộ với dataset mới.

| Biến thể | PSG | CAD | Loại câu nhắc | Dice ↑ | IoU ↑ | HD95 ↓ (px) | CBL ↑ | Best Val Dice | Epoch dừng |
|---|---|---|---|---|---|---|---|---|---|
| V1: Concat đơn giản (không PSG, không CAD) | ✗ | ✗ | Plateau Heatmap | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| V2: Chỉ PSG | ✓ | ✗ | Plateau Heatmap | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| V3: Chỉ CAD | ✗ | ✓ | Plateau Heatmap | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| V4: PSG + CAD, Binary bbox | ✓ | ✓ | Binary bbox | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| **V5: PSG + CAD, Heatmap (đề xuất)** | ✓ | ✓ | Plateau Heatmap | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |

**Kết quả theo kịch bản Shift và Mixed 70/30:**

| Biến thể | Shift Dice | Shift HD95 | Mixed Dice | Mixed HD95 | Mixed CBL |
|---|---|---|---|---|---|
| V1 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| V2 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| V3 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| V4 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| **V5** | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |

**Visualization:** Xem ảnh minh họa 10 mẫu test đầu tại **03_Minh_Chung_Hinh_Anh — Mục C.Ablation**.

---

## D. Đánh Giá Theo Đặc Tính Tổn Thương

### D.1 PGA vs Baseline — Nhóm Dễ / Khó

| Nhóm | Mô hình | Dice | HD95 (px) | CBL |
|---|---|---|---|---|
| Dễ | U-Net | ⏳ | ⏳ | ⏳ |
| Dễ | Attention U-Net | ⏳ | ⏳ | ⏳ |
| **Dễ** | **PGA-UNet** | ⏳ | ⏳ | ⏳ |
| Khó | U-Net | ⏳ | ⏳ | ⏳ |
| Khó | Attention U-Net | ⏳ | ⏳ | ⏳ |
| **Khó** | **PGA-UNet** | ⏳ | ⏳ | ⏳ |

### D.2 PGA vs SAM-Med2D — 3 Nhóm Đặc Tính

| Nhóm | Mô hình | Dice | HD95 (px) | CBL |
|---|---|---|---|---|
| Tổn thương nhỏ | SAM-Med2D | ⏳ | ⏳* | ⏳ |
| **Tổn thương nhỏ** | **PGA-UNet** | ⏳ | ⏳ | ⏳ |
| Biên giới mờ | SAM-Med2D | ⏳ | ⏳* | ⏳ |
| **Biên giới mờ** | **PGA-UNet** | ⏳ | ⏳ | ⏳ |
| Tổn thương rõ nét | SAM-Med2D | ⏳ | ⏳* | ⏳ |
| **Tổn thương rõ nét** | **PGA-UNet** | ⏳ | ⏳ | ⏳ |

---

## E. Đánh Giá Độ Ổn Định (Cross-Validation)

> ⏳ **Chưa chạy** — train lại PGA với phân chia ngẫu nhiên mới (seed khác).

| Lần chạy | Seed | Dice ↑ | HD95 ↓ (px) | CBL ↑ |
|---|---|---|---|---|
| Lần 1 — Gốc (Zoom-out) | 42 | ⏳ | ⏳ | ⏳ |
| Lần 2 — Split mới | ⏳ | ⏳ | ⏳ | ⏳ |
| **Mean ± Std** | — | ⏳ | ⏳ | ⏳ |

---

## F. Thông Tin Huấn Luyện

| Mô hình | Epoch dừng | Best Val Dice | Ghi chú |
|---|---|---|---|
| U-Net | ⏳ | ⏳ | Early stop patience=15 |
| Attention U-Net | ⏳ | ⏳ | Early stop patience=15 |
| **PGA-UNet** | ⏳ | ⏳ | Early stop patience=15 |
| SAM-Med2D | ⏳ | ⏳ | Fine-tune từ pretrained ViT-B |

**Cấu hình chung:** IMG_SIZE=512 (PGA/baseline), 256 (SAM); Batch=4; AdamW; BCE+Dice loss; ReduceLROnPlateau.

---

# PHẦN II — ĐÓNG GÓP 2: Pipeline Lâm Sàng

## G. Kết Quả Mô Hình Phân Lớp Sàng Lọc (MobileNetV4)

| Độ đo | Giá trị |
|---|---|
| Độ chính xác tổng thể (Accuracy) | ⏳ |
| Độ chính xác (Precision / PPV) | ⏳ |
| Độ nhạy (Recall / Sensitivity) | ⏳ |
| Độ đặc hiệu (Specificity) | ⏳ |
| Giá trị dự báo Âm tính (NPV) | ⏳ |
| Điểm F1 | ⏳ |
| **AUC-ROC** | ⏳ |

---

## H. Kết Quả Cơ Chế Phòng Vệ GradCAM + IPR

> ⏳ **Chờ chạy lại** — cần checkpoint PGA mới sau khi train xong.

**Thực nghiệm:** Toàn bộ test samples có góc tối ≥70% (N=⏳), câu nhắc đặt vào góc tối.

| Nhóm theo Dice IPR k=1 | N | Dice trước | Dice k=1 | CBL k=1 |
|---|---|---|---|---|
| GradCAM tốt (D ≥ 0.90) | ⏳ | 0.000 | ⏳ | ⏳ |
| GradCAM khá (0.70 ≤ D < 0.90) | ⏳ | 0.000 | ⏳ | ⏳ |
| GradCAM trung bình (0.50 ≤ D < 0.70) | ⏳ | 0.000 | ⏳ | ⏳ |
| GradCAM yếu (D < 0.50) | ⏳ | 0.000 | ⏳ | ⏳ |
| **Tổng / Trung bình** | **⏳** | **0.000** | ⏳ | ⏳ |

- Tỷ lệ phát hiện: ⏳
- Cứu hộ thành công (Dice ≥ 0.70): ⏳

---

## I. Sai Số Tích Lũy Pipeline (Cascading Error)

**Ước tính lý thuyết (cập nhật sau khi có số mới):**

| Thành phần | Giá trị | Ý nghĩa |
|---|---|---|
| Recall MobileNetV4 | ⏳ | % ca bệnh bị bỏ sót ở bước sàng lọc |
| Dice PGA-UNet (Mixed 70/30) | ⏳ | Hiệu năng phân đoạn trên ca đã qua sàng lọc |
| **Hiệu năng tổng (ước tính)** | ⏳ | Bottleneck nằm ở phân lớp, không phải PGA |

> ⏳ Cập nhật sau khi có kết quả MobileNetV4 và PGA mới.
