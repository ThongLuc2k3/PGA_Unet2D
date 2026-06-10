Submission folder 
Mục 1.6 của 01.md: CBL hình như độ đo liên quan đến tâm mà trong file ghi
CBL (Contour-Based metric): đánh giá chất lượng đường biên, trọng số cao ở vùng viền; bổ sung Dice về độ chính xác đường viền.
Nên sửa lại là: CBL (Centroid-Based Localization Score): Đánh giá khả năng định vị chính xác của vùng dự đoán so với ground truth dựa trên khoảng cách tâm điểm
(cái này tui copy từ nhóm đợt 1 rồi kêu gemini viết lại, do là CBL trên hình như do nhóm đợt 1 tự tạo ra và định nghĩa)


Mục K.2 của 02.md: Công thức bị in ra như sau:
Công thức: $$\text{Pipeline Dice} = \frac{\sum_{i \in \text{polygon(TP)}} \text{Dice}i}{N{\text{polygon(TP)}} + N_{\text{image(FP)}}} = \frac{\sum 226 \text{ Dice}}{226 + 38} = \frac{...}{264} = 0.7296$$


Mục A.1 và F của 03.md: Bị nhầm màu khi định nghĩa TP, FP, FN do đó không khớp với hình
Phải sửa lại là:
Mục A.1
Quy ước màu trong ảnh overlay phân đoạn:
TP (True Positive): pixel dự đoán là tổn thương VÀ thực sự là tổn thương → màu xanh lá (intersection)
FP (False Positive): pixel dự đoán là tổn thương nhưng KHÔNG phải tổn thương → màu đỏ (dự đoán thừa)
FN (False Negative): pixel KHÔNG được dự đoán là tổn thương nhưng thực sự là tổn thương → màu xanh dương (bỏ sót)


Mục F
Quy ước màu trong ảnh overlay và định nghĩa TP/FP/FN:
TP (True Positive): pixel được dự đoán là tổn thương VÀ thực sự là tổn thương → màu xanh lá
FP (False Positive): pixel được dự đoán là tổn thương nhưng KHÔNG phải tổn thương → màu đỏ (dự đoán thừa, sai dương)
FN (False Negative): pixel KHÔNG được dự đoán là tổn thương nhưng thực sự là tổn thương → màu xanh dương (bỏ sót, sai âm)