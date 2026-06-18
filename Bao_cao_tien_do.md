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




Full cuộc trò truyện:

Alo. Các em có nghe rõ không?
 Dạ em nghe rõ thầy ơi.
Rồi bây giờ là cái lịch thì cũng đã có post lên rồi đó ha.
 Là mình nắm được cái lịch khi nào nộp bài rồi vân vân.
 Thì bây giờ còn nước còn tác ha. Ha.
 Thì à bây giờ là 10 17 rồi thì 10 thì bây giờ kế hoạch là làm sao?
 Từ bây giờ đến cuối tháng s bây giờ đến cuối tháng s thì cố gắng cái luận văn nó cho tươm tất một chút.
 Tại vì hình như là 15 tháng 7 là nộp đó đúng không? Theo cái báo của Khoa đó.
 Thì cái luận văn hiện nay xem sơ qua thì nó hỗn loạn, rối loạn quá nha. Nó rối loạn quá.
 Thì bây giờ mình sẽ phải a làm song song hai việc thì là vừa cài đặt và vừa vừa cài đặt và vừa trình bày luận văn.
 Rồi thì bây giờ từng nhóm mở cái báo cáo ra góp ý là sửa. Mở đi trên nhóm nào đi.
 Từng bước đi. Mỗi nhóm khoảng 30 phút.
Dạ. Dạ. Để nhớ em trước thì để giúp cho cái chuẩn bị cái tư thế đồ share rồi coi.
 Bây giờ để giúp giúp em a cái trình bày nè cái đề tài của em là cái gì?
Dạ
thì tất cả những nhóm khác là nghe theo nhé đúng theo cái format cái như vậy thôi sẽ hỏi đi hỏi lại
phát triển phát triển hệ thống phân đoạn ảnh ít quan dựa vào câu nhắc dùng khoan
ừ rồi thế thì bây giờ mình sẽ chú ý những cái câu quan trọng trước ha thì bây giờ à để làm á thì mình phải trả lời chuyện thứ nhất nè bây giờ mình đ mình muốn đem ra bảo vệ cái gì?
 Cái đóng góp của mình là cái gì? Cái final solution của mình là cái gì? Đúng không?
 Đầu tiên mình phải tự trả lời được câu hỏi đó.
 Cái giải pháp cuối cùng của mình trong cái phát triển hệ thống phân đoạn ảnh x quang về xương dựa vào c nhắc trực quang thì cái final solution của mình là cái gì?
 Phải trả lời được.
 Và trong đó cái nào là kế thừa, cái nào là đóng góp? Đâu? Em nói khoảng 5 phút coi.
Dư Thì đầu tiên là cái đóng góc của em, em muốn đóng góc vào là khi một hệ thống phát triển phân đoạn ảnh truyền thống như Unitet hoặc Unit thì nó không nó tự học nó phân đoạn một cách vừa trên nó học và nó không có một sự hướng dẫn nào hết nên thường à độ tin cậy thường rất thấp.
 Nên a em muốn đóng góc đưa vào câu nhắc mềm của bác sĩ đưa from vào để a khoanh vùng chú ý.
 Thì khi mà khoanh vùng chú ý thì à à các Hệ thống này nó sẽ tập trung chú ý vào phần from đó để nó học một cách tốt hơn.
 Đó thì đóng góp chỗ nào không rõ.
 Em về em soi lại đóng góp mình chỗ nào.
À
tức là cái chuyện mà phân đoạn dựa vào câu nhắc trực quan thì người ta cũng cái ý đó người ta đã làm rồi.
 Thí dụ như là Sam không là một cái hệ thống rất là lớn nó cũng đã làm rồi thì mình đóng góp mình là chỗ nào mình phải tìm cho. ra chứ mình không nói được. Hiểu không?
 Cái chuyện mà đưa tch vô là người ta đã làm rồi, đâu phải là đóng góp của em. Nói tầm bậy bà hiểu không?
 Mình phải cho rõ mình có quyền kế thừa nhưng mà mình phải nói đúng cái đóng góp á của mình á.
Đ góp của em là cái gì?
Ờ đóng góp của em là à sử dụng một mô hình à nhỏ huấn lệ luyện lệ từ đầu.
 Còn mô hình sau là mô hình huấn luyện lớn trên tập lớn của dữ liệu.
 À cái thứ hai là sử dụng from của em. Thì
bây giờ á em phải xem nè cái chữ cái cách nà mình nói rối loạn quá phải không?
Dạ
nói rối loạn quá.
 Bây giờ em xem như thế này n để em trả lời nè.
 Bây giờ em về em chích lại cuối cùng á cái final solution của em là cái gì?
 Cái giải pháp cuối cùng của em là cái gì? Cái mô hình của em là là cái gì? Đúng không?
 Trong hai giai đoạn offline và online thì phân đoạn thì thực chất nó chỉ có hai công đoạn thôi.
 Công đoạn Đoạn thứ nhất là feature extraction rút chích đặc trưng đúng không?
 Và công đoạn thứ hai là decoder để mà nó ra cái mas đúng không?
 Nó chỉ có hai công đoạn thôi.
 Thì như vậy là mình cải tiếng cải lùi mà mình tham gia xử lý công đoạn nào.
 Thí dụ bây giờ công đoạn image encoder thì hồi xưa là chỉ có email encoder thôi đúng không? Bây giờ công đoạn đó nó phình ra thêm
nó có thêm cái text encoder đúng chưa?
Dạ.
Đó. Rồi nó có thêm cái gì nữa? Có thêm cái fusion attention gì đó. hơn
trước khi đi ra cái decoder đúng không?
Dạ.
Rồi còn cái decoder thì có gì mới không?
 Thí dụ vậy mình soi ngay vào những cái chuyện vậy.
 Thứ nhất là cái ý tưởng đưa t vô là mình kế thừa thôi chứ mình không có ý gì mới.
 Còn nếu mà mới á là mình phải nói á là mình không phải là đưa tex tùm lum mà cái tex này mình chú ý đến cái quá trình khám nghiệm lâm sàn là cái ứng dụng này nó nằm ở đâu?
 Nó nằm ở ông bác sĩ độc ảnh hay ông bác sĩ khám chính chứ đừng có nói Google. Hiểu không?
 Phân đoạn này là ai dùng? User là ai?
 Còn hiện nay các bài báo là nó vu nó làm linh tinh, nó làm chung chung vậy thôi. Ai muốn làm cái gì làm.
 Còn mình á thì cũng là tex nhưng mà mình nói có cái khác,
 có cái khác biệt là mình chú ý đến quy trình khám chữa bệnh. Được chưa?
Cái của em, cái của em from box á thầy mà cái của cái của Sam á là nó sử dụng nó mã hóa thành token để nó truy xất của vi còn của em là up concast trực tiếp vô luôn cái kia.
 Thì cái này có phải là Cái thượng không
thì khoan thì để giúp cho em cái cách này chứ mấy em làm xong em không biết là mấy em đóng góp cái gì thì không được phải không?
Dạ.
Bây giờ chuyện thứ nhất là cái ý tưởng á là cái phân đoạn này có dùng tex thì cái đó không có mới.
 Nhưng mà khi đó mình mới tìm ra cái chỗ nào nó mơi mới ở chỗ á là cái câu tex này đó là mình nhắm nhắm cụ thể cho em user là ai là có phải ông bác sĩ đọc ảnh hay không hay là ai trong quy trình khám chữa bệnh là ai hiểu không?
 Bác sĩ đọc ảnh
 ờ thì phải cho rõ đó.
 Và khi ông bác sĩ đọc ảnh thì mình để ý xem ổng sẽ đưa những câu text nào chứ không thể đưa câu vu được. Đúng chưa?
 Thì cái khác của mình là chỗ đó.
 Thì thành ra mình phải trích ra những cái câu text mà có mà khả dĩ có thể đưa vào.
 Đó là chuyện thứ nhất.
 Đó về mình xem cái chuyện đó.
 Rồi chuyện thứ hai á là trong cái kiến trúc của nó đó.
 Kiến trúc của nó thì như đã nói chỉ có hai cái module thôi.
 Một cái phân đoạn thì chỉ có email coder và decoder.
 Thì bây giờ của mình là có thay đổi cái gì trong hai cái module cơ bản đó thì mình nói vào.
 Ví dụ encoder thì có thêm cái text encoder và attention fusion gì đó đúng không?
Dạ
có thêm cái chuyện đó.
 Thì như vậy soi lại các kỹ thuật mà mình đã dùng trong đó thì có cái gì khác hay không? Hiểu không?
 Tự mình phải soi chứ giờ mình không nói sao ai biết.
 Hiểu không?
Dạ
mình nói thiếu thông tin quá đi.
 Tức là trong encoder thì Thì và fusion attention thì mình làm sao để mình quyện được cái tex vào đúng không?
 Mình quyện được cái tex vào thì phải giải thích cái điều đó.
 Tại vì mình nói là có prom mà te có visual prom thì cái quan trọng là mã hóa visual prom thế nào rồi quyện nó vào thế nào thì tập trung vào giải thích cái đấy.
Dạ.
Và cái kỹ thuật đó nó khác cái gì? Nó khác những cái phương pháp trước cái nào.
 Còn không thì nếu kế thừa thì bảo kế thừa.
À
còn khi đã kế thừa rồi thì xem coi mình có thể sửa cái gì trong đó nữa không.
 Giai đoạn Cuối này là cái giai đoạn contribution nè, hiểu không?
Dạ.
Chứ đừng có lấy lấy cái này ghép cái kia thì là chi? Lấy cái này ghép kia thì người ta đâu có cần đến mình phải không?
Dạ.
Mình kế thừa phương pháp của người ta. Cách làm việc nè, kế thừa phương pháp của người ta. Hiểu không?
 Rồi nhưng mà phải mở lòng mở trí ra đọc cái phương pháp của người ta người ta làm cái gì để mình học rồi và khi mình đọc như vậy á mình xem coi mình có thể thêm thắt cái gì trong đó không. Hiểu không?
 Chứ mình lấy lấy nguyên si như vậy đâu được.
 Thì như vậy của em là bây giờ hỏi là cái công đoạn email coder và fution rồi đó attention rồi đó thì là em lấy lại nguyên x hay là sao đó mình tự mình soi lại đi.
Dạ thì b
rồi cái chỗ mà mã hóa cái visual drum có gì đặc biệt không?
Dạ có.
Thì
ban đầu là em sẽ lấy lại cái góc kế thừa từ attention unit là unit có thêm attention.
 Cái thứ hai là em a tham khảo cách sử dụng from của Summit 2D sau đó. Nhưng mà submit 2D thì
nói những câu như vậy á thì không ai hiểu cái gì hết á và nó cũng không giúp em cái gì.
 Em nói em lấy lại extension unit là cái gì?
 Bây giờ cái người ta đang muốn biết nè là bây giờ em không phải phân đoạn dựa vào ảnh không mà em có cái visual prom đúng chưa?
Dạ vâng.
Thành ra người ta đang rất thắc mắc là em dùng kỹ thuật nào để mà em xử lý được cả ảnh và visual drum nó quyện lại với nhau.
 Còn khi em bảo gì đó attention unit thì attention unit là có dùng tex không? Em em cứ nói lên lửng như vậy hiểu không?
 Thành ra rất là khó hiểu chưa? á em cứ nói lơ lửng như vậy.
 Attention là attention cái gì trên chính cái ảnh đó thôi hả? Hay là sao? Có có dính gì đến tex không? Thí dụ vậy hiểu không?
Dạ
nó cứ lên lửng lên lửng vậy à.
 Tension chả hiểu là nó đã tension trên ảnh hay là trên vision prom hay là tension cái gì không rõ lắm nha.
 Em dùng attention gì rồi rồi như vậy là cái vision prom lại lấy kỹ thuật đâu để xử lý.
 Vision from em ban đầu là em sử dụng berry là vùng mà bên trong from là sẽ là 1, bên ngoài là sẽ là 0. Sau đó em cộng dồn vào trong hỏi em là bây giờ cái kỹ thuật mà mã hóa Visum Prom là em lấy em kế thừa ở đâu và có sửa gì không?
 Rồi sau đó cái kỹ thuật mà em f trộn cái cái cái embedding embedding vector của Vision Prom với eding vectơ của ảnh á thì hai cái đó mình trộn lại mình dùng kỹ thuật gì đó hai cái chỗ đó trước thấy chưa?
Dạ
hai khâu đó là quan trọng nhất trước khi đưa vào cái decoder thì coi hai cái đó kỹ thuật đó mình soi lại mình lấy lấy lấy lấy cái gì mình kế thừa cái gì và mình có sửa gì không hiểu không thì em soi lại coi cái vision prime mã hóa bằng cái gì
ờ Vision form sau nhiều lần thử nghiệm thì em chốt là nó mã hóa thành một Cái head thì cái headmap này là à đường như là Sam thì nó mã hóa bằng cái gì?
 À Sam thì nó mã hóa thành token để nó truy xuất K value với nhau tại vì nó sử dụng là VIP.
Rồi thì như vậy em á về em phải so sánh hai cái kỹ thuật đó nó khác nhau cái gì về bản chất. Nó hiểu không?
Dạ.
Hiểu không? Rồi và như vậy em có sửa đổi gì không?
Dạ.
Hay là em lấy nguyên si cái hitm kia của con Pháp kia?
Dạ cái này em có sự đổi tại ban đầu là em sử dụng là theo kiểu nó là binary nhưng mà em thấy binary thì nó có góc cạnh đồ các thứ nên kết quả nó không được tốt nên em chuyển ra thành headmap để mấy cái góc cảnh nó sẽ bị bào mòn đi để nó vậy về em tập trung trong cái chương 3 cái phần đóng góp em nói rõ cái đóng góp đó nói hiểu không?
Dạ
và đồng thời khi mình nói đó là đóng góp là người ta soi ngay người ta soi xuống cái phần thực nghiệm em có minh chứng không?
Dạ có.
Nếu em bảo đó là đóng góp thì em phải có một cái bản So sánh giữa cái cách mà em mã hóa Vision Rom theo 01 với lại mã hóa theo hitmap.
 Nếu em có cái gì hơn thì đó là cái minh chứng. Hiểu cách làm việc không?
Dạ.
Đó thì về hiện nay á là nó là trình bày không rõ lắm phải bổ sung ngay lập tức trong một tuần nha.
Dạ.
Bổ sung các kỹ thuật mới trong vòng một tuần. Hiểu không?
Dạ.
Để để đưa cái hạng lên.
 Như vậy đầu tiên là về soi lại là mình có sửa đổi cái chỗ là là encoder cái vision prom đúng chưa?
 Đó và mình phải làm sao mình lập bảng so sánh nếu mà thử được cái vision prom của cái cách làm của Sam á với lại cái cách làm này thì coi nó bản chất nó khác nhau cái gì được chưa?
 Rồi bây giờ khi quyện vào thì dùng kỹ thuật gì?
 Làm sao để cho vấn đề là làm sao để nó hiểu được cái visum trum đó nó ứng hợp gì với cái ảnh á thấy không? Thì mình quyện lại bằng cách nào đúng chưa?
 Để mà mình đưa vào decoder nó hiểu được và phân đoạn đúng chỗ ha.
 Đó thì cái kỹ thuật đó là mình dùng lại ở đâu hay là có sửa gì không?
 Ừ thì from của em nó tiếp xúc với lại encoder và decoder.
 Thì ở encoder trong quá trình nó học để chích xuất thì à nó đóng góp ở phần shit ở khúc này.
 Khi mà ra kết quả thì nó sẽ nhân thêm một cái trọng số của from nữa là trọng số này em đã hit map ra để nó ra thành trọng số là từ 0 đến 1.
 Em nói những câu đó rất là khó hiểu phải không? Để làm gì? Em nói không nghe được cái bản chất vấn đề.
 Bây giờ người ta rất muốn biết nè. Khi em nhận prom và ảnh vô em làm sao không biết mà em truyền cái vecơ cuối. Vector eming vecơ cuối á vào cho cái decoder. đó để mà nó giúp cho thằng decoder nó phân đoạn đúng cái chỗ mà mình đã vision trum đúng không?
Dạ.
Người ta muốn biết cái kỹ thuật đó là mình làm cái gì chứ còn tự nhiên là lấy hai vecơ ghép ghép ghép lại thì đâu có ý nghĩa gì.
 Hiểu không?
Dạ.
Em em đưa vào decoder cái gì cái đã. Em đưa vào decoder cái gì? Đầu vào
đầu vào decoder thì nó vẫn phân nó vẫn dự đoán giống như mô hình attention unit nhưng mà nó có thêm ưu tiên là trong cái vùng của bên trong from nó sẽ không bị mất đi là ở decoder nó sẽ loại đi những cái thành phần mà không có độ tin cậy cao nhưng mà nó vẫn giữ lại những cái trong front nhưng mà do ở
 thôi bây giờ thôi được rồi bây giờ về chuyện của em nhé em phải làm sáng tỏ hai cái module encoder và decoder được hiểu chưa
dạ
trong encoder em kế thừa cái gì em sửa cái gì decoder kế thừa gì sửa gì và khi đó phải làm nổi bật lên cái vai trò của vision prom và khi có vision prom thì các kỹ thuật nào nó đã giúp mình để mà à tận dụng được cái vision vào vào đây ha thì nghe trong bài là không hề thấy không hiểu được là đã làm cái gì trong đó nha.
 Rồi và khi đó thì phải vẽ ra offline online nha. Offline on online.
 Đó chư và cái lost function thì có gì thay đổi không?
 Nếu có thêm visual trum thì lost function có gì thay đổi không? Cái lost function trong giai đoạn học á Có function. Ừ. Có
 rồi. Đó. Thì về xem phải giải thích ra lost function có gì thay đổi không.
Và khi mình đã xác tín là mình có cái đóng góp đó thì soi lại cái thực nghiệm thì các mục đích thực nghiệm đều phải minh chứng được cho cái mà mình gọi là đóng góp.
 Tức là mình thực hiện upation study mình so sánh với những cái mà mình bảo là mình đã sửa đó ha.
 So với cái góc á mình đã sửa thì mới thấy cái hơn của mình. là cái gì hiểu không?
 Rồi và bây giờ khi phân đoạn thì một cái thắc mắc nè là bây giờ cái ảnh đầu vào á trong giai đoạn học ảnh đầu vào của em kích thước bao nhiêu?
Ờ ảnh đầu vào là kích mỗi kích thước sau đó nó sẽ resign về 512
tức là nhưng mà từ bao nhiêu về 512?
Ờ mà mọi mọi loại kích thước sau đó nó resiz về 512
không? Thì bây giờ cụ thể đi trên tập BTXRD là kính thứ bao nhiêu? 2000 mấy tới 1000 mấy tới 2000 mấy hoặc 3000 mấy nó chạy rộng
như vậy là resiz xuống chỉ còn 1/4 và 1/6
dạ
thì như vậy là là vấn đề lớn thể không
à cái của em cũng có thể mở rộng lên 1024 hoặc là 2048 nhưng mà quan trọng là sợ nó nặng quá chạy không nổ
như vậy thì ngay cái ảnh đầu vào mà mình như vậy thì rất là kẹt hiểu không
 đó chứ còn 1/6 1/4 thì rõ ràng là là mình thử cho vui chứ còn nó nó không mang ý nghĩa lắm.
Hoặc là em có thể dựa vào cái cái ảnh của nó để xác định kích thước gần nhất như là như một nó 1200 thì em có thể nâng nó lên là 1024 để nó chạy cũng được.
 Bây giờ mình về mình có thể một cái chỗ mà mình có thể cải tiếng nè là mình xem làm sao á trong giai đoạn học cái ảnh đầu vào á mình có thể giữ nguyên cái size được không?
 Mình không có resize ha. mà mình chỉ lấy giống như là chia thành những cái pature đó thì về coi cái sin transformer coi cái kiến trúc sin biết không? Sin transformer
 S transformer đây nè.
 Ờ thì trong kiến trúc đó nó có giữ cho mình cái a cái cái cái size nó không phải resize thì xem coi có dùng gì được không.
 Sin transformer SW N rồi transformer ha.
 Chứ còn phân đoạn này mà mình resiz xuống vậy thì nhưng mà nếu mà mình resiz như vậy và mình phân đoạn không có visual drum và sau đó nếu có visual drum thì nếu như nó không làm ảnh hưởng á thì đó là cái công khá cái cái phát hiện khá là thú vị của Vision Trum. Nó hiểu không?
 Bây giờ mình cứ phân đoạn nhưng mà cứ cho nó scale xuống thì chắc chắn đủ là cái performance hiệu suất nó không cao rồi
 đúng không?
Tại vì những cái size những cái streamer nó nhỏ quá đó mà resize xuống như mà 1/6 1/4 thì còn cái gì nữa đâu thì quá là khó thấy không?
 Đó rồi trong cái mạng đó mà nó down xem link chừng vài lần nữa thôi thì là cái feature map cũng không còn gì.
 Thành ra bây giờ nè một là về phải xem có thể cải thiện là không có resize mà dùng cái kiến trúc sin transformer xem có được không.
 Còn không thì mình sẽ thử một cái là phân đoạn với cũng cái size như nhỏ như thế 512 1024 rồi so với thằng T có nghĩa là so với thằng Visum DR chứ so với Visum DR tức là mặc dù cái size nó bé nhưng mà nếu có Visum DR thì nó cũng giúp cho mình phân đoạn được ví dụ vậy nếu mà có được cái thông tin minh chứng đó thì rất là hay.
Hình như em cũng có cái đó so sánh với B Rồi thôi được như vậy là về xác định lại cái đóng góp ha hiện nay là rối loạn quá và cái minh chứng cho cái đóng góp thấy không?
Dạ.
Rồi cho xem sơ một số cái kết quả và phân đoạn này đó thì khi mà mình gặp cái ảnh không có bệnh thì nó làm sao?
Ờ gặp không ảnh không bệnh thì em sẽ qua một cái mô hình phân lớp phân lớp mà em chỉ sử dụng lại để fight tin nó lại thôi để nó đưa ra kết quả là có bệnh hay không bệnh.
Nhưng mà cái quy trình là sao? Khi trong quy trình là sao? Trong giai đoạn học mình phải học cái gì? Giai đoạn test mình test cái gì?
Sẽ đưa sẽ đưa một cái ảnh ít quang vào cái from bóx buộc nghi ngờ của bác sĩ.
 Sau đó nó sẽ qua một cái mô hình phân lớp.
 Mô hình này nó sẽ xác định là có bị bệnh khối u hay không hay là có.
 Nếu như không thì mô hình sẽ kết thúc. Nếu có thì nó sẽ đưa đưa vào để mô hình.
Thì bây giờ cái chuyện mà phát hiện có bệnh hay không á là độ chính xác nó bao nhiêu? Tại vì không thì nó ảnh hưởng cái thằng sau.
 Dạ hình như là 88% khi mà kết hợp thêm cái mô hình của em nữa thì nó sẽ giảm xuống cộng 76%.
 Như vậy là mình bị ngay tại thằng kia nó sai ngay từ thằng kia.
 Nhưng mà cái đó là cái đó nó nằm ngoài cái đề tài nên là tụi em chỉ có thể dùng lại nên không có thời gian để phát.
 Không tại vì trong phân đoạn thì không thể nói nằm ngoài đề tài được.
 Phân đoạn thì người ta có thể đưa cho em một cái ảnh bất kỳ.
 Nếu mà không bệnh thì mình đừng có đóng cái mas và có bệnh thì mình đóng cái mas hiểu không? Chứ không thể mà chỉ đưa em cái ảnh có bệnh không được.
 Người ta đâu có biết thực tế đâu biết ảnh nào có bệnh hay không bệnh. Hiểu không?
Dạ.
À nhưng mà như thế này, thí dụ người ta đưa cái ảnh vô mà em bảo là có vision tr thí dụ bây giờ ông bác sĩ ổng không đóng đưa đưa đưa cái ảnh mà vô và ông bác sĩ ổng nhìn ổng cũng không chắc là chỗ nào có bệnh là ổng không đánh gì cả. Tức là visum prom là bằng rỗng á.
Dạ.
Thì có thể có đó có xem là cái tín hiệu của cái ảnh không bệnh không? Hiểu không?
 Khi ổng ổng không đánh cái vùng gì hết thì là xem như là ổng ổng cũng không chắc là cái trong đó có bệnh hay không.
Ờ thì cái phân lớp nó không có sử dụng from, nó chỉ sử dụng ảnh không để nó phân thôi.
Không không. Nhưng mà trong cái quy trình của em á, nếu mà cái ông bác sĩ ổng ổng không có cho Vision Prom á thì hệ thống làm sao hiểu không?
Dạ vâng.
Visual Prom là bạn rỗng á.
Dạ.
Thì hệ thống làm sao? Hay là lúc nào cũng phải cho
 vậy thì chắc chắc nếu là from rỗng thì em sẽ dựa thêm cái phân tích của phương lớp để Em đưa ra kết quả cuối cùng nhưng mà thường là sẽ là không có bện t em phải coi lại cái đó nha.
 Cái đó là bị thủng đó nha.
 Một là ảnh không bệnh với lại bác sĩ không đưa prom không không vẽ prom ổ ổng cũng không rõ nữa. Ổng rõ ổng không vẽ. Hiểu không?
 Dạ.
Rồi chuyện nữa là nếu như ổng vẽ prom mà sai á ổng ổng nhận thức sai ổng vẽ ổ đóng sai thì sao?
 Thí dụ cái U nó nằm ở góc trái bên dưới ông đi ổ đóng nút phải bên trên thì hệ thống làm sao?
Hệ thống nếu như cái vùng em nghĩ hệ thống nó vẫn phân đoạn theo cái from của bác sĩ tại vì nó dựa vào cái vùng chú ý của bác sĩ đó.
 Em phải lý luận thêm nha.
Em phải lý đó chỉ cho em cái cách và em phải lý luận discuss trên cái bảng phải lý luận thêm nha.
 Thứ còn mình ra một cái bảng vậy người ta hỏi tứ tung hết trong vòng 15 phút là em chịu chết. Hiểu không?
 Ở hậu trường em phải chuẩn bị tư thế sẵn sàng như vậy. Tự mình hỏi mình và tự trả lời. Hiểu chưa?
 Chứ ra đó đợi người ta hỏi làm sao mà làm sao mà em xoay kịp. Hiểu không?
Dạ.
Như vậy là cái xác suất mà cái ông bác bác bác sĩ đóng đóng đóng sai á là bao nhiêu phần trăm. Còn hiện nay là em giả sử là ông bác sĩ đóng đúng hết đúng không?
Dạ.
Ờ đó thì em phải discus phải nói cho rõ ràng mọi thứ.
 Vậy rồi em mở chat GVT ra.
 Hiện tại thì cũng chỉ là kiểu em dự đoán bác sĩ đoán sai nhưng mà vẫn trong cái vùng đó chỉ là sai lệch tâm lên thôi.
Không thì và em disc cho rõ ràng em phải cho rõ ràng chứ đây là lộn xộn lắm thấy không?
 Em mở chat civity ra chỉ cho cách làm việc nè.
 Hiện nay viết rối loạn quá nha. Và chỉnh lại chỉnh trang lại cho đàng hoàng.
 Và trong luận văn thì mình theo trình bày chương 3 phương pháp á, phương pháp đề xuất á theo trình tự nguyên lý, phương pháp giải thuật ha.
 Nguyên lý phương pháp giải thuật và trong đó phải có những cái algorithm đinh những cái algorithm là chính yếu phải có nhai viết cái anh algorism hiểu không? Trong luượng văn không thấy anh algorism ở đâu. đâu mở chat ra đi.
Dạ rồi. Ủa em chia sẻ share đi.
 Em share vào cái screen á thì để khi em đổi cái nào người ta đều thấy hết khỏi phải thay đổi tới lui.
 Bấm lại cái share và cái screen á. Rồi em upload cái bài của em vô đi. Cái báo cáo của em vô.
 Và mấy em phải tự kiểm tra cái báo cáo mình phải ít nhất là 10 lần nha.
 Phải tự kiểm tra ít nhất là 10 lần chứ còn mình làm mà mình cứ vứt đó mình trả. Sửa gì hết rồi sao? Ai là lại không có sai phải không?
 Nhưng mà mình phải sửa tới sửa lui chứ. Bốt thảy vô
đó là cái báo cáo á hả?
Dạ em viết trong
hả?
Dạ em viết trong main
báo chính phải không?
Dạ. Em bảo nêu các lỗi sai nghiêm trọng của báo cáo đính kèm thì sao nó có công cụ mình không xài nó bắt lỗi giùm cho mình.
Dạ em cũng có hỏi tối qua nên nó không đưa ra được nhiều tại v nó có nhiều
đâu rồi bấm đi. Em làm vật nào vậy? Chat GVT này có có mua bản quyền không hay là
không?
À có đăng ký có đóng phí cho nó không?
Dạ không. Nếu có đóng phí thì có bên bên đây thầy. Như vậy thì sợ nó không có
4.8
nó không có làm chậm. Cái nào có đóng phí á nó làm kỹ lắm không?
 Nó nói linh tinh trong báo cáo đính kèm. Cái này nó suy luận hơi lâu thôi. Thôi tắt tắt tắt đi thôi. Tắt đi
 tắt đi thoát ra thoát ra là sao thầy
em thoát đi để thôi để cho xem lẹ khỏi mất cộng. Em thoát của em đi. Th sao ta? Em đừng có share nữa.
Dạ. Xong
của em là có vision prom ha.
Dạ.
Đó thì về làm theo cái đó mình nói nó tìm cho mình cái lỗi để cho mình đỡ mất công ha. Rồi. thì để xem để cho xem thì nó đầy lỗi hết và mới bắn Bấm sơ vậy thôi. Đó, chưa có gì hết. Rồi thấy không?
 Dạ thấy.
Đây hỏi sơ nữa thôi nè. Nếu có lỗi sai nghiệm chọn mình cũng đừng có quá tin ha. Nhưng mà để tham khảo ha.
 Đây g lỗi sai nè. So sánh PJ PJ là cái mô hình mình đề xuất á đúng không? Với UNET là không công bằng ha.
Cái này em đang so sánh B nên t Nhưng nó sẽ không không bằng tại cái của cải tiến.
Thì như vậy mình đừng có dùng từ so sánh phải nói là sao chứ nếu đã so sánh thì phải tìm cách cho nó phe ha.
Dạ.
Chứ mình làm linh tinh quá thì lúc thì nó bảo đánh giá trên 187 ảnh. Còn cái này đánh giá trên 232 mẫu polygon.
Một ảnh nó sẽ có nhiều khối u nhưng mà from nó sẽ tính theo cái mẫu của khối u.
Thì phải nói cho rõ chứ mình nói linh tinh mình nói chung chung chung chung vậy rồi lấy con số chung chung ra mình so thì không được. Thấy không?
Dạ.
Đó thì về đây là nó nói rất rất rõ nè những cái lỗi nè ha.
 Tức là PJ Unit trong thiết lập có prom đặt kết quả cao hơn cái bên Lự động không dùng prom à như thế đây là so sánh ngân hàng giữa không nên viết như thể đây là so sánh ngân hàng giữa các mô hình thì về coi lại nha về mặt kiến trúc kết quả cao hơn có thể đến từ thông tin bổ sung nhưng không nhất thiết là do kiến trúc này ưu việt ha như vậy là hiện nay á mình nói hơn hay là sao đó thì có phải là do cái vision pr không hay là do cái kiến trúc để chưa Chứ mình nói vậy nó mơ hồ quá.
 Tại hai hệ thống là hai kiến trúc khác nhau. Hiểu chưa?
Dạ.
Rồi Visual Prom rồi có cái dù không dùng nhưng mà nhưng mà biết là công của anh nào? Có hai anh đóng góp là Vision Prm và cái kiến trúc thì công của anh nào đó thì nay rất là mơ hồ.
 Có nguy cơ Oracle Prom hoặc dùng Prom quá lý tưởng. Đó thì đây là nó nêu rất rõ những cái này nè ha.
 Thì có gì để để share lại Em tham khảo về em vào em hỏi nó thấy không? Đây là lỗi nghiêm trọng nè. Bác sĩ không có sẵn crow mas để tạo. Còn em làm sao?
Em
em lấy prom hitm được sinh bao bx lý tưởng bao quanh khao trước có phải không?
Dạ nhưng mà bao của em nó rộng hơn hoặc nó sẽ bị lợt tâm so với chút.
Sao nó bảo như thế này thì về coi lại nha. Về coi lại tức là nó bảo là cái bóc á. Cái bóc nó chưa có vẽ thật ha. Để coi lại Thì nó nói sao đó mình nghe rồi mình nó có khi nó nói cũng không đúng lắm.
Dạ.
Đơn vị đánh giá bị lẫn nè. Ảnh polygon rồi ph polygon nè nha. Vậy coi lại lộn xộn nè nha.
Đó là vì di Io không cùng đơn vị thống kê ha. Đó so sánh trực tiếp thì dễ sai bằng chất. Đó về coi lại ba cái khái niệm đó.
 Đó cái gì tùm lum là đai trung bình theo ảnh rồi lesson rồi tùm lum hết. B slide extension unit có thể chưa được tối ưu thì báo cáo attention unit thấp hơn do chưa được tối ưu thì đây là điểm yếu lớn nếu b chưa được tool công bằng thì kết luận mô hình đề xuất vườn trội bị giảm suất thuyết phục hiểu không
 dạ
đó bị lỗi nhiều lắm về phải coi lại nha đó cần làm lại gì n để gửi lại cái này so sánh với sam 2 chưa chặt tức là peja unit dùng 512 Nhưng mà sa m dùng 256
vì cấu hình của tác giả chỉ m tối đa 256
à nhưng mà em em so sánh em bảo là em so sánh
thì là cái điều kiện nó phải là như nhau phải không? Còn mình so vậy mình có hơn mình cũng không có khẳng định được tại vì thằng kia nó dùng kích thước bé quá hiểu không? Phải cẩn thận lại.
 Mình nói là đây nè nó bảo là không được kết luận quá mạnh nè. Thấy không? Nó chưa đảm bảo nè. Hiểu chưa?
Dạ
em em phải dùng từ ngữ hoặc là em discuss như thế nào đấy.
 Còn em muốn Muốn so sánh thì em phải có điều kiện nó phe get the keeper. Cái nguy cơ sót bệnh nè thấy không? Get the keeper.
 Tại vì âm tính thì dừng không phân đoạn nữa ha. Đó thì như vậy người ta sẽ claim mình là f negative nguy hiểm hơn f positive không? Tức là có bệnh mà bảo là không bệnh á thì nguy hiểm hơn là không bệnh mà bảo là có bệnh.
Dạ. Cái đó thì tụi em có điều điều chỉnh mô hình để tăng lên từ 78 lên 88 rồi thầy.
Ờ thì em phải chú ý cho nó nhiều hơn.
Rồi pipeline N2M giảm mạnh chưa sẵn sàng triển khai đó. Tại vì cái thằng này đúng thì thằng sau là cái xác suất á. Xác suất đúng là nó lại nhân với cái thằng này. Hiểu không?
Ví dụ ngay cả mình được 0,9 đi. 0,9 mà nhân với 0,8 còn có 0,7 không?
Thành ra mình xem coi có cách nào giảm bớt cái cái chuyện đó không phải suy nghĩ nha. Dạ.
Còn hiện nay tại vì em đưa vô em em phân loại thẳng thần hiểu chưa? Em em phân loại thẳng thần nhưng mà thí dụ như có những cái mẫu thì chắc chắn là nó là u phải không? Thì mình đừng có đưa vô phân loại nữa. Thí dụ như vậy hiểu không?
 Đưa phân loại nhiều khi nó lại bảo là không u thì mất công. Thì xem coi có cách nào giảm bớt cái cái cái tỷ số độ chính xác này không tăng lên. Hiểu không? cao hơn nữa không nha.
 Việc xóa ký hiệu Elloi coi là tại sao nó nói cái đó ý nghĩa gì. Tại vì cái ảnh của em á em phải coi là ai xài. Em user là bác sĩ đọc ảnh đúng không?
Dạ.
Và trên ảnh nó có RN thì ổng ổng biết là trái phải và như vậy khi em xóa thì ổng nhìn ổng lấy không biết cái ảnh đó là trái hay phải đúng không?
Đó thì phải xem lại coi. đó xem lại coi
khi mà mô hình học thì nó sẽ xóa nhưng mà cái hiển thị thì nó vương giữ hiển thị
ừ thì em phải nói sao đó cho nó hợp lý thể không chứ còn ông bác sĩ ổng nhìn á để mà ổng đánh được cái cái bóc á cái prom á đúng không?
Dạ
thì ổng cái chuyện trái phải quan trọng lắm á hiểu không?
Lệch bên là chết người ta rồi đó hiểu không? Tay đang đau tay trái nó mổ tay phải là chết người ta hiểu không?
Chưa có external validation nè chỉ có một bộ dữ liệu duy nhất Thấy không? Chỉ thử cho anh có một bộ dữ liệu duy nhất rồi.
 Tuyên bố hỗ trợ chẩn đoán hơi quá so với output. Không nên nhấn mạnh mà chưa có mas. Đó thì coi coi nó nó claim những cái đó như thế nào về sửa được cái gì sửa nha.
 Rồi thì về nhắc để gửi cho cái share cho em cái link này ha. Em coi rồi em gõ thêm vào nha. Trong này hỏi hỏi nhiều lắm nha. Em vô nè rất nhiều lỗi nha. để mà mình sửa rồi thôi được rồi hiểu ha.
Dạ
thì trong tuần này trong vòng một tuần nha sửa. Mấy em làm cận cảnh quá gần tới ngày rồi mà trong tuần này sửa lại hết những cái lỗi vừa rồi nha. Rồi tiếp đi người kế tiếp nhóm em ạ.
Sửa tới