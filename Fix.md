update (xóa và thay thế lại ảnh) trong images của report và submission để nó lưu ảnh mới của 2file subcat (pga baseline và sam) trong resul. và cập nhật lại
  định lượng của report và submission do 2 file này thay đổi.

Submission folder 
Phần README.md: Bỏ luôn mục tác giả

Phần 01.md
1.3 Kiểm tra và giải thích rõ hơn về binary mask, gaussian2D
1.4 Giải thích ý nghĩa từng chỉ số đánh giá dice, iou, presicion, recall, hd95, cbl
1.6 
Bị lỗi hd95*(norm), trong bảng Tóm Tắt So Sánh cũng bị, mục 2E trong 02.md cũng dính
cần nói rõ viết tắt của zero-shot, finetune là ZS và FT
1.7 Giải thích ý nghĩa từng thí nghiệm V1 → V5 (tui bỏ sót phần này)
1.8 Cần nói rõ TB là viết tắt của trung bình, mục 2H của 02.md cũng bị
1.9 Kiểm tra và giải thích rõ (Δ+0.6919) (xuất hiện 2 lần trong 1.9), xuất hiện 2 lần trong mục 2I của 02.md, mục 3I của 03.md (chỉ xuất hiện 1 lần), 
2.1 Giai đoạn 2 là mở khóa toàn bộ trọng số trừ các lớp BatchNorm

The BatchNormalization layers need to be kept frozen (more details). If they are also turned to trainable, the first epoch after unfreezing will significantly reduce accuracy.


Phần 02.md
mục 1B của efficientnet-b3 sửa cross entropy thành BCE, batch size từ 32 về 16
mục 2J cần sửa Standalone (mục 2.1 và 2.2 của 01.md cũng bị), giải thích ý nghĩa từng chỉ số đánh giá



Phần 03.md
mục A.1 cần giải thích TP, FP, FN là gì trước khi show ảnh, tương tự cho mục 3F, 3G
mục A.1 và A.2 show các ảnh giống hệt nhau
mục 3D cần giải thích ý nghĩa của màu vàng là phần giao, màu đỏ là dự đoán, màu xanh lá là GT trước khi show ảnh, tương tự cho mục 3E, 3H, 3I
mục 3G không cần hiển thị ảnh
mục 3H sửa lại file Subcat của PGA và baseline (PGA dùng các ảnh dễ và khó cho trùng với unet, att)

Phần 05.md
Sửa tên mục Kế thừa nguyên sắc thành Kế thừa trực tiếp

