# PHỤ LỤC A: PHÂN TÍCH CHUYÊN SÂU KIẾN TRÚC VÀ KHẢ NĂNG TỔNG QUÁT HÓA

Phụ lục A tập hợp các số liệu chi tiết mà Chương 4 chỉ nhắc ngắn gọn: chi phí tính toán, nghiên cứu loại bỏ thành phần, độ ổn định khi chia lại dữ liệu nhiều lần, và hiệu năng theo từng nhóm đặc tính tổn thương trên cả BTXRD lẫn FracAtlas. Phần này được tách riêng để Chương 4 giữ được mạch trình bày chính, trong khi các số liệu chi tiết vẫn có thể được đối chiếu khi cần.

## A.1 Chi phí tính toán: PGA-UNet so với SAM-Med2D

| Mô hình | Tham số tổng (M) | Tham số học (M) | FLOPs (G) | Checkpoint (MB) | Bộ nhớ GPU đỉnh (MB) | Độ trễ GPU (ms/ảnh) | Độ trễ CPU (ms/ảnh) |
|---|---|---|---|---|---|---|---|
| PGA-UNet (256×256) | 2.950 | 2.950 | 7.742 | 11.3 | 3300.8 | 8.46 ± 0.83 | 83.87 ± 2.08 |
| PGA-UNet (512×512) | 2.950 | 2.950 | 30.968 | 11.3 | 3429.8 | 21.83 ± 0.23 | 309.84 ± 8.24 |
| SAM-Med2D (256×256) | 271.242 | 184.569 | 92.024 | 2443.2 | 3332.8 | 60.70 ± 1.54 | 769.40 ± 11.36 |

Ở cùng độ phân giải 256×256, chênh lệch là rất lớn: SAM-Med2D nhiều tham số hơn khoảng 92 lần, số phép tính cao hơn gần 12 lần, checkpoint lớn hơn 215 lần, và chậm hơn PGA-UNet 7,2 lần trên GPU. Trên CPU khoảng cách còn lớn hơn, khoảng 9,2 lần. Đối với một hệ thống có bác sĩ chẩn đoán ảnh tương tác trực tiếp, thời gian chờ vài chục mili giây mỗi lần chỉnh câu nhắc khác biệt đáng kể so với thời gian chờ gần một giây.

Bộ nhớ GPU đỉnh là chỉ số duy nhất chưa cho thấy khoảng cách rõ như các chỉ số còn lại. Nhiều khả năng chỉ số này còn phụ thuộc cách khung chạy cấp phát bộ nhớ, không chỉ phụ thuộc kiến trúc mô hình. Vì vậy, khi so sánh chi phí triển khai, khóa luận ưu tiên nhìn vào số tham số, số phép tính, dung lượng checkpoint và độ trễ suy luận.

## A.2 Trên BTXRD

### A.2.1 Đóng góp của kiến trúc và câu nhắc

Tám cấu hình dưới đây chỉ khác nhau ở ba yếu tố: có PSG tại bộ mã hóa hay không, cơ chế chú ý trên kết nối tắt của nhánh giải mã (không dùng / cổng chú ý nguyên bản của Attention U-Net / CAD), và câu nhắc là bản đồ nhiệt Gaussian hay mặt nạ hộp giới hạn nhị phân. Tất cả được huấn luyện lại từ đầu, cùng điều kiện, trên BTXRD.

| Cấu hình | PSG | Chú ý trên kết nối tắt | Câu nhắc | Bao trọn↑ | Lệch tâm↑ | Hỗn hợp↑ |
|---|---|---|---|---|---|---|
| U-Net+Concat (Gaussian) | ✗ | Không | Gaussian | 0.8763 | 0.7364 | 0.8216 |
| U-Net+PSG | ✓ | Không | Gaussian | 0.8673 | 0.7388 | 0.8162 |
| U-Net+CAD | ✗ | CAD | Gaussian | **0.8861** | 0.7406 | 0.8292 |
| PGA-UNet (nhị phân) | ✓ | CAD | Nhị phân | 0.8780 | 0.7434 | 0.8267 |
| U-Net+Concat (nhị phân) | ✗ | Không | Nhị phân | 0.8781 | 0.7312 | 0.8202 |
| **PGA-UNet** | ✓ | CAD | Gaussian | 0.8607 | **0.8423** | **0.8560** |
| U-Net+PSG+Cổng chú ý nguyên bản | ✓ | Nguyên bản | Gaussian | 0.8680 | 0.7359 | 0.8173 |
| U-Net+Cổng chú ý nguyên bản | ✗ | Nguyên bản | Gaussian | 0.8738 | 0.7314 | 0.8193 |

Điểm đáng chú ý đầu tiên là lợi ích lớn nhất đến từ việc có câu nhắc. U-Net không dùng câu nhắc chỉ đạt Dice 0,4740 trên BTXRD, trong khi cách tích hợp đơn giản nhất là nối thẳng câu nhắc vào ảnh đầu vào đã nâng Dice lên 0,8763 ở kịch bản Bao trọn. Điều này cho thấy trước khi xét đến PSG hay CAD, bản thân thông tin câu nhắc đã tạo ra khác biệt rất lớn.

Khi xét riêng lẻ, từng thành phần không tạo ra cải thiện đáng kể. PSG khi đứng một mình chỉ nhích Dice thêm 0,0024 ở Lệch tâm, còn hai kịch bản kia giảm nhẹ (−0,0090 ở Bao trọn, −0,0054 ở Hỗn hợp). CAD khi đứng một mình cho kết quả tốt hơn: đạt 0,8861 ở Bao trọn, cao nhất trong tám cấu hình, và nhỉnh hơn cổng chú ý nguyên bản ở cả ba kịch bản, nhưng mức chênh vẫn nhỏ (0,0092–0,0123). Việc thay đổi cách biểu diễn câu nhắc từ Gaussian sang nhị phân cũng chỉ tạo ra khác biệt dưới 0,006, khi câu nhắc chưa qua PSG/CAD mà chỉ được nối kênh trực tiếp.

Hiệu quả chỉ thể hiện rõ khi ba thành phần được kết hợp đồng thời. PGA-UNet đầy đủ tăng 0,1059 Dice so với ghép kênh thông thường ở Lệch tâm, trong khi cộng riêng PSG (0,0024) với CAD (0,0042) chỉ ra 0,0066, chưa bằng một phần mười sáu mức cải thiện thực tế. Điều này cho thấy lợi ích không cộng dồn theo phép cộng tuyến tính đơn giản, mà chỉ xuất hiện khi tín hiệu câu nhắc được giữ xuyên suốt từ bộ mã hóa đến chú ý ở nhánh giải mã.

Hạn chế của PGA-UNet nằm ở kịch bản Bao trọn, tức khi câu nhắc gần như lý tưởng. Ở đây PGA-UNet (0,8607) thấp hơn U-Net+CAD (0,8861) một khoảng 0,0254. Điều này phù hợp với đặc điểm thiết kế: mặt nạ nhị phân có biên rõ nên có lợi khi vị trí hộp giới hạn hoàn toàn chính xác, còn bản đồ Gaussian chấp nhận giảm nhẹ hiệu năng đỉnh để đổi lấy độ bền khi câu nhắc bị lệch. Trong thực tế, khi bác sĩ chẩn đoán ảnh tự vẽ hộp giới hạn, sai lệch vài điểm ảnh xảy ra phổ biến hơn nhiều so với việc luôn xác định đúng tuyệt đối vị trí tổn thương.

Nhìn chung, nghiên cứu loại bỏ thành phần cho thấy PGA-UNet không được thiết kế để đạt hiệu năng cao nhất khi câu nhắc lý tưởng, mà để duy trì hiệu năng ổn định hơn khi câu nhắc không lý tưởng. Trên BTXRD, PGA-UNet thể hiện đúng xu hướng này, với 0,8423 ở Lệch tâm và 0,8560 ở Hỗn hợp, hai giá trị cao nhất trong bảng.

### A.2.2 Độ ổn định qua kiểm chứng chéo ngẫu nhiên lặp lại

PGA-UNet được đánh giá bằng kiểm chứng chéo ngẫu nhiên lặp lại 4 lần trên tập huấn luyện/xác thực. Ở mỗi lần, dữ liệu được xáo lại theo cấp độ ảnh; các đa giác thuộc cùng một ảnh luôn được giữ trong cùng một phần để tránh rò rỉ dữ liệu. Cần lưu ý đây không phải k-fold cross-validation theo nghĩa kỹ thuật chuẩn, mà là 4 lần chia ngẫu nhiên độc lập nhằm xem xét mức độ nhạy của kết quả với cách chia dữ liệu.

| Lần | Bao trọn↑ | Lệch tâm↑ | Hỗn hợp↑ |
|---|---|---|---|
| 1 | 0.8514 | 0.8206 | 0.8424 |
| 2 | 0.8755 | 0.8534 | 0.8677 |
| 3 | 0.8602 | 0.8414 | 0.8533 |
| 4 | 0.8646 | 0.8426 | 0.8610 |
| **Trung bình ± độ lệch chuẩn** | **0.8629 ± 0.0087** | **0.8395 ± 0.0119** | **0.8561 ± 0.0094** |

| Kịch bản | Dice↑ | IoU↑ | Precision↑ | Recall↑ | HD95↓ | CBL↑ |
|---|---|---|---|---|---|---|
| Bao trọn | 0.8629 | 0.7672 | 0.8506 | 0.8910 | 11.14 | 0.9548 |
| Lệch tâm | 0.8395 | 0.7332 | 0.8393 | 0.8574 | 13.25 | 0.9381 |
| Hỗn hợp (70% Bao trọn + 30% Lệch tâm) | 0.8561 | 0.7573 | 0.8466 | 0.8820 | 11.90 | 0.9501 |

Độ lệch chuẩn Dice dao động từ 0,0087 đến 0,0119, tức là khá nhỏ. Kịch bản Lệch tâm dao động nhiều nhất, điều này phù hợp vì bản thân cách tạo câu nhắc ở kịch bản này đã có yếu tố ngẫu nhiên. Ngoài ra, Dice trung bình sau 4 lần ở Bao trọn là 0,8629, khá gần với kết quả trên tập kiểm thử giữ riêng là 0,8607. Điều này cho thấy kết quả báo cáo không phụ thuộc vào một lần chia dữ liệu cụ thể.

### A.2.3 Theo đặc tính tổn thương

**So với U-Net theo mức hiệu năng của chính U-Net.** Chia tập kiểm thử theo Dice của U-Net (50 ảnh tốt nhất, 50 ảnh tệ nhất) để kiểm tra liệu cải thiện của PGA-UNet có chỉ đến từ những trường hợp mô hình cơ sở vốn đã xử lý tốt hay không.

| Nhóm | Mô hình | Dice↑ | IoU↑ | Precision↑ | Recall↑ | HD95↓ (px) | CBL↑ |
|---|---|---|---|---|---|---|---|
| U-Net hoạt động tốt | U-Net | 0.8488 | 0.7403 | 0.8481 | 0.8618 | 51.34 | 0.9194 |
| | PGA-UNet | **0.8972** | **0.8160** | **0.8656** | **0.9368** | **13.20** | **0.9666** |
| U-Net hoạt động kém | U-Net | 0.0211 | 0.0111 | 0.0396 | 0.1063 | 284.72 | 0.0708 |
| | PGA-UNet | **0.8261** | **0.7168** | **0.8313** | **0.8429** | **7.75** | **0.9456** |

Kết quả cho thấy điều này không hoàn toàn đúng. Ở nhóm U-Net làm tốt, PGA-UNet vẫn tăng thêm 0,0484 Dice. Ở nhóm U-Net gần như không phân đoạn được tổn thương (Dice 0,0211, HD95 284,7 điểm ảnh), PGA-UNet vẫn đạt 0,8261 và giảm HD95 xuống còn 7,75. Cần lưu ý đây là 50 ảnh U-Net làm tệ nhất theo chính U-Net, nên mức chênh lớn này không nên hiểu là mức cải thiện trung bình của toàn tập. Dù vậy, kết quả cho thấy PGA-UNet không suy giảm theo cùng cách với mô hình cơ sở.

**So với SAM-Med2D theo đặc tính tổn thương, cùng độ phân giải 256×256** (để loại yếu tố độ phân giải khỏi phép so sánh kiến trúc):

| Nhóm | Mô hình | Dice↑ | IoU↑ | Precision↑ | Recall↑ | HD95↓ (px) | CBL↑ |
|---|---|---|---|---|---|---|---|
| Tổn thương nhỏ | SAM-Med2D | 0.1356 | 0.0909 | 0.4331 | 0.0932 | 265.55 | 0.4257 |
| | PGA-UNet | **0.6870** | **0.5383** | 0.5687 | **0.9354** | **5.98** | **0.9092** |
| Biên mờ | SAM-Med2D | 0.5759 | 0.4260 | **0.8866** | 0.4616 | 28.74 | 0.9000 |
| | PGA-UNet | **0.7970** | **0.6715** | 0.7317 | **0.8977** | **18.84** | **0.9397** |
| Tổn thương rõ | SAM-Med2D | 0.8529 | 0.7469 | **0.8807** | 0.8342 | 24.33 | 0.9587 |
| | PGA-UNet | **0.8660** | **0.7669** | 0.8050 | **0.9455** | **23.08** | **0.9599** |

Khoảng cách giữa hai mô hình thay đổi theo độ khó của tổn thương: 0,5514 Dice ở nhóm nhỏ, chỉ còn 0,0131 ở nhóm rõ. Một điểm lặp lại ở cả ba nhóm: SAM-Med2D luôn cao hơn về Precision, PGA-UNet luôn cao hơn về Recall. Điều này cho thấy SAM-Med2D thiên về dự đoán thận trọng, còn PGA-UNet bao phủ vùng tổn thương rộng hơn, chấp nhận giảm nhẹ độ chính xác để tăng độ nhạy.

**Ảnh hưởng của độ phân giải, cùng ba nhóm trên:**

| Nhóm | Độ phân giải | Dice↑ | IoU↑ | Precision↑ | Recall↑ | HD95 (px) | CBL↑ |
|---|---|---|---|---|---|---|---|
| Tổn thương nhỏ | 256×256 | 0.6870 | 0.5383 | 0.5687 | **0.9354** | 5.98 | 0.9092 |
| | 512×512 | **0.8301** | **0.7212** | **0.8285** | 0.8553 | 3.06 | **0.9408** |
| Biên mờ | 256×256 | 0.7970 | 0.6715 | 0.7317 | **0.8977** | 18.84 | 0.9397 |
| | 512×512 | **0.8448** | **0.7421** | **0.8527** | 0.8552 | 13.87 | **0.9546** |
| Tổn thương rõ | 256×256 | 0.8660 | 0.7669 | 0.8050 | **0.9455** | 23.08 | 0.9599 |
| | 512×512 | **0.8826** | **0.7925** | **0.8477** | 0.9261 | 22.79 | **0.9629** |

*(HD95 tính theo điểm ảnh ở từng độ phân giải riêng, nên không so trực tiếp được giữa hai cột.)*

Tăng độ phân giải không mang lại lợi ích đồng đều: nhóm tổn thương nhỏ được lợi nhiều nhất (+0,1431 Dice, Precision tăng từ 0,5687 lên 0,8285), còn nhóm tổn thương rõ chỉ tăng 0,0166 vì hiệu năng ở cả hai độ phân giải đã ở mức cao. PGA-UNet đã vượt SAM-Med2D ngay ở 256×256, còn 512×512 chủ yếu giúp thêm cho nhóm tổn thương nhỏ. Điều này cho thấy lợi thế của PGA-UNet trên tổn thương nhỏ chủ yếu đến từ kiến trúc, còn độ phân giải cao chỉ đóng góp thêm.

## A.3 Trên FracAtlas

Cùng ba nhóm thí nghiệm trên được lặp lại trên FracAtlas. Đây là bộ dữ liệu gãy xương nên hình thái tổn thương khác khá nhiều so với khối u xương của BTXRD. Tất cả mô hình đều được huấn luyện lại từ đầu, không dùng lại trọng số từ BTXRD. Mục tiêu ở đây không phải kiểm tra tổng quát hóa liên miền theo kiểu huấn luyện ở một nơi rồi suy luận ở nơi chưa từng thấy, mà là xem xét thiết kế của PGA-UNet có tái lập được xu hướng quan sát trên BTXRD hay chỉ là trùng hợp ngẫu nhiên của riêng bộ dữ liệu đó.

### A.3.1 Đóng góp của kiến trúc và câu nhắc

| Cấu hình | PSG | Chú ý trên kết nối tắt | Câu nhắc | Bao trọn↑ | Lệch tâm↑ | Hỗn hợp↑ |
|---|---|---|---|---|---|---|
| U-Net+Concat (Gaussian) | ✗ | Không | Gaussian | 0.8131 | 0.6579 | 0.7573 |
| U-Net+PSG | ✓ | Không | Gaussian | 0.8211 | 0.6760 | 0.7700 |
| U-Net+CAD | ✗ | CAD | Gaussian | 0.7806 | 0.6551 | 0.7271 |
| PGA-UNet (nhị phân) | ✓ | CAD | Nhị phân | 0.7907 | 0.6845 | 0.7474 |
| U-Net+Concat (nhị phân) | ✗ | Không | Nhị phân | 0.8203 | 0.6630 | 0.7658 |
| **PGA-UNet** | ✓ | CAD | Gaussian | 0.8169 | **0.7850** | **0.8129** |
| U-Net+PSG+Cổng chú ý nguyên bản | ✓ | Nguyên bản | Gaussian | **0.8351** | 0.6927 | 0.7838 |
| U-Net+Cổng chú ý nguyên bản | ✗ | Nguyên bản | Gaussian | 0.7896 | 0.6630 | 0.7378 |

Xu hướng tổng thể giống với BTXRD: PGA-UNet không đứng đầu ở Bao trọn (0,8169, thấp hơn U-Net+PSG+cổng chú ý nguyên bản với 0,8351) nhưng đứng đầu rõ rệt ở hai kịch bản có sai lệch: 0,7850 ở Lệch tâm, 0,8129 ở Hỗn hợp, cải thiện lần lượt 0,1271 và 0,0556 so với ghép kênh thông thường.

Khác biệt so với BTXRD nằm ở vai trò riêng lẻ của từng thành phần. Trên FracAtlas, PSG khi đứng một mình có ích rõ hơn hẳn (+0,008 đến +0,018 ở cả ba kịch bản, trong khi trên BTXRD mức chênh gần như bằng 0), có thể do vùng gãy xương nhỏ và mảnh hưởng lợi rõ từ tín hiệu không gian ở tầng mã hóa. Ngược lại, CAD khi đứng một mình (không có PSG) làm giảm Dice 0,0028–0,0325 so với ghép kênh, ngược chiều so với BTXRD, nơi CAD một mình vẫn nhỉnh hơn. Cổng chú ý nguyên bản có xu hướng tương tự, chỉ phát huy hiệu quả khi kết hợp với PSG (0,8351 ở Bao trọn, cao nhất trong bảng này).

Điểm chung quan trọng nhất giữa hai bộ dữ liệu: CAD và Gaussian chỉ thật sự tạo khác biệt lớn ở Lệch tâm khi đi cùng PSG. Từng thành phần riêng lẻ dao động nhiều theo dữ liệu, nhưng bộ ba kết hợp thì ổn định. Số liệu kiểm định thống kê cho phần này nằm ở Mục A.4.

### A.3.2 Độ ổn định qua kiểm chứng chéo ngẫu nhiên lặp lại

Cùng thủ tục kiểm chứng chéo ngẫu nhiên lặp lại 4 lần, số mẫu đa giác ở mỗi lần dao động nhẹ từ 89 đến 95 vì số vùng gãy trên mỗi ảnh không giống nhau.

| Lần | Số mẫu | Bao trọn↑ | Lệch tâm↑ | Hỗn hợp↑ |
|---|---|---|---|---|
| 1 | 89 | 0.8127 | 0.8025 | 0.8060 |
| 2 | 93 | 0.8026 | 0.7862 | 0.7981 |
| 3 | 95 | 0.8200 | 0.7930 | 0.8161 |
| 4 | 90 | 0.8222 | 0.7798 | 0.8082 |
| **Trung bình ± độ lệch chuẩn** | **91.75 ± 2.38** | **0.8144 ± 0.0077** | **0.7904 ± 0.0084** | **0.8071 ± 0.0064** |

| Kịch bản | Dice↑ | IoU↑ | Precision↑ | Recall↑ | HD95↓ (px) | CBL↑ |
|---|---|---|---|---|---|---|
| Bao trọn | 0.8144 | 0.6955 | 0.7735 | 0.8809 | 8.28 | 0.9541 |
| Lệch tâm | 0.7904 | 0.6627 | 0.7589 | 0.8460 | 9.57 | 0.9337 |
| Hỗn hợp (70% Bao trọn + 30% Lệch tâm) | 0.8071 | 0.6859 | 0.7671 | 0.8723 | 8.84 | 0.9476 |

Độ lệch chuẩn Dice ở đây là 0,0064–0,0084, thấp hơn cả BTXRD, và Dice trung bình qua 4 lần chỉ chênh 0,0025–0,0058 so với tập kiểm thử giữ riêng. Điều này cho thấy độ ổn định trước cách chia dữ liệu không phải là đặc điểm riêng của BTXRD.

### A.3.3 Theo đặc tính tổn thương

So với BTXRD, quy mô mỗi nhóm phải thu nhỏ (36 ảnh/nhóm thay vì 50, vì FracAtlas chỉ có 72 ảnh kiểm thử) nhưng xu hướng quan sát được gần như tương tự.

| Nhóm | Mô hình | Dice↑ | IoU↑ | Precision↑ | Recall↑ | HD95↓ (px) | CBL↑ |
|---|---|---|---|---|---|---|---|
| TOP-DICE (N=36) | U-Net | 0.6532 | 0.5018 | 0.6266 | 0.7500 | 82.10 | 0.7595 |
| | PGA-UNet | **0.8324** | **0.7179** | **0.7920** | **0.8975** | **8.04** | **0.9600** |
| BOTTOM-DICE (N=36) | U-Net | 0.1130 | 0.0654 | 0.1397 | 0.1784 | 191.54 | 0.1662 |
| | PGA-UNet | **0.8015** | **0.6726** | **0.7370** | **0.8974** | **6.85** | **0.9493** |

U-Net giảm từ Dice 0,6532 ở nhóm hoạt động tốt nhất xuống 0,1130 ở nhóm hoạt động kém nhất, trong khi PGA-UNet gần như không thay đổi (0,8324 → 0,8015).

| Nhóm | Mô hình | Dice↑ | IoU↑ | Precision↑ | Recall↑ | HD95↓ (px) | CBL↑ |
|---|---|---|---|---|---|---|---|
| Tổn thương nhỏ | SAM-Med2D | 0.4395 | 0.3141 | **0.7793** | 0.3507 | 30.94 | 0.8210 |
| | PGA-UNet | **0.7584** | **0.6178** | 0.6652 | **0.9006** | **6.04** | **0.9125** |
| Biên mờ | SAM-Med2D | 0.5787 | 0.4132 | **0.7814** | 0.4953 | 14.80 | 0.9005 |
| | PGA-UNet | **0.7926** | **0.6627** | 0.7118 | **0.9060** | **9.41** | **0.9566** |
| Tổn thương rõ | SAM-Med2D | 0.7677 | 0.6253 | **0.8451** | 0.7178 | 9.86 | 0.9373 |
| | PGA-UNet | **0.8358** | **0.7213** | 0.8105 | **0.8801** | **8.17** | **0.9563** |

So với SAM-Med2D ở cùng 256×256, khoảng cách thay đổi theo độ khó tương tự trên BTXRD: 0,319 Dice ở tổn thương nhỏ, còn 0,068 ở tổn thương rõ, vẫn theo cùng xu hướng Precision/Recall đảo chiều giữa hai mô hình.

| Nhóm | Độ phân giải | Dice↑ | IoU↑ | Precision↑ | Recall↑ | HD95↓ (px) | CBL↑ |
|---|---|---|---|---|---|---|---|
| Tổn thương nhỏ | 256×256 | 0.7584 | 0.6178 | 0.6652 | 0.9006 | 6.04 | 0.9125 |
| | 512×512 | **0.8028** | **0.6756** | **0.7269** | **0.9150** | **5.05** | **0.9400** |
| Biên mờ | 256×256 | 0.7926 | 0.6627 | 0.7118 | **0.9060** | 9.41 | **0.9566** |
| | 512×512 | **0.8039** | **0.6775** | **0.7439** | 0.8925 | **9.29** | 0.9552 |
| Tổn thương rõ | 256×256 | 0.8358 | 0.7213 | 0.8105 | **0.8801** | 8.17 | 0.9563 |
| | 512×512 | **0.8404** | **0.7280** | **0.8203** | 0.8786 | **8.09** | **0.9626** |

Tăng độ phân giải lên 512×512 vẫn ưu ái tổn thương nhỏ nhất (+0,0444 Dice) hơn hẳn hai nhóm còn lại (+0,0113 và +0,0046), khớp với BTXRD và cho thấy thêm đây là xu hướng của kiến trúc/bài toán chứ không phải trùng hợp của riêng một bộ dữ liệu.

## A.4 Nhìn cả hai bộ dữ liệu: kiểm định thống kê và kết luận

Toàn bộ nhận xét ở trên đến giờ đều dựa vào chênh lệch Dice trung bình. Để xem chênh lệch đó có đáng tin ở cấp từng ảnh hay không, sáu cặp cấu hình ứng với các câu hỏi kiến trúc chính được đưa qua kiểm định Wilcoxon signed-rank, bắt cặp Dice theo ảnh, lặp lại cho ba kịch bản và cả hai bộ dữ liệu, tổng cộng 36 phép kiểm định. Giá trị p ở đây là p thô, chưa hiệu chỉnh cho việc kiểm định nhiều lần, nên chỉ nên đọc p<0,001 là bằng chứng chắc chắn, còn p quanh 0,05 nên xem như gợi ý hơn là kết luận.

| Cặp cấu hình | Kịch bản | ΔDice BTXRD | p BTXRD | ΔDice FracAtlas | p FracAtlas |
|---|---|---|---|---|---|
| U-Net + Cổng chú ý nguyên bản − U-Net+Concat(Gaussian) | Bao trọn | −0.0024 | 0,255 | −0.0235 | <0,001 |
| | Lệch tâm | −0.0050 | 0,607 | +0.0050 | 0,255 |
| | Hỗn hợp | −0.0023 | 0,395 | −0.0195 | <0,001 |
| U-Net + CAD − U-Net+Cổng chú ý nguyên bản | Bao trọn | +0.0122 | <0,001 | −0.0089 | 0,025 |
| | Lệch tâm | +0.0092 | 0,152 | −0.0079 | 0,141 |
| | Hỗn hợp | +0.0098 | 0,003 | −0.0107 | 0,023 |
| U-Net + PSG + Cổng chú ý nguyên bản − U-Net + PSG | Bao trọn | +0.0007 | 0,129 | +0.0140 | 0,009 |
| | Lệch tâm | −0.0030 | 0,376 | +0.0167 | 0,005 |
| | Hỗn hợp | +0.0011 | 0,074 | +0.0138 | 0,002 |
| PGA-UNet (Gaussian) − U-Net + PSG + Cổng chú ý nguyên bản | Bao trọn | −0.0073 | 0,025 | −0.0182 | <0,001 |
| | Lệch tâm | **+0.1065** | **<0,001** | **+0.0924** | **<0,001** |
| | Hỗn hợp | +0.0388 | 0,001 | +0.0291 | 0,161 |
| U-Net + Concat (Gaussian) − U-Net + Concat (nhị phân) | Bao trọn | −0.0018 | 0,896 | −0.0072 | 0,007 |
| | Lệch tâm | +0.0052 | 0,013 | −0.0050 | 0,284 |
| | Hỗn hợp | +0.0015 | 0,226 | −0.0085 | 0,006 |
| PGA-UNet (Gaussian) − PGA-UNet (nhị phân) | Bao trọn | −0.0173 | <0,001 | +0.0262 | <0,001 |
| | Lệch tâm | **+0.0990** | **<0,001** | **+0.1005** | **<0,001** |
| | Hỗn hợp | +0.0293 | 0,012 | +0.0655 | <0,001 |

Kết quả rõ và nhất quán nhất giữa hai bộ dữ liệu: thay cổng chú ý nguyên bản bằng CAD (khi đã có PSG) làm Dice tăng 0,1065 trên BTXRD và 0,0924 trên FracAtlas ở Lệch tâm, cả hai đều p<0,001. Gaussian so với nhị phân trong cấu hình đầy đủ cho kết quả tương tự: +0,0990 và +0,1005 ở Lệch tâm, cũng p<0,001 ở cả hai bộ dữ liệu. Đây là hai kết quả duy nhất trong toàn bảng vừa có mức chênh lớn, vừa có ý nghĩa thống kê mạnh trên cả hai bộ dữ liệu: CAD và Gaussian giúp mô hình duy trì hiệu năng ổn định hơn khi câu nhắc bị lệch, và đây không phải là hiện tượng ngẫu nhiên của riêng một bộ dữ liệu.

Ngoài hai kết quả trên, các so sánh còn lại không cho một xu hướng rõ ràng. Vai trò riêng lẻ của PSG hay cổng chú ý nguyên bản đổi chiều tùy bộ dữ liệu: CAD một mình nhỉnh hơn cổng chú ý nguyên bản trên BTXRD nhưng lại thấp hơn trên FracAtlas ở cùng kịch bản. Mức chênh ở những trường hợp này đều dưới 0,02 Dice, nên chưa đủ cơ sở để coi là một quy luật kiến trúc chung. Đây cũng chỉ là so sánh riêng trong từng bộ dữ liệu, không phải một kiểm định tương tác chính thức giữa kiến trúc và loại dữ liệu, nên chưa thể khẳng định có tương tác thống kê thật sự giữa hai yếu tố này.

Về độ ổn định, kiểm chứng chéo ngẫu nhiên lặp lại 4 lần trên cả hai bộ dữ liệu đều cho độ lệch chuẩn Dice dưới 0,012, thấp hơn rõ rệt so với mức chênh lệch giữa các cấu hình. Tuy vậy, đây là hai loại biến động khác nhau: một do cách chia dữ liệu, một do thay đổi kiến trúc; vì vậy không nên gộp chung thành một tỷ lệ tín hiệu trên nhiễu.

Tóm lại, trên cả hai bộ dữ liệu, PGA-UNet được huấn luyện lại độc lập, không chia sẻ trọng số, và vẫn giữ đúng một xu hướng: chấp nhận giảm nhẹ hiệu năng ở Bao trọn để đổi lấy lợi thế lớn và có ý nghĩa thống kê ở Lệch tâm và Hỗn hợp. Đây là bằng chứng về khả năng tái lập của thiết kế trên hai loại tổn thương khác nhau (u xương và gãy xương), chứ chưa phải bằng chứng tổng quát hóa liên miền theo nghĩa huấn luyện ở một nơi rồi suy luận trên miền chưa từng thấy.

---

# PHỤ LỤC B: ĐÁNH GIÁ LUỒNG XỬ LÝ HAI GIAI ĐOẠN

Phụ lục B trả lời một câu hỏi khác: nếu đặt PGA-UNet phía sau một bước sàng lọc tự động là Gatekeeper, tức một EfficientNet-B3 dùng để phân loại ảnh bình thường/bất thường, thì lỗi ở bước sàng lọc sẽ ảnh hưởng thế nào đến kết quả phân đoạn cuối cùng. Cần nói rõ ngay từ đầu rằng Gatekeeper không phải đóng góp kiến trúc chính của khóa luận. Phần này cũng không nhằm chứng minh hiệu năng của một hệ thống chẩn đoán tự động hoàn chỉnh, mà chỉ xem xét lỗi định tuyến ảnh hưởng ra sao đến toàn bộ luồng xử lý khi chưa có bác sĩ chẩn đoán ảnh can thiệp lại.

## B.1 Trên BTXRD

| Chỉ số | Kết quả |
|---|---|
| Accuracy | 87,73% |
| Precision | 86,53% |
| Sensitivity | 89,30% |
| Specificity | 86,17% |
| F1-score | 87,90% |
| AUC-ROC | 0,9421 |

AUC-ROC 0,9421 và Accuracy 87,73% cho thấy Gatekeeper phân biệt khá tốt hai loại ảnh trên BTXRD. Nhưng ở ngưỡng mặc định 0,5, vẫn có 20/187 ảnh bệnh lý bị bỏ sót (Sensitivity 89,30%), đủ để cho thấy không nên dùng Gatekeeper như một bộ lọc tự động loại bỏ hoàn toàn ảnh âm tính mà không qua bước xem xét lại.

Để xem sai số ở bước sàng lọc lan xuống kết quả cuối thế nào, khóa luận tính một chỉ số Dice toàn luồng có phạt lỗi định tuyến:

$$\mathrm{Dice}_{\text{pipeline}} = \frac{\sum_{i \in \text{TP}} \mathrm{Dice}_{\text{img}}(i)}{N_{\text{TP}} + N_{\text{FP}} + N_{\text{FN}}}$$

(ảnh bệnh lý bị bỏ sót và ảnh bình thường bị chuyển nhầm đều đóng góp giá trị 0 vào tử số).

| Thống kê | Giá trị |
|---|---|
| Tổng số ảnh | 375 |
| TP / FP / FN / TN | 167 / 26 / 20 / 162 |
| Dice của PGA-UNet trên ảnh TP | 0,8626 |
| **Dice toàn luồng có phạt lỗi định tuyến** | **0,6763** |
| IoU toàn luồng có phạt lỗi định tuyến | 0,6003 |

Giả sử không có bác sĩ chẩn đoán ảnh nào sửa lại quyết định của Gatekeeper, tức xét trong kịch bản xấu nhất chứ không phải quy trình thực tế đã đề xuất ở Chương 3, Dice toàn luồng giảm từ 0,8626 xuống 0,6763. Phần giảm 0,1863 này đến từ cả hai loại lỗi định tuyến: 26 ảnh bình thường bị chuyển nhầm và 20 ảnh bệnh lý bị bỏ sót, cả hai đều được tính là 0 trong công thức trên. Trong hai loại lỗi này, ảnh bệnh lý bị bỏ sót (FN) đáng ngại hơn về mặt lâm sàng, vì đó là ca bệnh không bao giờ đến được PGA-UNet. Nhìn chung, mô-đun phân đoạn vẫn hoạt động ổn định; vấn đề chính nằm ở bước sàng lọc phía trước.

## B.2 Trên FracAtlas

Gatekeeper giữ nguyên kiến trúc và quy trình huấn luyện, chỉ huấn luyện lại hoàn toàn trên FracAtlas, dữ liệu mất cân bằng hơn nhiều (72 ảnh bệnh lý trên tổng 409, so với gần 50/50 của BTXRD).

| Chỉ số | Kết quả |
|---|---|
| Accuracy | 88,26% |
| Precision | 65,38% |
| Sensitivity | 70,83% |
| Specificity | 91,99% |
| F1-score | 68,00% |
| AUC-ROC | 0,9132 |

AUC-ROC vẫn khá (0,9132), nhưng Sensitivity giảm rõ rệt xuống 70,83%, tương ứng 21/72 ảnh bệnh lý bị bỏ sót. Ngược lại, 310/337 ảnh bình thường được phân loại đúng, Specificity 91,99%. Có thể thấy trên dữ liệu mất cân bằng, mô hình có xu hướng thiên về dự đoán an toàn (nhãn bình thường), đồng thời cũng khó nhận diện các đường gãy nhỏ và mảnh hơn.

| Thống kê | Giá trị |
|---|---|
| Tổng số ảnh | 409 |
| Ảnh bệnh lý / ảnh bình thường | 72 / 337 |
| TP / FP / FN / TN | 51 / 27 / 21 / 310 |
| Dice của PGA-UNet trên ảnh TP | 0,8211 |
| **Dice toàn luồng có phạt lỗi định tuyến** | **0,4230** |
| IoU toàn luồng có phạt lỗi định tuyến | 0,3611 |

Hệ quả dây chuyền rõ hơn nhiều so với BTXRD: Dice toàn luồng chỉ còn 0,4230, dù PGA-UNet vẫn đạt 0,8211 trên đúng những ảnh được chuyển đến nó. Khi hạ ngưỡng phân loại xuống 0,3, Sensitivity tăng lên 84,72%, nhưng Specificity giảm còn 84,87%, cho thấy sự đánh đổi thường gặp giữa bỏ sót và báo động nhầm, không tồn tại một ngưỡng phân loại tối ưu cho cả hai chỉ số.

## B.3 Kết luận chung

Kết quả trên cả hai bộ dữ liệu cho thấy cùng một xu hướng: bản thân PGA-UNet không hề yếu đi khi đặt sau Gatekeeper, nhưng sai số ở bước sàng lọc lan trực tiếp xuống kết quả cuối, và mức độ ảnh hưởng phụ thuộc nhiều vào việc dữ liệu có cân bằng hay không. FracAtlas mất cân bằng hơn nên chịu ảnh hưởng nặng hơn hẳn BTXRD. Đây cũng là lý do trong quy trình đề xuất, Gatekeeper chỉ nên đóng vai trò gợi ý ưu tiên; quyết định chuyển bước và cung cấp hộp giới hạn vẫn cần bác sĩ chẩn đoán ảnh xác nhận, không nên để hệ thống tự quyết định hoàn toàn.
