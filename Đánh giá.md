===== PHASE 1: CHƯƠNG 3 =====

🟠 Nên sửaMục 3.1.3, Đoạn 2"...CAD bổ sung câu nhắc trực tiếp vào g: cấu kiện unetUp_PromptAttention tích hợp tri thức câu nhắc..."Đưa trực tiếp tên biến/lớp (class) của mã nguồn vào văn bản học thuật. Trong bài báo chuẩn, kiến trúc mạng cần được mô tả bằng các khái niệm tổng quát, độc lập với ngôn ngữ lập trình."...CAD bổ sung câu nhắc trực tiếp vào g: khối giải mã chú ý có điều kiện tích hợp tri thức câu nhắc..."
🟠 Nên sửaMục 3.1.3, Đoạn cuối"Tín hiệu g' sau đó được đưa vào Cổng chú ý (GridAttentionBlock2D) tiêu chuẩn để tính..."Tương tự như trên, mang tên lớp lập trình vào bài viết làm giảm tính hàn lâm và tính tổng quát của phương pháp."Tín hiệu g' sau đó được đưa vào Cổng chú ý không gian lưới 2D tiêu chuẩn để tính..."
🟠 Nên sửaMục 3.1.1, Đoạn 2, Câu 2"Cách này giữ tín hiệu mạnh và đồng đều trong vùng câu nhắc, không suy giảm về tâm như Gaussian thuần, đồng thời làm mềm đường biên để tránh đạo hàm giả tạo khi lan truyền qua các tầng tích chập, hạn chế vốn có của mặt nạ nhị phân sắc cạnh khiến mạng dễ học theo cạnh hộp bao thay vì đặc trưng thực của tổn thương."Câu quá dài (56 chữ), nhồi nhét nhiều ý giải thích liên tiếp gây ngộp cho người đọc. Thuật ngữ "đạo hàm giả tạo" (dịch word-by-word từ artificial gradients) không quen thuộc trong tiếng Việt."Cách này giữ tín hiệu phân bố đều trong vùng câu nhắc và làm mềm đường biên để hạn chế sự biến thiên gradient đột ngột qua các tầng tích chập. Điều này khắc phục nhược điểm của mặt nạ nhị phân sắc cạnh, giúp mạng không học vẹt theo viền hộp bao mà tập trung vào đặc trưng thực của tổn thương."
🟠 Nên sửaBảng 3.1 (Cột 2) và Mục 3.1.2 (Đoạn 1)"Gợi ý từ hướng tiêm bản đồ không gian vào CNN...""...tiêm bản đồ nhiệt Gaussian..."Từ "tiêm" được dịch thô từ chữ "inject" trong tiếng Anh. Dù hiểu được ý, nhưng từ này mang tính dịch máy (Vietlish) và không phải văn phong học thuật tự nhiên.Thay bằng từ "đưa... vào" hoặc "tích hợp".Ví dụ: "Gợi ý từ hướng tích hợp bản đồ không gian vào CNN..."
🟡 Có thể cải thiệnMục 3.1, Đoạn 2 (trước Hình 3.1)"Chuỗi kế thừa tuyến tính: U-Net [2] (nền bộ mã hóa - bộ giải mã) → Attention U-Net [3] (bổ sung Cổng chú ý không gian mềm) → PGA-UNet..."Dùng trực tiếp ký hiệu mũi tên (→) để nối các khái niệm trong một đoạn văn xuôi là cách trình bày không chính quy."Kiến trúc được phát triển qua ba giai đoạn: kế thừa khung cơ sở từ U-Net [2], tích hợp Cổng chú ý không gian mềm từ Attention U-Net [3], và cuối cùng hình thành PGA-UNet..."
🟡 Có thể cải thiệnMục 3.1.2, Đoạn 1"PSG cụ thể hóa hướng này thành một cơ chế cổng nhân (không phải ghép kênh), huấn luyện từ đầu trên CNN nhẹ, đưa tín hiệu câu nhắc vào ngay từ giai đoạn trích xuất đặc trưng, chỉ khuếch đại chứ không triệt tiêu tín hiệu gốc (α ∈ [0, 1] bên dưới)."Câu văn liên tục dùng dấu phẩy để chèn thêm các cụm giải thích phụ, khiến luồng đọc bị vụn và lan man."PSG áp dụng cơ chế cổng nhân (gating mechanism) được huấn luyện từ đầu để tích hợp câu nhắc ngay tại giai đoạn trích xuất. Cơ chế này chỉ khuếch đại đặc trưng vùng mục tiêu mà không triệt tiêu tín hiệu gốc (thông qua hệ số α ∈ [0, 1])."
🟡 Có thể cải thiệnMục 3.1.1, Đoạn 2, Câu 1"...với Bmask ∈ {0, 1}H×W là mặt nạ nhị phân của hộp giới hạn (đệm 5 px mỗi phía)."Viết tắt "px" phổ biến trong văn bản thông thường, nhưng trong bài báo khoa học nên viết rõ để đảm bảo tính trang trọng."...với Bmask ∈ {0, 1}H×W là mặt nạ nhị phân của hộp giới hạn (đệm 5 pixel mỗi phía)."

🔴 Nghiêm trọng	Mục 3.2, Algorithm 1 (Bước 4) & Algorithm 2 (Bước 3)	Sinh Bản đồ nhiệt: Hi = Gaussian Blur (Bi,mask, k=31)	Sử dụng tên hàm API của thư viện lập trình (Gaussian Blur) trong mã giả thuật toán. IEEE yêu cầu mã giả phải độc lập với ngôn ngữ lập trình và dùng ký hiệu toán học.	Sinh Bản đồ nhiệt: Hi = Bi,mask * KGaussian (k=31)
🔴 Nghiêm trọng	Mục 3.2, Algorithm 1 (Bước 10)	Tính Dice xác thực trên tập xác thực; cập nhật ReduceLROnPlateau	Viết trực tiếp tên class của thư viện PyTorch (ReduceLROnPlateau) vào thuật toán. Thuật toán chỉ nên mô tả logic, công cụ cụ thể để ở phần "Thiết lập thực nghiệm".	Tính Dice xác thực; cập nhật tốc độ học (giảm tỷ lệ theo cơ chế thích ứng)
🟠 Nên sửa	Mục 3.2, Algorithm 1 (Bước 8)	Cập nhật: θ ← θ − η∇θL (AdamW, giới hạn đạo hàm ≤ 1.0	Lỗi đánh máy: thiếu dấu đóng ngoặc đơn ở cuối biểu thức.	Cập nhật: θ ← θ − η∇θL (AdamW, giới hạn đạo hàm ≤ 1.0)
🟠 Nên sửa	Mục 3.2, Algorithm 2 (Bước 2)	return Vui lòng khoanh hộp giới hạn lên vùng nghi ngờ	Thuật toán toán học/logic trả về (return) một câu thoại UI tiếng Việt trực tiếp là không chuẩn mực trong bài báo khoa học.	return ∅ (Khởi tạo yêu cầu người dùng cung cấp hộp giới hạn)
🟠 Nên sửa	Xuyên suốt Mục 3.3 (vd: Mục 3.3.1)	Efficient Net-B3	Viết sai tên chuẩn của mô hình nền tảng. Tên gốc theo công bố của tác giả (Google) là viết liền.	EfficientNet-B3
🟠 Nên sửa	Mục 3.3.1, Đoạn 2, Bullet 2	"...hệ thống hỏi lại một lần (Bác sĩ vẫn nghi ngờ, muốn tự thử phân đoạn?) để phòng âm tính giả..."	Đưa trực tiếp câu thoại giao diện (UI text) vào bài báo học thuật làm giảm tính hàn lâm. Cần trừu tượng hóa thành cơ chế logic.	"...hệ thống phát cảnh báo yêu cầu chuyên gia xác nhận lại nhằm phòng tránh rủi ro âm tính giả..."
🟡 Có thể cải thiện	Mục 3.2, Đoạn 2 (Câu nhắc rỗng)	"...ma trận không không mang thông tin định hướng..."	Hiện tượng lặp từ "không không" (ma trận zero không mang...) gây vấp khi đọc.	"...ma trận zero (toàn trị số 0) không cung cấp thông tin định hướng..."
🟡 Có thể cải thiện	Mục 3.3.1, Đoạn 2, Bullet 2	"Bác sĩ có thể kết thúc quy trình, hoặc tự khoanh hộp giới hạn để ép ảnh vào giai đoạn phân đoạn..."	Cụm từ "ép ảnh vào" mang sắc thái khẩu ngữ, chưa thực sự phù hợp với văn phong kỹ thuật học thuật.	"Bác sĩ có thể kết thúc quy trình, hoặc chủ động cung cấp hộp giới hạn để chuyển ảnh sang giai đoạn phân đoạn..."
🟡 Có thể cải thiện	Mục 3.3.2, Đoạn 1	"...thao tác này chỉ vẽ lại hộp giới hạn và gọi lại cùng quy trình suy luận..."	Từ "gọi lại" (gọi hàm - recall/call) mang nặng tư duy lập trình viên.	"...thao tác này chỉ cần cập nhật hộp giới hạn và thực thi lại quy trình suy luận..."
sửa

===== PHASE 2: CHƯƠNG 4 (bao gồm tham chiếu chéo tới Chương 5) =====

🔴 Nghiêm trọngMục 4.1.2, Đoạn về Attention U-Net"Attention U-Net (mô hình cơ sở có Cổng chú ý, không câu nhắc): Kiến trúc kế thừa trực tiếp của PGA-UNet [3] (Chương 3)..."Viết ngược logic nhân quả. Attention U-Net là mô hình tiền nhiệm ra đời trước (2018), PGA-UNet mới là mô hình kế thừa từ nó. Viết như bản gốc sẽ làm người đọc hiểu lầm Attention U-Net là biến thể sinh ra sau PGA-UNet."...Kiến trúc tiền nhiệm mà PGA-UNet kế thừa trực tiếp [3] (Chương 3)..."
🔴 Nghiêm trọngMục 4.1.3, Bước 3 (trước PT 4.4)"Tính Dice cấp độ ảnh: Chỉ số Dice được tính một lần duy nhất giữa $M_{pred}$ và $M_{GT}$"Ký hiệu toán học bất nhất. Ở Bước 2 ngay phía trên, mặt nạ dự đoán được định nghĩa có dấu mũ là $\hat{M}_{pred}$. Phương trình (4.4) bên dưới cũng dùng $\hat{M}_{pred}$. Việc thiếu dấu mũ ở câu dẫn gây đứt gãy tính chặt chẽ của biểu thức."...Chỉ số Dice được tính một lần duy nhất giữa $\hat{M}_{pred}$ và $M_{GT}$:"
🔴 Nghiêm trọngMục 4.1.2, phần Siêu tham số kiến trúc (Bullet 1)"...giảm dần từ tầng gần bottleneck đến tầng gần đầu ra; giảm về các tầng cuối để tránh hình dạng thô..."Lỗi đánh máy làm khuyết mất chủ ngữ/tham số của vế câu. Chữ "giảm" bị đứng chơ vơ khiến người đọc không rõ đại lượng nào đang được nói tới (dù có thể ngầm hiểu là hệ số $w_l$)."...giảm dần từ tầng gần bottleneck đến tầng gần đầu ra; giảm hệ số $w_l$ về các tầng cuối để tránh hình dạng thô..."
🟠 Nên sửaMục 4.1.3, Bước 1 & Bước 2"...tất cả mask nhị phân GT $\{G_1, G_2, ..., G_K\}$ được hợp nhất thành một mask GT duy nhất...""Mô hình được chạy suy luận riêng cho từng bbox $B_{k}$ tương ứng, sinh ra K mask xác suất..."Bất nhất thuật ngữ. Ở phần đầu khóa luận, tác giả đã có "Bảng đối chiếu thuật ngữ" quy định dịch sang tiếng Việt. Việc chèn lẫn lộn các từ tiếng Anh (mask, bbox, GT) vào câu văn tiếng Việt làm mất đi tính trang trọng của khóa luận IEEE.Sửa Bước 1: "...tất cả mặt nạ nhãn gốc $\{G_1, G_2, ..., G_K\}$ được hợp nhất thành một mặt nạ duy nhất..."Sửa Bước 2: "Mô hình được chạy suy luận riêng cho từng hộp giới hạn $B_{k}$ tương ứng, sinh ra K mặt nạ xác suất..."
🟠 Nên sửaMục 4.1.2, Đoạn về SAM-Med2D"Được đánh giá ở hai chế độ: chưa tinh chỉnh (dùng thẳng điểm lưu trọng số tiền huấn luyện...) và đã tỉnh chỉnh..."Cụm từ "dùng thẳng" mang văn phong khẩu ngữ (informal), chưa chuẩn học thuật. Ngoài ra có lỗi gõ dấu ngã/hỏi ở chữ "tỉnh chỉnh" (cần sửa thành "tinh chỉnh")."Được đánh giá ở hai chế độ: chưa tinh chỉnh (sử dụng trực tiếp điểm lưu trọng số tiền huấn luyện...) và đã tinh chỉnh..."
🔴 Nghiêm trọngMục 4.2.2, Đoạn "Ghi chú về điểm lưu trọng số...""...(best_sam.pth, train Dice tăng liên tục $0.6266 \rightarrow 0.8981$ qua 11 vòng lặp)..."Đưa trực tiếp tên file mã nguồn/file trọng số (best_sam.pth) vào văn bản học thuật. Giống như các lỗi ở chương 3, bài báo IEEE cần sự trừu tượng hóa, không nhắc đến file vật lý trên ổ cứng."...(trọng số tốt nhất, Dice huấn luyện tăng liên tục từ $0.6266$ đến $0.8981$ qua 11 vòng lặp)..."
🟠 Nên sửaMục 4.2.3, Đoạn 1"Mục 4.2.2 đã chứng minh PGA-UNet vượt SAM-Med2D ngay cả khi cùng chạy ở $256 \times 256$ Mục này đánh giá PGA-UNet ở độ phân giải gốc..."Thiếu dấu chấm câu sau "256x256", dẫn đến hai câu độc lập bị dính liền vào nhau (run-on sentence)."...ngay cả khi cùng chạy ở $256 \times 256$. Mục này đánh giá..."
🟠 Nên sửaMục 4.2.3, Đoạn ngay dưới Hình 4.3"...khoảng cách với SAM-Med2D thực tế còn lớn hơn mức đã chứng minh ở $256 \times 256$ Về tính bền bỉ..."Thiếu dấu chấm câu phân tách hai ý (hiệu năng và tính bền bỉ)."...lớn hơn mức đã chứng minh ở $256 \times 256$. Về tính bền bỉ..."
🟠 Nên sửaMục 4.2.3, Đoạn ngay dưới Hình 4.3"...suy luận bắc cầu PGA-512 > PGA-256 > SAM-256 cho thấy khoảng cách..."Việc dùng ký hiệu toán học "lớn hơn" (>) nối các mô hình trong một đoạn văn xuôi để diễn đạt ý "hiệu năng tốt hơn" là cách hành văn phi chính quy (informal) và không đạt chuẩn IEEE."...theo tính chất bắc cầu, hiệu năng của PGA-UNet (512) vượt qua PGA-UNet (256) và cao hơn hẳn SAM-Med2D (256), cho thấy khoảng cách..."
🟠 Nên sửaMục 4.2.2, Đoạn "Ghi chú về điểm lưu trọng số...""Ghi chú về điểm lưu trọng số đã tỉnh chỉnh trên FracAtlas..."Lỗi gõ phím (Typo): sai dấu hỏi/ngã ở từ "tinh chỉnh"."...trọng số đã tinh chỉnh trên FracAtlas..."
🟡 Có thể cải thiệnMục 4.2.3, Đoạn "Lưu ý HD95...""...do đó cột này không in đậm ở hàng nào trong các bảng dưới đây, không phải độ phân giải cao kém bám biên hơn, chỉ là khác đơn vị đo."Lời giải thích mang tính chất trần thuật, khẩu ngữ, giống như đang nói chuyện trực tiếp với người đọc. Cần viết súc tích và học thuật hơn."...do đó, cột này không được in đậm để tránh hiểu nhầm về hiệu năng bám biên giữa các hệ quy chiếu khác nhau."
🟡 Có thể cải thiệnBảng 4.3, 4.4, 4.5, 4.6Tiêu đề: "...Attention U-Net (tự động, 512) so PGA-UNet (512, Bao trọn)..."Thiếu giới từ "với" khiến cụm từ "so PGA-UNet" có vẻ cụt ngủn trong văn bản học thuật tiếng Việt."...Attention U-Net (tự động, 512) so với PGA-UNet (512, Bao trọn)..."
🟡 Có thể cải thiệnMục 4.2.1, Đoạn cuối trang 33"Dấu hiệu đầu tiên của tính tổng quát ở cấp độ thiết kế: lợi ích của câu nhắc không phải hiện tượng quá khớp riêng của BTXRD..."Dịch từ "overfitting" thành "hiện tượng quá khớp" là đúng, nhưng cụm từ "quá khớp riêng của BTXRD" nghe hơi gượng ép. Thường chỉ nói mô hình bị quá khớp trên một tập dữ liệu."...không chỉ là kết quả đặc thù trên BTXRD..."
Nghiêm trọngMục 4.3.1 (Phân tích ablation, Quan sát 2, 3, 4) và Mục 4.3.3 (Bullet 1, 2)Ví dụ 1: "...Zoom -0.0025, Lệch tâm -0.0050..."Ví dụ 2: "Zoom giảm nhẹ nhưng vẫn có ý nghĩa..."Bất nhất thuật ngữ. Ở đầu Chương 4 và trong tất cả các bảng (Bảng 4.10, 4.11...), bạn sử dụng tên kịch bản là "Bao trọn". Việc tự ý dùng từ "Zoom" (dịch từ Zoom-out) trong văn xuôi làm đứt gãy sự liên kết với bảng biểu, khiến người đọc bối rối không rõ "Zoom" là độ đo mới hay kịch bản nào.Thay thế toàn bộ từ "Zoom" trong các đoạn phân tích văn xuôi thành "Bao trọn".Ví dụ: "...Bao trọn -0.0025, Lệch tâm -0.0050..." và "Bao trọn giảm nhẹ nhưng vẫn có ý nghĩa..."
🟠 Nên sửaMục 4.3.1, Đoạn 2 (Giải thích tên biến thể)"Đặt tên trực tiếp theo cấu hình kiến trúc (thay vì ký hiệu V1-V8 trung tính, dù các thư mục kết quả gốc vẫn giữ ký hiệu này để truy vết) để thấy ngay đây là một ablation kiến trúc:"Mang văn phong báo cáo tiến độ/đồ án. Việc nhắc đến cấu trúc "thư mục kết quả gốc" (local folders) trong một bài báo khoa học là tối kỵ vì nó không mang thông tin học thuật và không cần thiết cho độc giả."Để làm rõ vai trò của từng thành phần, các biến thể được đặt tên trực tiếp theo cấu hình kiến trúc:"
🟠 Nên sửaMục 4.3.1, phần "Điểm neo mức không câu nhắc""Giả thuyết lý giải (suy luận lý thuyết, chưa kiểm chứng bằng nghiên cứu loại bỏ thành phần riêng): Không có câu nhắc định hướng..."Cách rào đón quá dài dòng, đặt trong ngoặc đơn gây loãng mạch đọc. Trong phân tích kết quả, việc đưa ra lý giải dựa trên suy luận là bình thường, chỉ cần diễn đạt súc tích."Lý giải tiềm năng: Không có câu nhắc định hướng..."
🟡 Có thể cải thiệnMục 4.3, Đoạn 1"...nên trình bày riêng từng bộ dữ liệu trước rồi tổng hợp sau sẽ trung thực và rõ ràng hơn là ép vào một bảng gộp."Cụm từ "ép vào một bảng gộp" mang sắc thái văn nói (khẩu ngữ), thiếu tính khách quan của văn phong IEEE."...nên việc phân tích độc lập trên từng bộ dữ liệu trước khi tổng hợp sẽ giúp làm rõ xu hướng và tránh nhiễu thông tin so với việc gộp chung."
🟡 Có thể cải thiệnMục 4.3.3, Phân tích Bảng 4.21 (Bullet 4)"Khác biệt thật với BTXRD, xác nhận bằng kiểm định: hai đóng góp riêng lẻ biên độ nhỏ đổi chiều dấu có ý nghĩa ở cả hai bộ dữ liệu."Diễn đạt dịch sát nghĩa (word-by-word) từ tiếng Anh (e.g., "real difference", "change sign significantly"), đọc khá gượng ép trong tiếng Việt học thuật."Sự khác biệt có ý nghĩa thống kê so với BTXRD: hai đóng góp riêng lẻ (biên độ nhỏ) có sự đảo chiều xu hướng một cách có ý nghĩa ở cả hai bộ dữ liệu."
🟡 Có thể cải thiệnMục 4.3.3, Đoạn cuối"...chưa kiểm định tổng quát hóa liên miền theo nghĩa chặt) được tổng hợp thành hướng phát triển tại Chương 5."Dấu đóng ngoặc đơn ) ở cuối câu bị thừa (hoặc do thiếu dấu mở ngoặc trước đó).Bỏ dấu đóng ngoặc đơn: "...chưa kiểm định tổng quát hóa liên miền theo nghĩa chặt được tổng hợp thành hướng phát triển tại Chương 5."
🔴 Nghiêm trọngMục 4.4.2, Đoạn "Phân tích các ca bỏ sót trên FracAtlas""...dùng dữ liệu cấp độ ảnh (cls_prob, gt_label) từ results/pipeline_detail.csv của lần chạy pipeline FracAtlas."Đưa trực tiếp tên biến trong mã nguồn (cls_prob, gt_label) và đường dẫn file kết quả cục bộ (results/pipeline_detail.csv) vào bài. Đây là lỗi tối kỵ trong văn phong IEEE, làm mất tính hàn lâm và biến bài báo thành báo cáo gỡ lỗi (debug report)."...dựa trên xác suất dự đoán và nhãn gốc ở cấp độ ảnh của FracAtlas."
🔴 Nghiêm trọngBảng 4.23 và Bảng 4.29 (Tiêu đề bảng)"Phân bố xác suất dự đoán (cls_prob) của..."Tương tự lỗi trên, đưa tên biến code vào tiêu đề bảng."Phân bố xác suất dự đoán ($p$) của..."
🟠 Nên sửaMục 4.4.1, Đoạn "Kiến trúc: Efficient Net-B3 tinh chỉnh...""Hàm mất mát: BCEWithLogitsLoss; tối ưu: AdamW; dừng sớm: patience = 15 (theo Accuracy); giới hạn đạo hàm: max_norm = 1.0."Dùng trực tiếp tên class và tham số của thư viện PyTorch. IEEE yêu cầu sử dụng khái niệm toán học/thuật ngữ học máy độc lập với framework."Hàm mất mát: Entropy chéo nhị phân (Binary Cross-Entropy); tối ưu: AdamW; dừng sớm sau 15 vòng lặp không cải thiện độ chính xác; cắt xén đạo hàm (gradient clipping) với chuẩn tối đa 1.0."
🟠 Nên sửaMục 4.4.1, Đoạn "Kiến trúc...", mô tả Giai đoạn 2"Mở khóa toàn bộ, $LR=10^{-5}$, Cosine AnnealingLR."Dùng tên class bộ lập lịch của PyTorch (CosineAnnealingLR)."Mở khóa toàn bộ trọng số, $LR=10^{-5}$, sử dụng lịch trình giảm tốc độ học hình sin (Cosine Annealing)."
🟠 Nên sửaMục 4.4.1, Đoạn "Tương quan với kích thước tổn thương""...tính bằng công thức shoelace trên tọa độ polygon GT..."Sử dụng từ ghép Vietlish (polygon GT), thiếu sự đồng bộ với các phần trước vốn đã dùng "đa giác" và "nhãn gốc"."...tính bằng công thức Shoelace dựa trên tọa độ đa giác của nhãn gốc..."
🟡 Có thể cải thiệnMục 4.4.1, Đoạn "Lưu ý về phạm vi số liệu""...cấu hình confusion matrix hiện tại..."Chèn từ tiếng Anh vào giữa câu tiếng Việt trong khi ngành AI đã có thuật ngữ tương đương rất phổ biến."...cấu hình ma trận nhầm lẫn (confusion matrix) hiện tại..."
🟡 Có thể cải thiệnXuyên suốt Mục 4.4"Efficient Net-B3"Tên mạng nền tảng viết sai quy cách (tương tự Chương 3)."EfficientNet-B3" (viết liền).
🔴 Nghiêm trọngMục 5.2, Hạn chế 1 (Sai số tích lũy)"...kéo hiệu năng đầu cuối xuống đáng kể so với PGA-UNet đơn lẻ (Mục 5.1), hạn chế cố hữu của kiến trúc hai giai đoạn."Tham chiếu chéo sai. Mục 5.1 là phần tóm tắt kết luận của Chương 5, không chứa số liệu chứng minh sự sụt giảm hiệu năng. Các phân tích về sai số tích lũy kéo hiệu năng đầu cuối xuống nằm ở Mục 4.4 (cụ thể là Bảng 4.26 và 4.31). Việc dẫn nguồn chéo sai trong khóa luận sẽ làm người đọc không thể tra cứu lại lập luận."...kéo hiệu năng đầu cuối xuống đáng kể so với PGA-UNet đơn lẻ (Mục 4.4), hạn chế cố hữu của kiến trúc hai giai đoạn."
🟠 Nên sửaMục 4.5, Đoạn 2"...đóng góp quyết định đến từ việc điều kiện hóa attention bằng đặc trưng câu nhắc (CAD) chứ không phải bản thân cơ chế attention;"Bất nhất thuật ngữ. Xuyên suốt Chương 2, 3 và 4, khóa luận đã tuân thủ việc dịch "attention mechanism" thành "cơ chế chú ý" (như đã quy định ở Bảng thuật ngữ đầu bài). Việc sử dụng lại tiếng Anh ở phần tổng kết làm giảm tính nhất quán và trang trọng."...đóng góp quyết định đến từ việc điều kiện hóa chú ý bằng đặc trưng câu nhắc (CAD) chứ không phải bản thân cơ chế chú ý;"
🟠 Nên sửaMục 4.5, Đoạn 4"...kéo Pipeline Dice từ 0.6763 xuống 0.4230 dù bản thân PGA UNet trên các ảnh lọt qua đúng vẫn giữ Dice ≈ 0.82."Lỗi đánh máy: Thiếu dấu gạch nối trong tên mô hình cốt lõi của khóa luận."...kéo Pipeline Dice từ 0.6763 xuống 0.4230 dù bản thân PGA-UNet trên các ảnh lọt qua đúng vẫn giữ Dice ≈ 0.82."
🟠 Nên sửaMục 5.1, Đoạn 2"Đóng góp kỹ thuật cốt lõi là kiến trúc PGA UNet (Prompt-Guided Attention U-Net, ~3M tham số)..."Tương tự lỗi trên, thiếu dấu gạch nối trong tên mô hình ở ngay phần kết luận trọng tâm."Đóng góp kỹ thuật cốt lõi là kiến trúc PGA-UNet (Prompt-Guided Attention U-Net, ~3M tham số)..." 

===== PHASE 3: CHƯƠNG 2 =====

🔴 Nghiêm trọngMục 2.4.1, Đoạn dẫn trước PT (2.4)"Chỉ số IoU: diện tích phần giao chia diện tích phần hợp của hai mặt na."Lỗi đánh máy thiếu dấu làm sai chính tả tiếng Việt, ảnh hưởng đến độ chuyên nghiệp của văn bản học thuật."Chỉ số IoU: diện tích phần giao chia diện tích phần hợp của hai mặt nạ."
🟠 Nên sửaMục 2.3.2, Đoạn 1, Câu 1"Sau khi có Bản đồ nhiệt câu nhắc H, bài toán tiếp theo là tiêm thông tin này vào U-Net."Bất nhất thuật ngữ và văn phong. Ở Chương 3 chúng ta đã thống nhất không dùng từ "tiêm" (dịch thô từ inject) mà dùng "tích hợp" để đảm bảo tính hàn lâm."Sau khi có Bản đồ nhiệt câu nhắc H, bài toán tiếp theo là tích hợp thông tin này vào U-Net."
🟠 Nên sửaMục 2.3.1, Đoạn ngay dưới PT (2.2)"Cách biểu diễn này mang $\overline{y}$ nghĩa lâm sàng: $H(x,y)$ đạt cực đại..."Lỗi hiển thị/gõ nhầm mã LaTeX. Thay vì gõ chữ "ý", văn bản lại dùng ký hiệu toán học $\overline{y}$ (\bar{y}), làm đứt gãy mạch đọc."Cách biểu diễn này mang ý nghĩa lâm sàng: $H(x,y)$ đạt cực đại..."
🟡 Có thể cải thiệnMục 2.3.1, Đoạn "Biến thể triển khai...""Biến thể triển khai, Plateau Heatmap: Một biến thể phổ biến là Plateau Heatmap: gán đồng nhất giá trị 1.0..."Lặp cụm từ tiếng Anh và lạm dụng dấu hai chấm (:) liên tiếp trong cùng một câu gây lủng củng."Biến thể Plateau Heatmap: Khác với phân phối chuẩn, biến thể này gán đồng nhất giá trị 1.0..."
🟡 Có thể cải thiệnMục 2.4.4, Đoạn 1"Các độ đo định vị phổ biến (DIOU, GIoU) đo lệch tâm..."Bất nhất cách viết hoa acronym. Cùng là hậu tố IoU (Intersection over Union) nhưng viết thành DIOU và GIoU."Các độ đo định vị phổ biến (DIoU, GIoU) đo lệch tâm..."
🟡 Có thể cải thiệnMục 2.3.1, Đoạn cuối"...cho phép Cổng không gian nhân trực tiếp theo phần tử (Phương trình (3.3)) mà không cần chiếu một vector không mang cấu trúc không gian vào bản đồ đặc trưng 2D."Việc lặp lại chữ "không gian" ba lần trong một câu dài khiến câu văn bị nặng nề. Người đọc chuyên ngành chỉ cần dùng từ "rời rạc" là đủ hiểu đặc tính của vector nhúng."...mà không cần chiếu một vector rời rạc vào bản đồ đặc trưng 2D."

===== PHASE 4: CHƯƠNG 1 + TÀI LIỆU THAM KHẢO [6][7] =====

🔴 Nghiêm trọngMục 1.3, Phát biểu bài toán, Phương trình (1.1)M = 1[fseg (I, H(B); seg) ≥ 0.5]Mâu thuẫn ký hiệu toán học. Ở câu định nghĩa ngay phía trên, mặt nạ dự đoán đầu ra được ký hiệu là $\hat{M}$. Tuy nhiên, trong công thức lại dùng $M$ (ký hiệu chuẩn thường quy ước là nhãn gốc/Ground Truth), làm đứt gãy sự chặt chẽ của định nghĩa toán học.$\hat{M} = \mathbf{1}[f_{seg}(I, H(B); \theta_{seg}) \ge 0.5]$(Lưu ý: Bổ sung thêm dấu mũ cho $\hat{M}$ và viết đúng ký hiệu trọng số $\theta_{seg}$)
🟠 Nên sửaMục 1.2.1, Đoạn 3 và Đoạn 4"Một hướng nghiên cứu đang được quan tâm là phân đoạn tương tác... Tuy nhiên, cách tích hợp hiệu quả tín hiệu định hướng vào kiến trúc mạng nơ-ron vẫn là hướng nghiên cứu đang được quan tâm, đặc biệt trong ảnh y khoa chuyên biệt."Lặp cấu trúc từ vựng ở hai đoạn liên tiếp. Câu văn khá dài và mang phong cách sinh văn bản tự động (liệt kê nhiều vế cân đối quá mức). Cần súc tích hơn."Phân đoạn tương tác đang là một hướng tiếp cận hứa hẹn, nơi chuyên gia cung cấp hộp giới hạn để định hướng mô hình. Cơ chế này vừa cải thiện độ chính xác, vừa đảm bảo chuyên gia y tế luôn nắm quyền kiểm soát. Tuy nhiên, cách tích hợp hiệu quả định hướng này vào mạng nơ-ron chuyên biệt cho ảnh y khoa vẫn là một thách thức lớn."
🟠 Nên sửaMục 1.5, Đóng góp 1"...không tạo đạo hàm giả tạo tại đường biên hộp giới hạn."Bất nhất thuật ngữ (Lỗi này đã được đồng bộ ở Chương 3). "Đạo hàm giả tạo" (dịch word-by-word từ artificial gradients) không phải là thuật ngữ học máy tiếng Việt chuẩn mực."...hạn chế sự biến thiên gradient đột ngột tại đường biên hộp giới hạn."
🟡 Có thể cải thiệnMục 1.3, Đoạn ngay dưới công thức (1.1)"Thiết kế này phản ánh triết lý con người luôn giám sát trong vòng lặp xuyên suốt cả hai bước..."Dấu hiệu AI/Văn phong nghị luận. Từ "triết lý" (philosophy) mang sắc thái quá hoa mỹ đối với một phát biểu bài toán trong kỹ thuật phần mềm/AI."Thiết kế này tuân thủ nguyên tắc human-in-the-loop (con người luôn trong vòng lặp) xuyên suốt cả hai bước..."
🟡 Có thể cải thiệnMục 1.2.2, Đoạn 2"Một hệ thống phân đoạn đáng tin cậy cần khả năng chịu đựng sai sót: nhận biết khi câu nhắc có vấn đề và phản hồi phù hợp..."Thiếu đồng bộ với toàn bài. Xuyên suốt Chương 3 và 4, khóa luận đều sử dụng thuật ngữ "tính bền bỉ" (robustness) để chỉ khả năng mô hình chịu được sai lệch câu nhắc. "Chịu đựng sai sót" nghe giống khái niệm fault tolerance của hệ thống phân tán."Một hệ thống phân đoạn đáng tin cậy cần có tính bền bỉ: hoạt động ổn định khi câu nhắc bị sai lệch và phản hồi phù hợp..."
🔴 Nghiêm trọng	Tài liệu tham khảo, Mục [6] và [7]	
"[6] C. Xu, L. Zhang, L. Wang, et al., Boundary-Aware Test-Time Adaptation for Zero-Shot Medical Image Segmentation, 2025. [Online]..."



"[7] H. Yang... Prompt Mechanisms in Medical Imaging: A Comprehensive Survey, 2025. [Online]..."

Thiếu hoàn toàn thông tin nơi xuất bản (Venue). Theo chuẩn IEEE, một bài báo phải ghi rõ được đăng ở Tạp chí (Journal), Hội nghị (Conference) nào, hoặc tối thiểu phải ghi là "arXiv preprint" nếu là bản thảo chưa xuất bản. Chỉ để Tên bài + Năm + Link là sai quy cách trích dẫn học thuật.	
Bổ sung thông tin xuất bản hoặc arXiv ID. Ví dụ:



"...Medical Image Segmentation, arXiv preprint arXiv:2512.04520, 2025."

===== PHASE 5: PHẦN ĐẦU (Tóm tắt, Danh mục Bảng, Tài liệu tham khảo [1], Danh mục ký hiệu, Bảng đối chiếu thuật ngữ) =====

🟠 Nên sửa	Tóm tắt khóa luận, Đoạn 2 và Đoạn 3	
"...mặt nạ cấp độ pixel."



"Một module sàng lọc..."

Sử dụng từ tiếng Anh chêm vào văn bản tiếng Việt ở ngay phần Tóm tắt trang trọng nhất của khóa luận. Cần thuần Việt theo yêu cầu.	
"...mặt nạ cấp độ điểm ảnh."



"Một mô-đun sàng lọc..." (hoặc "khối sàng lọc").

🟠 Nên sửa	Tóm tắt khóa luận, Đoạn 2 và 3	
"...ảnh y tế 2D..."



"...nhỏ hơn nhiều lần về số tham số (PGA-UNet ~3M, SAM-Med2D ~91M)."

Viết tắt ký hiệu số lượng (M) và số chiều (2D) theo phong cách tiếng Anh/kỹ thuật. Ở Tóm tắt khóa luận tiếng Việt, nên viết rõ ràng thành chữ.	
"...ảnh y tế hai chiều..."



"...nhỏ hơn nhiều lần về số tham số (PGA-UNet ~3 triệu, SAM-Med2D ~91 triệu)."

🟠 Nên sửa	Danh mục Bảng, Tiêu đề Bảng 4.18 và Bảng 4.26	"...luồng xử lý Gatekeeper → PGA-UNet trên dataset_online..."	Lỗi "rò rỉ" tên biến mã nguồn (code variable) vào ngay phần Mục lục/Danh mục Bảng đầu tài liệu, gây mất tính hàn lâm ngay trước khi người đọc vào nội dung chính.	"...luồng xử lý Gatekeeper → PGA-UNet trên tập dữ liệu kiểm thử..."
🟡 Có thể cải thiện	Tài liệu tham khảo, Mục [1]	"...Available: https://www.cuh.nhs.uk... (visited on 01/01/2025)."	Định dạng ngày truy cập tài liệu mạng (URL) không đúng chuẩn IEEE.	"...Available: https://www.cuh.nhs.uk... [Accessed: Jan. 1, 2025]."
🟡 Có thể cải thiện	Danh mục Bảng, Tiêu đề Bảng 4.15	"PGA-UNet 256 VS SAM-Med2D theo đặc tính lâm sàng..."	Lạm dụng từ viết tắt tiếng Anh (VS = versus) và viết hoa toàn bộ không cần thiết trong văn bản học thuật tiếng Việt.	"PGA-UNet (256) so với SAM-Med2D theo đặc tính lâm sàng..."
🟡 Có thể cải thiện	Danh mục các ký hiệu và chữ viết tắt	"Efficient Net-B3"	Tên mạng nền tảng viết sai quy cách công bố gốc của tác giả (Google). Lỗi này kéo theo sự sai lệch ở toàn bộ các phần sau.	"EfficientNet-B3" (Viết liền hoàn toàn).
🟡 Có thể cải thiện	Bảng đối chiếu thuật ngữ chuyên ngành	
"Bộ mã hóa"


"Bộ giải mã"


"vector nhúng"


"vòng lặp"

Không nhất quán trong việc viết hoa chữ cái đầu tiên ở cột "Thuật ngữ tiếng Việt". Chỗ thì viết hoa chữ đầu, chỗ thì viết thường.	Cần đồng bộ viết hoa chữ cái đầu cho toàn bộ danh sách. Sửa thành: "Vector nhúng", "Vòng lặp".