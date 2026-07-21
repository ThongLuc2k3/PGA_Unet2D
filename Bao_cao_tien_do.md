# Báo cáo tiến độ

Ngày cập nhật: 2026-07-20

## Trạng thái hiện tại

- Phần report chính trong `Report/` đã được rà và chỉnh lại để thống nhất cách diễn đạt với phạm vi thực nghiệm hiện tại.
- Các kết quả chính hiện được mô tả nhất quán theo thiết lập **phân đoạn có hướng dẫn bằng hộp giới hạn**.
- Cách gọi được ưu tiên trong toàn repo:
  - `câu nhắc` hoặc `câu nhắc trực quan`, thay cho việc lạm dụng từ `prompt` khi không cần thiết;
  - `mô-đun`, thay cho `module` trong phần mô tả tiếng Việt;
  - `Gatekeeper` được giữ như tên riêng của mô-đun sàng lọc hỗ trợ;
  - `PGA-UNet` được mô tả là mô hình khoảng `3 triệu` tham số trong report và README hiện tại.

## Những việc đã hoàn tất gần đây

1. Siết lại các phát biểu trong report để không vượt quá điều thiết kế thực nghiệm thực sự chứng minh.
2. Đồng bộ cách mô tả PSG và CAD với công thức và mã nguồn.
3. Rà lại văn phong để giảm các chỗ diễn đạt nặng mùi AI hoặc lẫn Anh--Việt không cần thiết.
4. Bổ sung tài liệu nền ở Chương 1--2 và nâng số mục trong `Report/References/references.bib` lên trên 30.
5. Đồng bộ `README.md` với report hiện tại.

## Ghi chú

- `Đánh giá.md` là tài liệu phản biện và góp ý học thuật, không phải mô tả trạng thái cuối cùng của report.
- Môi trường terminal hiện tại không có `latexmk` và `pdflatex`, nên chưa kiểm tra lại việc build PDF trực tiếp từ dòng lệnh.
