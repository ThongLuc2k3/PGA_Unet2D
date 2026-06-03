# Minh Chứng Hình Ảnh

> Tất cả ảnh nằm trong thư mục `images/` cùng cấp với file này (21 file PNG).

---

## Tổng Quan Ảnh

| File | Nhóm | Nội dung |
|---|---|---|
| `system_architecture.png` | Hệ thống | Sơ đồ tổng thể 4 giai đoạn pipeline |
| `preprocessing_pipeline.png` | Hệ thống | Quy trình tiền xử lý 6 bước |
| `diagram_pga.png` | Kiến trúc | PGA-UNet với PSG + CAD |
| `diagram_unet.png` | Kiến trúc | U-Net baseline |
| `diagram_attunet.png` | Kiến trúc | Attention U-Net |
| `diagram_sammed2d.png` | Kiến trúc | SAM-Med2D (ViT-B + Adapter) |
| `vis_pga_1.png` | Kết quả PGA | IMG001768 — Zoom-out vs Shift |
| `vis_pga_2.png` | Kết quả PGA | IMG001538 — Pipeline cứu hộ GradCAM+IPR |
| `vis_pga_3.png` | Kết quả PGA | IMG001100 — Tổn thương lớn |
| `gradcam_ipr_rescue_1.png` | GradCAM Rescue | Minh họa 174 mẫu câu nhắc sai — nhóm 1 |
| `gradcam_ipr_rescue_2.png` | GradCAM Rescue | Minh họa 174 mẫu câu nhắc sai — nhóm 2 |
| `defense_pga_rescue_vis.png` | So sánh phòng vệ | PGA GradCAM rescue vs Ground Truth |
| `defense_sam_dark_corner.png` | So sánh phòng vệ | SAM-Med2D với câu nhắc góc tối — không có cứu hộ |
| `vis_sam_1.png` | Kết quả SAM | IMG001768 — 3 kịch bản |
| `vis_sam_2.png` | Kết quả SAM | IMG001538 |
| `vis_unet_1.png` | Kết quả baseline | U-Net — over-segmentation |
| `vis_unet_2.png` | Kết quả baseline | U-Net — mẫu bổ sung |
| `vis_attunet_1.png` | Kết quả baseline | Attention U-Net — attention khuếch đại nhiễu |
| `vis_attunet_2.png` | Kết quả baseline | Attention U-Net — mặt nạ lệch hoàn toàn |
| `classification_evaluation.png` | Phân lớp | Confusion matrix + ROC AUC=0.9514 |
| `app_interface.png` | Ứng dụng | Giao diện Gradio end-to-end |

---

## A. Sơ Đồ Hệ Thống Tổng Thể

### A.0 Kiến trúc pipeline 4 giai đoạn
**File:** `images/system_architecture.png`

Luồng xử lý end-to-end: Tiền xử lý (YOLOv11 xóa nhiễu) → Sàng lọc (MobileNetV4) → Phân đoạn có hướng dẫn (PGA-UNet) → Thẩm định an toàn (GradCAM + IPR). Minh họa cả hai kịch bản: câu nhắc hợp lệ (luồng thường) và câu nhắc sai (luồng cứu hộ).

### A.0b Quy trình tiền xử lý 6 bước
**File:** `images/preprocessing_pipeline.png`

Từ ảnh JPEG thô → xóa ICC Profile → gán nhãn nhiễu trên Roboflow → huấn luyện YOLOv11s → phát hiện và xóa nhiễu R/L bằng inpainting → chuẩn hóa thang xám → resize 512×512.

---

## A. Sơ Đồ Kiến Trúc

### A.1 Kiến trúc PGA-UNet đề xuất
**File:** `images/diagram_pga.png`

Minh họa hai thành phần đóng góp chính:
- **Prompt Spatial Gate (PSG):** tích hợp bản đồ nhiệt câu nhắc vào bộ mã hóa qua phép nhân có chọn lọc
- **Conditioned Attention Decoder (CAD):** điều kiện hóa tín hiệu gating bằng câu nhắc tại từng tầng giải mã, trọng số giảm dần

### A.2 Kiến trúc U-Net cơ sở
**File:** `images/diagram_unet.png`

Nền tảng encoder-decoder đối xứng với kết nối tắt — cả 4 mô hình đều dựa trên kiến trúc này.

### A.3 Kiến trúc Attention U-Net
**File:** `images/diagram_attunet.png`

Cổng chú ý (Attention Gate) tại kết nối tắt — tiền đề cho Conditioned Attention của PGA-UNet.

### A.4 Kiến trúc SAM-Med2D (mô hình so sánh)
**File:** `images/diagram_sammed2d.png`

ViT-B Image Encoder + Adapter layers + Mask Decoder — ~100M tham số, fine-tune từ 4M+ ảnh y tế.

---

## B. Kết Quả Phân Loại Sàng Lọc (MobileNetV4)

**File:** `images/classification_evaluation.png`

Bao gồm: (a) Ma trận nhầm lẫn, (b) Đường cong ROC (AUC=0.9514), (c) Phân phối xác suất dự đoán.

---

## C. Kết Quả Phân Đoạn — PGA-UNet

### C.1 Mẫu IMG001768 (Kịch bản Zoom-out và Shift)
**File:** `images/vis_pga_1.png`

Hàng trên: Zoom-out (câu nhắc lý tưởng) — Hàng dưới: Shift (câu nhắc lệch tâm).  
Các cột: Ảnh gốc | Prompt heatmap | Ground Truth | Dự đoán | Overlay.  
Minh chứng tính bền bỉ: Dice giảm nhẹ từ 0.8606 (Zoom-out) xuống 0.8380 (Shift) — chỉ −2.6%.

### C.2 Mẫu IMG001538 (Pipeline cứu hộ GradCAM + IPR)
**File:** `images/vis_pga_2.png`

Minh họa chuỗi hành động khi câu nhắc hoàn toàn sai vị trí:
1. Phát hiện → từ chối → kích hoạt GradCAM
2. GradCAM trích xuất điểm neo cứu hộ
3. IPR vòng 1 → mặt nạ thô bám vùng tổn thương
4. IPR vòng 2 → mặt nạ hội tụ, bám sát Ground Truth

### C.3 Mẫu IMG001100 (Tổn thương lớn vùng đùi)
**File:** `images/vis_pga_3.png`

PGA-UNet phân đoạn chính xác tổn thương lớn ở cả kịch bản Zoom-out và Shift.

---

## D. Kết Quả Phân Đoạn — SAM-Med2D (So Sánh)

### D.1 Mẫu IMG001768 — 3 kịch bản prompt
**File:** `images/vis_sam_1.png`

3 hàng: Zoom-out / Shift / Mixed 70/30 — 4 cột: Bbox prompt | Ground Truth | SAM prediction | Overlay.  
Dice(Zoom-out)=0.7624, Dice(Shift)=0.7273 — thấp hơn PGA ở cả 3 kịch bản.

### D.2 Mẫu IMG001538 — Hạn chế độ phân giải 256×256
**File:** `images/vis_sam_2.png`

Minh chứng hạn chế của SAM-Med2D trên cấu trúc xương nhỏ: tổn thương bị mờ, bỏ sót nhiều ở độ phân giải 256px.

---

## E. Kết Quả Phân Đoạn — Baseline (U-Net, Attention U-Net)

### E.1 U-Net — Phân đoạn sai khi không có câu nhắc
**File:** `images/vis_unet_1.png` và `images/vis_unet_2.png`

Minh họa hiện tượng over-segmentation và nhầm lẫn cấu trúc xương khi mô hình tự tìm kiếm vùng tổn thương không có hướng dẫn.

### E.2 Attention U-Net — Attention khuếch đại nhiễu
**File:** `images/vis_attunet_1.png` và `images/vis_attunet_2.png`

Attention Gate khuếch đại sai vùng (thiết bị cố định xương, bờ khớp) khi không có tín hiệu định hướng — dẫn đến Dice thấp hơn cả U-Net cơ sở.

---

## F. Minh Chứng Cơ Chế Phòng Vệ (Đóng Góp 2)

### F.1 GradCAM Rescue — Các mẫu thực nghiệm
**File:** `images/gradcam_ipr_rescue_1.png` và `images/gradcam_ipr_rescue_2.png`

Kết quả thực nghiệm trên 174 mẫu câu nhắc sai hoàn toàn (đặt vào góc tối ≥70% đen). Mỗi hàng là một mẫu, hiển thị: ảnh gốc + câu nhắc sai | bản đồ nhiệt GradCAM | mặt nạ sau IPR k=1 | Ground Truth. Minh chứng trực quan cho tỷ lệ phát hiện 100% và cơ chế cứu hộ bán tự động.

### F.2 So sánh phòng vệ: PGA vs SAM-Med2D
**File:** `images/defense_pga_rescue_vis.png`

PGA-UNet khi nhận câu nhắc góc tối: từ chối → GradCAM → IPR → xuất mặt nạ gợi ý. Kết quả GradCAM CBL=0.298, cứu hộ thành công 21.8% ca.

**File:** `images/defense_sam_dark_corner.png`

SAM-Med2D khi nhận **cùng câu nhắc góc tối**: không có kiểm duyệt, trả về mặt nạ sai im lặng. GradCAM CBL=0.497 (tốt hơn PGA về định vị) nhưng **không có pipeline cứu hộ tích hợp** — đây là khoảng trống mà Đóng góp 2 lấp đầy.

---

## G. Ứng Dụng Tích Hợp

### G.1 Giao diện Gradio (app.py)
**File:** `images/app_interface.png`

Giao diện end-to-end: bác sĩ tải ảnh X-quang → MobileNetV4 phân lớp tự động → vẽ hộp giới hạn → PGA-UNet phân đoạn → hiển thị mặt nạ kèm bản đồ nhiệt GradCAM. Kịch bản câu nhắc sai: hệ thống tự động hiển thị "Mặt nạ gợi ý" song song.
