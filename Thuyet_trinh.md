# Bài Thuyết Trình Khóa Luận Tốt Nghiệp
## PGA-UNet: Phân Đoạn Tổn Thương Xương Trên Ảnh X-Quang Với Hướng Dẫn Mềm Từ Câu Nhắc Không Gian

**Sinh viên:** Thong Luc  
**Thời lượng ước tính:** 15–20 phút

---

## SLIDE 1 — MỞ ĐẦU

Kính chào Hội đồng, kính thưa quý thầy cô.

Em xin phép trình bày khóa luận tốt nghiệp với đề tài:
**"Phân đoạn tổn thương xương trên ảnh X-quang với hướng dẫn mềm từ câu nhắc không gian"**

---

## SLIDE 2 — BỐI CẢNH VÀ ĐỘNG LỰC

Trong thực tế lâm sàng, bác sĩ chẩn đoán hình ảnh phải đọc và phân tích hàng trăm phim X-quang mỗi ngày — điển hình như Cambridge University Hospitals thực hiện hơn 174.000 ca chụp mỗi năm, tương đương 200–300 bệnh nhân mỗi ngày.

Khi nghi ngờ có tổn thương xương, bác sĩ cần **khoanh vùng chính xác** để đo kích thước, theo dõi diễn tiến và lập kế hoạch điều trị. Hiện tại việc này được thực hiện **thủ công** trên hệ thống PACS — tốn thời gian, phụ thuộc kinh nghiệm cá nhân và tiềm ẩn sai sót.

Các giải pháp phân đoạn hoàn toàn tự động (như U-Net) gặp khó khăn đặc thù với X-quang xương: độ tương phản thấp, cấu trúc giải phẫu chồng lấp, tổn thương trông gần giống mô lành. Kết quả: **Dice chỉ đạt 0.45** — không đủ tin cậy cho lâm sàng.

---

## SLIDE 3 — PHÁT BIỂU BÀI TOÁN

**Người dùng cuối:** Bác sĩ chẩn đoán hình ảnh (radiologist) làm việc trong ca đọc phim, sử dụng hệ thống PACS. Thao tác duy nhất họ cần thực hiện là **khoanh một hộp giới hạn** bao quanh vùng nghi ngờ.

**Bài toán (giai đoạn Online):**
- **Đầu vào:** Ảnh X-quang xương `I` + hộp giới hạn `B = (x1, y1, x2, y2)` do bác sĩ vẽ
- **Đầu ra:** Mặt nạ phân đoạn nhị phân `M̂` — pixel = 1 là vùng tổn thương

Yêu cầu then chốt: hệ thống phải **bền vững** trước sai lệch thực tế trong cách bác sĩ vẽ hộp — lệch tâm, kích thước không hoàn hảo.

---

## SLIDE 4 — KIẾN TRÚC HỆ THỐNG TỔNG THỂ

Hệ thống gồm hai module hoạt động tuần tự:

**Bước 1 — Sàng lọc tự động (Gatekeeper):**
- Ảnh X-quang đi qua **EfficientNet\_B3** (~12M tham số, pretrained ImageNet)
- Tính xác suất bệnh lý p̂ ∈ [0,1]
- Nếu p̂ < 0.5: dừng, báo "bình thường"
- Nếu p̂ ≥ 0.5: chuyển sang Bước 2

**Bước 2 — Phân đoạn có hướng dẫn (PGA-UNet):**
- Bác sĩ khoanh hộp giới hạn B
- Hệ thống chuyển B → Bản đồ nhiệt câu nhắc H (Prompt Heatmap)
- PGA-UNet nhận cặp (ảnh, heatmap) → xuất mặt nạ phân đoạn M̂

Triết lý thiết kế: **human-in-the-loop** — tự động hoá sàng lọc, trao quyền định hướng không gian cho bác sĩ.

---

## SLIDE 5 — ĐÓNG GÓP CHÍNH: HƯỚNG DẪN MỀM QUA PROMPT HEATMAP

Đây là đóng góp kỹ thuật trọng tâm của khóa luận.

**Vấn đề với các cách biểu diễn hiện có:**
- **SAM / SAM-Med2D:** mã hóa hộp thành vector rời rạc 256 chiều → mất thông tin không gian 2D, khó tích hợp vào U-Net CNN
- **Mặt nạ nhị phân phẳng:** đường biên sắc nét tạo gradient giả → mô hình học bám theo biên hộp thay vì biên tổn thương thực

**Giải pháp đề xuất — Plateau Heatmap:**
- Vùng trong hộp: giá trị = 1.0 (plateau đồng đều)
- Làm mềm biên bằng Gaussian blur (kernel 31×31)
- Kết quả: kênh ảnh H ∈ [0,1]^(H×W) đi **song hành** cùng ảnh X-quang vào toàn bộ mạng

**Tại sao hiệu quả:** Tín hiệu liên tục không có đường biên sắc nét → mô hình không thể "ghi nhớ" vị trí tâm hộp → khi bác sĩ vẽ lệch, mô hình vẫn tìm được tổn thương đúng.

**Bằng chứng (ablation study V4 vs V5):**
- Binary prompt → Dice Shift = 0.7378
- Gaussian Heatmap → Dice Shift = **0.8382** (+0.1004, tăng 13.6%)

---

## SLIDE 6 — KIẾN TRÚC PGA-UNET

PGA-UNet là kiến trúc U-Net nhẹ (~3M tham số) được thiết kế để khai thác tín hiệu heatmap liên tục.

**Tại Encoder — Prompt Spatial Gate (PSG):**

Tại tầng encoder thứ l:
```
x̃^l = x^l ⊙ (1 + α · σ(W_gate * H^l))
```
- Khuếch đại đặc trưng trong vùng câu nhắc (nhân với hệ số > 1)
- Không triệt tiêu vùng ngoài (vẫn nhân ≈ 1) → bảo toàn thông tin toàn cục
- α là tham số học được, khởi tạo 0.1 để ổn định giai đoạn đầu

**Tại Decoder — Conditioned Attention (CAD):**

Tín hiệu gating được điều kiện hóa bằng câu nhắc:
```
g' = g + c · α · w_l · p_enc
```
- c: điểm tin cậy câu nhắc (học được qua GAP)
- w_l: hệ số tỷ lệ giảm dần theo tầng (chi tiết triển khai)
- Câu nhắc tham gia ở mức định hướng ngữ nghĩa, giảm dần khi tái tạo chi tiết biên

**So sánh với SAM:** SAM dùng transformer + positional embedding rời rạc. PGA dùng CNN + heatmap 2D — phù hợp tự nhiên với kiến trúc feature map không gian.

---

## SLIDE 7 — KẾT QUẢ: SO SÁNH BASELINE

Đánh giá trên tập kiểm thử 232 mẫu per-polygon, bộ dữ liệu BTXRD.

| Mô hình | Dice ↑ | IoU ↑ | HD95 ↓ |
|---|---|---|---|
| U-Net (tự động) | 0.4534 | 0.3671 | 128.61 |
| Attention U-Net (tự động) | 0.4159 | 0.3306 | 132.86 |
| **PGA-UNet Zoom-out** | **0.8524** | **0.7527** | **13.96** |

**Quan sát:** Attention U-Net thậm chí tệ hơn U-Net — khi không có tín hiệu định hướng, cơ chế attention tự do khuếch đại nhiễu (bờ khớp xương, dị vật) thay vì tổn thương. Điều này chứng minh attention chỉ phát huy khi được "neo" bởi prompt rõ ràng.

---

## SLIDE 8 — KẾT QUẢ: SO SÁNH VỚI SAM-Med2D

| Mô hình | Kịch bản | Dice ↑ | Params |
|---|---|---|---|
| PGA-UNet | Zoom-out | **0.8524** | ~3M |
| PGA-UNet | Shift | **0.8382** | ~3M |
| PGA-UNet | Mixed | **0.8496** | ~3M |
| SAM-Med2D (fine-tuned) | Zoom-out | 0.7350 | ~91M |
| SAM-Med2D (fine-tuned) | Shift | 0.7097 | ~91M |
| SAM-Med2D (zero-shot) | Zoom-out | 0.5337 | ~91M |

**PGA-UNet vượt SAM-Med2D fine-tuned ~12–13 điểm Dice** với số tham số nhỏ hơn **30 lần**, huấn luyện hoàn toàn từ đầu trên BTXRD — không cần pretrained quy mô lớn.

---

## SLIDE 9 — KẾT QUẢ: ABLATION STUDY

| Biến thể | PSG | CAD | Prompt | Dice Zoom ↑ | Dice Shift ↑ | Dice Mixed ↑ |
|---|---|---|---|---|---|---|
| V1: Baseline concat | ✗ | ✗ | Gaussian | 0.8718 | 0.7201 | 0.8158 |
| V2: PSG only | ✓ | ✗ | Gaussian | 0.8643 | 0.7291 | 0.8146 |
| V3: CAD only | ✗ | ✓ | Gaussian | 0.8827 | 0.7335 | 0.8256 |
| V4: Full + Binary | ✓ | ✓ | Binary | 0.8800 | 0.7378 | 0.8276 |
| **V5: Full + Gaussian** | ✓ | ✓ | **Gaussian** | 0.8524 | **0.8382** | **0.8496** |

**Phát hiện quan trọng nhất:** V4→V5 (chỉ thay Binary → Gaussian):
- Dice Shift **+0.1004** (+13.6%)
- Dice Mixed **+0.0220** (+2.7%)
- Dice Zoom-out giảm nhẹ -0.0276 — **trade-off có chủ đích** để đổi lấy robustness

---

## SLIDE 10 — KẾT QUẢ: TÍNH BỀN VỮNG VÀ ĐỘ ỔN ĐỊNH

**Cross-validation 4-fold (trung bình ± độ lệch chuẩn):**

| Kịch bản | Dice | IoU | HD95 |
|---|---|---|---|
| Zoom-out | 0.8784 ± 0.0019 | 0.7897 | 10.29 |
| Shift | 0.8522 ± 0.0099 | 0.7522 | 12.60 |
| Mixed | 0.8723 ± 0.0035 | 0.7807 | 10.91 |

Độ lệch chuẩn rất thấp (±0.002 đến ±0.010) xác nhận mô hình ổn định, không phụ thuộc cách phân chia dữ liệu.

**Sub-category analysis — nhóm "Khó" (bottom-50 U-Net Dice):**
- U-Net: Dice = **0.0000** (sụp đổ hoàn toàn)
- Attention U-Net: Dice = 0.0929
- PGA-UNet: Dice = **0.8181** (duy trì ổn định)

---

## SLIDE 11 — KẾT QUẢ: PIPELINE END-TO-END

**Module Gatekeeper (EfficientNet\_B3):**

| Độ đo | Kết quả |
|---|---|
| Accuracy | 85.60% |
| Precision | 91.30% |
| Recall / Sensitivity | 78.61% |
| Specificity | 92.55% |
| AUC-ROC | 0.9258 |

**Pipeline tổng thể (luồng hỗn hợp bình thường + bệnh lý):**
- Pipeline Dice = **0.7296** trên 264 đơn vị (226 TP polygon + 38 FP)
- Bottleneck: Specificity 79.79% → 38 ảnh bình thường bị phân loại sai gán Dice = 0
- Cải thiện Specificity là hướng phát triển ưu tiên

---

## SLIDE 12 — KẾT LUẬN VÀ HẠN CHẾ

**Những gì đã đạt được:**
1. Đề xuất và kiểm chứng phương pháp **hướng dẫn mềm qua Gaussian Heatmap** — biểu diễn câu nhắc liên tục 2D giúp mô hình bền vững trước sai số câu nhắc (+0.10 Dice Shift so với binary)
2. PGA-UNet (~3M params) vượt SAM-Med2D (~91M params) trên bộ BTXRD, chứng minh kiến trúc chuyên biệt hiệu quả hơn foundation model đa mục đích trên domain hẹp
3. Đánh giá end-to-end pipeline lâm sàng thực tế (không chỉ đánh giá phân đoạn đơn lẻ)

**Hạn chế thừa nhận:**
- Chưa ablate lịch trình trọng số decoder (giảm dần vs cố định vs tăng dần) — đang thực hiện thực nghiệm bổ sung (V6, V7, V8)
- Bounding box đánh giá được sinh tự động, chưa có user study với bác sĩ thực
- Chỉ kiểm chứng trên bộ BTXRD (X-quang chi), chưa đánh giá khả năng tổng quát hóa sang domain khác
- Specificity của Gatekeeper (79.79%) cần cải thiện để giảm FP trong pipeline

**Hướng phát triển:**
- Hoàn thiện ablation V6/V7/V8 về lịch trình trọng số
- Thu thập 50+ ca bác sĩ thực vẽ hộp để đánh giá robustness thực tế
- Kiểm chứng trên bộ dữ liệu X-quang xương thứ hai

---

## SLIDE 13 — KẾT THÚC

Kính thưa Hội đồng,

Khóa luận này đề xuất một hướng tiếp cận cụ thể và có kiểm chứng để hỗ trợ bác sĩ chẩn đoán hình ảnh: thay vì cố gắng thay thế phán đoán của bác sĩ, hệ thống **đặt bác sĩ vào vị trí kiểm soát** và chuyển thao tác đơn giản nhất — khoanh một hộp — thành kết quả phân đoạn có độ chính xác cao.

**Câu hỏi cốt lõi mà khóa luận trả lời:** Cần biểu diễn tín hiệu định hướng của bác sĩ như thế nào để mô hình vừa chính xác vừa bền vững trong điều kiện thực tế?

Câu trả lời: **Liên tục và có gradient — không phải rời rạc hay nhị phân.**

Em xin trân trọng cảm ơn Hội đồng và kính mời thầy cô đặt câu hỏi.

---

## PHỤ LỤC — CÂU HỎI PHẢN BIỆN THƯỜNG GẶP

### Q1: Tại sao không dùng binary mask thay vì Gaussian Heatmap?
**A:** Binary mask tạo gradient giả tại đường biên → mạng học bám biên hộp thay vì biên tổn thương. Gaussian Heatmap cung cấp tín hiệu liên tục, mô hình không thể "ghi nhớ" biên hộp. Ablation V4→V5 chứng minh: +0.1004 Dice Shift.

### Q2: Lịch trình w_l = {1.0, 0.7, 0.4, 0.2} dựa trên cơ sở nào?
**A:** Đây là siêu tham số triển khai được xác định thực nghiệm trên tập xác thực. Hướng giảm dần có cơ sở trực giác (tầng phân giải cao cần tự do tái tạo chi tiết biên hơn là bị ép bởi bounding box thô), nhưng em chưa có ablation so sánh giảm dần vs cố định vs tăng dần. Thực nghiệm bổ sung đang được thực hiện (V6, V7, V8).

### Q3: Tại sao PGA-UNet 3M params vượt SAM-Med2D 91M params?
**A:** SAM-Med2D là foundation model đa mục đích — pretrain trên 4.6M ảnh y tế đa dạng nhưng không đặc thù cho X-quang xương. PGA-UNet được thiết kế và huấn luyện chuyên biệt cho bài toán này. Trên domain hẹp với dữ liệu đặc thù, mô hình chuyên biệt thường vượt mô hình đa mục đích dù nhỏ hơn nhiều lần. Ngoài ra SAM dùng resolution 256×256, PGA dùng 512×512 — SAM mất chi tiết trên ảnh X-quang.

### Q4: Bounding box do bác sĩ vẽ có thực sự lệch bao nhiêu?
**A:** Em mô phỏng bằng Shift ngẫu nhiên trên bộ test, chưa có user study với bác sĩ thực. Đây là hạn chế được thừa nhận. Nếu có thêm thời gian, ưu tiên thu thập 50+ ca bác sĩ thực vẽ để đánh giá distribution sai lệch thực tế.

### Q5: Tại sao Attention U-Net lại tệ hơn cả U-Net?
**A:** Khi không có tín hiệu định hướng, cổng chú ý tự do dễ bị kích hoạt bởi vùng có gradient mạnh không phải tổn thương (bờ khớp xương, thiết bị cố định). Attention khi đó khuếch đại nhiễu thay vì tổn thương. Tuy nhiên em thừa nhận kết quả này cũng có thể do chưa tối ưu siêu tham số cho Attention U-Net trên BTXRD — cần thêm thực nghiệm để khẳng định.
