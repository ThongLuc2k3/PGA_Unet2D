# Nháp: Q + gợi ý vùng như tín hiệu HỖ TRỢ (không phải đóng góp) + sanity-check ảnh lành

Bản tiếng Việt, chờ duyệt. Sau khi OK sẽ mirror sang 5 file EN rồi build + commit.

**Framing chốt (theo ý user):**
- Q và gợi ý vùng KHÔNG phải đóng góp chính, chỉ là hai tín hiệu hỗ trợ không cần nhãn,
  dựng trên chính trọng số mô hình đã học, trình bày ở mức thăm dò.
- Q: đo mask "lắc" bao nhiêu khi hộp bị nhiễu, cho một con số để soi kỹ hơn một mask cụ thể.
- Gợi ý vùng: cũng do trọng số đã học dẫn dắt; hộp ngẫu nhiên chỉ là giàn giáo cho một
  tính năng nhỏ nhóm đang hướng tới.
- Kém trên ảnh lành: một phần vì trọng số học trên ảnh bệnh nên chưa tốt trên ảnh lành;
  nhóm phát triển thêm sau.

Nguồn số: `Result/File_test/test-boxquality-normal-images-{btxrd,fracatlas}.ipynb`
(checkpoint PGA-512 `00`; mỗi ảnh 50 hộp ngẫu nhiên, cạnh trong `[0.15,0.55]` khung ảnh).

| | BTXRD | FracAtlas |
|---|---|---|
| ảnh lành | 1879 | 3366 |
| số hộp | 93.950 | 168.300 |
| Q trung vị | 0.00 | 0.07 |
| Q p90 | 0.75 | 0.82 |
| hộp Q ≥ 0.5 | 28% | 42% |
| TB của (Q lớn nhất mỗi ảnh) | 0.85 | 0.90 |

=======================================================================

## A. Danh sách đóng góp (`vietnam/access_vietnam.tex` ~dòng 80)

**[QUYẾT ĐỊNH 1]** Bullet hiện tại:
> \item Mô tả một điểm tự đánh giá không cần huấn luyện, dựa trên độ dứt khoát của
> mask và độ ổn định khi prompt bị nhiễu, cho phép xếp hạng độ tin cậy mà không cần
> nhãn thật, đồng thời có thể lọc ra một danh sách ngắn vùng nghi ngờ để bác sĩ xem lại.

### Phương án 1a (khuyến nghị): bỏ khỏi danh sách, chuyển thành 1 câu mờ ngay sau `\end{itemize}`

Xóa bullet trên. Thêm 1 câu ngay sau danh sách:
> Ngoài phần đóng góp trên, hệ thống còn lộ ra hai tín hiệu hỗ trợ không cần nhãn,
> tính trực tiếp từ đầu ra của mô hình đã huấn luyện: một điểm tự đánh giá xếp hạng
> độ tin cậy của mask, và một danh sách ngắn vùng ứng viên. Cả hai được trình bày ở
> mức thăm dò, không phải là đóng góp chính của bài.

### Phương án 1b: giữ 1 bullet nhưng hạ giọng
> \item Trình bày ở mức thăm dò hai tín hiệu hỗ trợ không cần nhãn, tính từ đầu ra
> của mô hình đã huấn luyện: một điểm tự đánh giá xếp hạng độ tin cậy của mask (dựa
> trên độ dứt khoát và độ ổn định khi prompt bị nhiễu), và một danh sách ngắn vùng
> ứng viên để bác sĩ xem lại.

=======================================================================

## B. Abstract (`vietnam/access_vietnam.tex` ~dòng 54, câu cuối)

**[QUYẾT ĐỊNH 2]** Câu hiện tại:
> Ngoài ra, một điểm tự đánh giá không cần huấn luyện, dựa trên độ dứt khoát của mask
> và độ ổn định khi prompt bị nhiễu, cho phép xếp hạng độ tin cậy của dự đoán mà
> không cần nhãn thật, đạt tương quan thứ hạng khoảng 0.5 đến 0.7 với Dice thực tế.

### Phương án 2a (khuyến nghị): bỏ số Spearman, rút ngắn
> Hệ thống cũng kèm hai tín hiệu hỗ trợ không cần nhãn, tính từ đầu ra của mô hình:
> một điểm tự đánh giá độ tin cậy của mask và một danh sách ngắn vùng ứng viên, cả
> hai ở mức thăm dò.

### Phương án 2b: giữ nguyên (có số)

=======================================================================

## C. Mục III.F (`vietnam/access_vietnam.tex` ~dòng 176, đoạn mở đầu)

Câu mở hiện tại:
> Bên cạnh mask dự đoán, PGA-UNet còn trả về một số vô hướng $Q$, ước lượng mức độ
> đáng tin của dự đoán mà không cần đến đáp án thật. $Q$ không phải một đại lượng
> được học; nó chỉ được tính từ chính đầu ra của mô hình lúc suy luận, là trung bình
> cộng của hai chỉ dấu.

### Sửa: thêm 1 câu định vị + 1 câu giới hạn (cuối đoạn "heuristic")

Thêm vào cuối câu mở:
> ... là trung bình cộng của hai chỉ dấu. $Q$ được dùng như một tín hiệu hỗ trợ,
> giúp người dùng soi kỹ hơn một mask cụ thể chứ không phải một thành phần cốt lõi
> của phương pháp.

Thêm vào cuối đoạn "$Q$ chỉ là một tín hiệu xếp hạng heuristic..." (sau câu "0.7 không
có nghĩa là 70%"):
> ... xác suất $70\%$ mask đúng. $Q$ cũng giả định rằng trong hộp đã có tổn thương:
> nó đo chất lượng của mask, không đo việc có hay không có tổn thương.

### Sửa câu cuối III.F về gợi ý vùng

Câu hiện tại:
> Chúng tôi tái dùng chính điểm số này để lọc ra một danh sách ngắn các vùng nghi
> ngờ khi không có prompt: ... Đây chỉ là một công cụ hỗ trợ xem lại, không phải một
> bộ phát hiện tự động.

Thêm 1 vế:
> ... không phải một bộ phát hiện tự động, mà chỉ là giàn giáo cho một tính năng gợi
> ý nhỏ chúng tôi đang hướng tới.

=======================================================================

## D. Mục IV (`vietnam/access_vietnam.tex` ~dòng 245 + ~248)

### D1. Thêm câu protocol đối chứng âm (~dòng 245, sau câu mô tả 50 hộp gợi ý vùng)
> ... và không có mask dự đoán nào tham gia vào phép đo độ phủ này. Như một đối chứng
> âm, cùng quy trình 50 hộp này còn được chạy trên các ảnh lành của mỗi bộ dữ liệu
> (1879 ảnh của BTXRD, 3366 ảnh của FracAtlas); vì không có tổn thương nên không định
> nghĩa độ phủ, chúng tôi chỉ báo cáo phân bố của $Q$.

### D2. Sửa câu "không mở rộng thêm gì" (~dòng 248)
Cũ:
> Điểm tự đánh giá và danh sách vùng ứng viên chỉ được xem là phân tích phụ trợ, đúng
> phạm vi hẹp đã nói ở Mục III.F, không mở rộng thêm gì ở đây.

Mới:
> Điểm tự đánh giá và danh sách vùng ứng viên chỉ được xem là phân tích phụ trợ, đúng
> phạm vi hẹp đã nói ở Mục III.F; ngoài một đối chứng âm trên ảnh lành, chúng tôi
> không mở rộng thêm gì ở đây.

=======================================================================

## E. Mục V-L (`vietnam/access_vietnam.tex` ~dòng 665)

### E1. Câu mở đầu mục: thêm định vị "tận dụng trọng số đã học, mức thăm dò"

Cũ:
> Dù không cần đến đáp án thật, điểm $Q$ đã trình bày ở Mục III.F vẫn bám khá sát Dice
> thật của từng prompt (Bảng~\ref{tab:selfassess}).

Mới:
> Hai tín hiệu hỗ trợ dưới đây tính trực tiếp từ đầu ra của mô hình đã huấn luyện và
> được trình bày ở mức thăm dò. Dù không cần đến đáp án thật, điểm $Q$ ở Mục III.F
> vẫn bám khá sát Dice thật của từng prompt trên các ảnh có tổn thương
> (Bảng~\ref{tab:selfassess}).

### E2. Đoạn gợi ý vùng: đổi câu chốt

Cũ (câu cuối đoạn):
> Nói cho chắc: đây chỉ là công cụ hỗ trợ xem lại thôi, $Q$ không phải xác suất thật,
> và danh sách này không thay được việc bác sĩ tự kiểm tra lại.

Mới:
> Đây chỉ là giàn giáo cho một tính năng gợi ý nhỏ: $Q$ không phải xác suất thật,
> danh sách này không thay được việc bác sĩ tự kiểm tra, và như phần tiếp theo cho
> thấy, nó chỉ có ý nghĩa khi ảnh thực sự có tổn thương.

### E3. ĐOẠN MỚI (sau đoạn gợi ý vùng + bảng tab:suggest, trước Hình demo-suggest)

> **Kiểm tra trên ảnh không có tổn thương.** Điểm $Q$ mặc định rằng trong hộp có tổn
> thương. Để soi lại giả định này, chúng tôi chạy đúng quy trình 50 hộp ở trên nhưng
> trên các ảnh lành của mỗi bộ dữ liệu (1879 ảnh không tổn thương của BTXRD, 3366 ảnh
> không gãy của FracAtlas), nơi không có độ phủ để tính (Bảng~\ref{tab:boxquality-normal}).
> $Q$ chưa ở mức thấp một cách đáng tin: trung vị sụt về gần 0, nhưng vẫn còn khoảng
> 28\% hộp trên BTXRD và 42\% hộp trên FracAtlas vượt ngưỡng $Q = 0.5$, và hầu như ảnh
> lành nào cũng có một cách đặt hộp cho điểm cao (trung bình của giá trị $Q$ lớn nhất
> mỗi ảnh là 0.85 và 0.90). Kết quả này một phần đến từ chỗ trọng số của mô hình chỉ
> được học trên ảnh có tổn thương, không có lớp âm tính, nên với một hộp bất kỳ nó vẫn
> phân đoạn dứt khoát và ổn định phần cấu trúc nằm trong hộp, còn $Q$ thì thưởng đúng
> cho hành vi đó. Vì vậy $Q$ chỉ nên hiểu là một tín hiệu chất lượng có điều kiện: nó
> xếp hạng độ tốt của một mask sau khi tổn thương đã được khoanh vùng, chứ tự nó chưa
> báo được việc không có tổn thương. Đưa thêm ảnh lành vào huấn luyện là hướng chúng
> tôi sẽ phát triển tiếp.

### E4. BẢNG MỚI `tab:boxquality-normal` (ngay sau đoạn E3)

```latex
\begin{table}[H]
\caption{Phân bố điểm tự đánh giá $Q$ trên các ảnh lành (không tổn thương), mỗi ảnh
lấy 50 hộp ngẫu nhiên. Không có tổn thương nên không định nghĩa độ phủ; chỉ báo cáo
phân bố của $Q$.}
\label{tab:boxquality-normal}
\centering
\scriptsize
\resizebox{\columnwidth}{!}{%
\begin{tabular}{lccccc}
\toprule
Bộ dữ liệu & Ảnh lành & $Q$ trung vị & $Q$ p90 & Hộp $Q\!\ge\!0.5$ & $\overline{Q_{\max}/\text{ảnh}}$ \\
\midrule
BTXRD    & 1879 & 0.00 & 0.75 & 28\% & 0.85 \\
FracAtlas & 3366 & 0.07 & 0.82 & 42\% & 0.90 \\
\bottomrule
\end{tabular}
}
\end{table}
```

=======================================================================

## F. Bàn luận (`vietnam/access_vietnam.tex` ~dòng 717, đoạn hạn chế)

Câu hiện tại (trong đoạn limitations, nói hộp phủ một phần / âm / sai vùng):
> Các trường hợp hộp chỉ phủ một phần tổn thương, hộp âm, hay hộp nhắm sai vùng không
> được bài này xử lý.

Mới:
> Các trường hợp hộp chỉ phủ một phần tổn thương, hộp âm, hay hộp nhắm sai vùng không
> được bài này xử lý; một phép kiểm tra trực tiếp cho thấy riêng điểm $Q$ vẫn ở mức
> cao trên nhiều hộp vẽ vào vùng giải phẫu lành, do trọng số mô hình chỉ được học trên
> ảnh có tổn thương. Muốn $Q$ báo được cả việc không có tổn thương thì cần huấn luyện
> thêm với vùng lành, hoặc ghép $Q$ với một cổng phát hiện hiện diện tổn thương riêng.

=======================================================================

## G. Kết luận (`vietnam/access_vietnam.tex` ~dòng 722 + ~724)

### G1. Câu về điểm tự đánh giá (~dòng 722)
Cũ:
> ... và một điểm tự đánh giá không cần huấn luyện cũng cho ra một cách xếp hạng độ
> tin cậy tuy chưa hiệu chuẩn nhưng vẫn dùng được, ngay cả khi không có nhãn thật.

Mới:
> ... kèm hai tín hiệu hỗ trợ không cần nhãn: một điểm tự đánh giá xếp hạng độ tin cậy
> của mask cho các hộp thực sự chứa tổn thương, và một danh sách ngắn vùng ứng viên,
> cả hai còn ở mức thăm dò.

### G2. Đoạn future-work (~dòng 724): thêm 1 vế vào chỗ "biến điểm tự đánh giá thành tín hiệu đã hiệu chuẩn"
> ... cùng với việc biến điểm tự đánh giá thành một tín hiệu đã hiệu chuẩn, và huấn
> luyện thêm với vùng không tổn thương để điểm cũng phản ánh được sự vắng mặt tổn
> thương, để dùng cho việc gợi ý vùng nghi ngờ trong một quy trình xem lại lâm sàng
> thực sự.

=======================================================================

## H. Bản tiếng Anh (sau khi VN duyệt)

Mirror A-G sang: `01-introduction.tex`, `00-frontmatter.tex`, `03-method.tex`,
`04-experimental-setup.tex`, `05-results.tex` (+ bảng `tab:boxquality-normal`),
`06-discussion.tex`, `07-conclusion.tex`. Build xelatex EN + VN. Grep sạch `—/–/--`.
Check `\ref` không treo. Commit + push.

## I. Việc KHÔNG làm
- Không thêm baseline hộp ngẫu nhiên cho gợi ý vùng (không claim năng lực định lượng).
- Không retrain với lớp âm tính (đổi bài toán, vỡ hết bảng số) -> future work, data đã có sẵn.
