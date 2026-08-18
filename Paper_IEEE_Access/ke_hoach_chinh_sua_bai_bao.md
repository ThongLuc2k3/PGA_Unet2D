# Kế hoạch chỉnh sửa bài báo PGA-UNet

## 0. Build + đồng bộ toàn bộ access_vietnam.tex (vòng gần nhất)

- Đã build `access.tex` bằng `latexmk -pdf` (11 trang, không lỗi fatal). Có 2 cảnh báo "Missing character" từ placeholder tiếng Việt gõ lỗi dấu (`\dj{}` trong `\address[2]` của `00-frontmatter.tex` và trong `biography.tex`, mục Lý Quốc Ngọc) — không sửa, thầy sẽ tự điền. Có cảnh báo "Overfull hbox 505pt" lặp lại ở header mỗi trang, do logo IEEE Access trong `ieeeaccess.cls`, không liên quan nội dung, không sửa.
- Trong lúc làm việc, phát hiện `05-results.tex`, `06-discussion.tex`, `07-conclusion.tex`, `02-related-work.tex`, `04-experimental-setup.tex` đã được chỉnh sửa trực tiếp trên đĩa (không phải do tôi) — nội dung mới hợp lý, đã dùng làm nguồn để dịch.
- Đã đọc lại **toàn bộ** `access.tex` (tất cả file trong `sections/`) và viết lại **toàn bộ** `access_vietnam.tex` từ đầu theo đúng nội dung hiện tại, thay vì vá từng đoạn. Lý do: khi rà kỹ phát hiện `02-related-work.tex` bản dịch bị lệch khá nhiều so với bản tiếng Anh hiện tại — có hẳn 1 đoạn thừa (nói về "patch-to-detection-to-segmentation") và 1 đoạn khác nội dung khác hẳn bản tiếng Anh mới, là tàn dư từ bản tiếng Anh cũ trước khi được viết lại theo khung "hai hướng" ở phiên làm việc trước. Đây là bằng chứng cho thấy các lần sửa từng phần trước đó đã bỏ sót phần `related-work`.
- Các nội dung khác cũng được bổ sung cho khớp đầy đủ bản tiếng Anh mới nhất: công thức mở rộng box theo tỉ lệ ngẫu nhiên $[0.15,0.45]$ trong `method.tex` (thiếu hẳn cả đoạn), câu "một họ kiến trúc chung, huấn luyện thành các mô hình riêng biệt" trong `experimental-setup.tex` (khớp ý kịch bản 1 mà thầy hỏi), câu giải thích vai trò Attention U-Net/SAM-Med2D trong mục Baseline, đoạn mở đầu mục "So sánh khớp điều kiện với SAM-Med2D" (trước đó cụt hẳn một nửa), và toàn bộ 3 câu mới thêm vào `discussion.tex`/`conclusion.tex` (đánh giá lại Attention U-Net comparison, hạn chế về prompt mô phỏng chưa tự nhiên, CBL trong kết luận, "looser and more realistic box protocols" trong hướng phát triển).
- Đã cấu trúc lại mục Thảo luận tiếng Việt theo đúng 6 điểm (Thứ nhất...Cuối cùng) khớp bản tiếng Anh, thay vì 5 điểm rút gọn như trước.
- Đã build thử `access_vietnam.tex` bằng `xelatex` (17 trang, không lỗi fatal, chỉ cảnh báo overfull hbox nhỏ và hyperref bookmark, không đáng ngại).
- Đã grep lại, không dính `—`/`–`/`--` sai quy định.

## 0b. AI khác rút gọn abstract/introduction, đã đánh giá và đồng bộ bản dịch

- Người dùng nhờ một AI khác viết lại `00-frontmatter.tex` (abstract) và `01-introduction.tex` cho ngắn gọn hơn, tránh cấu trúc lặp kiểu AI. Tôi đã rà lại: giữ đúng logic hai tầng so sánh (Attention U-Net = đo độ khó, SAM-Med2D = so sánh công bằng, không gộp chung một câu), số liệu khớp 100% với `05-results.tex`, không phạm quy định `—`/`–`/`--`, không đụng phạm vi ngoài 2 file này. Đánh giá: đạt yêu cầu.
- Chỉ sửa lại 1 chỗ: câu so SAM-Med2D bị rút gọn mất chi tiết "SAM-Med2D huấn luyện trên cả 2 điều kiện prompt còn PGA-UNet chỉ 1" (quan trọng vì làm chiến thắng ở điều kiện lệch tâm có giá trị hơn) — đã thêm lại "while SAM-Med2D saw both".
- Đã dịch lại đúng 2 đoạn abstract + introduction trong `access_vietnam.tex` theo bản tiếng Anh rút gọn mới này, build thử `xelatex` thành công (17 trang, không lỗi).

## 1. Mục tiêu trước mắt

Mục tiêu hiện tại không phải mở rộng thêm quá nhiều kỹ thuật mới, mà là:

- Viết lại `abstract` và `introduction` cho đúng bản chất bài toán.
- Đồng bộ `related work`, `results discussion`, và cách diễn giải so sánh.
- Dựa trên các kết quả đã có để tạo một câu chuyện bài báo chặt chẽ, dễ bảo vệ khi phản biện.

Ý chính cần giữ:

- Bài toán gốc khó vì tổn thương rất nhỏ, tương phản thấp, dễ chìm trong nền.
- Với loại tổn thương này, khó nhất là `khu trú đúng vùng`, không chỉ là vẽ mask.
- Hướng tự động hoàn toàn rất dễ thất bại vì phải tự tìm vài phần trăm pixel tổn thương trong toàn ảnh.
- Trong thực tế, người ta thường phải `thắt chặt vòng vây` trước, ví dụ chia patch, phát hiện vùng nghi ngờ, tạo bounding box, rồi mới segmentation.
- Cách của PGA-UNet là `nhảy cóc` qua bước detection đó bằng cách dùng luôn bounding box do bác sĩ cung cấp.
- Vì vậy, so với mô hình không dùng prompt, PGA-UNet không nên được diễn giải là "thắng trực diện", mà là cho thấy `prompt từ bác sĩ là thiết yếu`.
- So sánh công bằng về khả năng dùng prompt phải đặt với mô hình `cũng dùng prompt`, tức là `SAM-Med2D`.

## 2. Logic bài báo cần hiểu thật rõ

### 2.1. Không được nói sai bản chất so sánh với U-Net / Attention U-Net

- `Attention U-Net` hoặc `U-Net` là baseline tự động.
- Các mô hình này không được bác sĩ cung cấp vùng nghi ngờ.
- Chúng phải tự làm cả hai việc: tìm tổn thương ở đâu và tạo mask như thế nào.
- Vì thế, kết quả thấp của chúng trên BTXRD và FracAtlas chủ yếu cho thấy `bài toán không-prompt rất khó`, chứ không phải chỉ vì kiến trúc yếu.

Kết luận diễn giải đúng:

- Không nói: `PGA-UNet tốt hơn Attention U-Net nên kiến trúc tốt hơn`.
- Nên nói: `khi không có prompt, bài toán rất khó; khi có prompt từ bác sĩ, PGA-UNet tận dụng được tri thức khu trú đó để đạt kết quả cao hơn rõ rệt`.

### 2.2. Điểm so sánh công bằng thực sự là với SAM-Med2D

- Cả `PGA-UNet` và `SAM-Med2D` đều dùng prompt.
- Đây mới là so sánh cùng điều kiện thông tin.
- Khi so sánh này, ý chính không còn là "có prompt hay không", mà là:
  `đã có prompt rồi thì khai thác prompt như thế nào cho hiệu quả hơn`.

Kết luận diễn giải đúng:

- `SAM-Med2D` dùng prompt như một chỉ dẫn vị trí để tạo mask.
- `PGA-UNet` không chỉ khoanh vùng vị trí mà còn:
  - biến prompt thành prior không gian dày đặc,
  - khuếch đại tín hiệu vùng tổn thương nhỏ,
  - duy trì ảnh hưởng đó xuyên suốt encoder và decoder.

### 2.3. Ý nghĩa thật sự của PGA-UNet

- Không chỉ là "thêm prompt vào U-Net".
- Không chỉ là "segment trong bounding box".
- Điểm chính là:
  - prompt được biến thành bản đồ nhiệt Gaussian,
  - PSG khuếch đại đặc trưng liên quan prompt ở encoder,
  - CAD tiếp tục dùng thông tin prompt ở decoder,
  - nhờ đó tín hiệu tổn thương nhỏ không bị suy hao quá sớm qua các bước downsampling.

### 2.4. Ý "thắt chặt vòng vây"

Đây là ý trung tâm cần thể hiện rõ trong bài:

- Với tổn thương nhỏ, toàn ảnh là không gian tìm kiếm quá lớn.
- Cách làm thông thường là thu hẹp dần:
  - toàn ảnh,
  - patch / vùng nghi ngờ,
  - bounding box,
  - rồi mới segmentation.
- PGA-UNet bỏ qua bước detection trung gian bằng cách nhận trực tiếp bounding box từ bác sĩ.
- Vì vậy, prompt không chỉ là một tiện ích tương tác, mà là cách đưa tri thức khu trú của bác sĩ vào mô hình.

## 3. Các ý chính từ buổi trao đổi với thầy

### 3.1. Về bản chất bài toán và cách trình bày

- Phải nói rõ bài toán tổn thương nhỏ khó ở bước `khu trú`, không chỉ ở bước `segmentation`.
- Cần trình bày hai hướng rõ ràng:
  - hướng tự động hoàn toàn,
  - hướng dùng prompt / tương tác để thu hẹp không gian tìm kiếm.
- Không được gọi `U-Net` hay `Attention U-Net` là "một hướng" ngang hàng với prompt-based; đó là `technique` trong hướng tự động.
- PGA-UNet thuộc hướng dùng prompt để đi thẳng vào vùng nghi ngờ, rồi thiết kế kiến trúc để không làm mất tín hiệu vùng nhỏ.

### 3.2. Về bounding box

- Bounding box hiện tại đang random theo kiểu chưa tự nhiên.
- Nếu box quá sát tổn thương thì không thực tế vì bác sĩ khó đóng chính xác như vậy.
- Cần mô phỏng cách bác sĩ khoanh `thoải mái hơn`.
- Gợi ý của thầy:
  - lấy bounding box sát tổn thương làm gốc,
  - từ tâm box mở rộng gấp 2, gấp 3, thậm chí lớn hơn,
  - vẫn có thể cho lệch tâm nhưng phải đảm bảo tổn thương còn nằm trong box.

### 3.3. Về tổn thương nhỏ

- Tổn thương rất nhỏ nên cần "thắt chặt vòng vây".
- Nếu trên toàn ảnh tổn thương chỉ chiếm 1-2% pixel thì quá khó.
- Khi thu hẹp về patch hoặc bounding box, tỷ lệ tổn thương trong vùng đó tăng lên nhiều lần, segmentation dễ hơn.
- Phải dùng ý này để giải thích vì sao prompt có vai trò quan trọng.

### 3.4. Về cách so sánh với SAM-Med2D

- Cần chỉ ra rằng chỉ có bounding box thôi chưa chắc đủ.
- Nếu mô hình chỉ hiểu prompt như vùng cần phân đoạn, tín hiệu tổn thương nhỏ vẫn có thể quá yếu để tạo mask tốt.
- PGA-UNet khác ở chỗ:
  - prompt không chỉ giới hạn vị trí,
  - mà còn giúp khuếch đại và duy trì thông tin tổn thương nhỏ trong mạng.

### 3.5. Về loss và đánh giá

- Cần chú ý thêm loss cho vùng nhỏ.
- Thầy gợi ý xem các loss như focal loss, Tversky loss hoặc các biến thể phù hợp tổn thương nhỏ.
- `CBL` rất quan trọng.
- Với tổn thương nhỏ, tâm vùng khu trú có thể quan trọng hơn overlap thuần túy.
- Có thể bổ sung loss hoặc thành phần loss liên quan đến tâm.

### 3.6. Về hướng phát triển sau

- Có thể xây dựng thêm cơ chế `uncertainty / confidence score`.
- Khi bác sĩ chưa biết rõ có tổn thương hay không, hệ thống có thể gợi ý một số vùng nghi ngờ kèm độ tin cậy.
- Đây là hướng interactive hữu ích hơn là bắt bác sĩ tự khoanh từ đầu.
- Nhưng đây là hướng sau, không nên dồn quá nhiều thứ vào bài hiện tại.

### 3.7. Về chiến lược làm bài

- Trước mắt phải đẩy hết những gì đã có vào bài cho đầy đủ.
- Ưu tiên sửa `abstract` rồi mới sửa `introduction`.
- Khi định nghĩa và câu chuyện đúng thì các phần sau sẽ dễ sửa.
- Không nên tham quá nhiều kỹ thuật mới trong một bài.

### 3.8. Về so sánh với bài báo gốc của hai bộ dữ liệu

- Thầy muốn thêm số liệu của chính hai bài báo gốc công bố BTXRD và FracAtlas, dù hai bài đó không dùng visual prompt.
- Mục đích: cho thấy nếu không dùng prompt thì kết quả trên chính hai tập dữ liệu này thấp thế nào, làm nền cho lập luận `prompt là thiết yếu`.
- Không phải so sánh cạnh tranh, chỉ là điểm đối chiếu bối cảnh.

### 3.9. Về việc chọn Dice thay vì IoU khi bàn tổn thương nhỏ

- Với vùng tổn thương bé, thầy lưu ý nên dùng Dice khi trình bày so sánh, tránh dùng IoU làm chỉ số chính.
- Lý do: vùng càng nhỏ thì IoU càng nhạy và dễ biến động theo sai số biên, không phản ánh đúng mức độ hữu ích thực tế bằng Dice.

### 3.10. Về nhánh phân loại (classification) đã thử trước đây

- Thầy hỏi có nên thêm một hệ phân lớp `có tổn thương / không tổn thương` trước khi segmentation không.
- Nhóm đã từng thử hướng này, nhưng bỏ vì nó kéo lệch kết quả segmentation quá mạnh.
- Ghi lại làm bối cảnh, không đưa vào bài hiện tại, tránh bị hỏi lại và quên mất đã từng thử.

### 3.11. Ma trận huấn luyện/kiểm thử theo bộ dữ liệu (định hướng cho bài sau)

Thầy muốn có kịch bản rõ ràng cho ba trường hợp, để chuẩn bị trước khi phản biện hỏi:

- **Kịch bản 1 (hiện tại đang có):** hai mô hình cùng kiến trúc nhưng huấn luyện độc lập trên từng bộ dữ liệu (BTXRD riêng, FracAtlas riêng), mỗi mô hình chỉ kiểm thử trên đúng bộ dữ liệu đã huấn luyện.
- **Kịch bản 2 (chưa làm, cần làm rõ có định làm không):** vẫn hai bộ tham số huấn luyện độc lập như kịch bản 1, nhưng kiểm thử chéo, tức là bộ tham số huấn luyện trên BTXRD đem thử trên FracAtlas và ngược lại, để xem mức độ tổng quát hóa giữa hai loại tổn thương rất khác nhau (texture tổn thương da so với vết gãy xương).
- **Kịch bản 3 (hướng mở rộng bài sau):** một mô hình huấn luyện chung trên cả hai bộ dữ liệu gộp lại, ra một bộ tham số duy nhất, rồi kiểm thử trên cả hai bộ dữ liệu.
- Thầy nói rõ đây là lên kịch bản trước, không bắt buộc phải chạy hết cho bài hiện tại.

## 4. Các ý bổ sung và chỉnh sửa do người thực hiện đề xuất

### 4.1. Chỉnh logic so sánh

- Tách rõ hai tầng so sánh:
  - `Attention U-Net`: để chứng minh bài toán không-prompt là khó.
  - `SAM-Med2D`: để chứng minh cách khai thác prompt của PGA-UNet hiệu quả hơn.

### 4.2. Nhấn mạnh tổn thương nhỏ

- Trong `abstract`, `introduction`, `discussion`, cần nói rõ:
  - prompt chỉ khoanh vùng là chưa đủ,
  - tổn thương nhỏ cần được khuếch đại và bảo toàn tín hiệu.

### 4.3. Dùng các phân tích hỗ trợ

- Có thể nhắc `top dice / bottom dice` để cho thấy:
  - ở các ca Attention U-Net đã làm khá tốt, PGA-UNet vẫn ổn định hơn,
  - ở các ca Attention U-Net làm tệ, PGA-UNet giữ được vùng nghi ngờ tốt hơn nhiều.
- Dùng tập `small lesions` để làm bằng chứng mạnh nhất cho luận điểm chính.

### 4.4. Đồng bộ toàn bài

- Sau khi sửa `abstract` và `introduction`, phải đồng bộ:
  - `related work`,
  - phần mở đầu các mục `results`,
  - `discussion`,
  - `conclusion`,
  - caption hình nếu cần.

## 5. Các chỉnh sửa viết lách đã và đang cần làm

### 5.1. Đã làm

- Viết lại `abstract` (bản tiếng Anh, `00-frontmatter.tex`) theo đúng logic: hai hướng giải quyết, `thắt chặt vòng vây`, Attention U-Net chỉ dùng để cho thấy bài toán không-prompt khó, SAM-Med2D là so sánh công bằng.
- Viết lại `introduction` (bản tiếng Anh, `01-introduction.tex`) theo cùng logic, có thêm đoạn nói rõ câu hỏi khoa học trung tâm và cách đọc đúng từng phép so sánh.
- `related work` (`02-related-work.tex`) đã có sẵn khung `thắt chặt vòng vây` từ trước, khớp với abstract/introduction mới, không cần viết lại.
- Đã rà lại `abstract` và `introduction` một lần nữa: logic nhất quán với nhau, không còn câu nào đọc như "PGA-UNet thắng Attention U-Net" trực diện, không có `—`/`–`/`--` sai quy định của repo.
- Đã đồng bộ `discussion` (`06-discussion.tex`): câu thứ hai và ba của đoạn đầu được viết lại rõ ràng là Attention U-Net không nhận prompt nên chỉ dùng để đo độ khó của bài toán không-prompt, còn so sánh thật sự kiểm chứng thiết kế là với SAM-Med2D.
- Đã đồng bộ `conclusion` (`07-conclusion.tex`): thêm câu nói rõ vai trò của Attention U-Net (đo độ khó) khác với vai trò của SAM-Med2D (so sánh công bằng), và diễn giải lại cụm "Attention U-Net-defined failure cases" thành "gain concentrates exactly where localization is hardest" để tránh đọc như thắng thua trực diện.
- Đã đồng bộ `access_vietnam.tex` theo toàn bộ các thay đổi trên: abstract, introduction, và câu tương ứng trong phần kết luận tiếng Việt.
- Đã sửa `results` (`05-results.tex`), mục "Comparison with the Automatic Baseline": đoạn mở đầu trước đây viết như đang kiểm tra xem PGA-UNet có "lợi thế đo được" so với Attention U-Net hay không, đọc như so sánh trực diện. Viết lại rõ: Attention U-Net không nhận box nên đây không phải so sánh cùng điều kiện; mục đích là đo độ khó của bài toán khi mạng phải tự khu trú; khoảng cách với PGA-UNet là bằng chứng prompt cần thiết, không phải bằng chứng kiến trúc PGA-UNet vượt trội. Đồng bộ đoạn tương ứng trong `access_vietnam.tex` (mục "So sánh với baseline tự động").
- Đã rà toàn bộ `related-work` (`02-related-work.tex`), `experimental-setup` (`04-experimental-setup.tex`), và các mục còn lại của `results` (top/bottom-Dice, so sánh SAM-Med2D, small-lesion, ablation, failure modes): không tìm thấy câu nào diễn giải sai; các mục này đã trung lập hoặc đã tự đặt đúng khung (ví dụ mục top/bottom-Dice đã tự nói rõ không nên đọc như trung bình toàn cục).

### 5.1b. Vòng rà thứ ba: bảng bỏ IoU, gộp cột hình, thêm CBL vào abstract/introduction

- **Bảng:** thay `IoU` bằng `CBL` ở 3 bảng vốn có IoU: `tab:mccv` (Monte Carlo cross-validation), `tab:baseline` (so Attention U-Net), `tab:extreme` (Top-Dice/Bottom-Dice). Số liệu CBL lấy thật từ `repeated_split_summary.csv`, `attention_att_unet_results.csv`/`pga_unet2d_test_results.csv`, và `subcat_pga_vs_attention_unet.csv` (cả BTXRD và FracAtlas). Các bảng vốn không có IoU (`tab:resolution`, `tab:sam`, `tab:small`, ablation) giữ nguyên. Đồng bộ cả 3 bảng tương ứng trong `access_vietnam.tex` (Bảng 3, 4, 5).
- **Hình:** gộp cột "Input image" và cột "Prompts/Bbox" thành một cột duy nhất "Input image (with prompt)" (giữ ảnh có overlay prompt, bỏ ảnh input trơn) ở cả `unet_extreme_groups_btxrd.png` (chỉ áp dụng cho hàng PGA-UNet, hàng Attention U-Net không có cột prompt nên giữ nguyên 4 cột) và `small_lesion_sam_pga256_pga512.png` (áp dụng cho cả 3 hàng). Kết quả: cả hai hình giờ đều có 4 cột đều nhau mỗi hàng. Đã thay file, cập nhật caption Anh + Việt.
- **Abstract + Introduction:** thêm số liệu CBL vào đoạn so sánh SAM-Med2D trong `abstract` (SAM-Med2D CBL 0.4489 vs PGA-UNet CBL 0.9261 trên tập tổn thương nhỏ nhất BTXRD) và một câu trong `introduction` giải thích tại sao định vị theo tâm quan trọng ngang biên khi tổn thương quá nhỏ; thêm CBL vào 1 bullet đóng góp chính. Đồng bộ đầy đủ sang `access_vietnam.tex`.

### 5.2. Đã đồng bộ tiếp (vòng rà thứ hai)

- Đoạn "hạn chế" trong `discussion` được đồng bộ đầy đủ hai chiều giữa `06-discussion.tex` và `access_vietnam.tex`:
  - Thêm vào bản tiếng Anh đoạn hạn chế về loss (chưa có số hạng cho vùng nhỏ / tâm tổn thương, dù đánh giá đã có CBL) vốn trước đó chỉ có ở bản tiếng Việt.
  - Bổ sung vào bản tiếng Việt các ý vốn chỉ có ở bản tiếng Anh: mô hình chưa khai thác thêm nguồn thông tin ngoài ảnh + box prompt, vẫn cần giám sát bằng mask dày đặc, và Monte Carlo cross-validation chỉ phủ xu hướng chính còn ablation vẫn là một lần chia cố định.
  - Bỏ câu "đây cũng là điểm thầy đã lưu ý" trong bản tiếng Việt: đây là câu tham chiếu trực tiếp đến buổi trao đổi với thầy, không nên xuất hiện trong văn bản bài báo (kể cả bản tự kiểm tra); giữ lại đúng nội dung học thuật (prompt mô phỏng từ nhãn, chưa phản ánh cách bác sĩ thực khoanh vùng).

### 5.3. Phát hiện khi rà lại, chưa xử lý (báo lại chứ chưa tự sửa)

- `00-frontmatter.tex` dòng 10, trường `\address[2]` vẫn còn placeholder tiếng Việt gõ sai dấu (`[ c\`{\^a}n \dj{}i\`{\^e}n th\^ong tin ]`, ý là "cần điền thông tin"). Việc này không thuộc phạm vi hôm nay (thầy nói sẽ tự ghi affiliation) nên chỉ ghi chú lại, không tự sửa.
- Còn lại theo mục 4.4: rà các đoạn trong `results` để tránh câu nào vô tình diễn giải sai so sánh với `Attention U-Net`, và rà bảng/caption hình cho khớp câu chữ mới. Chưa làm.

## 6. Các chỉnh sửa kỹ thuật / thực nghiệm cần làm sau

### 6.1. Bounding box mô phỏng bác sĩ thực tế hơn

Mục tiêu:

- Thay cách sinh bounding box random hiện tại bằng cách mô phỏng hành vi khoanh vùng tự nhiên hơn.

Ý tưởng triển khai:

- Lấy bounding box bo sát tổn thương làm box gốc.
- Từ tâm box, mở rộng theo hệ số:
  - `x2`,
  - `x3`,
  - có thể thêm `x4` để thử.
- Vẫn cho phép lệch tâm.
- Mức lệch tâm nên khoảng `30% - 50%` kích thước box, với điều kiện tổn thương vẫn nằm trọn trong box.

Câu hỏi thực nghiệm cần trả lời:

- Khi box rộng hơn và tự nhiên hơn, hiệu năng PGA-UNet giảm bao nhiêu?
- Dù giảm, nó còn giữ ưu thế so với `SAM-Med2D` hay không?
- Điều kiện nào là hợp lý nhất giữa `thực tế lâm sàng` và `hiệu năng`.

### 6.2. Loss cho tổn thương nhỏ và khu trú theo tâm

Mục tiêu:

- Khi tổn thương nhỏ, loss hiện tại có thể chưa đủ nhạy với lỗi khu trú.

Ý tưởng triển khai:

- Thử thêm một hoặc vài thành phần:
  - focal loss,
  - Tversky / focal Tversky,
  - boundary-aware loss,
  - center-aware loss hoặc thành phần liên quan `CBL`.

Ưu tiên:

- Quan trọng nhất là làm cho tâm mask dự đoán gần tâm tổn thương.
- Nếu có thể, thêm một loss phản ánh sai lệch tâm.

### 6.3. Uncertainty / confidence estimation

Mục tiêu:

- Khi không có ground truth, hệ thống vẫn nên cho bác sĩ biết mức tin cậy của kết quả.

Ý tưởng triển khai:

- Huấn luyện thêm đầu ra dự đoán độ tin cậy của segmentation.
- Hoặc xây dựng score hậu kiểm từ xác suất mask / độ ổn định qua nhiều prompt.

Ứng dụng:

- Khi đưa một ảnh vào hệ thống, có thể sinh nhiều prompt ứng viên:
  - random box,
  - lưới patch,
  - các vùng chồng lấn.
- Chạy qua PGA-UNet.
- Chọn ra top-k vùng có độ tin cậy cao nhất để gợi ý cho bác sĩ.

### 6.4. Module gợi ý vùng nghi ngờ

Mục tiêu:

- Hệ thống không chỉ chờ bác sĩ khoanh box, mà còn gợi ý sẵn một số vùng.

Bản chất:

- Đây gần với một module detection / proposal.
- Nhưng ở mức bài toán tương tác, không cần xem nó là detector hoàn chỉnh.
- Có thể diễn giải là:
  - hệ thống đề nghị một số bounding box nghi ngờ,
  - bác sĩ chọn hoặc bỏ qua.

Lợi ích:

- Thực tế hơn trong lâm sàng.
- Tránh bắt bác sĩ phải tự khoanh hoàn toàn từ đầu.

## 7. Vấn đề hiển thị hình cần sửa

Vấn đề hiện tại:

- Phần trích xuất hình đang bị hiểu sai là cắt theo từng cột ảnh.

Yêu cầu đúng:

- Khi chọn một tên ảnh cụ thể, phải lấy `cả hàng` tương ứng của model đó để hiển thị.
- Không được tự ý crop theo từng cột riêng lẻ.
- Nếu một model có 4 cột, model khác có 5 cột thì vẫn chấp nhận khác nhau.
- Chỉ cần crop đủ đúng hàng của model đó rồi ghép lại.

Nhiệm vụ cần làm:

- Rà code tạo figure / crop figure.
- Xác định logic cắt hiện tại.
- Sửa theo hướng `crop by row of selected image`, không `crop by column`.

### 7.1. Đã sửa: `unet_extreme_groups_btxrd.png`

- Không tìm thấy code tạo 3 hình so sánh (`unet_extreme_groups_btxrd.png`, `small_lesion_sam_pga256_pga512.png`, `ablation_gaussian_vs_binary_case.png`) trong repo (`Results/`, `Source/`, `Paper_IEEE_Access/`), vì chúng không được commit, chỉ có file `.png` kết quả nằm sẵn trong `Paper_IEEE_Access/images/`.
- Với `unet_extreme_groups_btxrd.png`: xác định được nguồn gốc là các output ảnh (base64, nhúng sẵn trong output đã lưu) của notebook `Results/Result_BTXRD/test-subcat-pga-vs-attention-unet/test-subcat-pga-vs-attention-unet-btxrd.ipynb`, cell 3 (`visualize`, lưới 4 cột cho Attention U-Net) và cell 4 (`visualize_img`, lưới 5 cột cho PGA-UNet).
- Xác định đúng hàng cho từng ảnh bằng cách đối chiếu thứ tự `easy_stems`/`hard_stems` in ra trong output text của cell 3 (IMG000184 là phần tử thứ 3 → hàng 2 (0-index); IMG000791 là phần tử thứ 2 → hàng 1), xác nhận lại bằng cách so ảnh X-quang thật giữa hai lưới (khớp).
- Phát hiện thêm: hàm `visualize()` gọi `ax.set_ylabel(rec['stem'], ...)` rồi gọi `ax.axis('off')` ngay sau đó; `axis('off')` ẩn luôn ylabel, nên các ảnh lưới gốc **không hề hiển thị tên ảnh trên từng hàng** (đây là lỗi trong notebook, không sửa notebook lần này, chỉ ghi nhận).
- Cắt đúng, đủ hàng gốc (4 cột nguyên vẹn cho Attention U-Net, 5 cột nguyên vẹn cho PGA-UNet, gồm cả cột "Prompts (merged)" vốn bị bỏ ở ảnh cũ) rồi ghép thành ảnh mới, có tiêu đề cột riêng cho từng model (vì số cột và ý nghĩa cột khác nhau) và nhãn case. Đã thay thế file `Paper_IEEE_Access/images/results/unet_extreme_groups_btxrd.png`, cập nhật caption (Anh + Việt) nói rõ số panel khác nhau giữa hai model là có chủ đích.
- **Cập nhật vòng sau (5.1b):** theo yêu cầu gộp cột, cột "Input image" và cột "Prompts (merged)" của hàng PGA-UNet được gộp lại thành một cột "Input image (with prompt)" (giữ bản có overlay prompt). Hàng Attention U-Net không có cột prompt nên giữ nguyên 4 cột. Kết quả hai hàng đều có 4 cột. File và caption đã cập nhật theo bố cục mới này.
- **Cập nhật vòng sau nữa:** hàng PGA-UNet bị nhỏ hơn hàng Attention U-Net rõ rệt (do 2 notebook nguồn dùng figsize/số cột gốc khác nhau: `4.5*nr` cho Attention 4 cột, `4*nr` cho PGA 5 cột, nên panel PGA vốn nhỏ hơn theo pixel). Đã tính tỉ lệ = (độ rộng 1 cột Attention) / (độ rộng 1 cột PGA) ≈ 1.201, phóng to đều cả 4 panel của hàng PGA-UNet theo đúng tỉ lệ đó (giữ nguyên aspect ratio, dùng resize LANCZOS) để 2 hàng có cùng độ rộng cột, các cột thẳng hàng song song nhau. Đã thay lại file.

### 7.2. Đã sửa: `small_lesion_sam_pga256_pga512.png`

- Nguồn: notebook `Results/Result_BTXRD/test-subcat-pga-vs-sam-r256-r512/test-subcat-pga-vs-sam-r256-r512-btxrd.ipynb`, cell 6 (SAM-Med2D 256), cell 7 (PGA-UNet 256), cell 8 (PGA-UNet 512). Cả ba đều dùng chung một hàm `visualize_img` 5 cột (`Input image, Bbox / Prompt, Prediction (merged), GT (union), TP/FP/FN`) và cùng danh sách `small_lesion_balanced_test_stems`, nên cả ba lưới có cùng thứ tự hàng.
- IMG000868 là phần tử đầu tiên trong danh sách in ra ở cell 4 → hàng 0 ở cả ba lưới. Đã xác nhận lại bằng cách so ảnh X-quang thật (khớp, ảnh vai có 2 tổn thương nhỏ tách biệt).
- Ảnh cũ cũng bị lỗi y hệt mục 7.1: ép cả 3 hàng về 4 cột, bỏ cột "Bbox / Prompt", trong khi đó chính là cột quan trọng nhất để giải thích tại sao SAM-Med2D cho Dice=0.000 dù có prompt. Đã cắt đủ 5 cột gốc cho cả 3 hàng, ghép lại với 1 header chung (vì cả 3 hàng cùng layout cột), thay thế file, cập nhật caption (Anh + Việt) nêu rõ tên ảnh và phát hiện SAM-Med2D không tạo dự đoán nào từ cùng prompt.
- **Cập nhật vòng sau (5.1b):** gộp cột "Input image" và "Bbox / Prompt" thành một cột "Input image (with prompt)" cho cả 3 hàng (SAM-Med2D 256, PGA-UNet 256, PGA-UNet 512), còn lại 4 cột mỗi hàng, dùng chung 1 header. File và caption đã cập nhật theo bố cục mới này.

### 7.3. Đã gộp cột trực tiếp trên ảnh hiện có (không đổi case): `ablation_gaussian_vs_binary_case.png`, `prompt_robustness_examples.png`, `failure_case_overlap.png`

- Với `ablation_gaussian_vs_binary_case.png`: trước đó không tìm được notebook nguồn khớp (2 notebook `test-full-pga-heatmap-reference-btxrd.ipynb`/`test-full-binary-prompt-btxrd.ipynb` dùng ảnh IMG000013, còn ảnh trong bài dùng IMG001464, không khớp). Thay vì dựng lại từ notebook, lần này chỉ thao tác trực tiếp trên chính file `.png` đang có: dò biên cột bằng cách quét dòng/cột gần trắng tuyệt đối (giống cách làm ở mục 7.1/7.2), cắt bỏ cột "Input image" gốc, giữ cột "Prompt" (đổi tên thành "Input image (with prompt)"), giữ nguyên 3 cột còn lại (Prediction, Ground truth, TP/FP/FN). Không đổi case, không đổi số liệu, chỉ đổi cách trình bày cột. Vẽ lại tiêu đề mỗi hàng bằng font riêng (dùng dấu gạch ngang đơn `-` thay vì `--` gốc để không vi phạm quy định repo).
- `prompt_robustness_examples.png` (4 hàng: BTXRD/FracAtlas × Zoom-out/Shift, mỗi hàng vốn có 5 cột `Input image, Image+prompts, Prediction, Ground truth, TP/FP/FN`, ảnh minh họa cho mục "Monte Carlo Cross-Validation"/`fig:robust`): áp dụng đúng cách trên, gộp cột, vẽ lại tiêu đề + header cột.
- `failure_case_overlap.png` (mục "Failure Modes", 1 hàng 5 cột, vốn không có header/tiêu đề nào): áp dụng đúng cách trên, gộp cột, thêm header cột cho rõ ràng (trước đó ảnh này còn thiếu cả header, không riêng gì lỗi cột).
- Tất cả không cần sửa caption trong `.tex` vì các caption hiện tại không mô tả số cột cụ thể của các hình này.

## 8. Danh sách công việc chi tiết

### Nhóm A. Viết bài

1. Chốt logic câu chuyện bài báo. **Xong.**
2. Đồng bộ `abstract`, `introduction`, `related work`, `discussion`, `conclusion`, `results` (tiếng Anh + `access_vietnam.tex`). **Xong**, trừ phần hạn chế loss/CBL trong `discussion` nêu ở mục 5.2.
3. Sửa các câu diễn giải kết quả với `Attention U-Net` cho đúng vai trò baseline tự động. **Xong** ở abstract, introduction, discussion, conclusion, và mục "Comparison with the Automatic Baseline" trong `results`.
4. Nhấn mạnh so sánh công bằng với `SAM-Med2D`. **Xong** (đã có sẵn đúng khung, không cần sửa).
5. Nhấn mạnh bằng chứng mạnh nhất nằm ở tổn thương nhỏ và ablation. **Xong**, các mục này trong `results` đã có sẵn caveat đúng, không cần sửa.

### Nhóm B. Kiểm tra số liệu và minh họa

1. Rà lại các bảng liên quan `Attention U-Net`, `SAM-Med2D`, `small lesion`, `ablation`. **Xong**: số liệu và caption bảng không có gì sai, chỉ có câu dẫn trước bảng baseline cần sửa (đã sửa).
2. Rà caption hình để đồng nhất cách diễn giải. **Xong**: các caption hình hiện tại đều trung lập, không cần sửa.
3. Rà hình minh họa về prompt robustness và nhóm top/bottom dice. **Xong**, không có vấn đề.
4. Sửa logic crop hình theo hàng ảnh được chọn. Chưa làm (mục 7, việc code, không phải viết lách).

### Nhóm C. Chỉnh sửa pipeline prompt

1. Sửa cách sinh bounding box.
2. Thiết kế lại các mức mở rộng box từ tâm.
3. Thiết kế lại cơ chế lệch tâm nhưng vẫn giữ tổn thương trong box.
4. Chạy lại thực nghiệm với prompt thực tế hơn.

### Nhóm D. Chỉnh loss và độ đo

1. Rà loss hiện tại.
2. Thử loss dành cho small lesion.
3. Thử thêm thành phần liên quan tâm / `CBL`.
4. So sánh kết quả mới với cấu hình hiện tại.

### Nhóm E. Hướng mở rộng

1. Nghiên cứu confidence / uncertainty score.
2. Nghiên cứu module đề nghị vùng nghi ngờ.
3. Ma trận 3 kịch bản train/test theo bộ dữ liệu (xem mục 3.11): độc lập, kiểm thử chéo, train chung.
4. Xem khả năng đánh giá chéo miền hoặc external-domain transfer.

## 9. Thứ tự ưu tiên đề xuất

### Ưu tiên 1: Hoàn thiện bài hiện tại

- Sửa phần viết cho đúng logic. **Xong: abstract, introduction, related work, discussion, conclusion, results (tiếng Anh và bản tiếng Việt tự kiểm tra).**
- Điền đầy đủ kết quả đã có. **Đã có sẵn từ trước, không đổi.**
- Đồng bộ toàn bộ câu chuyện. **Xong**, còn lại là việc code (mục 6, 7), không phải viết lách.

### Ưu tiên 2: Sửa các chỗ ảnh hưởng trực tiếp đến tính hợp lý của thực nghiệm

- Bounding box mô phỏng thực tế hơn.
- Hình minh họa hiển thị đúng.

### Ưu tiên 3: Bổ sung cải tiến kỹ thuật thật sự có giá trị

- Loss cho small lesion / CBL.
- Confidence estimation.

### Ưu tiên 4: Hướng bài tiếp theo hoặc mở rộng sau

- Module đề nghị box.
- Ma trận 3 kịch bản train/test theo bộ dữ liệu.
- Đánh giá ngoài miền.

## 10. Kết luận ngắn

Nếu phải tóm gọn hướng chỉnh sửa hiện tại trong một câu:

`PGA-UNet không nên được trình bày như một mô hình đơn thuần thắng U-Net, mà là một hệ thống phân đoạn tương tác tận dụng tri thức khu trú của bác sĩ để giải quyết bài toán tổn thương nhỏ; và trong nhóm các mô hình cùng dùng prompt, đóng góp thật sự của nó nằm ở cách khuếch đại và duy trì tín hiệu tổn thương nhỏ xuyên suốt mạng tốt hơn cách dùng prompt kiểu chỉ khoanh vùng của SAM-Med2D.`
