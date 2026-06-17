Dưới đây là toàn bộ những gì thầy yêu cầu, ghi ra đầy đủ kể cả ý nhỏ. Mình nhóm theo chủ đề cho dễ dùng làm checklist.
Deadline & kế hoạch

Lịch nộp đã post lên, phải nắm rõ khi nào nộp; hình như 15/7 là hạn nộp (theo báo của Khoa) — cần confirm lại.
Từ giờ đến cuối tháng 6 phải làm luận văn cho tươm tất.
Làm song song hai việc: vừa cài đặt vừa trình bày luận văn.
Sửa hết các lỗi trong vòng 1 tuần; bổ sung các kỹ thuật mới cũng trong 1 tuần.
Làm sát ngày quá rồi, phải gấp.

Vấn đề tổng thể về cách trình bày

Luận văn hiện hỗn loạn, rối loạn, trình bày không rõ — phải chỉnh trang lại đàng hoàng ngay.
Nói chuyện đang lơ lửng, khó hiểu, thiếu thông tin, nói chung chung — phải nói rõ bản chất vấn đề.
Tự kiểm tra báo cáo ít nhất 10 lần, sửa tới sửa lui chứ không vứt đó.

Xác định đóng góp / Final solution (mục quan trọng nhất)

Phải tự trả lời được: đem ra bảo vệ cái gì? Đóng góp là gì? Final solution là gì?
Phải phân biệt rõ cái nào kế thừa, cái nào đóng góp.
Việc đưa prompt/text vào KHÔNG phải là đóng góp — SAM đã làm rồi. Đừng nói đó là đóng góp.
Có quyền kế thừa nhưng phải nói đúng đóng góp của mình, không nói tầm bậy.
Đừng "lấy cái này ghép cái kia" — ghép không thôi thì người ta không cần đến mình.
Kế thừa phương pháp của người ta thì phải đọc kỹ họ làm gì để học, rồi xem thêm thắt / sửa được gì trong đó.

Định vị user & prompt (cái khác biệt thật sự)

Phải xác định rõ user là ai: bác sĩ đọc ảnh hay bác sĩ khám chính — đừng nói chung chung kiểu "ai cũng dùng".
Cái mới của mình là prompt nhắm cụ thể theo quy trình khám chữa bệnh, khác với các bài báo làm linh tinh, chung chung.
Phải trích ra những câu prompt khả dĩ mà bác sĩ đọc ảnh thực sự sẽ đưa vào, không phải prompt vu vơ.

Làm rõ kiến trúc 2 module (Encoder & Decoder)

Nhấn mạnh: phân đoạn chỉ có 2 công đoạn — feature extraction (encoder) và decoder ra mask.
Encoder kế thừa gì, sửa gì? Decoder kế thừa gì, sửa gì? — phải nói vào cụ thể.
Encoder có thêm text encoder + attention fusion → soi lại các kỹ thuật đó khác gì so với phương pháp trước, hay lấy nguyên si.
Phải làm nổi bật vai trò của vision prompt và các kỹ thuật giúp tận dụng được vision prompt — đọc bài hiện tại không thấy đã làm gì trong đó.

Hai khâu quan trọng nhất: mã hóa & fusion

Mã hóa visual prompt: kế thừa ở đâu, có sửa gì không. So sánh bản chất với cách SAM mã hóa (token để truy xuất K–V vì dùng ViT) so với heatmap của mình.
Nêu rõ phần đã sửa: ban đầu dùng binary (trong = 1, ngoài = 0) → chuyển sang heatmap để bào mòn góc cạnh cho kết quả tốt hơn.
Fusion (quyện prompt với ảnh): dùng kỹ thuật gì để embedding vector của vision prompt quyện với embedding vector của ảnh, kế thừa hay sửa.
Phải giải thích làm sao prompt "ứng hợp" với ảnh để decoder hiểu và phân đoạn đúng chỗ.
Attention là attention trên cái gì? Trên ảnh, trên vision prompt, hay cái gì — nói rõ, đừng để lơ lửng.
Đừng nói kiểu "lấy hai vector ghép lại" — phải nói rõ kỹ thuật truyền vector embedding cuối vào decoder.

Loss function

Khi có visual prompt thì loss function trong giai đoạn học có thay đổi gì không — phải giải thích rõ.

Sơ đồ & trình bày Chương 3

Phải vẽ ra offline và online.
Trình bày Chương 3 (phương pháp đề xuất) theo trình tự: Nguyên lý → Phương pháp → Giải thuật.
Phải có algorithm (thuật toán) chính yếu viết ra — luận văn hiện không thấy algorithm đâu.

Thực nghiệm phải minh chứng cho đóng góp

Mọi mục đích thực nghiệm phải minh chứng được cho đóng góp.
Làm ablation study: so với cái gốc mình đã sửa để thấy cái hơn.
Phải có bảng so sánh binary vs heatmap để minh chứng đóng góp mã hóa prompt (người ta sẽ soi ngay xuống thực nghiệm khi nghe nói "đóng góp").

Kích thước ảnh đầu vào (vấn đề lớn)

Ảnh BTXRD gốc cỡ 2000–3000px, resize về 512 → chỉ còn 1/4–1/6 → vấn đề lớn, performance không cao, feature map gần như không còn gì.
Hướng cải tiến đề xuất:

Giữ nguyên size, chia thành patch, dùng Swin Transformer (SWIN) — về tìm hiểu kiến trúc này.
Hoặc nâng lên 1024 / 2048 (nhưng cân nhắc vì sợ nặng, chạy không nổi).
Hoặc dựa vào ảnh để chọn kích thước gần nhất (vd 1200 → nâng lên 1024).


Minh chứng thú vị cần làm: so sánh phân đoạn không vision prompt vs có vision prompt ở cùng size nhỏ — nếu có vision prompt vẫn phân đoạn tốt dù size bé thì đó là phát hiện hay (em hình như đã có so sánh với baseline rồi).

Quy trình & xử lý ảnh không bệnh

Phân đoạn không thể nói "nằm ngoài đề tài" — thực tế người ta đưa ảnh bất kỳ, không bệnh thì đừng đóng mask, có bệnh thì đóng mask.
Độ chính xác phát hiện bệnh 88%, khi kết hợp pipeline giảm còn 76% → sai ngay từ phân lớp sẽ kéo cả phần sau.

Các trường hợp "thủng" — phải lý luận thêm

Prompt rỗng (bác sĩ không vẽ gì): hệ thống xử lý ra sao? Có thể coi prompt rỗng là tín hiệu ảnh không bệnh không? (Đây là chỗ "bị thủng", phải coi lại.)
Bác sĩ vẽ prompt sai vị trí (u ở góc trái dưới mà đóng sang phải trên): hệ thống làm sao? Phải lý luận thêm.
Xác suất bác sĩ đóng sai là bao nhiêu %? Hiện đang giả sử bác sĩ đóng đúng hết — phải discuss rõ.
Hiện mới chỉ mô phỏng bác sĩ đoán sai nhưng vẫn trong vùng (lệch tâm) → discuss cho rõ ràng.

Xóa ký hiệu R/L

Phải giải thích tại sao xóa R/L và ý nghĩa. User là bác sĩ đọc ảnh, R/L cho biết trái/phải.
Nếu xóa thì bác sĩ không biết trái hay phải → trái/phải cực kỳ quan trọng (lệch bên là nguy hiểm tính mạng).
Giải pháp cần nói rõ: khi học thì xóa, nhưng khi hiển thị vẫn giữ R/L — phải trình bày cho hợp lý.

Gatekeeper & pipeline

Nguy cơ sót bệnh: FN (có bệnh bảo không bệnh) nguy hiểm hơn FP → phải chú ý nhiều hơn (đã tăng từ 78 lên 88).
Pipeline 2 tầng làm Dice giảm mạnh (vd 0.9 × 0.8 ≈ 0.7) → chưa sẵn sàng triển khai → phải tìm cách giảm sai số tích lũy.
Hiện đang phân loại thẳng tất cả → với mẫu chắc chắn là u thì đừng đưa vào phân loại nữa (tránh bị phân loại nhầm thành không u) → tìm cách tăng độ chính xác.

Các lỗi ChatGPT nêu mà thầy đồng tình (về sửa)

So sánh PGA vs U-Net không công bằng: đừng dùng từ "so sánh"; nếu so phải làm cho fair. Kết quả cao hơn có thể do thông tin bổ sung (vision prompt) chứ không chắc do kiến trúc ưu việt → phải làm rõ công của ai (vision prompt hay kiến trúc).
Đơn vị đánh giá bị lẫn: lúc 187 ảnh, lúc 232 mẫu per-polygon → Dice/IoU không cùng đơn vị thống kê, so trực tiếp dễ sai bản chất → coi lại 3 khái niệm này, nói rõ (1 ảnh nhiều khối u, prompt tính theo mẫu khối u).
Attention U-Net có thể chưa tối ưu → nếu baseline chưa được tinh chỉnh công bằng thì kết luận "vượt trội" giảm thuyết phục.
Nguy cơ Oracle Prompt / prompt quá lý tưởng: bác sĩ không có sẵn ground-truth mask; prompt heatmap đang sinh từ bbox lý tưởng bao quanh u → coi lại (bbox chưa vẽ thật, thực tế rộng hơn hoặc lệch tâm).
So sánh với SAM-Med2D chưa chặt: PGA dùng 512, SAM dùng 256 (do cấu hình tác giả) → điều kiện chưa như nhau → không kết luận quá mạnh, phải discuss / dùng từ ngữ cẩn thận.
Chưa có external validation — chỉ 1 bộ dữ liệu duy nhất (BTXRD).
Tuyên bố "hỗ trợ chẩn đoán" hơi quá so với output → không nên nhấn mạnh khi chưa có mask thật.

Chuẩn bị bảo vệ (hậu trường)

Phải tự hỏi mình và tự trả lời trước mọi câu — người ta hỏi tứ tung trong ~15 phút, không chuẩn bị thì không xoay kịp.
Phải biết discuss / lý luận trên từng bảng số liệu.
Dùng ChatGPT (bản trả phí làm kỹ hơn) để bắt lỗi nhưng đừng quá tin, chỉ tham khảo; vào hỏi thêm vì còn rất nhiều lỗi.
Gửi/share link ChatGPT đó cho thầy.

