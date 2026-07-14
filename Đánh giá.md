MỤC LỤC (đề xuất tổ chức lại, Chương 1–5) — bản chốt

## Chương 1 — GIỚI THIỆU (giữ nguyên)

1.1 Bối cảnh chung
1.2 Động lực nghiên cứu — 1.2.1 Động lực khoa học · 1.2.2 Động lực thực tiễn
1.3 Phát biểu bài toán
1.4 Thách thức của bài toán
1.5 Đóng góp của khóa luận
1.6 Bố cục của khóa luận

## Chương 2 — CÁC CÔNG TRÌNH LIÊN QUAN VÀ CƠ SỞ LÝ THUYẾT (giữ nguyên)

2.1 Các công trình liên quan — 2.1.1 Phân đoạn ảnh y khoa tự động · 2.1.2 Học máy tương tác trong y khoa
2.2 Cơ sở lý thuyết nền tảng — 2.2.1 CNN · 2.2.2 Kiến trúc U-Net · 2.2.3 Cơ chế chú ý và Attention U-Net
2.3 Học máy dựa trên câu nhắc — 2.3.1 Biểu diễn không gian của câu nhắc · 2.3.2 Cơ chế chú ý có điều kiện
2.4 Các độ đo đánh giá — 2.4.1 Dice và IoU · 2.4.2 Precision và Recall · 2.4.3 HD95 · 2.4.4 CBL
2.5 Tổng kết chương

## Chương 3 — MÔ HÌNH VÀ HỆ THỐNG ĐỀ XUẤT (giữ nguyên)

3.1 Mô hình PGA-UNet — 3.1.1 Biểu diễn câu nhắc trực quan · 3.1.2 Cổng không gian PSG · 3.1.3 Chú ý có điều kiện CAD
3.2 Luồng xử lý hai giai đoạn (ứng dụng thực tế)
3.3 Module sàng lọc (Gatekeeper)
3.4 Giải thuật hệ thống: Huấn luyện và Suy luận
3.5 Tổng kết chương

## Chương 4 — THỰC NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ (tổ chức lại)

### 4.1 Thiết lập môi trường thực nghiệm

- 4.1.1 Hai bộ dữ liệu (BTXRD, FracAtlas) và tiền xử lý đầu vào
- 4.1.2 Mô hình so sánh và cấu hình huấn luyện
- 4.1.3 Giao thức và độ đo đánh giá

### 4.2 Đánh giá hiệu năng phân đoạn
*(mỗi mục con trình bày cả hai dataset trong cùng một bảng/cùng một mạch văn, kết bằng một nhận định duy nhất xuyên hai miền — kể cả khi nhận định đó là "nhất quán" hay "chỉ đúng ở kịch bản X, khác biệt ở Y do đặc tính Z")*

- 4.2.1 So sánh với đường cơ sở U-Net
- 4.2.2 Tính bền bỉ trước sai lệch câu nhắc (Zoom-out, Shift, Mixed)
- 4.2.3 So sánh với mô hình nền tảng SAM-Med2D
- 4.2.4 Ảnh hưởng của độ phân giải và hiệu quả tính toán

*Cơ sở để gộp mục này:* đối chiếu số liệu 2 dataset cho các so sánh lớn (U-Net, SAM-Med2D, CAD) cho thấy hướng chênh lệch nhất quán ở kịch bản Shift/Mixed — đủ an toàn để viết 1 kết luận chung mỗi mục.

### 4.3 Phân tích chuyên sâu kiến trúc
*(giữ tách theo dataset — đây là nơi tập trung các đóng góp biên độ nhỏ có xu hướng đổi chiều giữa hai miền dữ liệu, đặc biệt ở kịch bản Zoom-out; gộp bảng ở đây sẽ cần chú thích ngoại lệ dày đặc, rối hơn để tách)*

- **4.3.1 Trên BTXRD**
  - Ablation: đóng góp của PSG và CAD
  - Độ ổn định qua đánh giá chéo 4-fold
  - Hiệu năng theo độ khó và đặc tính tổn thương
- **4.3.2 Trên FracAtlas**
  - Ablation: đóng góp của PSG và CAD
  - Độ ổn định qua đánh giá chéo 4-fold
  - Hiệu năng theo độ khó và đặc tính tổn thương
- **4.3.3 Kết luận đóng góp kiến trúc xuyên hai miền dữ liệu**
  - Cái gì nhất quán cả hai dataset (CAD quyết định tính bền bỉ, rõ nhất ở Shift) → khẳng định là đặc tính chung của kiến trúc.
  - Cái gì không tổng quát hóa được (đóng góp biên độ nhỏ đổi chiều ở Zoom-out) → nêu rõ, kèm giả thuyết lý giải ngắn (đặc tính hình thái tổn thương khác nhau giữa khối u và đường gãy mảnh), không nhận là quy luật kiến trúc.

*Lưu ý đánh số:* "Trên BTXRD" / "Trên FracAtlas" là 2 mục con có số riêng (4.3.1, 4.3.2); ba tiêu đề Ablation/Cross-val/Subcategory bên trong mỗi mục là tiêu đề in đậm không đánh số (không phải subsection), tránh trùng số giữa hai khối.

### 4.4 Đánh giá hệ thống đầu cuối (Gatekeeper + luồng xử lý hai giai đoạn)
*(giữ tách theo dataset — quy trình đánh giá Gatekeeper/pipeline của 2 dataset đủ khác biệt về đặc điểm nên không ép gộp bảng)*

- **4.4.1 Trên BTXRD**
  - Hiệu năng module Gatekeeper (EfficientNet_B3)
  - Ngưỡng phân loại và phân tích ca bỏ sót
  - Sai số tích lũy qua hai giai đoạn
  - Đánh giá trên tập hỗn hợp và các chỉ số lâm sàng
- **4.4.2 Trên FracAtlas**
  - Hiệu năng module Gatekeeper (EfficientNet_B3)
  - Ngưỡng phân loại và phân tích ca bỏ sót
  - Sai số tích lũy qua hai giai đoạn
  - Đánh giá trên tập hỗn hợp và các chỉ số lâm sàng

*Lưu ý đánh số:* tương tự 4.3 — bốn tiêu đề bên trong mỗi mục con là in đậm không đánh số.

### 4.5 Tổng kết chương
Gồm đoạn tổng hợp tính nhất quán/khác biệt BTXRD ↔ FracAtlas xuyên suốt cả 4.2, 4.3, 4.4 → khẳng định phạm vi tổng quát hóa thực sự của thiết kế PGA-UNet (không chỉ nhắc lại số liệu, mà trả lời thẳng câu hỏi "kiến trúc này tổng quát tới đâu, cụ thể ở điểm nào và không tổng quát ở điểm nào").

### Nguyên tắc trình bày xuyên suốt Chương 4 (không phải mục riêng)

- **Trực quan hóa:** không gom thành một mục "Trực quan hóa kết quả" riêng ở cuối chương. Mỗi hình minh họa định tính đặt ngay trong mục nói về số liệu định lượng tương ứng (ví dụ: ảnh minh họa ca Shift đặt ngay trong 4.2.2, không phải ở một mục trực quan hóa tách biệt).
- **Phân tích trường hợp thất bại:** tương tự — không gom vào một mục "Giới hạn kiến trúc" cuối chương. Case thất bại/khó liên quan đến chủ đề nào thì phân tích ngay trong mục đó (ví dụ: case tổn thương nhỏ đặt trong 4.3.1/4.3.2 phần đặc tính tổn thương, không phải mục riêng).
- Hai nguyên tắc trên áp dụng cho toàn bộ 4.2–4.4, không có mục số riêng nào chứa "hình ảnh" hay "thất bại" như một chủ đề độc lập.

## Chương 5 — KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN (giữ nguyên)

5.1 Kết luận những đóng góp đạt được
5.2 Hạn chế của hệ thống
5.3 Định hướng phát triển tương lai

---

## Ghi chú triển khai (thứ tự thực hiện, rủi ro tăng dần)

1. **4.2** — gộp bảng theo từng mục con, rủi ro số liệu thấp (chỉ ghép 2 bảng đã có sẵn + viết 1 đoạn nhận định chung).
2. **4.3** — di chuyển nội dung vào đúng khối BTXRD/FracAtlas (nội dung đã có sẵn, chỉ đổi vị trí + số mục), viết mới 4.3.3 (tổng hợp).
3. **4.4** — chỉ đổi số mục (BTXRD/FracAtlas đã tách sẵn trong bản hiện tại), không đổi nội dung.
4. **Phân bổ lại ảnh trực quan + case thất bại** — việc tốn công nhất, cần rà từng hình xem thuộc mục định lượng nào rồi di chuyển kèm đoạn văn mô tả.
5. **4.5 Tổng kết chương** — viết lại đoạn tổng hợp cuối cùng sau khi 4.2–4.4 đã ổn định.

Sau mỗi bước: rebuild `latexmk`, kiểm tra `Undefined reference`, không làm toàn bộ chương trong một lượt.
