# Danh sách việc cần sửa báo cáo KLTN

> Review toàn bộ 87 trang PDF. Ưu tiên từ cao xuống thấp.

---

## 🔴 KHẨN CẤP — Bắt buộc sửa trước khi nộp

### 1. Thêm Lời cam đoan *(bắt buộc theo quy định ĐHKHTN)*
- **Vấn đề:** `main.tex` dòng 152–153 đang comment out:
  ```latex
  %\addcontentsline{toc}{chapter}{Lời cam đoan}
  %\include{Appendix/reassurances}
  ```
- **Sửa:** Bỏ comment 2 dòng trên. File `Appendix/reassurances.tex` đã có sẵn.

---

### 2. Xóa viền đỏ hyperlink trong mục lục / danh sách hình / bảng
- **Vấn đề:** Toàn bộ mục lục, danh sách hình, danh sách bảng có viền đỏ bao quanh từng mục — do hyperlink chưa ẩn màu. Trông rất mất thẩm mỹ khi in và nộp.
- **Sửa:** Thêm vào `main.tex` (sau phần khai báo `\usepackage[unicode]{hyperref}`):
  ```latex
  \hypersetup{hidelinks}
  ```

---

### 3. Fix trang 27 gần như trắng hoàn toàn
- **Vấn đề:** Câu `"sáng của ký tự R/L là tổn thương xương."` nằm đơn độc ở đầu trang 27, phần còn lại trắng. Nguyên nhân: có `\clearpage` hoặc `\FloatBarrier` thừa trong `Chapter3/chapter3.tex` sau đoạn mô tả Lưu ý R/L.
- **Sửa:** Tìm và xóa `\clearpage` / `\newpage` / `\FloatBarrier` thừa trong section 3.2.2 của `Chapter3/chapter3.tex`.

---

### 4. Thống nhất tháng trên trang bìa và lời cảm ơn
- **Vấn đề:**
  - Trang bìa: `tháng 07/2026`
  - Lời cảm ơn (`Appendix/thanks.tex`): `tháng 6 năm 2026`
- **Sửa:** Chọn một tháng thống nhất (tháng 6 hoặc 7) rồi sửa cả hai nơi.

---

### 5. *(Đã sửa)* Đề cương — Bỏ so sánh với Attention U-Net
- **Trạng thái:** ✅ Đã sửa trong `Appendix/decuong.tex` dòng 74 và 85.
- **Lý do:** Attention U-Net được kế thừa kiến trúc (CAD mở rộng từ Attention Gate), không phải là mô hình đối sánh trong thực nghiệm.

---

## 🟠 QUAN TRỌNG — Ảnh hưởng đến điểm đánh giá học thuật

### 6. Tài liệu tham khảo quá ít (chỉ 8 tài liệu)
- **Vấn đề:** KLTN chuẩn cần 20–30+ tài liệu. Hiện tại:
  - `[1]` là website bệnh viện (không phải công trình khoa học)
  - `[2]` SAM-Med2D là arXiv preprint, chưa peer-reviewed
  - `[3]`, `[4]` là website tool (Roboflow, YOLO)
- **Cần bổ sung (gợi ý):**
  - SAM gốc (Kirillov et al., 2023, ICCV)
  - MedSAM (Ma et al., 2024)
  - nnU-Net (Isensee et al., 2021, Nature Methods)
  - TransUNet (Chen et al., 2021)
  - SwinUNet (Cao et al., 2022)
  - Survey về medical image segmentation
  - Survey về interactive segmentation
  - Các bài báo về bone tumor detection/segmentation
  - PACS system references
  - Các bài báo về prompt-based learning in computer vision

---

### 7. Thiếu kiểm định thống kê (Statistical Significance Test)
- **Vấn đề:** Mục 4.3.2 tự nhắc "kiểm định Wilcoxon signed-rank là bước được khuyến nghị" nhưng **không thực hiện và không báo cáo p-value** nào. Không có p-value thì kết luận "vượt trội" không có cơ sở thống kê.
- **Sửa:** Chạy Wilcoxon signed-rank test (phi tham số) trên 232 giá trị Dice per-polygon cho các cặp so sánh chính:
  - PGA-UNet (V5) vs V4 (Binary prompt)
  - PGA-UNet vs U-Net
  - PGA-UNet vs SAM-Med2D FT
  - Báo cáo p-value trong Bảng 4.7 hoặc text phân tích.

---

### 8. Thiếu đường cong huấn luyện (Training Curves)
- **Vấn đề:** Không có biểu đồ Loss/Dice theo epoch. Đây là hình cơ bản trong mọi báo cáo deep learning — xác nhận mô hình hội tụ ổn định, không overfit.
- **Sửa:** Thêm vào Section 4.1.2 hoặc 4.2 một figure gồm:
  - Train Loss vs Val Loss theo epoch (PGA-UNet)
  - Train Dice vs Val Dice theo epoch (PGA-UNet)
  - Có thể thêm U-Net để so sánh tốc độ hội tụ.

---

### 9. Section 4.4 Qualitative Results quá nghèo
- **Vấn đề:** Chỉ có **1 hình duy nhất** (Hình 4.1, 8 ảnh nhỏ khó đọc). Một hội đồng sẽ yêu cầu nhiều ví dụ hơn.
- **Sửa:** Thêm ít nhất 2 hình nữa:
  - Hình 4.2: So sánh trực quan PGA-UNet vs U-Net trên nhóm **Khó** (tổn thương nhỏ / biên giới mờ)
  - Hình 4.3: Failure cases — 3–4 trường hợp PGA-UNet dự đoán kém, kèm chú thích lý do

---

### 10. Thêm Abstract tiếng Anh
- **Vấn đề:** Trang đề cương đã có tiêu đề tiếng Anh nhưng `Appendix/tomtat.tex` chỉ có tiếng Việt. Báo cáo khoa học chuẩn cần cả 2 ngôn ngữ.
- **Sửa:** Thêm phần "Abstract" tiếng Anh vào `Appendix/tomtat.tex`, ngay sau phần tiếng Việt, có cùng cấu trúc: Problem / Solution / Results / Keywords.

---

## 🟡 NÊN SỬA — Cải thiện chất lượng tổng thể

### 11. Phần 2.1 Related Work quá ngắn
- **Vấn đề:** Chỉ đề cập 2 mô hình (U-Net, Attention U-Net) + SAM-Med2D trong 1.5 trang. Hội đồng thường hỏi về bức tranh tổng quan.
- **Sửa:** Mở rộng Section 2.1 thêm ít nhất:
  - nnU-Net (self-configuring, SOTA trên nhiều benchmark y tế)
  - TransUNet / SwinUNet (hybrid CNN-Transformer)
  - MedSAM, SEEM (các foundation model interactive khác)
  - Kết thúc bằng bảng tóm tắt so sánh các công trình liên quan.

---

### 12. Thiếu hình minh họa tiền xử lý (Section 3.2)
- **Vấn đề:** Mô tả quy trình xóa nhiễu R/L rất chi tiết nhưng không có ảnh ví dụ before/after. Khó thuyết phục hội đồng về hiệu quả tiền xử lý.
- **Sửa:** Thêm Hình 3.2b (hoặc thay thế Hình 3.2 hiện tại bằng một figure kết hợp flowchart + ví dụ ảnh) gồm:
  - 2 ảnh gốc chứa ký tự R/L
  - 2 ảnh tương ứng sau khi xóa nhiễu

---

### 13. Các trang trắng không cần thiết
- **Vấn đề:** Trang 8, 21, 39, 63, 69 — nội dung kết thúc rất sớm, phần còn lại của trang hoàn toàn trắng. Không nghiêm trọng nhưng trông thiếu chuyên nghiệp.
- **Sửa:** Kiểm tra và xóa `\clearpage` / `\newpage` thừa ở cuối các section tương ứng trong:
  - `Chapter1/chapter1.tex` (trang 8)
  - `Chapter2/chapter2.tex` (trang 21)
  - `Chapter3/chapter3.tex` (trang 39)
  - `Chapter4/chapter4.tex` (trang 63)
  - `Chapter5/chapter5.tex` (trang 69)

---

### 14. Thêm Phụ lục (Appendix)
- **Vấn đề:** `main.tex` dòng 197–198 có appendix bị comment out hoàn toàn. Không có phụ lục nào trong báo cáo.
- **Sửa (tối thiểu):** Thêm vào `Appendix/appendix1.tex`:
  - Bảng hyperparameters đầy đủ của tất cả mô hình (PGA-UNet, U-Net, EfficientNet_B3)
  - Thêm visualization kết quả bổ sung (10–15 ảnh) nếu còn chỗ

---

### 15. Hình ablation study thiếu trực quan hóa
- **Vấn đề:** Bảng 4.7 (Ablation) chỉ có số, không có hình so sánh trực quan V1 vs V5. Kết quả sẽ thuyết phục hơn nhiều nếu có hình side-by-side.
- **Sửa:** Thêm 1 figure trong Section 4.3.1 so sánh mask phân đoạn của V1 (concat heatmap đơn giản) vs V5 (PSG+CAD+Gaussian) trên cùng 1 ca ảnh, đặc biệt kịch bản Shift.

---

## Ghi chú từ review GVHD trước (giữ lại)

Phải tự kiểm tra báo cáo ít nhất 10 lần
1. Đóng góp
Xác định đóng góp: đóng góp gì (final solution)? Phần nào là kế thừa, phần nào là tự phát triển (sử dụng visual prompt ko phải là đóng góp).
Xác định đối tượng end user: bác sĩ đọc ảnh (đã xác định)
2 module phân đoạn Image Encoder, Mask Decoder thì có kế thừa/cải tiến cải lùi gì
Làm rõ kiến trúc khối mã hóa và hòa trộn: Giải thích sâu về kỹ thuật trong cách thức hoạt động của Image Encoder, Prompt Encoder, kỹ thuật xử lý để huyện prompt và encoder/decoder với nhau. Attention ở đây là trên ảnh hay prompt hay gì?
Nhấn mạnh kỹ thuật mã hóa visual prompt (kế thừa hay cải tiến từ đâu): giải thích từng kiểu prompt (heatmap vs binary(token)), giải thích lý do chọn heatmap, so sánh bản chất của 2 kỹ thuật này. Nói rõ đóng góp này trong chương 3 và khi nói là đóng góp thì sẽ bị soi xuống phần thực nghiệm để minh chứng
Giải thích hàm loss có thay đổi gì không khi có thêm visual prompt trong giai đoạn học không
Thực nghiệm phải luôn có minh chứng cho phần đóng góp

2. Về ảnh đầu vào
Về vấn đề resize ảnh thì có 2 hướng:
Hướng 1 (không resize): Thử nghiệm dùng kiến trúc Swin Transformer để chia ảnh thành các patch nhỏ
Hướng 2: Nếu phải resize, cần chứng minh rằng dù ảnh bị scale nhỏ nhưng khi có visual prompt hỗ trợ thì hiệu suất phân đoạn được kéo lại đáng kể

3. Quy trình pipeline
Nâng chỉ số Gatekeeper
Cần bổ sung phần thảo luận và chuẩn bị câu trả lời phản biện cho hai tình huống thực tế sau:
Bác sĩ không vẽ, không đưa bất kỳ gợi ý nào (prompt rỗng) thì hệ thống xử lý ra sao?
Bác sĩ nhận thức sai, vẽ bbox lệch tâm hoặc sai hoàn toàn vị trí thì hệ thống vận hành ra sao?
⇒ Phải đưa ra thêm các lý luận để giải thích thỏa đáng 

4. Sửa đổi thực nghiệm và đánh giá so sánh
Mọi tuyên bố cải tiến kỹ thuật (như việc thay đổi cách mã hóa từ binary sang heatmap) đều phải có số liệu thực nghiệm đối chứng trực tiếp để chứng minh tính hiệu quả
Đảm bảo tính công bằng:
Với unet và att unet thì đừng dùng từ so sánh hay lý luận như thế nào đó
Nói rõ về mẫu theo ảnh và mẫu theo GT
Kết quả tốt là do prompt hay do kiến trúc
Att unet chưa tối ưu
So sánh với sam-med2d cần cùng kích thước 256x256

5. Tiền xử lý dữ liệu
Cần nói rõ là việc xóa chữ R/L, văn bản thông tin bệnh nhân trên ảnh x quang là chỉ nằm trong phạm vi cho mô hình học đặc trưng. Trên giao diện làm việc thực tế thì vẫn hiển thị những thông tin đó.
