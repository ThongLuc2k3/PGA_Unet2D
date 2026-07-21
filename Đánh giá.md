## Ghi chú

- File này là bản nhận xét/phản biện học thuật, không phải mô tả trạng thái cuối cùng của report.
- Một số mục dưới đây đã được xử lý trong `Report/`; vì vậy cần đối chiếu với report hiện tại trước khi dùng lại nguyên văn.
- Cách gọi hiện được ưu tiên trong report:
  - `câu nhắc` hoặc `câu nhắc trực quan`;
  - `mô-đun` cho các thành phần hệ thống;
  - `Gatekeeper` là tên riêng của mô-đun sàng lọc hỗ trợ;
  - kết quả chính của PGA-UNet được diễn giải trong phạm vi **phân đoạn có hướng dẫn bằng hộp giới hạn**.

Nêu:
1.Các đóng góp của luận văn
2. Nêu các lỗi sai nghiêm trọng của luận văn trong phương pháp, thử nghiệm, cách trình bày.
Worked for 5m 16s

Tôi đánh giá trên toàn bộ bản khóa luận 105 trang, đặc biệt các Chương 3-5. Nhìn chung, khóa luận có ý tưởng kỹ thuật rõ, khối lượng thực nghiệm khá tốt, nhưng một số kết luận hiện đang mạnh hơn mức mà thiết kế thực nghiệm cho phép.

1. Các đóng góp của luận văn
1.1. Đề xuất mô hình phân đoạn tương tác PGA-UNet

Khóa luận xây dựng PGA-UNet, một mô hình CNN hạng nhẹ nhận hai đầu vào:

ảnh X-quang;
hộp giới hạn do người dùng cung cấp quanh vùng nghi ngờ.

Điểm hợp lý là mô hình không bắt buộc phải tự động tìm tổn thương trên toàn ảnh, mà khai thác thông tin định vị sơ bộ từ người dùng để thực hiện phân đoạn chính xác ở cấp độ pixel.

1.2. Biểu diễn hộp giới hạn bằng bản đồ nhiệt Gaussian dạng cao nguyên

Thay vì sử dụng hộp nhị phân có biên cứng, khóa luận:

chuyển hộp giới hạn thành mặt nạ nhị phân;
làm mềm biên bằng bộ lọc Gaussian;
giữ vùng giá trị tương đối cao trong toàn bộ hộp.

Biểu diễn này nhằm giảm sự phụ thuộc cứng vào đường biên hộp và tăng khả năng chịu sai lệch khi người dùng vẽ hộp chưa chính xác.

Đây là một thành phần có ý nghĩa, đặc biệt khi kết hợp với PSG và CAD. Tuy nhiên, chỉ riêng việc làm mịn hộp bằng Gaussian chưa đủ để được xem là đóng góp mới mạnh, vì tư tưởng dùng bản đồ mềm và spatial conditioning đã xuất hiện trong nhiều nghiên cứu trước.

1.3. Tích hợp câu nhắc vào bộ mã hóa bằng PSG

Khóa luận đề xuất Prompt Spatial Gate – PSG, đưa bản đồ câu nhắc vào nhiều tầng của encoder thay vì chỉ nối với ảnh ở đầu vào.

PSG cho phép đặc trưng mã hóa chịu ảnh hưởng trực tiếp của vị trí hộp giới hạn. Đây là cách giải quyết hợp lý cho vấn đề tín hiệu câu nhắc có thể suy giảm sau nhiều tầng tích chập và giảm mẫu.

1.4. Tích hợp câu nhắc vào bộ giải mã bằng CAD

Conditional Attention Decoder – CAD mở rộng Attention Gate bằng cách đưa đặc trưng câu nhắc vào tín hiệu điều khiển tại các skip connection.

Đóng góp kỹ thuật đáng chú ý nhất của khóa luận không phải PSG hoặc CAD đứng riêng, mà là quy trình duy trì câu nhắc xuyên suốt encoder-decoder:

PSG điều biến đặc trưng ở encoder;
CAD điều kiện hóa attention ở decoder;
bản đồ Gaussian cung cấp tín hiệu không gian mềm.

Kết quả ablation cho thấy tổ hợp này có lợi rõ nhất khi hộp bị lệch, chứ không nhất thiết đạt kết quả cao nhất khi hộp hoàn toàn lý tưởng.

1.5. Khảo sát tính bền bỉ trước sai lệch câu nhắc

Khóa luận xây dựng ba kịch bản:

Bao trọn;
Lệch tâm;
Hỗn hợp 70% Bao trọn và 30% Lệch tâm.

Đây là điểm tốt vì nghiên cứu không chỉ báo cáo kết quả với hộp hoàn hảo mà còn xem xét sai số thao tác người dùng. Kết quả trên cả BTXRD và FracAtlas cho thấy mô hình đầy đủ suy giảm ít hơn một số cấu hình đối sánh khi hộp bị lệch.

1.6. Đánh giá trên hai dạng tổn thương khác nhau

Mô hình được huấn luyện và đánh giá riêng trên:

BTXRD: khối u xương;
FracAtlas: gãy xương.

Việc tái lập xu hướng trên hai bộ dữ liệu là bằng chứng tốt về tính nhất quán của thiết kế trên hai miền dữ liệu. Tuy nhiên, đây chưa phải tổng quát hóa liên miền, vì mô hình được huấn luyện lại trên từng bộ dữ liệu.

1.7. Thực hiện nhiều phân tích thực nghiệm

Khóa luận có khối lượng thực nghiệm tương đối phong phú:

so sánh với U-Net, Attention U-Net và SAM-Med2D;
ablation tám cấu hình;
khảo sát 256×256 và 512×512;
đánh giá chéo 4-fold;
Wilcoxon bắt cặp theo ảnh;
phân tích nhóm tổn thương nhỏ, biên mờ, tổn thương rõ;
phân tích ảnh mà U-Net hoạt động tốt hoặc thất bại.

Đây là ưu điểm đáng ghi nhận đối với một khóa luận cử nhân.

1.8. Khảo sát luồng hai giai đoạn với Gatekeeper

Khóa luận bổ sung EfficientNet-B3 để sàng lọc ảnh bình thường/bệnh lý trước PGA-UNet. Phần này có giá trị như một khảo sát tích hợp hệ thống, đồng thời chỉ ra rằng lỗi sàng lọc có thể làm giảm mạnh hiệu năng toàn luồng.

Tuy nhiên, Gatekeeper nên được xem là nội dung mở rộng, không phải đóng góp khoa học trung tâm.

2. Các lỗi sai nghiêm trọng
A. Lỗi nghiêm trọng trong phương pháp
2.1. Câu nhắc kiểm thử được tạo từ nhãn thật — điều kiện “oracle prompt”

Đây là vấn đề quan trọng nhất.

Ở giai đoạn kiểm thử, hộp giới hạn được sinh từ chính mặt nạ ground truth. Đối với ảnh có nhiều tổn thương, hệ thống còn:

biết trước số lượng tổn thương;
tạo một hộp cho từng vùng ground truth;
chạy mô hình riêng cho từng hộp;
hợp nhất các mặt nạ dự đoán.

Như vậy, mô hình được cung cấp gần như chính xác:

vị trí tổn thương;
số tổn thương;
vùng không gian cần xử lý.

Thiết lập này phù hợp để đánh giá chất lượng phân đoạn khi đã có hộp đúng, nhưng không thể đại diện cho toàn bộ hệ thống phát hiện và phân đoạn tổn thương thực tế.

Đặc biệt, việc so sánh PGA-UNet có hộp ground truth với U-Net và Attention U-Net không có bất kỳ thông tin định vị nào là không công bằng. Phần chênh lệch Dice rất lớn chủ yếu phản ánh lợi ích của thông tin hộp, không chỉ phản ánh ưu điểm của PSG và CAD.

Cần sửa:

Tách rõ hai bài toán: phân đoạn tự động và phân đoạn có hộp hướng dẫn.
Baseline chính phải là các mô hình cùng nhận hộp, chẳng hạn U-Net+Concat, bbox-conditioned U-Net, DeepIGeoS hoặc các mô hình prompt-aware khác.
Không dùng mức tăng so với U-Net không có hộp làm bằng chứng trực tiếp cho tính mới của kiến trúc.
2.2. Kết luận “bền bỉ” chưa được kiểm chứng đúng nghĩa

Các hộp sai lệch đều được sinh bằng một quy tắc nhân tạo tương đối đơn giản:

dịch đúng 30% kích thước hộp;
mở rộng trong khoảng 15-45%;
Hỗn hợp cố định tỷ lệ 70/30.

Báo cáo còn cho biết quy tắc này được dùng trong cả huấn luyện và đánh giá. Vì vậy, mô hình có thể đã học đúng phân bố nhiễu mà nó gặp ở kiểm thử.

Đây mới là robustness đối với một bộ sinh nhiễu đã biết, chưa phải khả năng bền bỉ trước thao tác người dùng thực tế.

Cần sửa:

Huấn luyện một mô hình duy nhất trên tập nhiễu đa dạng.
Kiểm thử trên các mức dịch chưa xuất hiện khi huấn luyện: 10%, 20%, 40%, 60%.
Kiểm thử hộp quá rộng, quá hẹp, chỉ giao một phần, không giao tổn thương.
Mỗi ảnh cần sinh nhiều hộp ngẫu nhiên và báo cáo trung bình ± độ lệch chuẩn.
Tốt nhất cần có hộp do nhiều người dùng hoặc bác sĩ vẽ.
2.3. PSG không thực sự “đóng cổng” hoặc ức chế vùng không liên quan

PSG được định nghĩa gần dạng:

x
~
=x⊙(1+αA),

với A qua Sigmoid và α≥0.

Hệ số nhân vì vậy không nhỏ hơn 1. Cơ chế này chỉ có thể:

giữ nguyên;
hoặc khuếch đại đặc trưng.

Nó không thể giảm đặc trưng nền hoặc ức chế vùng ngoài câu nhắc. Vì thế, cách gọi “gate” và một số diễn giải về việc giảm ảnh hưởng vùng không liên quan chưa hoàn toàn phù hợp với công thức.

Cần sửa:

Gọi đúng là residual spatial amplification; hoặc
dùng cổng có khả năng cả tăng và giảm, chẳng hạn x⊙(ϵ+A);
hoặc dùng điều biến affine x⊙γ(H)+β(H);
trực quan hóa bản đồ PSG để chứng minh vùng nào được tăng hoặc giảm.
2.4. Các tham số câu nhắc phụ thuộc pixel, gây nhiễu khi so sánh độ phân giải

Khóa luận cố định:

Gaussian kernel k=31;
mở rộng thêm 5 pixel;
ngưỡng 0,5;

cho cả ảnh 256×256 và 512×512.

Nhưng 31 pixel và 5 pixel có ý nghĩa tương đối khác nhau ở hai độ phân giải. Bản đồ câu nhắc ở 256×256 sẽ bị làm mịn mạnh hơn về tỷ lệ so với ảnh 512×512.

Do đó, thí nghiệm “ảnh hưởng độ phân giải” không chỉ thay đổi độ phân giải ảnh mà đồng thời thay đổi:

độ rộng tương đối của Gaussian;
biên mở rộng tương đối;
mức độ khuếch tán của câu nhắc.

Đây là biến gây nhiễu nghiêm trọng.

Cần sửa: xác định kernel, margin và độ dịch theo tỷ lệ chiều rộng/chiều cao ảnh hoặc kích thước hộp, không dùng số pixel cố định.

2.5. Công thức CAD và mô tả triển khai chưa nhất quán

Trong phần công thức, CAD sử dụng các ký hiệu như:

α
l
CAD
	​

;
w
l
	​

;
đặc trưng p
enc
l
	​

;
hệ số c
l
	​

.

Nhưng phần cấu hình lại đề cập “hệ số kết nối dư của CAD λ=0,3” mà λ không được thể hiện rõ trong công thức tương ứng.

Ngoài ra chưa mô tả đủ:

số kênh của từng tầng;
cấu trúc chính xác của f
enc
	​

;
c
l
	​

 là scalar, vector theo kênh hay bản đồ;
vị trí normalization;
tham số nào học được, tham số nào cố định.

Điều này làm phương pháp khó tái tạo.

2.6. Không xử lý trường hợp câu nhắc sai hoàn toàn hoặc vùng không có tổn thương

Mô hình phân đoạn chỉ được huấn luyện bằng ảnh bệnh lý và hộp sinh từ ground truth. Vì vậy, mô hình chưa học các trường hợp:

hộp không chứa tổn thương;
người dùng khoanh nhầm vùng;
ảnh bình thường nhưng vẫn cung cấp hộp;
hộp chỉ chứa cấu trúc giải phẫu giống tổn thương.

Trong thực tế đây là các trường hợp rất quan trọng. Mô hình có thể bị ép tạo ra một mặt nạ dương tính chỉ vì luôn được huấn luyện với hộp có tổn thương.

Cần bổ sung:

negative boxes;
ảnh bình thường với mặt nạ rỗng;
loss phạt diện tích dự đoán sai;
khả năng trả về “không có vùng phù hợp”;
confidence hoặc uncertainty map.
2.7. Thay đổi kích thước ảnh chưa làm rõ việc giữ tỷ lệ hình học

Báo cáo chỉ nói đưa ảnh về 256×256 hoặc 512×512, nhưng không nêu rõ:

resize trực tiếp về hình vuông;
hay giữ tỷ lệ và padding;
cách chuẩn hóa cường độ;
ảnh một kênh được đưa vào mạng ra sao.

Nếu resize méo trực tiếp, hình dạng xương và tổn thương có thể bị biến dạng. Đây là vấn đề đáng kể đối với phân đoạn đường gãy và khối u.

B. Lỗi nghiêm trọng trong thực nghiệm
2.8. Baseline chính không công bằng

Bảng so sánh chính đặt cạnh nhau:

U-Net/Attention U-Net: chỉ nhận ảnh;
PGA-UNet: nhận ảnh và hộp gần ground truth.

Vì đầu vào không tương đương, không thể kết luận mức tăng Dice từ 0,47 lên 0,86 chủ yếu do kiến trúc PGA-UNet.

Chính ablation cho thấy chỉ cần U-Net+Concat nhận câu nhắc cũng đạt Dice rất cao trong kịch bản Bao trọn. Trên BTXRD, U-Net+CAD còn đạt 0,8861, cao hơn PGA-UNet 0,8607; trên FracAtlas, PSG+Cổng chú ý nguyên bản cũng cao hơn PGA-UNet khi hộp lý tưởng.

Do đó, kết luận đúng phải là:

PGA-UNet có ưu thế chủ yếu trong kịch bản hộp bị lệch theo bộ sinh nhiễu đã định nghĩa, không phải luôn có độ chính xác cao nhất.

2.9. Phân chia ở cấp độ ảnh, chưa chứng minh không rò rỉ theo bệnh nhân

Khóa luận chỉ xác nhận giữ các polygon của cùng một ảnh trong một phân vùng. Không thấy mô tả:

patient-level split;
study-level split;
loại bỏ ảnh trùng hoặc ảnh cùng bệnh nhân;
kiểm soát nhiều góc chụp của cùng ca.

Nếu một bệnh nhân có nhiều ảnh hoặc nhiều lần chụp, chia ở cấp độ ảnh có thể làm ảnh gần giống nhau xuất hiện ở train và test.

Đây là nguy cơ rò rỉ dữ liệu y khoa nghiêm trọng. Ít nhất báo cáo phải chứng minh mỗi bộ dữ liệu không có patient ID lặp giữa các tập.

2.10. Không đánh giá biến thiên do khởi tạo ngẫu nhiên

Các mô hình dường như chỉ được huấn luyện một lần cho mỗi cấu hình. Không có:

nhiều random seed;
trung bình ± độ lệch chuẩn giữa các lần chạy;
khoảng tin cậy bootstrap.

Đánh giá chéo 4-fold chỉ phản ánh thay đổi cách chia dữ liệu, không phản ánh biến thiên do quá trình tối ưu.

Vì vậy, các chênh lệch nhỏ như 0,002-0,02 Dice giữa các kiến trúc có thể chỉ là nhiễu huấn luyện.

2.11. Thực hiện 36 kiểm định nhưng không hiệu chỉnh so sánh nhiều lần

Khóa luận thực hiện sáu cặp cấu hình × ba kịch bản × hai bộ dữ liệu, tổng cộng 36 phép kiểm định Wilcoxon, nhưng dùng p-value thô.

Báo cáo đã thừa nhận chưa hiệu chỉnh, nhưng vẫn diễn giải nhiều kết quả quanh ngưỡng 0,05. Điều này làm tăng xác suất phát hiện dương tính giả.

Cần sửa:

Holm-Bonferroni hoặc Benjamini-Hochberg;
báo cáo effect size;
khoảng tin cậy của chênh lệch Dice;
phân biệt rõ phân tích xác nhận và phân tích thăm dò.

Các kết quả p<0,001 có thể vẫn khá mạnh, nhưng các kết quả khoảng 0,01-0,05 chưa đáng tin nếu chưa hiệu chỉnh.

2.12. Quy trình tinh chỉnh SAM-Med2D chưa đủ để kiểm tra tính công bằng

Báo cáo chỉ nêu lớp adapter và decoder được cập nhật, nhưng thiếu:

loss cụ thể;
số epoch;
learning rate;
scheduler;
cách sinh prompt khi huấn luyện;
augmentation;
checkpoint selection;
số seed;
lớp nào đóng băng chính xác.

Do đó, chưa thể biết SAM-Med2D đã được tinh chỉnh tối ưu hay chưa. Kết luận PGA-UNet tốt hơn SAM-Med2D vì vậy chưa hoàn toàn thuyết phục và khó tái lập.

2.13. Phân tích nhóm có tính vòng tròn

Một số nhóm được chọn dựa trên kết quả của chính mô hình đang bị so sánh:

“U-Net hoạt động kém” là 50 ảnh có Dice U-Net thấp nhất;
“Biên mờ” trên FracAtlas được xác định từ các ảnh có Dice SAM-Med2D thấp.

Sau đó báo cáo PGA-UNet tốt hơn rất nhiều trong đúng các nhóm này. Kết quả như vậy gần như được bảo đảm bởi cách chọn mẫu.

Báo cáo có ghi đây là phân tích mô tả, nhưng tên nhóm “biên mờ” và cách diễn giải vẫn dễ gây hiểu nhầm.

Cần sửa: nhóm tổn thương phải được xác định độc lập bằng:

tỷ lệ diện tích tổn thương;
độ tương phản định lượng;
độ phức tạp đường biên;
đánh giá của bác sĩ;
hoặc metadata có sẵn.
2.14. Chỉ số “Dice toàn luồng” là chỉ số tự định nghĩa và dễ gây hiểu sai

Công thức:

N
TP
	​

+N
FP
	​

+N
FN
	​

∑
i∈TP
	​

Dice
i
	​

	​


không phải Dice segmentation chuẩn. Nó trộn:

lỗi phân loại của Gatekeeper;
chất lượng phân đoạn có điều kiện;
và quy ước gán 0 cho FP/FN.

TN lại không tham gia mẫu số. Vì vậy, giá trị này khó so sánh với các nghiên cứu khác và không có diễn giải hình học như Dice thông thường.

Nên báo cáo tách biệt:

sensitivity, specificity, PR-AUC của Gatekeeper;
Dice trên toàn bộ ảnh bệnh lý;
Dice có điều kiện trên ảnh được định tuyến đúng;
tỷ lệ ca bệnh có được mặt nạ đúng ở toàn luồng;
lesion-level sensitivity hoặc FROC.

Không nên gọi chỉ số tự định nghĩa này đơn giản là “Dice toàn luồng”.

2.15. Gatekeeper thiếu gần như toàn bộ mô tả huấn luyện

Phần Gatekeeper không trình bày rõ:

số ảnh train/validation;
cách chia dữ liệu;
xử lý mất cân bằng;
augmentation;
optimizer và learning rate;
số epoch;
random seed;
tiêu chí chọn checkpoint;
ngưỡng 0,5 được chọn trước hay sau khi xem dữ liệu.

Trên FracAtlas, lớp bệnh lý chỉ có 72/409 ảnh kiểm thử, nhưng không báo cáo PR-AUC hoặc calibration. Accuracy 88,26% có thể gây cảm giác tốt trong khi sensitivity chỉ 70,83%.

Đây là lỗi tái lập nghiêm trọng.

2.16. Chưa định nghĩa cách tính HD95 khi dự đoán rỗng

HD95 không xác định khi một trong hai mặt nạ rỗng. U-Net có nhiều trường hợp gần như không phát hiện tổn thương, nhưng báo cáo vẫn đưa ra các giá trị HD95 hữu hạn rất lớn.

Cần mô tả rõ:

giá trị phạt khi mask rỗng;
có loại mẫu hay không;
khoảng cách được tính trước hay sau resize;
đơn vị pixel hay mm;
cách xử lý nhiều thành phần liên thông.

Nếu không, kết quả HD95 không tái lập được.

2.17. Kết luận về mô hình hạng nhẹ chưa có bằng chứng thực nghiệm

Động lực chính của PGA-UNet là khả năng triển khai trên phần cứng hạn chế, nhưng khóa luận chỉ báo cáo khoảng ba triệu tham số, không có:

FLOPs/MACs;
thời gian suy luận;
bộ nhớ cực đại;
tốc độ trên CPU;
tốc độ trên GPU;
so sánh cùng phần cứng với SAM-Med2D.

Số tham số nhỏ không đồng nghĩa chắc chắn suy luận nhanh hoặc tiết kiệm bộ nhớ. Do đó, kết luận về khả năng triển khai thực tế chưa được chứng minh.

2.18. Loại bỏ polygon chưa được mô tả minh bạch

FracAtlas loại một số polygon vì “quá nhỏ hoặc lỗi định dạng”, nhưng không nêu:

ngưỡng thế nào là quá nhỏ;
số mẫu theo từng nguyên nhân;
có phải chính các đường gãy khó nhất bị loại hay không;
ảnh tương ứng có bị loại hoàn toàn không.

Việc loại tổn thương rất nhỏ có thể làm kết quả tốt hơn và mâu thuẫn với tuyên bố mô hình hiệu quả trên tổn thương nhỏ.

C. Lỗi nghiêm trọng trong cách trình bày
2.19. Tuyên bố ứng dụng thực tế và hỗ trợ lâm sàng còn quá mạnh

Các cụm như “khả thi trong thực tế”, “hỗ trợ bác sĩ tốt hơn” chưa được chứng minh vì:

hộp được sinh từ ground truth;
chưa có bác sĩ tham gia;
chưa đo thời gian thao tác;
chưa đánh giá khác biệt giữa người dùng;
chưa có dữ liệu bệnh viện ngoài;
chưa đo tốc độ thực thi.

Nên gọi đây là prototype kỹ thuật hoặc proof-of-concept, không phải hệ thống sẵn sàng ứng dụng.

2.20. Abstract trình bày mức tăng so với U-Net dễ gây hiểu nhầm

Abstract nhấn mạnh Dice 0,8607 so với 0,4740 của U-Net nhưng không nhấn mạnh đủ rằng:

PGA-UNet nhận hộp gần ground truth;
U-Net không nhận hộp.

Đây không phải so sánh đầu vào tương đương. Abstract nên ưu tiên so sánh với U-Net+Concat, prompt-aware baselines và SAM-Med2D cùng hộp.

2.21. Related Work quá mỏng để chứng minh tính mới

Toàn bộ khóa luận chỉ có khoảng 11 tài liệu tham khảo. Phần liên quan chủ yếu gồm:

U-Net;
Attention U-Net;
DeepIGeoS;
SAM;
SAM-Med2D;
FiLM;
SPADE.

Chưa có khảo sát đủ về:

interactive medical image segmentation;
box-guided segmentation;
prompt-conditioned U-Net;
lightweight SAM;
prompt robustness;
click/box perturbation evaluation;
segmentation xương và gãy xương gần đây.

Do đó, chưa thể xác định chắc chắn PSG, CAD hoặc tổ hợp của chúng khác gì với các cơ chế conditioning đã có.

2.22. Thiếu thông tin để tái lập

Báo cáo cần bổ sung ít nhất:

bảng chi tiết số kênh và kích thước feature map;
số tham số từng cấu hình;
thuật toán preprocessing đầy đủ;
normalization ảnh;
augmentation ảnh;
random seed;
cách tạo split;
LR scheduler;
exact SAM-Med2D fine-tuning;
exact Gatekeeper training;
quy tắc xử lý mask rỗng;
mã nguồn hoặc cấu hình chạy.

Hiện tại Algorithm 1 và 2 chỉ mô tả ở mức khái quát.

2.23. Ký hiệu và thuật ngữ chưa nhất quán

Một số điểm cần sửa:

“Conditioned Attention Decoder” và “Conditional Attention Decoder” dùng không thống nhất;
α
gate
	​

, α
PSG
	​

, λ chưa nhất quán;
λ=0,3 xuất hiện ở phần cấu hình nhưng không rõ trong công thức;
một số bảng hiển thị ký hiệu “Ö” thay cho dấu không có thành phần;
lặp câu về chi phí tính toán ở phần suy luận;
lỗi chính tả “tổn thướng”;
dùng “đánh giá chéo” và “kiểm định chéo” lẫn nhau;
viết hoa “Phân vùng” không cần thiết.
2.24. Hình kiến trúc quá nhỏ và khó kiểm tra

Hình 3.1 chứa nhiều khối, mũi tên và ký hiệu nhưng kích thước chữ rất nhỏ. Người đọc khó xác định:

PSG nằm chính xác ở đâu;
CAD nhận những tensor nào;
kích thước và số kênh;
đường đi của prompt heatmap;
vị trí residual connection.

Nên tách thành:

sơ đồ tổng quát PGA-UNet;
hình phóng to PSG;
hình phóng to CAD;
bảng kích thước tensor.
2.25. Chương thực nghiệm dài và lặp kết luận

Các nhận xét về:

CAD tốt khi hộp lệch;
Gaussian hỗ trợ robustness;
PSG và CAD bổ trợ;
Gatekeeper làm giảm toàn luồng;

được lặp lại nhiều lần ở Mục 4.3.1, 4.3.2, 4.3.3, 4.5 và 5.1.

Có thể rút gọn đáng kể bằng:

một bảng tổng hợp kết luận ablation trên hai bộ dữ liệu;
một mục thống kê chung;
chuyển các bảng phân nhóm phụ sang phụ lục.
Kết luận đánh giá

Đóng góp thực chất và có giá trị nhất của khóa luận là:

Một kiến trúc U-Net nhẹ tích hợp hộp câu nhắc vào cả encoder và decoder, cho thấy khả năng chịu được một dạng sai lệch hộp mô phỏng tốt hơn các cấu hình prompt-aware đơn giản trên hai bộ dữ liệu.

Tuy nhiên, khóa luận hiện chưa đủ cơ sở để kết luận rằng:

PGA-UNet vượt trội chung so với các mô hình phân đoạn khác;
mô hình bền bỉ với thao tác bác sĩ thực tế;
hệ thống có thể triển khai lâm sàng;
mô hình có hiệu quả tính toán tốt hơn SAM-Med2D.

Ba nội dung cần sửa ưu tiên trước khi bảo vệ hoặc viết bài báo là:

Thiết kế lại so sánh công bằng với các baseline cùng nhận hộp và giảm sự phụ thuộc vào hộp sinh từ ground truth.
Làm lại đánh giá robustness theo nhiều mức nhiễu, nhiều hộp trên mỗi ảnh, nhiều seed và hiệu chỉnh thống kê.
Bổ sung đầy đủ split, preprocessing, SAM-Med2D/Gatekeeper training, efficiency và thu hẹp các tuyên bố lâm sàng.
