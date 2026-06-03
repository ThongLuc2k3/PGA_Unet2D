# Minh Chứng Số Liệu

> **Lưu ý:** Đề tài có hai đóng góp tách biệt. Số liệu Đóng góp 1 đánh giá PGA-UNet thuần túy (không qua MobileNetV4) — đây là số sạch để so sánh công bằng với SAM. Số liệu Đóng góp 2 đánh giá pipeline lâm sàng hoàn chỉnh và thừa nhận sai số tích lũy.
>
> ⏳ = số liệu đang chờ kết quả thực nghiệm bổ sung

---

# PHẦN I — ĐÓNG GÓP 1: Kiến Trúc PGA-UNet

## A. Kết Quả Phân Đoạn Tổng Hợp (N=248 test samples, BTXRD)

| Mô hình | Kịch bản | Dice ↑ | IoU ↑ | Độ chính xác ↑ | Độ bao phủ ↑ | HD95 ↓ (px) | CBL ↑ |
|---|---|---|---|---|---|---|---|
| U-Net (không có câu nhắc) | — | 0.5090 | 0.4125 | 0.6686 | 0.5235 | 125.12 | 0.6457 |
| Attention U-Net (không có câu nhắc) | — | 0.4110 | 0.3212 | 0.6261 | 0.4035 | 141.23 | 0.5917 |
| SAM-Med2D (zero-shot) | Zoom-out | 0.5298 | 0.3867 | 0.4703 | 0.6794 | 111.27* | 0.8199 |
| SAM-Med2D (zero-shot) | **Shift** | 0.5203 | 0.3763 | 0.4629 | 0.6665 | 115.55* | 0.8001 |
| SAM-Med2D (zero-shot) | Mixed 70/30 | 0.5289 | 0.3853 | 0.4687 | 0.6786 | 114.31* | 0.8125 |
| SAM-Med2D (fine-tuned) | Zoom-out | 0.7624 | 0.6424 | 0.7597 | 0.7880 | 52.08* | 0.9003 |
| SAM-Med2D (fine-tuned) | **Shift** | 0.7273 | 0.5983 | 0.7318 | 0.7496 | 54.44* | 0.8834 |
| SAM-Med2D (fine-tuned) | Mixed 70/30 | 0.7554 | 0.6325 | 0.7558 | 0.7813 | 51.84* | 0.8997 |
| **PGA-UNet (đề xuất)** | Zoom-out | **0.8606** | **0.7619** | **0.8479** | **0.8897** | **12.16** | **0.9558** |
| **PGA-UNet (đề xuất)** | Shift | **0.8380** | **0.7301** | **0.8331** | **0.8616** | **14.36** | **0.9388** |
| **PGA-UNet (đề xuất)** | Mixed 70/30 | **0.8558** | **0.7552** | **0.8428** | **0.8862** | **12.79** | **0.9532** |

> `*` HD95 của SAM-Med2D tính trên không gian ảnh 256×256 px. HD95 chuẩn hóa: PGA ≈ 0.025 vs SAM ≈ 0.204 — PGA chính xác hơn ~8× về đường biên.  
> U-Net/Att-UNet: N=187 (merged mask). PGA/SAM: N=248 (per-polygon).

**Ba kịch bản câu nhắc:**
- **Zoom-out**: câu nhắc lý tưởng bao quanh hoàn toàn tổn thương (+30%)
- **Shift**: câu nhắc bị dịch lệch ngẫu nhiên — mô phỏng thao tác không chính xác
- **Mixed 70/30**: 70% Zoom-out + 30% Shift — **kịch bản thực tế nhất**

---

## B. Ablation — Đóng Góp Từng Loại Câu Nhắc

> Giữ nguyên kiến trúc PGA-UNet đầy đủ, chỉ thay đổi loại câu nhắc đầu vào tại suy luận.

| Cấu hình câu nhắc | Dice ↑ | IoU ↑ | HD95 ↓ (px) | CBL ↑ |
|---|---|---|---|---|
| PGA + Câu nhắc rỗng | 0.0005 | 0.0002 | 501.51 | 0.0214 |
| PGA + Câu nhắc nhiễu ngẫu nhiên | 0.0015 | 0.0008 | 495.84 | 0.0208 |
| SAM-Med2D (fine-tuned, hard bbox) | 0.7624 | 0.6424 | 52.08* | 0.9003 |
| PGA + Hard binary bbox | 0.8593 | 0.7604 | 12.14 | 0.9572 |
| **PGA + Plateau Heatmap (triển khai)** | **0.8298** | **0.7184** | **14.25** | **0.9524** |
| PGA + Oracle (GT mask làm câu nhắc) | 0.5683 | 0.4076 | 24.26 | 0.9479 |

**Phân tích đóng góp từng thành phần:**
- **Δ_location +0.859**: câu nhắc vị trí là đóng góp cốt lõi — không có câu nhắc, PGA-UNet sụp đổ hoàn toàn
- **Δ_arch-SAM +0.097**: PSG+CAD (~4M tham số) vượt SAM-Med2D (~100M) khi cùng loại câu nhắc
- **Δ_soft −0.030**: Plateau Heatmap kém hơn hard bbox một chút nhưng cho đường biên mượt hơn
- **Oracle < hard bbox**: câu nhắc GT mask nằm ngoài phân phối huấn luyện → mô hình không nhận diện được

---

## C. Ablation — Đóng Góp Từng Thành Phần Kiến Trúc (V1–V5)

> Đánh giá trên kịch bản **Zoom-out** (N=248 test). Số liệu V1–V4 từ thực nghiệm Kaggle. V5 dùng checkpoint PGA gốc — sẽ cập nhật khi train lại hoàn tất.

| Biến thể | PSG | CAD | Loại câu nhắc | Dice ↑ | IoU ↑ | HD95 ↓ (px) | CBL ↑ | Best Val Dice | Epoch dừng |
|---|---|---|---|---|---|---|---|---|---|
| V1: Concat đơn giản (không PSG, không CAD) | ✗ | ✗ | Plateau Heatmap | 0.8722 | 0.7796 | 12.01 | 0.9666 | 0.8750 | 55/100 |
| V2: Chỉ PSG | ✓ | ✗ | Plateau Heatmap | 0.8707 | 0.7791 | 14.95 | 0.9610 | 0.8765 | 92/100 |
| V3: Chỉ CAD | ✗ | ✓ | Plateau Heatmap | 0.8864 | 0.8018 | 11.46 | 0.9685 | 0.9006 | 64/100 |
| V4: PSG + CAD, Binary bbox | ✓ | ✓ | Binary bbox | 0.8802 | 0.7909 | 11.45 | 0.9649 | 0.8913 | 67/100 |
| **V5: PSG + CAD, Heatmap (đề xuất)** | ✓ | ✓ | Plateau Heatmap | **0.8606** | **0.7619** | **12.16** | **0.9558** | 0.8652 | 60/100 |

**Kết quả theo kịch bản Shift và Mixed 70/30:**

| Biến thể | Shift Dice | Shift HD95 | Mixed Dice | Mixed HD95 | Mixed CBL |
|---|---|---|---|---|---|
| V1 | 0.7210 | 22.00 | 0.8222 | 15.23 | 0.9351 |
| V2 | 0.7285 | 24.40 | 0.8240 | 17.93 | 0.9310 |
| V3 | 0.7247 | 21.89 | 0.8337 | 14.81 | 0.9368 |
| V4 | 0.7321 | 20.88 | 0.8321 | 14.55 | 0.9352 |
| **V5** | **0.8380** | **14.36** | **0.8558** | **12.79** | **0.9532** |

> **Nhận xét:** V3 (CAD only) đạt Dice cao nhất trên zoom_out (0.8864) do CAD cung cấp attention decoder mạnh. V5 vượt trội rõ ở kịch bản Shift (+11.6pp so V4) — PSG+CAD+Heatmap giúp mô hình ổn định hơn khi prompt bị lệch, đây là ưu thế chính của kiến trúc đề xuất.

**Visualization:** Xem ảnh minh họa 10 mẫu test đầu tại **03_Minh_Chung_Hinh_Anh — Mục C.Ablation**.

---

## D. Đánh Giá Theo Đặc Tính Tổn Thương

### D.1 PGA vs Baseline — Nhóm Dễ / Khó

| Nhóm | Mô hình | Dice | HD95 (px) | CBL |
|---|---|---|---|---|
| Dễ (N=131) | U-Net | 0.7902 | 40.05 | 0.9156 |
| Dễ (N=131) | Attention U-Net | 0.5830 | 79.90 | 0.7570 |
| **Dễ (N=131)** | **PGA-UNet** | **0.8632** | **13.59** | **0.9569** |
| Khó (N=140) | U-Net | 0.2379 | 207.21 | 0.4005 |
| Khó (N=140) | Attention U-Net | 0.2266 | 208.65 | 0.4169 |
| **Khó (N=140)** | **PGA-UNet** | **0.8521** | **12.23** | **0.9536** |

> Nhóm **Khó**: U-Net/Att-UNet sụp đổ (Dice ≈ 0.23), PGA duy trì 0.8521 (+61.4%).

### D.2 PGA vs SAM-Med2D — 3 Nhóm Đặc Tính

| Nhóm | Mô hình | Dice | HD95 (px) | CBL |
|---|---|---|---|---|
| Tổn thương nhỏ (N=50) | SAM-Med2D | 0.2518 | 181.46* | 0.5484 |
| **Tổn thương nhỏ (N=50)** | **PGA-UNet** | **0.8166** | **3.03** | **0.9359** |
| Biên giới mờ (N=50) | SAM-Med2D | 0.4583 | 43.34* | 0.8307 |
| **Biên giới mờ (N=50)** | **PGA-UNet** | **0.8246** | **15.95** | **0.9454** |
| Tổn thương rõ nét (N=50) | SAM-Med2D | 0.8521 | 26.23* | 0.9530 |
| **Tổn thương rõ nét (N=50)** | **PGA-UNet** | **0.8945** | **21.76** | **0.9661** |

---

## E. Đánh Giá Độ Ổn Định (Cross-Validation)

> ⏳ **Chưa chạy** — train lại PGA với phân chia ngẫu nhiên mới (seed khác).

| Lần chạy | Seed | Dice ↑ | HD95 ↓ (px) | CBL ↑ |
|---|---|---|---|---|
| Lần 1 — Gốc (Zoom-out) | 42 | 0.8606 | 12.16 | 0.9558 |
| Lần 2 — Split mới | ⏳ | ⏳ | ⏳ | ⏳ |
| **Mean ± Std** | — | ⏳ | ⏳ | ⏳ |

---

## F. Thông Tin Huấn Luyện

| Mô hình | Epoch dừng | Best Val Dice | Ghi chú |
|---|---|---|---|
| U-Net | 82/100 | 0.5345 | Early stop patience=15 |
| Attention U-Net | 47/100 | 0.4364 | Early stop patience=15 |
| **PGA-UNet** | **60/100** | **0.8652** | Early stop patience=15 |
| SAM-Med2D | 12/50 | 0.7731 | Hội tụ nhanh nhờ pretrained ViT-B |

**Cấu hình chung:** IMG_SIZE=512 (PGA/baseline), 256 (SAM); Batch=4; AdamW; BCE+Dice loss; ReduceLROnPlateau.

---

# PHẦN II — ĐÓNG GÓP 2: Pipeline Lâm Sàng

## G. Kết Quả Mô Hình Phân Lớp Sàng Lọc (MobileNetV4)

| Độ đo | Giá trị |
|---|---|
| Độ chính xác tổng thể (Accuracy) | 85.77% |
| Độ chính xác (Precision / PPV) | 83.11% |
| Độ nhạy (Recall / Sensitivity) | **89.64%** |
| Độ đặc hiệu (Specificity) | 81.91% |
| Giá trị dự báo Âm tính (NPV) | 88.85% |
| Điểm F1 | 86.25% |
| **AUC-ROC** | **0.9514** |

> Recall = 89.64% là chỉ số ưu tiên: ~90% ca bệnh được bắt, không bỏ sót vào phân đoạn.

---

## H. Kết Quả Cơ Chế Phòng Vệ GradCAM + IPR

> ⏳ **Đang xem xét chạy lại** — số liệu bên dưới từ lần chạy trước, sẽ cập nhật.

**Thực nghiệm:** 174 ảnh, câu nhắc đặt vào góc tối (≥70% vùng câu nhắc là vùng tối).

| Nhóm theo Dice IPR k=1 | N | Dice trước | Dice k=1 | CBL k=1 |
|---|---|---|---|---|
| GradCAM tốt (D ≥ 0.90) | 9 | 0.000 | 0.922 | 0.961 |
| GradCAM khá (0.70 ≤ D < 0.90) | 29 | 0.000 | 0.807 | 0.918 |
| GradCAM trung bình (0.50 ≤ D < 0.70) | 19 | 0.000 | 0.598 | 0.811 |
| GradCAM yếu (D < 0.50) | 117 | 0.000 | 0.018 | 0.066 |
| **Tổng / Trung bình** | **174** | **0.000** | **0.260** | **0.298** |

- Tỷ lệ phát hiện: **174/174 = 100%**
- Cứu hộ thành công (Dice ≥ 0.70): **38/174 = 21.8%**
- SAM-Med2D: 100% phát hiện khi áp cùng tiêu chí, CBL=0.497 (tốt hơn PGA) nhưng **không có pipeline cứu hộ tích hợp**

---

## I. Sai Số Tích Lũy Pipeline (Cascading Error)

**Ước tính lý thuyết:**

$$\text{Hiệu năng tổng} \approx \text{Recall}_\text{MobileNetV4} \times \text{Dice}_\text{PGA} = 89.64\% \times 85.58\% \approx \mathbf{76.7\%}$$

| Thành phần | Giá trị | Ý nghĩa |
|---|---|---|
| Recall MobileNetV4 | 89.64% | 10.36% ca bệnh bị bỏ sót ở bước sàng lọc |
| Dice PGA-UNet (Mixed 70/30) | 85.58% | Hiệu năng phân đoạn trên ca đã qua sàng lọc |
| **Hiệu năng tổng (ước tính)** | **~76.7%** | Bottleneck nằm ở phân lớp, không phải PGA |

> ⏳ **Xác minh thực nghiệm đang chuẩn bị** — chạy full pipeline trên tập hỗn hợp (có bệnh + không bệnh).  
> **Lý giải:** hệ thống Human-in-the-loop — bác sĩ xác nhận trước khi phân đoạn, nên 10.36% bỏ sót vẫn có cơ hội được phát hiện thủ công.
