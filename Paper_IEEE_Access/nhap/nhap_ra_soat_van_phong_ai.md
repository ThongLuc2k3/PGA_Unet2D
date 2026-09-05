# Rà soát văn phong "quá AI" trong access.tex

Đọc toàn bộ 00 đến 08 (frontmatter/abstract, introduction, related work, method,
experimental setup, results, discussion, conclusion, back-matter). Dưới đây là
những gì tôi thấy cụ thể, có trích dẫn nguyên văn kèm file:dòng, không phải cảm
nhận chung chung.

## 1. Cùng một luận điểm bị nhắc lại bằng nhiều câu diễn giải khác nhau

Đây là dấu hiệu rõ nhất. Ý cốt lõi "prompt được giữ sống xuyên suốt mạng, thay
vì dùng một lần rồi bỏ" bị lặp lại ít nhất 6 lần, mỗi lần đổi vài chữ:

- Abstract (00-frontmatter.tex:21): "The goal is not only to use the prompt to
  indicate where segmentation should occur, but also to keep small-lesion-relevant
  features active throughout the network."
- Introduction (01-introduction.tex:11): "This design is intended to keep
  prompt-guided lesion features active throughout the network, rather than
  merely confining segmentation to a predefined box region."
- Related Work (02-related-work.tex:8): "...keeping the prompt live from the
  first encoder stage to the last decoder stage, rather than using it once and
  letting it fade."
- Method, phần CAD (03-method.tex:46): "This design is intended to keep the
  decoder conditioned on the prompt when the box is not perfectly centered."
- Method, câu tổng kết (03-method.tex:50): "...prompt information is both
  spatially softened and repeatedly reused, rather than being injected once
  and left to dissipate."
- Conclusion (07-conclusion.tex:2): "...keeps it active through an encoder-side
  Prompt Spatial Gate and a decoder-side Conditional Attention Decoder."

Một người viết thật thường chỉ phát biểu ý này thật rõ MỘT lần (thường ở
Introduction), rồi ở các chỗ khác chỉ nhắc lại ngắn gọn bằng cách trỏ về ý đó
("as described above", "for the reason given in the Introduction") chứ không
diễn giải lại toàn bộ ý bằng câu văn mới mỗi lần. Việc đổi từ ("rather than
merely confining" / "rather than using it once and letting it fade" / "rather
than being injected once and left to dissipate") mà giữ nguyên cấu trúc là
đúng kiểu AI diễn giải lại một ý nhiều cách để nghe "đa dạng" nhưng thực chất
là thừa.

**Hướng sửa:** giữ lại bản đầy đủ nhất ở Introduction, các chỗ khác cắt còn
một mệnh đề ngắn hoặc bỏ hẳn nếu không cần nhắc lại.

## 2. Một câu hỏi tu từ bị chép gần như nguyên văn ở hai mục khác nhau

- Introduction (01-introduction.tex:9): "Once a prompt has identified the
  region of interest, should it serve merely as a positional constraint for
  mask generation, or should it continue to shape feature extraction so that
  faint lesion signals survive downsampling?"
- Related Work (02-related-work.tex:6): "...once the prompt has localized the
  region, should it merely mark where the mask goes, or should it keep shaping
  feature extraction so a weak lesion signal survives downsampling?"

Hai câu này gần như là một câu được paraphrase, đặt ở hai mục cách nhau vài
trang. Đây là bằng chứng rõ nhất cho việc bài được viết theo kiểu "mỗi mục tự
sinh ra khung câu hỏi-trả lời riêng" mà không đối chiếu lại các mục khác đã
viết gì rồi.

**Hướng sửa:** chỉ đặt câu hỏi này một lần (Introduction, vì nó dẫn vào đóng
góp của bài), Related Work đổi thành một câu khẳng định ngắn nêu khoảng trống
trong các nghiên cứu trước, không hỏi lại.

## 3. Cấu trúc tu từ "không phải X mà là Y" lặp lại thành khuôn cứng

Không chỉ 2 câu trên, khuôn "not X, it is Y" / "was never X, it was Y" xuất
hiện lặp lại làm cả bài đọc như một giọng duy nhất, quá đều:

- Introduction (01:5): "This is why small-lesion segmentation is rarely just a
  boundary-delineation problem."
- Method (03:5): "It is not a side input consumed at the first layer and then
  forgotten. It becomes a dense spatial prior..."
- Discussion (06:3): "The question this article set out to answer was never
  whether a prompt helps in the abstract. It was whether..."
- Results (05:67): "So localization is a large part of the difficulty here,
  but having the box is not the whole story."

Từng câu riêng lẻ đọc ổn, nhưng gộp cả 4-5 mục đều dùng đúng một mẹo hùng biện
này thì lộ ra là văn phong máy, vì người viết thật hiếm khi tự giác lặp lại
một mẹo tu từ đều đặn như vậy xuyên suốt toàn bài.

**Hướng sửa:** chỉ giữ 1-2 chỗ dùng khuôn này (chỗ nào đáng nhất, có lẽ
Discussion), các chỗ còn lại viết lại thành câu trình bày thẳng, không vòng vo
qua phủ định trước.

## 4. Câu tự bình luận "ý nghĩa khoa học" hoặc câu hỏi tu từ mở đầu mục, giọng hơi kịch/PR

- Method (03-method.tex:50): "The scientific meaning of the contribution is
  that prompt information is both spatially softened and repeatedly reused..."
  — câu này tự đứng ra tuyên bố "ý nghĩa khoa học của đóng góp là..." ngay sau
  khi vừa liệt kê 4 bước tóm tắt phương pháp. Thừa và hơi phô trương so với
  văn phong khiêm tốn thường thấy ở IEEE Access.
- Results, mở đầu mục 3.3 (05-results.tex:71): "Where does that margin come
  from?" — câu hỏi tu từ dùng làm câu mở mục.
- Results, mở đầu mục 3.5 (05-results.tex:157): "If keeping weak evidence
  alive through the network matters anywhere, it is here." — câu văn kịch,
  đọc như câu mở đầu bài quảng cáo hơn là câu mở đầu mục kết quả.
- Results, cuối mục nhỏ lesion (05-results.tex:263): "Read narrowly, the
  smallest lesions are the stress case for the whole approach..." — "stress
  case" + "read narrowly" là lối viết có phần văn chương hóa, không cần thiết
  cho một câu chỉ đang nói "phần này khó nhất".

**Hướng sửa:** bỏ câu "scientific meaning..." (thừa, đã nói bằng 4 bước ngay
trên). Đổi câu hỏi tu từ mở mục thành câu trần thuật bình thường ("To see
where that margin comes from, we ranked..."). Bỏ chữ "stress case"/"Read
narrowly", nói thẳng "Trên đúng những ảnh này, cả prompt lẫn độ phân giải đều
ảnh hưởng nhiều hơn so với toàn tập."

## 5. Thiếu dấu vết cảm xúc/con người thật

Toàn bài không có bất kỳ chỗ nào cho thấy người viết có phản ứng cá nhân với
kết quả của chính mình: không có chỗ nào nói kiểu "kết quả này ban đầu khiến
chúng tôi bất ngờ", "chúng tôi kỳ vọng X nhưng thực tế lại là Y", hoặc một
nhận xét thoáng qua kiểu con người thường viết khi đọc lại số liệu của chính
mình. Tất cả các đoạn đều ở cùng một tông giọng "báo cáo trung tính, đã được
đánh bóng", kể cả những chỗ số liệu khá bất ngờ như:

- FracAtlas: Focal Dice loss làm HD95 vọt lên hơn 100 pixel (05:393, tab:loss)
  trong khi đang chỉ nói "Neither helped" — một kết quả tệ đến mức đó thường
  khiến người viết thật ghi thêm một câu kiểu "mức tệ này lớn hơn nhiều so với
  dự đoán ban đầu của chúng tôi khi thử nghiệm".
- Attention U-Net bottom-50 sụp xuống 0.031 Dice trên BTXRD (05:71) — gần như
  bằng không, một con số đáng để có một câu nhận xét trực tiếp hơn thay vì chỉ
  liệt kê trong câu văn trung tính.

**Hướng sửa:** đây là chỗ khó nhất vì IEEE Access không cho phép giọng văn quá
thân mật/informal. Tôi đề xuất KHÔNG thêm câu cảm xúc kiểu "chúng tôi bất ngờ"
(không phù hợp văn phong tạp chí, và tự thêm cảm xúc giả tạo sẽ phản tác dụng),
mà thay vào đó xử lý theo cách khác: giảm bớt độ đồng bộ, đồng đều giữa các
câu (mục 1-4 ở trên) để giọng văn bớt "được chải chuốt đều tăm tắp" — chỗ nào
số liệu bất ngờ thì cho phép câu văn ngắn hơn/trực tiếp hơn, không theo đúng
công thức "state result, then hedge" lặp lại ở mọi đoạn khác.

## Những gì KHÔNG có vấn đề (để không sửa nhầm)

- Bài đã rất khiêm tốn về mặt học thuật (rất nhiều hedge đúng chỗ: "This is
  not an architecture verdict", "no cross-dataset claim is made", "single-split
  noise", "Q is a heuristic ranking signal, not a calibrated probability"...).
  Đây không phải "nói quá lên" — phần overclaiming không phải vấn đề của bài
  này, không cần thêm hedge nữa.
- Không có em dash/en dash nào trong toàn bộ sections/ (đã grep, sạch).
- Phần Results với cấu trúc "câu chốt số liệu → bảng → câu diễn giải → câu giới
  hạn phạm vi" lặp lại ở mọi mục KHÔNG bị coi là lỗi ở đây — đây là cấu trúc
  báo cáo kết quả chuẩn, không phải "văn phong mượt kiểu AI"; nếu phá vỡ cấu
  trúc này để "cho có hồn" sẽ làm khó theo dõi số liệu hơn. Tôi chỉ đề xuất sửa
  các câu MỞ/ĐÓNG mục có tính tu từ, không đụng vào cách trình bày số liệu.

## Kế hoạch nếu bạn duyệt hướng trên

1. Introduction: giữ nguyên câu hỏi tu từ + câu "This design is intended to
   keep..." đầy đủ nhất (đây là nơi hợp lý nhất để phát biểu ý này lần đầu).
2. Related Work: bỏ câu hỏi tu từ trùng lặp, viết lại thành 1 câu khẳng định
   ngắn nêu khoảng trống nghiên cứu.
3. Method: bỏ câu "The scientific meaning of the contribution is..."; rút gọn
   câu "This design is intended to keep the decoder conditioned..." (CAD) vì ý
   đã nói ở Introduction.
4. Discussion: giữ cấu trúc "was never X, it was Y" (đây là chỗ hợp lý nhất
   để dùng, vì Discussion đúng là nơi tổng kết lại câu hỏi nghiên cứu).
5. Results: đổi 2 câu mở mục tu từ ("Where does that margin come from?" và
   "If keeping weak evidence alive... it is here.") thành câu trần thuật; bỏ
   "Read narrowly"/"stress case".
6. Conclusion: rút ngắn phần lặp lại ý "keeps it active..." nếu đọc lại thấy
   thừa so với Abstract.

Sau khi bạn xác nhận hướng này (hoặc chỉnh lại), tôi viết bản tiếng Anh cụ thể
cho từng câu rồi mới sửa vào .tex.

## Câu chữ cụ thể (before / after), chưa đụng vào .tex

### (a) Method, đoạn mở khung (03-method.tex:5)

BEFORE: "What sets this apart is where the prompt lives. It is not a side
input consumed at the first layer and then forgotten. It becomes a dense
spatial prior that stays active through the encoder and the decoder, which is
what should help when the box is coarse, slightly off-center, or wrapped
around a tiny lesion."

AFTER: "What sets this apart is where the prompt lives. Instead of entering
once at the first layer, it is kept as a dense spatial prior active through
the encoder and decoder, which should help when the box is coarse, slightly
off-center, or wrapped around a tiny lesion."

Lý do: gộp hai câu "It is not... It becomes..." thành một câu, bỏ khuôn phủ
định-rồi-khẳng định.

### (b) Related Work, câu hỏi tu từ trùng lặp + câu nối theo sau (02-related-work.tex:6,8)

BEFORE (dòng 6): "...none is tuned to a single radiograph task. That leaves
one question open for very small bone lesions: once the prompt has localized
the region, should it merely mark where the mask goes, or should it keep
shaping feature extraction so a weak lesion signal survives downsampling?"

AFTER: "...none is tuned to a single radiograph task. For very small bone
lesions, that leaves a gap: the prompt marks where the mask goes, but nothing
keeps it shaping feature extraction afterward, which is exactly where a weak
signal can be lost."

BEFORE (dòng 8, câu đầu + câu cuối đoạn): "That question is where this work
starts. [...] A lightweight prompt-guided CNN might do better by keeping the
prompt live from the first encoder stage to the last decoder stage, rather
than using it once and letting it fade. We study that setting directly..."

AFTER: "That gap is where this work starts. [...] A lightweight prompt-guided
CNN might do better by keeping the prompt live from the first encoder stage
to the last decoder stage. We study that setting directly..."

Lý do: bỏ câu hỏi trùng với Introduction, đổi thành câu khẳng định nêu khoảng
trống; bỏ vế "rather than using it once and letting it fade" vì ý đã nói đủ
rõ ở Introduction.

### (c) Method, CAD (03-method.tex:46)

BEFORE: "This design is intended to keep the decoder conditioned on the
prompt when the box is not perfectly centered."

AFTER: "As a result, the gate stays responsive to the prompt even when the
box is off-center."

Lý do: cắt khuôn "This design is intended to keep... active" đã lặp ở
Introduction, chỉ còn mô tả tác dụng trực tiếp.

### (d) Method, câu tổng kết cuối (03-method.tex:50)

BEFORE: "Taken together, the method can be summarized as follows: 1)
preprocess the image and prompt into a common square resolution, 2) encode
prompt-relevant spatial priors with PSG in the encoder, 3) propagate
prompt-conditioned context through CAD in the decoder, and 4) predict the
final binary lesion mask. The scientific meaning of the contribution is that
prompt information is both spatially softened and repeatedly reused, rather
than being injected once and left to dissipate."

AFTER: "Taken together, the method can be summarized as follows: 1)
preprocess the image and prompt into a common square resolution, 2) encode
prompt-relevant spatial priors with PSG in the encoder, 3) propagate
prompt-conditioned context through CAD in the decoder, and 4) predict the
final binary lesion mask."

Lý do: xóa hẳn câu "The scientific meaning of the contribution is..." — thừa,
lặp ý đã nói ở Introduction, và giọng hơi phô trương so với văn phong bài.

### (e) Results, mở mục 3.3 (05-results.tex:71)

BEFORE: "Where does that margin come from? We ranked the test images by
Attention U-Net Dice, kept the top 50 and the bottom 50 per dataset..."

AFTER: "To see where that margin comes from, we ranked the test images by
Attention U-Net Dice, kept the top 50 and the bottom 50 per dataset..."

Lý do: bỏ câu hỏi tu từ mở mục, nối thẳng vào câu mô tả cách làm.

### (f) Results, mở mục 3.5 (05-results.tex:157)

BEFORE: "If keeping weak evidence alive through the network matters anywhere,
it is here. The small-lesion subset is the 50 test images per dataset with
the least total lesion area, 7 to 433 pixels on BTXRD and 145 to 944 on
FracAtlas."

AFTER: "The small-lesion subset is where prompt-guided feature preservation
should matter most: these are the 50 test images per dataset with the least
total lesion area, 7 to 433 pixels on BTXRD and 145 to 944 on FracAtlas."

Lý do: bỏ câu "If X matters anywhere, it is here" (giọng PR), gộp thẳng vào
câu mô tả subset.

### (g) Results, cuối mục nhỏ lesion (05-results.tex:263)

BEFORE: "Read narrowly, the smallest lesions are the stress case for the
whole approach, and both the prompt conditioning and the input resolution
count for more here than on the full set."

AFTER: "On these smallest lesions, both prompt conditioning and input
resolution matter more than they do on the full test set."

Lý do: bỏ "Read narrowly"/"stress case", nói thẳng ý.

### Giữ nguyên, không sửa

- Abstract (00:21), Introduction (01:9, 01:11), Discussion (06:3): đây là nơi
  hợp lý nhất để phát biểu đầy đủ ý tưởng cốt lõi và dùng khuôn "was never X,
  it was Y" — giữ nguyên như bản gốc.
- Conclusion (07:2), câu "keeps it active through...": đã đủ ngắn (một mệnh
  đề), đúng chức năng tóm tắt phương pháp của một Conclusion, không sửa.

Bạn duyệt từng chỗ (a) đến (g) — đồng ý hết, hay muốn chỉnh câu nào trước khi
tôi sửa vào .tex?

## Cập nhật: đã áp dụng (a)-(g) vào access_vietnam.tex + rà soát thêm

Đã sửa cả 7 chỗ (a)-(g) trực tiếp vào `vietnam/access_vietnam.tex` và biên dịch
lại `access_vietnam.pdf` (dùng `xelatex`, không phải `pdflatex`, vì file này
cần `fontspec` cho font có dấu tiếng Việt).

Đọc thêm toàn bộ phần còn lại của bản dịch (Experimental Setup, hết Results,
Discussion, Conclusion, back-matter) không thấy thêm lỗi lặp cấu trúc/tu từ
nào khác — phần đó dịch bám sát bản tiếng Anh đã rà soát. Nhưng phát hiện 3
chỗ dịch quá sát nghĩa đen, đọc sượng trong tiếng Việt (ẩn dụ tiếng Anh dịch
thẳng không tự nhiên):

- (h) "mua thêm một biên nhất quán" (dịch của "buys a further, consistent
  margin") → "tạo thêm một khoảng cách ổn định"
- (i) "Độ phân giải cắn mạnh nhất ở đây." (dịch của "Resolution bites hardest
  here.") → "Ở đây độ phân giải ảnh hưởng rõ nhất."
- (j) "các lỗi có một khuôn." (dịch của "the failures have a pattern.") →
  "các lỗi này lặp lại theo một khuôn mẫu nhất định chứ không ngẫu nhiên."

Đã sửa cả 3, grep lại không còn em dash, compile sạch (26 trang).

## Cập nhật 2: phá vỡ mẫu lặp "đồng bộ máy móc" + giọng bớt trơn tru

Grep lại toàn file phát hiện hai câu giới hạn bị dán gần như nguyên văn nhiều
lần, đây mới là dấu hiệu "đồng bộ máy móc" rõ nhất (khác với lặp Ý, đây là lặp
gần như CHỮ):

**Câu "hộp phủ một phần / hộp âm / sai vùng nằm ngoài phạm vi"** xuất hiện 6
lần: Abstract (55), Method/Prompt Representation (144), Experimental
Setup/Scope (245), Results/robustness (505), Discussion (719), Conclusion
(724). Giữ nguyên bản đầy đủ ở Abstract và Method (chỗ định nghĩa phạm vi lần
đầu, hợp lý). Bốn chỗ còn lại đổi cách diễn đạt, đảo thứ tự mệnh đề, dùng từ
nối khác nhau, bớt trịnh trọng đều đặn:
- Experimental Setup (245): "Cũng xin nhắc lại: hộp phủ một phần, hộp âm, hay
  hộp sai vùng không nằm trong phạm vi khảo sát này, nên các tuyên bố của bài
  không dựa vào chúng."
- Results/robustness (505): "Chúng tôi cũng chưa thử hộp phủ một phần hay hộp
  sai vùng, nên con số này không nói được gì về hộp do bác sĩ tự vẽ tùy ý
  ngoài đời."
- Discussion (719): "...Trường hợp hộp chỉ phủ một phần, hộp âm, hay hộp sai
  vùng thì bài này chưa chạm tới."
- Conclusion (724): "Kết luận này chỉ đúng trong phạm vi protocol đã dùng:
  hộp mô phỏng quanh tổn thương có nhãn, chứ chưa phải phát hiện tự do, hộp
  sai vùng hay phủ một phần, ..."

**Câu "$Q$ là heuristic, không phải xác suất hiệu chuẩn / danh sách không
phải bộ phát hiện"** xuất hiện 4 lần: Mục III.F (190, 192 — giữ nguyên, đây
là nơi định nghĩa $Q$ lần đầu), Experimental Setup/Scope (245), Results/
self-assessment (685), Discussion (717). Ba chỗ sau đổi thành:
- (245): "Điểm tự đánh giá và danh sách vùng ứng viên chỉ được xem là phân
  tích phụ trợ, đúng phạm vi hẹp đã nói ở Mục III.F, không mở rộng thêm gì ở
  đây." (trỏ ngược lại thay vì lặp lại toàn bộ câu)
- (685): "Nói cho chắc: đây chỉ là công cụ hỗ trợ xem lại thôi, $Q$ không
  phải xác suất thật, và danh sách này không thay được việc bác sĩ tự kiểm
  tra lại." (giọng bớt trịnh trọng, thêm "Nói cho chắc" kiểu người viết thật
  hay chêm vào)
- (717): "$Q$ vẫn chỉ là một con số heuristic, chưa hiệu chuẩn, nên danh sách
  ứng viên dựng từ nó cũng chỉ nên dùng để gợi ý bác sĩ nhìn vào đâu trước,
  chứ không thay được việc tự phát hiện."

Đã compile lại, sạch, không em dash, 26 trang. Chủ đích chỉ sửa đúng hai mẫu
lặp gần-nguyên-văn này (bằng chứng rõ nhất, đo được bằng grep) chứ không viết
lại toàn bộ giọng văn 26 trang — tránh làm hỏng độ chính xác kỹ thuật của một
tài liệu vốn để tự đối chiếu số liệu.
