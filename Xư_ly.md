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
