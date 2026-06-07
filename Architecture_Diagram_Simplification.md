# Nhật ký Tư vấn: Hướng dẫn Chi tiết Đơn giản hóa Sơ đồ và Góp ý Phản biện

Tài liệu này tổng hợp các hạng mục cần chỉnh sửa cho từng file sơ đồ (`.drawio`) cụ thể nhằm tối ưu hóa cho bài báo cáo Khóa luận, đồng thời ghi lại các đánh giá phản biện khách quan về hệ thống để chuẩn bị cho Hội đồng bảo vệ.

---

## PHẦN I: HƯỚNG DẪN ĐƠN GIẢN HÓA SƠ ĐỒ

### 1. Sơ đồ Kiến trúc Mô hình (Architecture)

#### 1.1. arch_pga_unet2d.drawio (Lõi hệ thống)
*   **Image label:** Xóa phần phụ `1 ch | 512×512`. Chỉ giữ: **"Image"**.
*   **PSG Scale:** Xóa công thức `× (1+α·σ(Conv(p)))`. Giữ lại tiêu đề: **"PSG Scale"**.
*   **Prompt Gating:** Xóa công thức `g + conf·α·w·p`. Giữ lại tiêu đề: **"Prompt Gating"**.
*   **+ 0.3·skip:** Thay bằng: **"Residual Skip"**.
*   **+ β·p:** Thay bằng: **"Prompt Fusion"**.
*   **Lưu ý (Note):** Xóa toàn bộ dòng ghi chú dài (`PSG xen kẽ per encoder level... | +0.3·skip... | Input 512×512`). Không cần thiết trong sơ đồ kiến trúc.

#### 1.2. arch_sammed2d.drawio (SAM-Med2D)
*   **Noisy BBox:** Xóa `zoom_out / shift / mixed_7_3`. Thay bằng: **"Noisy BBox"** hoặc **"Prompt Perturbation"**.
*   **Image Encoder:** Xóa emoji 🔒 và ✏️, xóa `×12`. Đơn giản hóa thành: `Image Encoder (ViT-B)` với subtitle `Trainable Adapters`.
*   **Ghi chú (iter_note):** Xóa `iter_point=3`, `3× point refine`, `box only, single-pass`. Thay bằng: **"Iterative Point Refinement"**.

#### 1.3. arch_attention_unet2d.drawio & arch_unet2d.drawio
*   **Input label:** Xóa `1 ch | 256×256`. Thay bằng: **"Image"**.
*   **Output label:** Xóa `Conv 1×1`. Thay bằng: **"Mask"**.
*   **arch_attention_unet2d — Lưu ý AG:** Xóa dòng giải thích dài về Attention Gate / gating signal. Không cần thiết trong sơ đồ.

---

### 2. Sơ đồ Pipeline & Quy trình (Workflow)

#### 2.1. classification_pipeline.drawio
*   **MobileNetV4 Block:** Xóa dòng chữ nhỏ về `Pretrained ImageNet → Fine-tune...`.
*   **Khối Giai đoạn (ft):** Xóa bỏ hoàn toàn khối ghi chú giải thích về `Warmup` và `Full fine-tune`.

#### 2.2. preprocessing_pipeline.drawio
*   **Bước 1:** Xóa `(Xóa ICC Profile)`.
*   **Bước 3:** Xóa `(2000 / 3746 ảnh)`.
*   **Bước 7:** Xóa `512×512`. Chỉ ghi: **"Chuẩn hóa & Resize"**.

#### 2.3. pipeline_pga_app_inference.drawio (Sơ đồ quan trọng — cần cập nhật GradCAM)

> ⚠️ **GradCAM đã bị loại bỏ hoàn toàn khỏi hệ thống (06/06/2026).** IPR nay chạy trực tiếp sau kiểm tra điều kiện — không còn bước GradCAM trung gian. Phải cập nhật nhánh "cứu hộ" trong sơ đồ này.

*   **MobileNetV4:** Sửa metrics **sai** — drawio ghi `Acc = 88% | F1 = 88%` nhưng số thật là `Acc = 85.77% | F1 = 86.25%`. Nên xóa hẳn, chỉ giữ tên model.
*   **Inference₀:** Xóa công thức `(image, Prompt₀) → Prediction₀` và chú thích `Forward pass lần đầu`. Chỉ giữ: **"PGA-UNet Inference"**.
*   **Dec_rescue (Điều kiện phân nhánh):** Xóa `① Prompt >70% đen`, `② Prediction < 50px`, `③ Confidence < 0.25`. Thay nhãn thành: **"Câu nhắc hợp lệ?"**.
*   **Khối "Dự đoán rỗng":** Xóa `model(ảnh, Zero Prompt) → Mask = ∅` và xóa `✅ Achievement 1: Bảo hộ kích hoạt`. Chỉ giữ: **"Mặt nạ rỗng"**.
*   **Khối "GradCAM Mode": XÓA HOÀN TOÀN** (`Trích GradCAM từ Zero Prompt pass → Peak activation → Prompt₁`). GradCAM không còn trong hệ thống.
*   **IPR:** Cập nhật `k=3` → `k=5`. Xóa công thức `PGA-UNet(image, prompt_t) → pred_t...`. Chỉ để: **"IPR (k=1…5): Iterative Prompt Refinement"**.
*   **Output Mask:** Xóa `Rescue Box`, `Gradio UI — Mask Xanh + Box Vàng`, `Gradio UI — Mask Đỏ`. Chỉ giữ: **"Output: Mặt nạ phân đoạn"** và **"Output: Mặt nạ IPR"**.

#### 2.4. system_architecture.drawio
*   **PGA-UNet Phân đoạn:** Xóa công thức `(Image, Prompt₀) → Prediction₀` trong subtitle nhỏ.
*   **"IPR / GradCAM Rescue": ĐỔI TÊN HOÀN TOÀN** thành **"IPR (Tinh chỉnh câu nhắc)"**. Xóa cả `k=3` trong subtitle.
*   **"Kết quả phân đoạn":** Xóa `GradCAM Overlay` khỏi subtitle. Chỉ giữ: **"Binary Mask"**.

---

### 3. Bảng tổng hợp theo mức ưu tiên

| Mức độ | File | Thay đổi chính |
|---|---|---|
| 🔴 Bắt buộc | `pipeline_pga_app_inference.drawio` | Xóa khối GradCAM Mode; cập nhật k=3→k=5; sửa metrics sai (88%→85.77%) |
| 🔴 Bắt buộc | `system_architecture.drawio` | Đổi tên "IPR / GradCAM Rescue" → "IPR"; xóa "GradCAM Overlay" |
| 🟡 Nên làm | `arch_pga_unet2d.drawio` | Xóa công thức PSG/CAD; xóa Note; xóa `1 ch | 512×512` |
| 🟡 Nên làm | `arch_sammed2d.drawio` | Xóa emoji và iter_point chi tiết |
| 🟡 Nên làm | `arch_unet2d.drawio` & `arch_attention_unet2d.drawio` | Input→"Image"; Output→"Mask"; xóa AG note |
| 🟢 Tùy chọn | `classification_pipeline.drawio` | Xóa fine-tune detail note |
| 🟢 Tùy chọn | `preprocessing_pipeline.drawio` | Xóa ICC Profile, số ảnh, 512×512 |

### 4. Lý do thực hiện (Tại sao nên xóa?)
1.  **Nhất quán với report:** GradCAM đã bị xóa khỏi Chapter 1–5. Sơ đồ phải đồng bộ — hội đồng sẽ đối chiếu sơ đồ với report và phát hiện ngay mâu thuẫn.
2.  **Sửa số liệu sai:** `Acc = 88% | F1 = 88%` trong drawio không khớp với số chính thức `Acc = 85.77% | F1 = 86.25%`.
3.  **Chuyên nghiệp hóa:** Hội đồng quan tâm đến luồng dữ liệu, không phải con số chi tiết trong sơ đồ. Các chỉ số nên nằm ở phần Thực nghiệm.
4.  **Tránh lỗi thời:** Tham số đã đổi `k=3 → k=5`. Giữ số cụ thể trong sơ đồ tạo mâu thuẫn nội bộ.

---

## PHẦN II: GÓP Ý PHẢN BIỆN (PRE-DEFENSE REVIEW)

Đứng dưới góc độ của một Hội đồng phản biện khắt khe, dưới đây là 5 lỗ hổng hoặc điểm cần giải trình/rào trước trong báo cáo để đảm bảo tính chặt chẽ về mặt hệ thống y khoa:

### 1. Sự thiếu vắng thuật toán xóa nhiễu trong Inference Pipeline
*   **Vấn đề:** Ảnh đầu vào của hệ thống thực tế có thể chứa ký tự cản quang (R/L). Trong lúc huấn luyện, dữ liệu đã được làm sạch bằng YOLOv11s. Tuy nhiên, luồng \`app.py\` (Chương 4) có vẻ như chưa mô tả rõ việc tích hợp YOLOv11s vào quá trình tiền xử lý trước khi đưa vào MobileNetV4.
*   **Rủi ro:** Mô hình có thể dự đoán sai lệch hoàn toàn khi gặp chữ 'R' hoặc 'L' vì nó chưa từng thấy đặc trưng này trong lúc huấn luyện (Distribution Shift).
*   **Hướng giải quyết:** Cần làm rõ YOLOv11s có chạy ngầm trong \`app.py\` hay không. Nếu không, phải bổ sung phần "Đánh giá với dữ liệu chưa xóa nhiễu" hoặc đưa vào mục Hạn chế.

### 2. Ngưỡng phân loại (Threshold) cố định = 0.5
*   **Vấn đề:** MobileNetV4 sử dụng \`p > 0.5\` để quyết định Có/Không bệnh. Trong y tế (đặc biệt là sàng lọc), ưu tiên hàng đầu là **giảm tối đa False Negative (không bỏ sót bệnh nhân)**.
*   **Hướng giải quyết:** Thêm lập luận giải thích trong Chương 4 về việc có thể tinh chỉnh Threshold dựa trên đường cong ROC (điểm Youden) để đẩy Recall lên mức cao hơn (ví dụ 95%), chấp nhận hy sinh Specificity để đảm bảo tính an toàn y khoa.

### 3. Đảm bảo tính công bằng khi đánh giá Baseline (Attention U-Net)
*   **Vấn đề:** Attention U-Net có kết quả rất thấp (Dice 0.41) khi huấn luyện với cùng một bộ hyperparameters như PGA-UNet. Hội đồng có thể đặt câu hỏi về việc liệu Attention U-Net đã thực sự được "tune" đúng mức hay chưa.
*   **Hướng giải quyết:** Thêm câu rào trước vào báo cáo: *"Mặc dù các mô hình dùng chung cấu hình để đảm bảo tính đối chứng, kết quả của Attention U-Net có thể cải thiện nếu được Hyperparameter Search độc lập"*, đồng thời nhấn mạnh rằng sự sụt giảm này chủ yếu do nhiễu attention khi không có prompt định hướng.

### 4. Tác dụng phụ của thuật toán Inpainting
*   **Vấn đề:** Inpainting (xóa chữ R/L) về cơ bản là tạo ra pixel giả. Nếu vùng chữ nằm đè lên tổn thương, inpainting có thể làm biến dạng hình thái khối u.
*   **Hướng giải quyết:** Bổ sung thẳng vấn đề này vào mục **Hạn chế (Chương 5)**. Việc tự thừa nhận rủi ro thay đổi cấu trúc gradient vùng bệnh lý sẽ chứng tỏ bạn có tư duy phản biện và thấu hiểu rõ bản chất của xử lý ảnh y tế.

### 5. Thiếu sự tham gia đánh giá của chuyên gia Y tế (Clinical Validation)
*   **Vấn đề:** Khóa luận hiện tại chủ yếu tập trung vào các chỉ số kỹ thuật (Dice, IoU, HD95) mà thiếu đi chỉ số khả dụng do bác sĩ đánh giá trực tiếp trên ứng dụng.
*   **Hướng giải quyết:** Thêm vào mục Hạn chế và Định hướng tương lai: *"Hệ thống cần trải qua quá trình thử nghiệm mù (Blind Test) hoặc đánh giá lâm sàng với các bác sĩ X-quang để thu thập Mean Opinion Score (MOS), nhằm khẳng định tính thực tiễn của cơ chế cứu hộ IPR."*
Sau khi chạy xong thì lập kế hoạch trình bày để đảm bảo sẽ cần phải trình bày đủ ý.

Tìm ra những lỗ hỏng khả năng cao sẽ bị giám khảo khóa luận hỏi đến khi bảo vệ