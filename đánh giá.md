3. Results đang quá dài và phân mảnh
Khung dự kiến có 12 mục Results từ V-A đến V-L tại [khung_va_bo_cuc_viet_access.md:283](/home/thongluc/Khóa Luận Tốt Nghiệp/PGA_Unet2D/Paper_IEEE_Access/khung_va_bo_cuc_viet_access.md). Với bài IEEE Access, số lượng này khiến ba vấn đề xuất hiện:
- Claim chính và thí nghiệm phụ có trọng lượng hình thức gần như ngang nhau.
- Người đọc khó nhận ra đâu là kết quả quyết định.
- Nhiều bảng sử dụng lại cùng mô hình, prompt condition và tập con, gây cảm giác lặp.
Tôi đề nghị rút Results xuống còn 6 mục:
V-A. Overall performance and resolution effects
Gộp C11 và C13. Trình bày kết quả PGA-UNet trên hai dataset, ba độ phân giải và hai prompt condition.
V-B. Comparison with automatic and prompt-matched baselines
Gộp:
- Image-only Attention U-Net.
- Prompt-channel Attention U-Net.
- Prompt-crop Attention U-Net.
- SAM-Med2D.
Trong cùng mục nhưng chia hai tiểu đoạn rõ ràng:
1. Automatic reference.
2. Prompt-matched comparisons.
V-C. Small-lesion and difficult-case analyses
Đặt small-lesion làm phần chính. Top/bottom-Dice chỉ nên là phân tích phụ ở cuối mục hoặc supplementary.
Top/bottom-Dice không phải định nghĩa độ khó độc lập. Nó là subset được chọn theo lỗi của chính Attention U-Net, nên kết quả Attention U-Net thấp ở bottom group gần như là hệ quả của cách chọn nhóm. Giá trị thật của thí nghiệm là xem các mô hình prompt-guided phản ứng thế nào trên cùng những ảnh đó, không phải chứng minh “localization failure”.
V-D. Prompt displacement sensitivity and split stability
Gộp:
- center_zoom so với center_shift.
- Monte Carlo cross-validation.
Cả hai đều thuộc nhóm độ ổn định. Không cần một mục riêng chỉ để lặp lại chênh lệch prompt đã có trong mọi bảng.
V-E. Ablation and computational efficiency
Hai nội dung đều trả lời câu hỏi thiết kế có đáng giá không:
- Thành phần nào đóng góp.
- Chi phí của thiết kế.
Nếu ablation còn pending, không nên để “status note” trong manuscript nộp chính thức. Chỉ chèn mục này sau khi có số cuối.
V-F. Exploratory analyses and failure cases
Gồm:
- Loss comparison, rất ngắn.
- Failure modes.
- Self-assessment Q nếu quyết định giữ.
Cách gom này phân biệt rõ evidence chính và exploratory evidence.
4. C9 và C10 đang gây scope creep
Đây là điểm tôi sẽ đặc biệt thận trọng nếu đóng vai người hướng dẫn.
Bài được định vị là prompted segmentation với box do người dùng cung cấp. Nhưng C10 lại lấy 50 box ngẫu nhiên, xếp hạng rồi đề xuất top-k. Điều này tiến gần một bài toán candidate localization hoặc weak detection. Trong khi đó guardrails nói rõ prompt suggestion không phải nhiệm vụ đã được xác lập.
Dù luôn ghi “không phải detection”, người phản biện vẫn có thể hỏi:
- Các candidate box được sinh như thế nào?
- Có đánh giá trên ảnh âm tính không?
- Có bao nhiêu lesion trên mỗi ảnh?
- So với random ranking, saliency hoặc object proposal thì sao?
- Top-5 coverage có bị chi phối bởi box lớn và prior vị trí không?
- Tại sao một hệ thống yêu cầu clinician cung cấp box lại đồng thời đề xuất box?
Ngoài ra, tài liệu hiện mâu thuẫn về trạng thái:
- Đầu file khẳng định C9/C10 đã quay lại bài tại [khung_va_bo_cuc_viet_access.md:94](/home/thongluc/Khóa Luận Tốt Nghiệp/PGA_Unet2D/Paper_IEEE_Access/khung_va_bo_cuc_viet_access.md).
- Phần sau vẫn ghi BTXRD và Part B đang chờ tại [khung_va_bo_cuc_viet_access.md:423](/home/thongluc/Khóa Luận Tốt Nghiệp/PGA_Unet2D/Paper_IEEE_Access/khung_va_bo_cuc_viet_access.md).
- Mục quyết định cũng vẫn nói “chờ BTXRD để chốt” tại [khung_va_bo_cuc_viet_access.md:493](/home/thongluc/Khóa Luận Tốt Nghiệp/PGA_Unet2D/Paper_IEEE_Access/khung_va_bo_cuc_viet_access.md).
- claims_to_validate.md còn mô tả C9/C10 theo QualityHead cũ, không phải Q training-free.
Khuyến nghị của tôi:
- Giữ C9 như một exploratory analysis nếu kết quả đầy đủ trên cả hai dataset đã hoàn tất.
- Đưa C10 xuống supplementary hoặc future work.
- Không đưa C10 vào danh sách đóng góp chính.
- Không để candidate suggestion làm thay đổi problem statement của bài.
- Cần có baseline random-ranking trước khi trình bày C10 như một kết quả có ý nghĩa.
5. Một số thí nghiệm đang được đặt trọng lượng quá lớn
Top/bottom-Dice
Nên rút thành một bảng nhỏ hoặc supplementary. Đây là phân tích hậu nghiệm và selection-dependent. Nó không nên đứng ngang hàng với matched baseline hoặc small-lesion analysis.
Loss comparison
Kết quả âm tính là hữu ích, nhưng không phải đóng góp trung tâm. Một subsection riêng trong Results sẽ làm bài bị loãng. Tốt hơn là:
- Một đoạn cuối Experimental Setup hoặc Ablation.
- Một bảng supplementary.
- Một câu trong Discussion.
Ngoài ra, “mặc định tốt nhất hoặc ngang bằng” chỉ nên dùng nếu có uncertainty hoặc paired analysis. Từ các giá trị trung bình đơn lẻ, cách viết an toàn là “did not improve the observed test performance”.
Failure modes
Nên giữ. Tuy nhiên một ảnh minh họa không đủ để chia failure thành ba loại tổng quát như tổn thương dài, chồng lấn giải phẫu và tương phản yếu. Nếu chỉ có một hình, hãy gọi là “representative failure case”, không gọi là taxonomy of failure modes.
6. Thứ tự Results nên phản ánh sức mạnh bằng chứng
Hiện small-lesion đứng sau top/bottom và SAM comparison. Tôi đề nghị đặt thứ tự theo logic:
1. Mô hình hoạt động tổng thể ra sao?
2. Prompt access có tác động thế nào?
3. Khi cùng nhận prompt, PGA-UNet so với các mô hình khác ra sao?
4. Lợi ích có rõ hơn trên tổn thương nhỏ không?
5. Kết quả có ổn định trước displacement và split không?
6. Thành phần và chi phí ra sao?
7. Những gì chưa hoạt động hoặc còn thất bại?
Đây là tiến trình tự nhiên hơn từ bằng chứng rộng đến bằng chứng chuyên biệt.
7. Introduction không nên liệt kê quá nhiều contribution
Phần dự kiến gắn Introduction với C1, C3, C6, C7, C8, C4, C5 và C12. Danh sách này quá dài. Contribution nên giới hạn ở ba ý:
1. Kiến trúc PGA-UNet với Gaussian prompt, PSG và CAD.
2. Đánh giá có kiểm soát, tách automatic reference khỏi prompt-matched baselines trên hai dataset.
3. Phân tích small-lesion, prompt displacement, resolution và computational cost.
Monte Carlo, loss experiment, Q và candidate suggestion không nên mỗi thứ trở thành một contribution riêng.
8. Related Work cần phục vụ đúng câu hỏi trung tâm
Ba nhóm hiện tại là hợp lý. Tuy nhiên bảng prior work phải tránh biến thành bảng “checklist ưu thế” quá rộng. Nên dùng các cột thực sự phục vụ gap:
- Automatic hay prompted.
- Loại prompt.
- CNN hay foundation model.
- Prompt được tích hợp ở input, encoder hay decoder.
- Có đánh giá small-lesion hay không.
- Có kiểm tra prompt perturbation hay không.
Không nên đưa quá nhiều cột như clinical readiness, confidence, suggestion nếu các nội dung đó không phải trọng tâm đã được xác lập.
9. Method và Experimental Setup cần điều chỉnh nhẹ
Method nên chỉ trình bày thành phần của phương pháp. center_zoom, center_shift, center_mixed là protocol tạo prompt, vì vậy:
- Method chỉ cần định nghĩa biểu diễn box và Gaussian map.
- Chi tiết xác suất 80/20, shift ratio, deterministic test shift nên đặt ở Experimental Setup.
Q training-free, nếu giữ, nên gọi là “post-hoc self-assessment heuristic”, không nên tạo cảm giác nó là một nhánh cốt lõi của kiến trúc.
Mục “Offline and online framework” chỉ nên giữ nếu thật sự có hai giai đoạn rõ ràng và hình minh họa giúp hiểu luồng hệ thống. Nếu “offline” chỉ là huấn luyện và “online” chỉ là inference thông thường, mục này không tạo thêm giá trị khoa học.
10. Các lỗi quản trị tài liệu cần sửa trước khi viết tiếp
Tệp này đang vừa là:
- Khung lập luận.
- Nhật ký quyết định.
- Sổ số liệu.
- Danh sách việc.
- Ghi chú resume chat.
- Báo cáo bug.
- Mục lục bài báo.
Do đó nó có nhiều lớp trạng thái cũ và mới cùng tồn tại. Ví dụ C9/C10 vừa “gạt bỏ”, vừa “có triển vọng”, vừa “đã quay lại”. Điều này nguy hiểm hơn lỗi văn phong vì có thể dẫn đến viết sai claim.
Ngoài ra:
- Có hai mục cùng nhãn ## F: mục lục và số liệu.
- Phần “đang chờ”, “chưa làm” không còn khớp với khẳng định ở đầu file.
- claims_to_validate.md chưa đồng bộ với Q mới.
- Các con số pending và số canonical đang xen kẽ.
- Một số câu dùng “đây là bằng chứng mạnh nhất” trước khi hoàn tất kiểm định và chốt checkpoint.
Nên tách thành ba tệp:
- manuscript_outline.md: chỉ chứa câu chuyện và bố cục.
- claim_evidence_status.md: claim, bằng chứng, trạng thái, số canonical.
- work_log.md: lịch sử quyết định, bug, việc đang chờ.
Bố cục tôi khuyến nghị
I. Introduction
II. Related Work
III. Method
    A. Problem formulation and workflow
    B. Gaussian box-prompt representation
    C. Prompt Spatial Gate
    D. Conditional Attention Decoder
    E. Training objective
    F. Optional post-hoc self-assessment heuristic

IV. Experimental Setup
    A. Datasets and image-level splits
    B. Prompt simulation and preprocessing
    C. Training and checkpoint selection
    D. Baselines
    E. Metrics and statistical analysis
    F. Scope and limitations of the protocol

V. Results
    A. Overall results across datasets and resolutions
    B. Automatic-reference and prompt-matched comparisons
    C. Small-lesion and difficult-case analyses
    D. Prompt-displacement sensitivity and split stability
    E. Ablation and computational efficiency
    F. Exploratory findings and representative failures

VI. Discussion
VII. Conclusion
Phán quyết cuối cùng
Khung này có nền tảng tốt và rõ ràng tốt hơn nhiều bản thảo thông thường, đặc biệt ở việc phân biệt automatic reference với prompt-matched comparison. Tuy nhiên, trước khi chuyển sang .tex, tôi sẽ yêu cầu ba sửa đổi bắt buộc:
1. Làm yếu spine để không tuyên bố localization là nguyên nhân chính và PSG/CAD đã được chứng minh bảo toàn feature.
2. Rút Results từ 12 mục xuống khoảng 6 mục, đưa top/bottom, loss và C10 về vai trò phụ.
3. Đồng bộ lại trạng thái C9/C10, checkpoint và số liệu giữa tệp này với claims_to_validate.md.
Sau ba thay đổi đó, bố cục sẽ chặt hơn, dễ bảo vệ trước phản biện hơn và làm đóng góp PGA-UNet nổi bật thay vì bị chìm trong số lượng thí nghiệm.


10:13 AM