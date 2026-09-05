# Rà soát và sửa văn phong AI trong access.tex / access_vietnam.tex

Ghi lại các lỗi văn phong "quá AI" đã tìm thấy khi rà soát toàn bộ bài báo
(Abstract, Introduction, Related Work, Method, Experimental Setup, Results,
Discussion, Conclusion) và cách đã sửa. Đây là bản ghi trạng thái đã chốt,
không phải đề xuất chờ duyệt.

## Các loại lỗi đã sửa

**1. Một luận điểm bị diễn giải lại nhiều lần bằng nhiều câu khác nhau.**
Ý "prompt được giữ hoạt động xuyên suốt mạng, không dùng một lần rồi bỏ" từng
lặp lại (đổi từ, giữ nguyên cấu trúc câu) ở Abstract, Introduction, Related
Work, Method (2 chỗ), Conclusion. Đã gom về phát biểu đầy đủ nhất ở
Introduction, các chỗ khác rút gọn hoặc bỏ.

**2. Câu hỏi tu từ bị chép gần như nguyên văn ở 2 mục.**
Introduction và Related Work từng đặt cùng một câu hỏi tu từ (chỉ paraphrase
nhẹ). Giữ câu hỏi ở Introduction, Related Work đổi thành câu khẳng định nêu
khoảng trống nghiên cứu.

**3. Khuôn tu từ "không phải X mà là Y" lặp thành công thức cứng.**
Xuất hiện ở nhiều mục (Introduction, Method, Discussion, Results). Chỉ giữ ở
Discussion — nơi hợp lý nhất để tổng kết lại câu hỏi nghiên cứu; các chỗ khác
viết lại thành câu trần thuật thẳng.

**4. Câu tự PR/kịch tính mở hoặc đóng mục.**
Bỏ: "The scientific meaning of the contribution is..." (Method), "Where does
that margin come from?" và "If keeping weak evidence alive... it is here."
(mở mục Results), "Read narrowly... stress case" (đóng mục tổn thương nhỏ).
Thay bằng câu trần thuật bình thường.

**5. Hai câu giới hạn phạm vi bị dán gần như nguyên văn nhiều lần (đồng bộ
máy móc, khác với lặp Ý ở mục 1 — đây là lặp gần như CHỮ).**
- "hộp phủ một phần / hộp âm / sai vùng nằm ngoài phạm vi" — xuất hiện 6 lần
  (Abstract, Method, Experimental Setup, Results, Discussion, Conclusion).
  Giữ bản đầy đủ ở Abstract và Method (nơi định nghĩa phạm vi lần đầu), 4 chỗ
  còn lại đổi cách diễn đạt, đảo thứ tự mệnh đề, dùng từ nối khác nhau.
- "$Q$ là heuristic, không phải xác suất hiệu chuẩn / danh sách không phải bộ
  phát hiện" — xuất hiện 4 lần (Mục III.F, Experimental Setup, Results,
  Discussion). Giữ bản đầy đủ ở Mục III.F (nơi định nghĩa $Q$ lần đầu), 3 chỗ
  còn lại rút gọn hoặc trỏ ngược lại thay vì lặp nguyên câu.

**6. Vài chỗ dịch tiếng Việt quá sát nghĩa đen, đọc như dịch máy.**
"buys a further, consistent margin" → "tạo thêm một khoảng cách ổn định";
"Resolution bites hardest here" → "Ở đây độ phân giải ảnh hưởng rõ nhất";
"the failures have a pattern" → "các lỗi này lặp lại theo một khuôn mẫu nhất
định chứ không ngẫu nhiên".

**7. Vài câu bị hỏi lại và làm rõ theo yêu cầu riêng.**
Ví dụ: câu mô tả 2 baseline Attention U-Net khớp prompt được viết rõ là do
nhóm tự bổ sung (không phải kế thừa từ nghiên cứu khác); câu về Monte Carlo
được xác nhận đúng qua đối chiếu code/notebook thật (không sửa); câu về
"prompt dropout/nhiễu prompt" bị xóa hẳn vì kiểm tra `dataset.py`/`train.py`
không thấy cơ chế này trong code.

## Những gì cố tình giữ nguyên (không phải lỗi)

- Bài vốn đã khiêm tốn về mặt học thuật (nhiều hedge đúng chỗ: "not an
  architecture verdict", "no cross-dataset claim", "Q is a heuristic, not a
  calibrated probability"...). Đây không phải overclaiming, không cần thêm
  hedge nữa.
- Cấu trúc Results "câu chốt số liệu → bảng → diễn giải → giới hạn phạm vi"
  lặp lại ở mọi mục — đây là cấu trúc báo cáo kết quả chuẩn, không phải văn
  phong AI, không đụng vào.
- Không có em dash/en dash nào trong toàn bộ tài liệu.

## Các đợt sửa tiếp theo (đã áp dụng, không còn là đề xuất)

- `access_vietnam.tex` sau đó được viết lại toàn bộ theo lối hành văn tạp chí
  tiếng Việt tự nhiên (không còn cấu trúc dịch từng câu), giữ nguyên số
  liệu/bảng/công thức toán.
- Danh sách vùng ứng viên (candidate shortlist) rút gọn còn top-5, bỏ top-3,
  đồng bộ ở cả 2 bản.
- Toàn bộ nội dung và các sửa factual (bỏ claim sai, bỏ câu "đang chạy" lỗi
  thời, làm rõ 2 baseline tự bổ sung, mở rộng hướng nghiên cứu tiếp theo, câu
  Monte Carlo giữ nguyên vì đã xác nhận đúng) đã được dịch ngược và đồng bộ
  sang `access.tex` (tiếng Anh).
- Tài liệu tham khảo (`references.tex` và phần References của bản Việt) đã
  gắn link ẩn cho cả dòng trích dẫn, không chỉ phần tiêu đề.
- Sửa lỗi hình/bảng rớt sai vị trí trong `access_vietnam.tex` (ép `[H]` thay
  vì `[h]`).
- Volume/year ở footer `access.tex` đổi từ mặc định "11, 2023" thành
  "14, 2026" cho khớp ngày bản thảo.

Xem lịch sử commit của repo để biết chi tiết từng đợt sửa.
