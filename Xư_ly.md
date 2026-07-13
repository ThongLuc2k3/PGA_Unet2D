# KẾ HOẠCH CHỈNH SỬA KHÓA LUẬN — PGA-UNet2D

Tài liệu này tổng hợp lại toàn bộ các nhận xét (về đóng góp, lỗi sai nghiêm trọng, lỗi trình bày, và các vấn đề riêng của Chương 4) thành một **kế hoạch chỉnh sửa có cấu trúc**. Mỗi **Kế hoạch lớn** là một nhóm vấn đề cùng bản chất; bên trong là các **Kế hoạch nhỏ** — từng đầu việc cụ thể, kèm lý do (bằng chứng/số liệu đã có) và hướng sửa.

---

## ĐÁNH GIÁ NỀN (căn cứ để lập kế hoạch)

Trước khi liệt kê kế hoạch sửa, cần thống nhất hiện trạng: khóa luận **đủ minh chứng cho đóng góp kỹ thuật cốt lõi** (PGA-UNet, Gaussian heatmap, PSG/CAD, so sánh U-Net/SAM-Med2D, robustness theo kịch bản đã định nghĩa, hiệu quả trên BTXRD + kiểm tra thêm FracAtlas), nhưng **chưa đủ minh chứng cho các claim mạnh về lâm sàng** (triển khai thực tế, an toàn sàng lọc, tổng quát hóa rộng, độ tin cậy với bác sĩ thật, readiness cho PACS/hospital workflow).

Chi tiết theo từng đóng góp:

1. **PGA-UNet vs U-Net/SAM-Med2D**: Bảng 4.2–4.5 cho thấy PGA-UNet vượt cả hai. Bảng 4.3: prompt lệch tâm (Shift) chỉ làm Dice giảm từ 0.8584 → 0.8454 (giảm rất ít) → claim bền bỉ với prompt lệch có cơ sở. Bảng 4.5 (cùng độ phân giải 256×256): PGA-UNet 256 đạt Dice 0.8420/0.8048/0.8317 (Zoom-out/Shift/Mixed) so với SAM-Med2D fine-tuned 0.7432/0.7159/0.7355 → claim "nhẹ nhưng hiệu quả hơn SAM-Med2D" được hỗ trợ rõ.
2. **Gaussian Heatmap + PSG + CAD**: Bảng 4.7 — V5 (đầy đủ PSG+CAD+Gaussian) đạt Dice Shift 0.8454, cao hơn rõ V1 concat heatmap (0.7268), V2 PSG-only (0.7348), V3 CAD-only (0.7410), V4 full PGA + binary prompt (0.7433). Ablation chưa full factorial (thiếu binary+concat, kiểm định thống kê cặp, prompt ngẫu nhiên/sai vị trí).
3. **Robustness prompt lệch**: đủ cho 3 kịch bản Zoom-out/Shift/Mixed (Shift vẫn giữ Dice 0.8454), nhưng **chưa đủ** để nói "bền bỉ trong lâm sàng thực tế" (chưa test bbox quá nhỏ/quá lớn/sai hoàn toàn/nhiều bác sĩ/nhiều tổn thương trong 1 ảnh).
4. **Tổng quát hóa liên miền (FracAtlas)**: Bảng 4.14 — Dice 0.7842–0.8169 tùy độ phân giải/kịch bản. Bảng 4.18 — PGA-UNet vượt SAM-Med2D rõ rệt ở nhóm tổn thương nhỏ (SAM-Med2D FT Dice 0.4395 vs PGA-UNet 512 Dice 0.8028). Nhưng N=72 ảnh test, và FracAtlas có train/val/test riêng (573/72/72) nên **không phải** true cross-dataset zero-shot generalization.
5. **Pipeline end-to-end**: Bảng 4.19 — Gatekeeper AUC-ROC 0.9405, Accuracy 88.00%, Recall 88.77%, Specificity 87.23%, F1 88.06%. Recall 88.77% nghĩa là bỏ sót 21/187 ca bệnh (11.23%) — nghiêm trọng cho hệ thống y khoa. Pipeline Dice 0.7544, thấp hơn rõ so với PGA-UNet riêng lẻ do sai số tích lũy từ Gatekeeper.

Các kế hoạch bên dưới xử lý từng nhóm vấn đề phát sinh từ đánh giá này.

---

## KẾ HOẠCH LỚN A: Hạ mức claim cho khớp với bằng chứng thực nghiệm

Vấn đề chung: nhiều chỗ trong khóa luận diễn giải kết quả mạnh hơn mức bằng chứng cho phép.

**A.1 — Sửa claim Gatekeeper "an toàn"** ✅ ĐÃ LÀM
Hiện diễn giải Recall 88.77% (bỏ sót 21/187 ca) là "đảm bảo an toàn sàng lọc", NPV 88.65% là "đủ tin cậy làm bộ lọc sơ cấp" — kết luận quá mạnh so với yêu cầu an toàn lâm sàng. Sửa: chỉ nói Gatekeeper có hiệu năng ban đầu khá tốt, **chưa đủ an toàn** để tự động chặn ảnh âm tính; cần ưu tiên tăng sensitivity và có cơ chế không cho Gatekeeper loại bỏ ca nghi ngờ.

**A.2 — Sửa claim "bền bỉ trong lâm sàng thực tế" → "bền vững trong kịch bản mô phỏng có kiểm soát"** ✅ ĐÃ LÀM
Chỉ đánh giá qua Zoom-out/Shift/Mixed (bbox mô phỏng), chưa có bbox từ nhiều bác sĩ, bbox quá nhỏ/quá lớn/sai hoàn toàn, nhiều tổn thương trong cùng ảnh. Sửa câu chữ ở mọi nơi xuất hiện (đặc biệt phần kết luận): "bền vững trước sai lệch bbox có kiểm soát trong các kịch bản Zoom-out/Shift/Mixed", không viết "bền bỉ trong lâm sàng thực tế".

**A.3 — Sửa claim "tổng quát hóa liên miền" trên FracAtlas** ✅ ĐÃ LÀM
FracAtlas có train/val/test riêng (573/72/72) → mô hình đã được huấn luyện lại trên FracAtlas, không phải test trực tiếp mô hình train-trên-BTXRD. Sửa cách viết: "đánh giá bổ sung trên bộ dữ liệu thứ hai sau khi huấn luyện/tinh chỉnh trên FracAtlas", không dùng "cross-dataset generalization" theo nghĩa external domain generalization trừ khi bổ sung thí nghiệm ở A.3.1.

**A.4 — Sửa mâu thuẫn "pipeline phản ánh sát điều kiện lâm sàng" vs. thiết kế human-in-the-loop** ✅ ĐÃ LÀM
Thiết kế hiện tại: Gatekeeper âm tính → dừng, không qua PGA-UNet, bác sĩ không có cơ hội vẽ bbox. Điều này mâu thuẫn với mô tả "human-in-the-loop" vì ở nhánh âm tính con người bị loại khỏi vòng quyết định. Sửa mô tả kiến trúc: Gatekeeper không nên là bộ chặn cứng, chỉ nên là module cảnh báo/triage mềm (xem B.3).

**A.5 — Hạ mức claim novelty của PSG/CAD** ✅ ĐÃ LÀM (khảo sát C.2/C.13 vẫn nên bổ sung sau để củng cố thêm)
Hiện mô tả PSG là "thành phần mới hoàn toàn", CAD là mở rộng Attention Gate, nhưng khảo sát liên quan còn hẹp (chủ yếu U-Net, Attention U-Net, SAM-Med2D). Cần bổ sung khảo sát (xem C.2) trước khi giữ nguyên mức claim "mới hoàn toàn".

**A.6 — Viết lại phần kết luận chung ở mức thận trọng** ✅ ĐÃ LÀM
Kết luận hiện tại viết "tính bền bỉ cao trong điều kiện lâm sàng thực tế" — dễ bị phản biện. Sửa thành: một hệ thống **thử nghiệm/tiền lâm sàng** có tiềm năng hỗ trợ phân đoạn tương tác, chưa đủ bằng chứng khẳng định an toàn hoặc sẵn sàng triển khai lâm sàng.

---

## KẾ HOẠCH LỚN B: Sửa lỗi phương pháp đánh giá (nghiêm trọng nhất)

**B.1 — Sửa công thức Pipeline Dice** ✅ ĐÃ LÀM
Hiện tại: FN (ảnh có bệnh nhưng Gatekeeper dự đoán âm) không qua PGA-UNet và "không tính" — mẫu số Pipeline Dice chỉ gồm TP+FP, FN không bị đưa vào với Dice=0. Điều này làm chỉ số pipeline "đẹp" hơn thực tế vì ca bị bỏ sót hoàn toàn không bị phạt. Sửa: tính lại Pipeline Dice trong đó **mọi FN bệnh lý được gán Dice = 0** trong mẫu số/tử số end-to-end.

**B.2 — Bổ sung các chỉ số end-to-end phản ánh đúng rủi ro lâm sàng** ✅ ĐÃ LÀM
Báo cáo thêm riêng: sensitivity bệnh lý (ở cấp độ ảnh), lesion-level recall, false negative rate, và một metric end-to-end đã tính FN=0 Dice như B.1 — không chỉ dựa vào Pipeline Dice hiện tại.

**B.3 — Đổi thiết kế Gatekeeper từ "bộ chặn cứng" sang "module triage mềm"** ✅ ĐÃ LÀM
Vì Gatekeeper bỏ sót 21/187 ca và đang được mô tả như một bước chặn cứng trước phân đoạn, cần đề xuất/chỉnh sửa thiết kế: Gatekeeper chỉ đưa ra cảnh báo/độ ưu tiên, bác sĩ vẫn có thể kiểm tra và chủ động kích hoạt phân đoạn ngay cả khi Gatekeeper dự đoán âm tính — giữ đúng tinh thần human-in-the-loop (liên kết A.4).

**B.4 — Phân tích định lượng các ca FN của Gatekeeper** ✅ ĐÃ LÀM
Bổ sung: confusion matrix đầy đủ, phân tích đặc điểm của 21 ca bị bỏ sót (loại tổn thương, kích thước, độ mờ), thử nghiệm chọn ngưỡng (threshold) ưu tiên sensitivity cao thay vì ngưỡng mặc định, và đánh giá hậu quả khi Gatekeeper chặn nhầm ảnh có bệnh.

---

## KẾ HOẠCH LỚN C: Bổ sung thực nghiệm còn thiếu

Phạm vi đã được rút gọn theo quyết định của người dùng: bỏ C.3, C.5, C.6, C.7 (ban đầu), C.9 (xem lý do ở mục "Đã bỏ khỏi phạm vi" bên dưới); C.4 đổi hướng thành sửa report thay vì thêm ablation; C.8 sau đó được khôi phục lại thành C.14. Sau đó bổ sung thêm **V7, V8** (2 biến thể ablation mới — xem ghi chú tại D.4) để khép kín câu hỏi "attention cần điều kiện hóa hay tự nó đã đủ".

**Cập nhật lớn (mới nhất): người dùng đã tự chạy xong ablation V1-V8 trên CẢ 2 dataset (BTXRD và FracAtlas)** — mỗi biến thể nằm trong `Result/Result_BTXRD/Ablation/V{1-8}/` và `Result/Result_FracAtlas/Ablation/V{1-8}/`, đều có đủ `*_results.csv` (trung bình) và `*_per_image.csv` (per-image, phục vụ Wilcoxon). Điều này làm **C.10 coi như xong** và **C.1 hết bị chặn** (đã có đủ dữ liệu để tính kiểm định, chỉ cần tôi viết code và chạy).

**[CẬP NHẬT — xem trạng thái thật sự mới nhất ở cuối file]** C.1/C.2/C.4/C.10/C.13/C.15/C.16 nay đều ✅ đã xong. **Chỉ còn thật sự CHƯA làm: C.11, C.12 (chờ GPU), C.14 (chưa bắt đầu).**

## Cập nhật (phiên viết report V1-V8): đã hoàn tất bước 1, 3, 4, 5, 6 của "KẾ HOẠCH TRIỂN KHAI TỪNG BƯỚC"

Đã chốt bộ số liệu chính thức V1-V8 (8 biến thể × 2 dataset × 3 kịch bản = 48 dòng, đối chiếu CSV `*_results.csv` với số cũ trong report — chênh lệch nhỏ ở V1-V4/V6 BTXRD do train lại cùng đợt, không đảo chiều kết luận nào). Đã cập nhật report:

- **Bảng~`tab:ablation_arch` (BTXRD, mục 4.3.1):** mở rộng 5→8 hàng (thêm U-Net+Binary, U-Net+PSG+Attention gốc, U-Net+Attention gốc). Đổi cột "CAD" thành "Attention (giải mã)" (giá trị Không/Gốc/CAD) để phản ánh đúng 3 mức chú ý. Viết lại phần mô tả 8 biến thể + giải thích lưới $2\times3$.
- **`chart_ablation.png`:** vẽ lại 8 bar/subplot (script `make_chart_ablation_btxrd.py`), giữ palette cũ (xanh dương `#2a78d6`=PGA-UNet đề xuất, xám=còn lại).
- **Mục mới 4.4.6 "Ablation kiến trúc trên FracAtlas"** (trước "Thảo luận" FracAtlas): Bảng~`tab:fracatlas_ablation_arch` (8 hàng) + Hình~`fig:chart_fracatlas_ablation` (`chart_fracatlas_ablation.png`), viết mới hoàn toàn (trước đây FracAtlas không có mục ablation).
- **C.16 (Attention U-Net thuần vs U-Net thuần):** thêm làm "điểm neo mức không câu nhắc" ở cả 2 mục ablation (BTXRD: Dice 0.4122 vs 0.4790, Δ=−0.0668; FracAtlas: 0.2467 vs 0.3831, Δ=−0.1364), lấy từ `test-attention-unet2d-btxrd.ipynb`/`test-attention-unet2d-fracatlas.ipynb`.
- **Phân tích ablation viết lại hoàn toàn** theo 5 quan sát (BTXRD) + đối chiếu trung thực BTXRD/FracAtlas (4 bullet, mục cuối FracAtlas): phát hiện chính "CAD (điều kiện hóa) mới quyết định tính bền bỉ, không phải bản thân attention" tái lặp nhất quán ở cả 2 dataset (V6 vs V7: Shift BTXRD +0.1064/FracAtlas +0.0923); một số đóng góp riêng lẻ biên độ nhỏ (CAD đơn độc không PSG, Attention gốc+PSG) đổi chiều giữa 2 dataset — đã nêu trung thực, KHÔNG ép theo giả thuyết ban đầu, và flag rõ cần Wilcoxon (C.1) trước khi khẳng định các đóng góp nhỏ này.
- **chapter1.tex dòng 108:** sửa số Shift synergy từ "+0.12" → "+0.11" (khớp số liệu mới V6−V1=+0.1059).
- **Build:** sạch, 128 trang (từ 123), không lỗi/undefined reference, đã xem trực quan các trang bảng/hình/phân tích mới (trang 57-58, 75-77).

## Cập nhật (cùng phiên): đã hoàn tất bước 2 và 7 — Wilcoxon signed-rank + viết lại phân tích với p-value chính thức

Đã viết và chạy `wilcoxon_ablation.py` (per-image CSV, bắt cặp theo `img_name`, `scipy.stats.wilcoxon`), 36 kết quả (6 cặp × 2 dataset × 3 kịch bản), lưu tại scratchpad `wilcoxon_results.csv`. Đã cập nhật report:

- **Bảng mới `tab:wilcoxon_ablation`** (mục 4.3.1, sau Hình ablation BTXRD): đầy đủ 36 kết quả (Δ Dice + p-value + mức ý nghĩa), trình bày song song BTXRD/FracAtlas, kèm đoạn "Diễn giải kiểm định".
- **Phát hiện chính được xác nhận thống kê mạnh nhất:** V6−V7 (CAD so Attention gốc, có PSG) ở Shift: $p<0{,}001$ cả 2 dataset (BTXRD +0.1065, FracAtlas +0.0924) — bằng chứng thống kê mạnh nhất cho luận điểm "điều kiện hóa (CAD) quyết định tính bền bỉ, không phải bản thân attention".
- **Phát hiện quan trọng khác:** một số cặp biên độ nhỏ (V3−V8 CAD đơn độc không PSG; V7−V2 Attention gốc đơn độc có PSG; V1−V5 Gaussian/Binary kiến trúc cơ sở) có ý nghĩa thống kê ($p<0.05$) NHƯNG ĐỔI CHIỀU DẤU giữa BTXRD và FracAtlas — xác nhận đây là hiện tượng thật (không phải nhiễu, vì cả 2 chiều đều $p<0.05$), không phải một quy luật kiến trúc phổ quát. Đã viết trung thực điều này, không ép theo giả thuyết ban đầu.
- Cập nhật lại điểm (2)(3) trong phân tích ablation BTXRD (mục 4.3.1) và toàn bộ 4 bullet đối chiếu BTXRD/FracAtlas (mục 4.4.6) để trích dẫn p-value cụ thể thay vì chỉ mô tả delta.
- **Build:** sạch, 130 trang (từ 128), không lỗi/undefined reference, đã xem trực quan trang 61-62 (bảng Wilcoxon BTXRD) và trang 78 (đối chiếu FracAtlas).

**Trạng thái C.1: ✅ HOÀN TẤT.** Toàn bộ "KẾ HOẠCH TRIỂN KHAI TỪNG BƯỚC" (8 bước) cho ablation V1-V8 đã xong. Việc còn lại trong Kế hoạch lớn C: C.11/C.12 (chờ GPU), C.14 (ảnh minh họa định tính, chưa làm).

### Việc có thể làm ngay (dữ liệu đã sẵn sàng)

**C.10 — Ablation V1-V8 trên FracAtlas** ✅ **ĐÃ CHẠY XONG** (BTXRD lẫn FracAtlas)
Cả 8 biến thể (V1-V8) đều đã có kết quả thật cho cả 2 dataset. **Việc còn lại không phải chạy thêm nữa, mà là tổng hợp số liệu vào Bảng ablation Chương 4** — bảng hiện tại trong báo cáo mới có 5-6 hàng (V1-V6), cần mở rộng thêm V7, V8, và bổ sung hẳn phần "Ablation trên FracAtlas" (hiện Chapter 4 phần FracAtlas chưa có mục ablation vì trước đó chưa chạy). Đưa CSV cho tôi là tôi cập nhật bảng + phân tích ngay.

**C.1 — Kiểm định thống kê chính thức** ✅ **HẾT BỊ CHẶN, script đã viết, CHƯA chạy**
Đã có đủ per-image CSV cho tất cả 8 biến thể, cả 2 dataset. 6 cặp đáng kiểm định nhất (chênh lệch sát nhau — bỏ qua các cặp PGA vs U-Net/SAM-Med2D vì chênh quá lớn):
- **V1 vs V8** (U-Net+Concat vs U-Net+Attention gốc — không PSG): attention tự nó có giúp không?
- **V8 vs V3** (U-Net+Attention gốc vs U-Net+CAD — không PSG): điều kiện hóa có giúp thêm không?
- **V2 vs V7** (U-Net+PSG vs U-Net+PSG+Attention gốc — có PSG): attention tự nó có giúp không, khi đã có PSG?
- **V7 vs V6** (U-Net+PSG+Attention gốc vs PGA-UNet đề xuất — có PSG): điều kiện hóa có giúp thêm không, khi đã có PSG?
- **V1 vs V5** (U-Net+Concat Gaussian vs U-Net+Concat Binary — baseline, không PSG/CAD): loại câu nhắc (Gaussian vs Binary) có khác biệt không ở baseline?
- **V4 vs V6** (PGA-UNet Binary vs PGA-UNet Gaussian — kiến trúc đầy đủ): loại câu nhắc có khác biệt không ở kiến trúc đầy đủ? (đáng chú ý: số liệu trung bình sơ bộ cho thấy dấu lệch đổi chiều giữa 3 kịch bản prompt — cần kiểm định để xác nhận có ý nghĩa thống kê hay chỉ là nhiễu)

*Khung diễn giải đã thống nhất cho cặp V1/V8 và V2/V7 (GIẢ THUYẾT — cần đối chiếu với dấu delta + p-value thực tế trước khi viết vào báo cáo, không được ép số liệu theo giả thuyết):* Attention U-Net thuần (không câu nhắc gì cả) đã biết cho kết quả THẤP HƠN U-Net gốc (xem C.16). Giả thuyết: không có tín hiệu nào phân tách vùng tổn thương với nền/nhiễu, nên cổng chú ý tự học dễ lọc nhầm giữa tổn thương thật và nhiễu. Suy rộng ra:
  - Mức không PSG (V1 vs V8): câu nhắc mới chỉ nối kênh (concat), chưa chủ động khuếch đại đặc trưng → ranh giới tổn thương/nhiễu chưa rõ → kỳ vọng attention (V8) không cải thiện rõ so với V1 (có thể không có ý nghĩa thống kê, hoặc lệch rất nhỏ).
  - Mức có PSG (V2 vs V7): PSG đã chủ động khuếch đại vùng tổn thương theo câu nhắc trước khi vào attention → khoảng cách tổn thương/nhiễu được nới rộng → kỳ vọng attention (V7) cải thiện rõ và nhất quán hơn so với V2.
  - Đây là khung diễn giải để **kiểm tra**, không phải kết luận có sẵn — nếu số liệu thật không khớp thì viết đúng theo số liệu thật.

*Việc cần làm:* chạy script đã viết sẵn (`wilcoxon_ablation.py`, dùng `scipy.stats.wilcoxon` trên cột `dice`, khớp theo `img_name`) cho cả 6 cặp × 2 dataset × 3 kịch bản prompt (zoom_out/shift/mixed_7_3) = 36 kết quả, đối chiếu với khung giả thuyết trên rồi viết đoạn phân tích vào Chapter 4.

### Còn phải chờ GPU/thực nghiệm mới

**C.11 — Train Gatekeeper + đánh giá Pipeline end-to-end trên FracAtlas**
BTXRD có `efficientnet_b3.ipynb` (Gatekeeper) và `test-pipeline-evaluation.ipynb` (pipeline end-to-end); FracAtlas hiện chưa có notebook/kết quả tương đương. Đây là bổ sung trả lời trực tiếp điểm yếu bị phê bình nặng nhất: pipeline/Gatekeeper mới chỉ được validate trên một dataset.
*Chuẩn bị:* copy `efficientnet_b3.ipynb` + `test-pipeline-evaluation.ipynb` từ Result_BTXRD, đổi dataset. **Điều kiện tiên quyết cần kiểm tra trước:** FracAtlas gốc có nhãn "fracture/no-fracture" ở cấp ảnh hay không.

**C.12 — Chạy 4-fold cross-validation trên FracAtlas** *(ưu tiên thấp nhất, chỉ làm nếu còn thời gian)*
BTXRD có `test-pga-dataset-1234.ipynb`; FracAtlas chưa có. Train set FracAtlas nhỏ (573 ảnh) nên "có thì tốt" chứ không bắt buộc — làm sau C.11 nếu còn thời gian.

**C.16 — So sánh Attention U-Net thuần vs U-Net thuần (không câu nhắc)** ✅ **DỮ LIỆU ĐÃ CÓ, sẵn sàng viết vào report**
`Result/Result_BTXRD/test-attention-unet2d-btxrd.ipynb` và `Result/Result_FracAtlas/test-attention-unet2d-fracatlas.ipynb` (cả 2 dataset) đã test Attention U-Net thuần (không câu nhắc) — đối chiếu với `Unet2D.ipynb` (U-Net gốc, cũng không câu nhắc). Đây là điểm neo "mức 0 câu nhắc" cho câu chuyện attention-vs-nhiễu đã bàn ở C.1: đã biết Attention U-Net thuần cho Dice **thấp hơn** U-Net gốc (không có PSG/CAD nào cả) — đúng tinh thần giả thuyết "attention không có tín hiệu dẫn dắt thì dễ lọc nhầm tổn thương/nhiễu". Kết hợp với V1/V8 (mức concat) và V2/V7 (mức PSG) ở C.1, tạo thành 1 mạch 3 bậc dẫn dắt ngày càng rõ: không câu nhắc (attunet thua unet) → concat (chưa rõ) → PSG (attention thắng rõ) — đúng câu chuyện PSG "khuếch đại khoảng cách tổn thương/nhiễu" giúp attention lọc chuẩn hơn.
*Việc cần làm:* lấy số liệu Dice trung bình (3 kịch bản, cả 2 dataset) từ 2 notebook trên, đưa vào Chương 4 (vị trí cụ thể quyết định lúc triển khai — xem bước 6 trong kế hoạch triển khai cuối file).

### Đã bỏ khỏi phạm vi (quyết định của người dùng)

**C.3, C.5, C.6, C.7, C.8, C.9 — BỎ, không làm.** Lý do từng mục:
- **C.3** (ablation prompt ngẫu nhiên/sai vị trí): bỏ — PGA-UNet vận hành trong phạm vi câu nhắc cho phép (thiết kế đã giới hạn phạm vi sai lệch câu nhắc hợp lý), không cần chứng minh với 2 kịch bản cực đoan này.
- **C.5** (baseline U-Net+bbox channel...): bỏ — **đã có sẵn**, chính là biến thể U-Net+Concat (V1 cũ) trong ablation hiện tại (Bảng ablation kiến trúc, D.4), không cần làm thêm.
- **C.6** (cross-dataset generalization thật, train 1 dataset → test thẳng dataset kia): bỏ — BTXRD (u xương) và FracAtlas (gãy xương) là hai loại tổn thương khác biệt về hình thái, phép thử zero-shot liên miền kiểu này không phù hợp/không có ý nghĩa giữa 2 domain quá khác nhau.
- **C.7** (confidence interval, external validation): bỏ — chưa cần thiết ở mức độ khóa luận đại học.
- **C.8** (bổ sung nhiều ảnh minh họa định tính): bỏ — chưa cần thiết ở mức độ khóa luận đại học.
- **C.9** (đánh giá liên chuyên gia): bỏ — cần người thật (nhiều bác sĩ), ngoài khả năng thực hiện.

**C.4 — Ablation tiền xử lý** ✅ **ĐÃ LÀM (đổi thành xóa nội dung tiền xử lý + đồng bộ toàn bộ số liệu BTXRD)**
User xác nhận đã train lại toàn bộ trên **dataset gốc, không qua bước tiền xử lý YOLOv11s+Roboflow** (số liệu Result_BTXRD/*.ipynb đã cập nhật). Đã thực hiện:
1. **Xóa/viết lại mô tả tiền xử lý:** Chapter3 (đổi tên mục 3.2 → "Bộ dữ liệu ảnh X-quang và đặc điểm nhiễu kỹ thuật", đổi subsec:preprocessing_pipeline → "Huấn luyện trực tiếp trên ảnh gốc, không qua bước tiền xử lý loại nhiễu", xóa `fig:preprocessing_pipeline`); Algorithm 1/2 (xóa bước "Tiền xử lý YOLOv11s xóa R/L", bỏ khái niệm bản sao I' riêng cho model, dùng chung 1 ảnh gốc I xuyên suốt); Chapter1 (câu mô tả Chương 3); Appendix/decuong.tex Giai đoạn 2; Chapter4 (câu "Lý do chọn BTXRD", câu "Ảnh chất lượng thấp").
2. **Đồng bộ lại TOÀN BỘ số liệu BTXRD ở Chapter4** theo notebook đã re-run (dataset gốc): `tab:baseline_comparison`, `tab:robustness_comparison`, `tab:sam_comparison` (PGA-256/SAM-FT-256/SAM-ZS-256 — phát hiện quan trọng: ở cấu hình mới PGA **vượt trội SAM ngay cả cùng độ phân giải** về độ bền bỉ, đảo ngược kết luận cũ), `tab:pga_256_512`, `tab:cross_validation`+per-fold, `tab:subcat_baseline`, `tab:subcat_sam`, `tab:subcat_sam_256`, `tab:classification_results` (Gatekeeper), `tab:pipeline_eval` (Pipeline Dice 0.6793→0.6763, TP/FP/FN/TN 166/24/21/164→167/26/20/162). Cập nhật kèm chapter1.tex/chapter5.tex/tomtat.tex headline numbers. Vẽ lại 2 biểu đồ: `chart_baseline_sam_comparison.png`, `chart_subcat_btxrd.png`.
3. **CHƯA làm được (thiếu dữ liệu mới, đã flag rõ trong report):** 3 bảng phân tích FN chi tiết (phân bố xác suất, threshold sweep, so sánh diện tích FN/TP) và bảng lesion-level (Mục 4.7.5) vẫn dùng confusion matrix CŨ (166/24/21/164) vì không tìm thấy notebook nào tính lại các phân tích per-polygon/per-threshold này trên cấu hình mới (167/26/20/162) — đã thêm ghi chú rõ ràng ngay trong report (đầu Mục "Phân tích các ca bỏ sót") flag đây là số liệu cũ, cần chạy lại trước khi nộp chính thức.
4. **Build:** sạch, 130 trang, không lỗi/undefined reference, đã xem trực quan các trang bảng chính (47, 50, 62, 90...).
5. **Đã xóa hẳn trích dẫn Roboflow/YOLOv11s** (không chỉ recharacterize): xóa câu nhắc "một số phiên bản thử nghiệm ban đầu từng cân nhắc..." khỏi Chapter3, xóa 2 entry `yolov11`/`roboflow2023` khỏi `references.bib`, xóa dòng YOLOv11s khỏi `Appendix/danhmuctuvietat.tex` (giữ lại R/L vì vẫn dùng xuyên suốt). Xác nhận không còn "Roboflow"/"YOLO" ở bất kỳ trang PDF nào. Build lại sạch, 130 trang.

### Nhóm còn giữ lại — Không cần thực nghiệm, chỉ cần đọc/viết/tổng hợp

**C.2 — Khảo sát liên quan (related work) rộng hơn để bảo vệ claim novelty** ✅ ĐÃ LÀM (vòng 1)
Bổ sung khảo sát các phương pháp đưa prompt/bbox/mask/click vào CNN, attention U-Net có điều kiện, interactive segmentation y khoa, MedSAM, SAM-based adapters, nnU-Net-based prompt variants — làm nền cho A.5.

**C.13 — Tìm kiếm bài báo liên quan có kiến trúc tương tự PSG/CAD/PGA-UNet** ✅ ĐÃ LÀM (vòng 1)
Chủ động tìm càng nhiều càng tốt các bài báo/công trình đã công bố có kiến trúc/ý tưởng tương tự: (a) cơ chế "gate" không gian điều biến đặc trưng encoder theo tín hiệu câu nhắc/mask (tương tự PSG), (b) cơ chế attention ở decoder được điều kiện hóa bởi đặc trưng câu nhắc (tương tự CAD), (c) kiến trúc kết hợp cả hai dạng (tương tự tổng thể PGA-UNet).

*Kết quả khảo sát (đã được người dùng duyệt trước khi đưa vào báo cáo):* ý tưởng nền tảng (tiêm bản đồ không gian vào CNN; attention gate ở decoder) đã có người làm trước — không phải "hoàn toàn mới" — nhưng cách cụ thể hóa và kết hợp cả hai trong một CNN nhẹ huấn luyện từ đầu cho bbox-prompt thì chưa thấy công trình nào giống hệt — không phải "chỉ ghép lại cái cũ". Đã chốt mức claim trung dung này.
- **PSG** — gần nhất: DeepIGeoS (Wang et al., TPAMI 2019, ghép kênh bản đồ khoảng cách tương tác — khác PSG ở chỗ concat chứ không phải gate nhân) và một công trình cuối 2025 tiêm Gaussian heatmap vào các tầng encoder của SAM lúc test-time adaptation (Xu et al. 2025, arXiv 2512.04520 — áp dụng trên ViT nền tảng, không phải CNN huấn luyện từ đầu).
- **CAD** — không tìm thấy công trình nào làm đúng "attention gate decoder điều kiện hóa bằng đặc trưng câu nhắc bên ngoài" (khác Attention U-Net gốc vốn tự điều kiện hóa bằng đặc trưng decoder nội bộ).
- **Bối cảnh chung**: khảo sát "Prompt Mechanisms in Medical Imaging: A Comprehensive Survey" (Yang et al. 2025, arXiv 2507.01055) xác nhận phần lớn hướng nghiên cứu hiện nay tập trung vào tinh chỉnh mô hình nền tảng (SAM adapters...), củng cố việc định vị PGA-UNet là hướng CNN nhẹ khác biệt.

**Đã cập nhật vào report** (không đào sâu thêm — đúng theo yêu cầu người dùng, chỉ hiểu sơ ý tưởng đối chiếu):
- `Report/References/references.bib`: thêm 3 entry mới (`wang2019deepigeos`, `xu2025boundaryaware`, `yang2025promptmechanisms`).
- `Report/Chapter3/chapter3.tex`: sửa Bảng~`tab:inheritance_contribution` (hàng PSG: bỏ "Không có"/"**Hoàn toàn mới**" quá mạnh, thay bằng cột "Kế thừa từ" trích 2 công trình gần nhất + cột "Đóng góp mới" nêu cụ thể "cơ chế gate nhân, không phải ghép kênh"); mở rộng đoạn văn giới thiệu PSG (Mục~3.3.2) với cùng tinh thần.
- `Report/Chapter1/chapter1.tex`: mục Đóng góp — câu PSG bổ sung trích dẫn ngắn gọn + trỏ sang Bảng~3.1 (Chương 3) để xem chi tiết; câu CAD bổ sung `\cite{oktay2018attentionunet}` còn thiếu.
- Build sạch, 123 trang, không lỗi/undefined reference; đã kiểm tra trực quan bảng + đoạn văn (không tràn lề, trích dẫn hiển thị đúng số [9][10][11]).

*Lưu ý phạm vi:* khảo sát này không toàn diện tuyệt đối (~7 lượt tìm kiếm), câu chữ trong báo cáo giữ mức thận trọng ("trong phạm vi tài liệu đã khảo sát") thay vì khẳng định tuyệt đối không ai làm giống.

**C.14 — Bổ sung kết quả định tính của mô hình** *(nhiệm vụ mới, khôi phục lại tinh thần C.8 đã bỏ trước đó)*
Bổ sung minh họa định tính (ảnh dự đoán thực tế) cho các trường hợp: ca đúng, ca sai, ca FN của Gatekeeper, ca FP, ca tổn thương nhỏ, ca câu nhắc lệch, ca gãy/khối u khó, ca có nhiễu ảnh — giúp phần phân tích lỗi có sức thuyết phục trực quan hơn ngoài các bảng số liệu định lượng.
*Chuẩn bị:* không cần train gì mới, chỉ cần lục lại ảnh dự đoán đã lưu từ các notebook cũ (nhiều notebook đã có sẵn cell visualization theo đúng style 5 cột: Ảnh gốc/Ảnh+Prompt/Dự đoán/GT/TP-FP-FN) và chọn lọc, ghép hình minh họa phù hợp đưa vào Chương 4.

**C.15 — Cập nhật lại ảnh sơ đồ pipeline (`pipeline_pga_app_inference`)** ✅ **ĐÃ LÀM**
User đã tự export `diagrams/pipeline_pga_app_inference.drawio` → `Report/images/pipeline_pga_app_inference.png` (file PNG cập nhật 12/07). Đã xem trực tiếp: khớp đúng thiết kế "triage mềm" mô tả trong Chapter 3 — Gatekeeper → "Kết quả phân lớp" → nếu "Có bệnh" thì bác sĩ vẽ bounding box sau khi xác nhận; nếu "Không bệnh" có thêm nhánh hỏi "Bác sĩ vẫn nghi ngờ, muốn tự thử phân đoạn?" cho phép override (vẽ vùng nghi ngờ) hoặc kết thúc. Không còn mâu thuẫn với văn bản Chapter 3. Không cần làm gì thêm.

---

## KẾ HOẠCH LỚN D: Tái cấu trúc Chương 4 theo đúng nguồn dữ liệu thực nghiệm

Vấn đề chung: các bảng trong Chương 4 hiện chưa theo một trật tự logic rõ ràng, có phần trùng lặp ý và không phản ánh đúng cách các notebook kết quả đã được tổ chức.

**D.1 — Thiết lập lại trật tự trình bày tổng thể của Chương 4** ✅ ĐÃ LÀM
Trình bày lại theo mạch: thiết lập dữ liệu → mô hình so sánh → chỉ số đánh giá → kết quả chính → ablation → phân tích lỗi → đánh giá pipeline. Đây là khung sườn để sắp xếp lại toàn bộ các mục con bên dưới.

**D.2 — Gộp/làm rõ mục 4.2.3 và 4.2.4 (đang bị trùng ý)** ✅ ĐÃ LÀM (hoàn tất thật sự ở phiên D.3, xem ghi chú bên dưới)
4.2.3 "So sánh với SAM-Med2D" và 4.2.4 "Kiểm chứng công bằng tại cùng độ phân giải 256×256" hiện đọc như lặp lại cùng một ý (cả hai đều là so sánh PGA-UNet vs SAM-Med2D ở 256). Nguồn dữ liệu của cả hai là cùng một notebook: `Result/Result_BTXRD/test-pga-samzs-samft-r256.ipynb`. Gộp lại thành một mục duy nhất (hoặc làm rõ 4.2.4 là phần mở rộng phân tích riêng biệt, không lặp lại số liệu đã trình bày ở 4.2.3).

*Lưu ý quá trình xử lý:* lần đầu làm D.2, đã chọn hướng "làm rõ vai trò riêng biệt" mà KHÔNG gộp bảng, giữ 4.2.3 = PGA@512 vs SAM@256 (nghĩ đây là so sánh "mỗi model ở cấu hình mặc định"). Sau đó ở D.3, đối chiếu lại `pga-vs-unet2d-r512.ipynb` và `test-pga-samzs-samft-r256.ipynb`, xác nhận PGA@512 trong 4.2.3 thực ra bị lấy nhầm từ notebook U-Net (không phải từ thực nghiệm 3-model gốc của tác giả), đúng như D.2 ĐÃ GHI TỪ ĐẦU (cả hai bảng cùng nguồn `test-pga-samzs-samft-r256.ipynb`). Đã sửa lại đúng theo bản gốc: 4.2.3 giờ dùng toàn bộ số liệu 256 (PGA/SAM-FT/SAM-ZS cùng 1 thực nghiệm), xóa hẳn bảng 4.2.4 vì nay trùng hoàn toàn.

**D.3 — Chuẩn hóa lại bảng so sánh SAM-Med2D (mục 4.2.3)** ✅ ĐÃ LÀM (phạm vi rộng hơn dự kiến ban đầu)
Bảng hiện tại đang chuẩn hóa cả HD95 và chỉ có một kích thước (256) — không cần thiết phải đưa HD95 vào, và nên trình bày theo format đẹp/gọn giống bảng FracAtlas (mục 4.14/4.18) thay vì format hiện tại.

*Thực tế đã làm (vượt phạm vi ban đầu):* không chỉ là vấn đề định dạng HD95. Phát hiện bảng 4.2.3 đang trộn 2 checkpoint khác độ phân giải (PGA@512 từ notebook U-Net + SAM@256), gây hiểu lầm khi so HD95 thô. Đã sửa tận gốc: đổi toàn bộ bảng 4.2.3 về đúng 1 thực nghiệm `test-pga-samzs-samft-r256.ipynb` (PGA@256 vs SAM-FT@256 vs SAM-ZS@256), qua đó hoàn tất luôn D.2 (gộp 4.2.3/4.2.4, xóa bảng trùng). Hệ quả kèm theo:
- Sửa lại claim "PGA bền bỉ hơn SAM trước sai số câu nhắc": ở cùng 256, PGA sụt Dice Shift (−4.4%) còn nhiều hơn SAM-FT (−3.6%) — claim cũ chỉ đúng khi so PGA@512 với SAM@256, đã viết lại trung thực (lợi thế bền bỉ đến từ độ phân giải 512, không phải bản thân kiến trúc ở cùng điều kiện).
- HD95 giờ so sánh trực tiếp được (cùng 256×256): PGA thắng rõ (6.14–7.77px vs SAM-FT 9.17–9.70px), không cần footnote caveat nữa.
- Vẽ lại Hình 4.1 (`chart_baseline_sam_comparison.png`) dùng đúng PGA@256 (0.842/0.805/0.832) thay vì PGA@512 (0.858/0.845/0.855) để khớp bảng.
- Cập nhật cross-reference còn sót ở phần FracAtlas (không còn trỏ tới `subsec:fair256`/`tab:sam_comparison_256` đã xóa).

*Hệ quả CHƯA xử lý, cần cân nhắc khi làm D.9 (rà soát cuối):* `chapter5.tex` (Kết luận) và `tomtat.tex` (Tóm tắt) vẫn đang viết headline "PGA-UNet đạt Dice = 0.8584... vượt... SAM-Med2D fine-tuned (0.7432, +0.1234)" — đây lại là kiểu so sánh PGA@512 vs SAM@256 vừa bỏ khỏi 4.2.3. Đã hỏi lại, quyết định: **giữ nguyên như hiện tại**, coi đây là cách trình bày chấp nhận được cho phần tóm tắt/kết luận (nêu số tốt nhất của từng mô hình), không bắt buộc phải đổi theo số 256 kiểu apples-to-apples như trong Chương 4. Ghi lại ở đây để D.9 không hiểu nhầm là bỏ sót.

**D.4 — Đổi tên biến thể trong ablation kiến trúc (mục 4.3.1)** ✅ ĐÃ LÀM (nhưng xem thay đổi mới bên dưới — cần cập nhật lại bảng)
Thay vì gọi V1/V2/V3/V4/V5, đặt tên theo kiến trúc để người đọc hiểu ngay đây là ablation kiến trúc: U-Net, U-Net+PSG, U-Net+CAD, U-Net+PSG+CAD (PGA đầy đủ), v.v.

*Cập nhật (quyết định mới của người dùng, đã điều chỉnh 2 lần):* Lần 1 định **bỏ hẳn V4 cũ**, thay bằng "U-Net+Binary". Lần 2 (chốt lại): **giữ nguyên toàn bộ V1-V4 gốc, không xóa/thay gì** — "U-Net+Binary" là biến thể **MỚI, thêm vào**, và để tránh trùng số với V5 gốc (vốn đã là tên file `V5_Full_HeatmapPrompt.ipynb` = PGA-UNet đề xuất), đã đổi tên toàn bộ theo sơ đồ:

- V1 U-Net+Concat (Gaussian) — giữ nguyên
- V2 U-Net+PSG (Gaussian) — giữ nguyên
- V3 U-Net+CAD (Gaussian) — giữ nguyên
- V4 PGA-UNet (Binary) (PSG+CAD+Binary) — giữ nguyên, **không bỏ**
- **V5 U-Net+Binary (MỚI)** — không PSG/CAD, kênh input binary thay Gaussian (chiếm vị trí số 5)
- **V6 PGA-UNet (đề xuất)** (PSG+CAD+Gaussian) — đổi từ tên file V5 cũ sang V6 (chỉ đổi tên file nội bộ, tên gọi trong báo cáo "PGA-UNet (đề xuất)" không đổi)

Bảng ablation trong Chapter 4 giờ sẽ có **6 hàng** thay vì 5 (thêm U-Net+Binary), không phải thay thế hàng nào.

**Đã đổi tên + đồng bộ toàn bộ 4 folder liên quan** (`Source/File_Train/Ablation`, `Source/File_Test/Ablation`, `Result/Result_BTXRD/Ablation`, `Result/Result_FracAtlas/Ablation`):
- `V5_Full_HeatmapPrompt.ipynb` → `V6_Full_HeatmapPrompt.ipynb` (sửa nội dung V5→V6 bên trong)
- `V4_NoPSG_NoCAD_Binary.ipynb` (train) → `V5_NoPSG_NoCAD_Binary.ipynb` (+ bản `..._FracAtlas.ipynb`)
- `test-v4-nopsg-nocad-binary.ipynb` (test) → `test-v5-nopsg-nocad-binary.ipynb` (cả BTXRD và FracAtlas, cả `Source/File_Test/Ablation` lẫn `Result/...`)
- **Đã bổ sung export CSV per-image cho TOÀN BỘ V1-V4 gốc** (không chỉ V1-V3 như dự tính ban đầu) ở cả 3 folder test (`Source/File_Test/Ablation`, `Result/Result_BTXRD/Ablation`, `Result/Result_FracAtlas/Ablation`), phòng khi cần kiểm định thêm cặp khác sau này.

**Cập nhật tiếp theo: thêm V7, V8** để khép kín câu hỏi "attention cần điều kiện hóa hay tự nó đã đủ" (xem trao đổi chi tiết trong lịch sử phiên làm việc):
- **V7 U-Net+PSG+Attention gốc** (PSG bật, decoder dùng `GridAttentionBlock2D` gốc — y hệt CAD nhưng bỏ 2 điểm tiêm câu nhắc `g_fused`/`p_refine`)
- **V8 U-Net+Attention gốc + concat** (giống hệt V1 nhưng decoder dùng Cổng chú ý gốc thay vì nối kênh đơn thuần, không PSG)

Cùng với V1/V2/V3/V6 có sẵn, giờ đủ lưới 2×3 hoàn chỉnh: {không PSG, có PSG} × {không attention, attention chưa điều kiện hóa, CAD đã điều kiện hóa}. **Bảng ablation Chương 4 giờ sẽ có 8 hàng** (V1-V8), không phải 6.

File: `Source/File_Train/Ablation/V7_PSG_Attention.ipynb`, `V8_NoPSG_Attention_Concat.ipynb` (train) + `test-v7-psg-attention.ipynb`, `test-v8-nopsg-attention-concat.ipynb` (test, cả 3 folder).

**Trạng thái: ✅ ĐÃ CHẠY XONG TẤT CẢ (V1-V8, cả BTXRD và FracAtlas)** — người dùng đã tự train+test toàn bộ, kết quả nằm ở `Result/Result_BTXRD/Ablation/V{1-8}/` và `Result/Result_FracAtlas/Ablation/V{1-8}/` (mỗi thư mục có `*_results.csv` + `*_per_image.csv`). **Việc còn lại là cập nhật report**: mở rộng Bảng~`tab:ablation_arch` từ 6 lên 8 hàng, cập nhật Hình~`fig:chart_ablation`, viết thêm phần "Ablation trên FracAtlas" (Chapter 4 phần FracAtlas hiện chưa có mục này), và bổ sung phân tích cho V7/V8 (đúng câu chuyện attention vs điều kiện hóa). Đưa CSV cho tôi là cập nhật ngay — xem thêm C.1/C.10.

**D.5 — Sửa caption bảng 4.8 và 4.9 để mạch lạc theo tầng bậc** ✅ ĐÃ LÀM
Bảng 4.8 nên có caption: "Dice Score từng fold trong đánh giá chéo 4-fold PGA-UNet (kịch bản Zoom-out/Shift/Mixed)"; Bảng 4.9 nên có caption: "Kết quả đánh giá chéo 4-fold PGA-UNet trên 3 kịch bản prompt (trung bình 4 fold)". Cách đặt tên này giúp người đọc thấy ngay bảng sau là tổng hợp/trung bình của bảng trước.

**D.6 — Ánh xạ rõ vai trò từng notebook kết quả vào đúng mục của Chương 4** ✅ ĐÃ LÀM
Làm rõ trong văn bản (ví dụ ở đầu mỗi mục, hoặc trong phụ lục mô tả nguồn số liệu) vai trò của từng notebook, tránh người đọc nhầm lẫn các bảng có vẻ trùng nhau:
- `pga-vs-unet2d-r512.ipynb` → so sánh PGA-UNet vs U-Net **cùng kích thước 512**.
- `test-pga-samzs-samft-r256.ipynb` → so sánh PGA-UNet vs SAM-Med2D **chưa fine-tune (zero-shot)** và **đã fine-tune**, cùng kích thước 256.
- `test-subcat-pga-vs-baseline.ipynb` → so sánh PGA-UNet vs U-Net theo **subcategory** (ảnh U-Net tin cậy nhất/kém nhất), ở 512.
- `test-subcat-pga-vs-sam-r256-r512.ipynb` → so sánh PGA-UNet vs SAM-Med2D fine-tuned theo 3 loại tổn thương (nhỏ/mờ/rõ): SAM-Med2D chỉ ở 256 (để so cùng cấp), PGA-UNet có cả 256 và 512 (để chứng minh lợi thế train tùy ý kích thước không bị resize quá mức, khác với SAM-Med2D vốn cố định 256 và rất khó mở lên 512).

*Đã xác nhận lại (phiên D.3):* đối chiếu trực tiếp output của `pga-vs-unet2d-r512.ipynb` (in rõ `IMG_SIZE=512`) và `test-pga-samzs-samft-r256.ipynb` (in rõ `IMG_SIZE=256`, chứa cả PGA/SAM-FT/SAM-ZS cùng 1 lần chạy) — mapping D.6 mô tả ở trên là chính xác 100%, không cần chỉnh sửa.

**D.7 — Bổ sung so sánh PGA-256 vs PGA-512** ✅ ĐÃ LÀM
Hiện không có notebook riêng cho so sánh này, nhưng dữ liệu đã có sẵn trong `pga-vs-unet2d-r512.ipynb` (PGA-512) và `test-pga-samzs-samft-r256.ipynb` (PGA-256) — có thể cắt/khớp số liệu từ hai file này để dựng một bảng so sánh PGA-256 vs PGA-512, làm rõ luận điểm: PGA-UNet có thể train lại tùy ý ở độ phân giải cao hơn (512) mà không bị giới hạn kiến trúc như SAM-Med2D (vốn cố định 256, khó mở rộng).

*Cập nhật sau D.3:* việc này giờ càng cần thiết hơn, vì sau khi sửa 4.2.3 về thuần 256 (D.2/D.3), câu chuyện "PGA-512 vs SAM-256" không còn xuất hiện trực tiếp trong Chương 4 nữa — bảng D.7 sẽ là nơi phục hồi lại luận điểm đó một cách gián tiếp/bắc cầu (PGA-512 > PGA-256 ở Bảng~này, PGA-256 > SAM-256 ở Bảng~4.2.3 → suy ra PGA-512 còn cách biệt SAM lớn hơn nữa), thay vì nhét vào 1 bảng trộn độ phân giải như cách làm cũ. Số liệu PGA-256 đã có sẵn nguyên trong `tab:sam_comparison` (0.8420/0.8048/0.8317); PGA-512 lấy từ `tab:baseline_comparison`/`tab:robustness_comparison` (0.8584/0.8454/0.8554).

**D.8 — Áp dụng cùng cấu trúc mapping notebook cho phần FracAtlas (mục 4.4.2–4.4.5)** ✅ ĐÃ LÀM
Thư mục `Result/Result_FracAtlas/` chứa đúng 4 notebook cùng tên với BTXRD: `pga-vs-unet2d-r512.ipynb`, `test-pga-samzs-samft-r256.ipynb`, `test-subcat-pga-vs-baseline.ipynb`, `test-subcat-pga-vs-sam-r256-r512.ipynb`. Vì vậy phần FracAtlas (mục 4.4) nên chia thành 4 mục con 4.4.2–4.4.5, mirror đúng logic đã áp dụng cho BTXRD ở D.6:
- 4.4.2 PGA-UNet vs U-Net cùng kích thước 512 (từ `pga-vs-unet2d-r512.ipynb`).
- 4.4.3 PGA-UNet vs SAM-Med2D (zero-shot & fine-tuned) cùng kích thước 256 (từ `test-pga-samzs-samft-r256.ipynb`) — áp dụng luôn D.3 (bỏ HD95, format gọn) cho bảng này.
- 4.4.4 PGA-UNet vs U-Net theo subcategory (ảnh tin cậy nhất/kém nhất), ở 512 (từ `test-subcat-pga-vs-baseline.ipynb`).
- 4.4.5 PGA-UNet vs SAM-Med2D fine-tuned theo 3 loại tổn thương (nhỏ/mờ/rõ): SAM-Med2D chỉ ở 256, PGA-UNet có cả 256 và 512 (từ `test-subcat-pga-vs-sam-r256-r512.ipynb`) — cùng luận điểm về lợi thế train tùy ý kích thước như D.6.

Lưu ý khác biệt: FracAtlas **không có** notebook tương đương cho đánh giá chéo 4-fold (`test-pga-dataset-1234.ipynb`), Gatekeeper (`efficientnet-b3.ipynb`), hay pipeline end-to-end (`test-pipeline-evaluation.ipynb`) — thư mục `Result_FracAtlas/Ablation/` hiện cũng đang trống. Ba phần này (4-fold CV, Gatekeeper, pipeline) chỉ tồn tại ở BTXRD và không cần ép vào phần trình bày FracAtlas; nếu muốn có ablation trên FracAtlas thì đây là hạng mục thực nghiệm còn thiếu (bổ sung vào Kế hoạch lớn C nếu còn thời gian).

**D.9 — Rà soát toàn bộ Chương 4 sau khi tái cấu trúc** ✅ ĐÃ LÀM
Sau khi áp dụng D.1–D.8, đọc lại toàn chương để đảm bảo không còn mục nào lặp ý (như tình trạng 4.2.3/4.2.4 ban đầu), cấu trúc 4.4.x (FracAtlas) phản ánh đúng song song với 4.2.x (BTXRD), và mỗi bảng/mục đều có thể truy ngược về đúng notebook nguồn.

---

## KẾ HOẠCH LỚN E: Sửa lỗi trình bày hình thức toàn khóa luận

**E.1 — Chuyển đề cương khóa luận vào phụ lục** 🔁 THAY THẾ (theo yêu cầu riêng của trường)
Phần "ĐỀ CƯƠNG KHOÁ LUẬN TỐT NGHIỆP" hiện nằm ngay sau lời cảm ơn, trước mục lục — không nên xuất hiện như một chương/phần chính. Chuyển toàn bộ vào phụ lục.
Bỏ qua theo yêu cầu trường (giữ nguyên vị trí đề cương). Thay bằng nhiệm vụ mới: dịch toàn bộ thuật ngữ chuyên ngành tiếng Anh trong thân bài sang tiếng Việt + bảng đối chiếu thuật ngữ ở phụ lục — **✅ ĐÃ LÀM** (Appendix/doichieuthuatngu.tex mới, ~35 thuật ngữ, áp dụng xuyên suốt Chapter1–5 + Appendix; hoàn thiện thêm ở E.9).

**E.2 — Sửa ngôi xưng trong lời cam đoan** ✅ ĐÃ LÀM
Hiện ghi "Tôi xin cam đoan..." dù khóa luận do hai sinh viên thực hiện. Sửa thành "Chúng tôi xin cam đoan đây là công trình nghiên cứu của nhóm...".

**E.3 — Thống nhất thuật ngữ "khóa luận" (bỏ "luận văn")** ✅ ĐÃ LÀM
Lời cam đoan hiện dùng "luận văn" — dễ gây nhầm với luận văn thạc sĩ. Rà soát toàn văn bản, thống nhất dùng "khóa luận".

**E.4 — Chuẩn hóa đánh số trang phần đầu** ✅ ĐÃ LÀM
Trang bìa thứ hai hiện hiển thị số trang "2" (trang bìa thường không đánh số hiển thị), sau đó chuyển sang số La Mã cho lời cam đoan/cảm ơn/đề cương/mục lục. Chuẩn hóa lại theo quy ước: trang bìa không số, phần mở đầu số La Mã, nội dung chính số Ả Rập.

**E.5 — Gộp hệ thống tài liệu tham khảo thành một danh mục duy nhất** ❌ BỎ (theo quy định của trường)
Phần đề cương hiện có danh mục tài liệu tham khảo riêng (chỉ vài mục, đánh số lại từ [1]) tách biệt với danh mục đầy đủ ở cuối khóa luận — gây rối trích dẫn (đề cương trích [7][8][9] nhưng danh mục ngay sau chỉ có [1]-[4]). Bỏ danh mục riêng trong đề cương (đã chuyển vào phụ lục theo E.1), chỉ giữ một danh mục thống nhất ở cuối.
Bỏ hẳn, không làm cả bản gốc lẫn phần thay thế (danh mục tham khảo hợp nhất thứ 3): đây là quy định của trường, giữ nguyên đề cương với danh mục tham khảo riêng như hiện tại.

**E.6 — Sửa lỗi encoding/ký tự lạ toàn văn bản** ✅ ĐÃ KIỂM TRA (không phát hiện lỗi còn tồn tại)
Nhiều chỗ lỗi font: "X￾quang", "PGA￾UNet", "end-to￾end", "256Ö256", "512Ö512", "PGAö512". Kiểm tra lại font, LaTeX encoding, gói tiếng Việt, ký hiệu nhân "×", và cách ngắt dòng/gạch nối.

**E.7 — Sửa tên đề tài khóa luận** ⏸️ TẠM HOÃN (không tự sửa)
Tên hiện tại "Phát triển hệ thống phân đoạn ảnh X-quang về xương dựa vào câu nhắc trực quan" — cụm "ảnh X-quang về xương" không tự nhiên. Đề xuất: "Phát triển hệ thống phân đoạn tổn thương xương trên ảnh X-quang dựa trên câu nhắc trực quan" (hoặc ngắn hơn: "Phân đoạn tổn thương xương trên ảnh X-quang dựa trên câu nhắc trực quan").
Lý do hoãn: đổi tên đề tài khóa luận cần báo/xin phép trường trước (thủ tục hành chính, không thể tự ý sửa trong báo cáo). Giữ nguyên tên hiện tại ở `\tenKL` (main.tex) cho đến khi có xác nhận từ trường.

**E.8 — Rút gọn caption hình/bảng** ✅ ĐÃ LÀM
Nhiều caption dài như một đoạn văn và lồng cả kết luận nhân quả (ví dụ Hình 4.7: "Đường biên bám sát GT nhờ cơ chế Prompt Spatial Gate và Conditioned Attention"). Viết lại caption ngắn gọn, chỉ mô tả nội dung hình/bảng; phần diễn giải nhân quả để trong văn bản phân tích.

**E.9 — Chuẩn hóa thuật ngữ Anh–Việt** ✅ ĐÃ LÀM
Các cụm Gatekeeper, pipeline end-to-end, image-level, baseline comparison, robustness, sub-category, cross-dataset, prompt-guided, zero-shot, fine-tuned xuất hiện dày đặc và lẫn lộn. Quy tắc: lần đầu xuất hiện ghi tiếng Việt kèm tiếng Anh trong ngoặc, sau đó dùng nhất quán một cách gọi. Ví dụ: "đánh giá liên bộ dữ liệu" thay cho "cross-dataset", "đánh giá theo ảnh" thay cho "image-level", "đường ống xử lý đầu cuối" (hoặc thống nhất "pipeline đầu cuối").
Ghi chú: hầu hết các cụm (Gatekeeper, robustness, cross-dataset, prompt-guided, zero-shot, fine-tuned, baseline comparison) đã được dịch/chuẩn hóa nhất quán từ phiên dịch thuật ngữ trước (E.1-thay thế) và phiên E.10. Kiểm tra lại lần này phát hiện 2 khoảng trống: "image-level" và "sub-category" bị bỏ sót (dùng lẫn lộn bare tiếng Anh và các biến thể tiếng Việt rời rạc như "cấp độ ảnh"/"đánh giá theo ảnh" trong ~30 chỗ ở Chapter4, rải rác Chapter1/5). Đã chuẩn hóa: "image-level" → gloss đầy đủ một lần tại tiêu đề Mục 4.2.2 + định nghĩa ("cấp độ ảnh (image-level)"), sau đó dùng nhất quán "cấp độ ảnh" trong toàn bộ phần còn lại (Chapter1/4/5). "sub-category" → gloss một lần tại Mục 4.3 ("nhóm nhỏ (sub-category)"), sau đó dùng nhất quán "nhóm nhỏ". Cũng dịch nốt 3 chỗ "pipeline"/"pipeline end-to-end" còn sót trong Appendix/decuong.tex → "luồng xử lý"/"luồng xử lý đầu cuối". Bổ sung 2 dòng "Cấp độ ảnh/Image-level" và "Nhóm nhỏ/Sub-category" vào bảng đối chiếu thuật ngữ (Appendix/doichieuthuatngu.tex). Build lại sạch, 123 trang, không lỗi/undefined reference.

**E.10 — Viết lại tiêu đề mục Chương 4 theo văn phong khóa luận** ✅ ĐÃ LÀM
Nhiều tiêu đề hiện mang dáng dấp bài báo (Baseline Comparison, Robustness, SOTA Prompt-based, Cross-dataset, Sub-Category). Viết lại theo mạch logic khóa luận (liên kết D.1): thiết lập dữ liệu → mô hình so sánh → chỉ số → kết quả chính → ablation → phân tích lỗi → đánh giá pipeline.
Đã sửa 14 tiêu đề mục/tiểu mục ở Chương 4 (loại bỏ gloss tiếng Anh kiểu bài báo). Tái kiểm tra lần này (cùng phiên E.9) xác nhận không còn tiêu đề nào sót kiểu bài báo, không có chương khác tham chiếu tiêu đề cũ bằng văn bản thuần.

**E.11 — Chuẩn hóa định dạng danh mục tài liệu tham khảo** ✅ ĐÃ LÀM
Hiện có URL tách kiểu "https : / / …", một số mục ghi "Truy cập năm 2025", một số ghi phiên bản, arXiv, DOI không đồng nhất. Chọn một chuẩn trích dẫn cụ thể (IEEE/ACM/APA) và áp dụng thống nhất cho toàn bộ danh mục.
Đã chọn chuẩn IEEE: `\usepackage[style=ieee, sorting=none, backend=bibtex]{biblatex}` (bỏ `sorting=nty`/`defernumbers=true` cũ và bỏ `\DeclareNameAlias{...}{family-given}` thủ công vì style=ieee tự định dạng tên tác giả dạng viết tắt + đánh số theo đúng thứ tự trích dẫn lần đầu trong bài, đúng quy ước IEEE). Cài thêm gói `biblatex-ieee` (`tlmgr install biblatex-ieee`, không cần biber, chạy tốt với `backend=bibtex` hiện có). Chuẩn hóa 3 mục `@misc` (cuh2024xray, yolov11, roboflow2023): đổi `howpublished = {\url{...}}` → field `url` chuẩn để được style tự thêm "[Online]. Available: ..." nhất quán với các mục khác; đổi note thủ công "Truy cập năm 2025" → field `urldate` chuẩn (biblatex tự render "(visited on 01/01/2025)"). Sửa lỗi giãn cách chữ kiểu "https : / / …" trong URL dài khi canh đều hai lề: thêm `\usepackage{xurl}` (ngắt URL sạch hơn) và bọc `\printbibliography` trong `\begingroup\raggedright...\endgroup` (loại bỏ hoàn toàn hiện tượng giãn dòng vì không còn canh đều). Build sạch, 123 trang, không lỗi/undefined reference, đã kiểm tra trực quan cả 2 trang danh mục tham khảo (ảnh render PDF).

**E.12 — Sửa văn phong một số cụm từ chưa chuẩn học thuật** ✅ ĐÃ LÀM
"module gác cổng" → "module sàng lọc"; "đánh giá toàn diện" → "đánh giá trên nhiều khía cạnh"; "mô phỏng điều kiện lâm sàng thực tế" → "mô phỏng một phần luồng xử lý lâm sàng"; "hệ thống đủ thông minh" → "hệ thống có khả năng hỗ trợ tương tác".
Đã sửa cả 4 cụm tại đúng các vị trí xuất hiện (Chapter1 mục tiêu khóa luận + tóm tắt Chương 4; Appendix/tomtat.tex; Chapter3 tổng kết chương; Appendix/decuong.tex). Riêng "module gác cổng sàng lọc" (Chapter3.tex:299, cụm lặp) rút gọn còn "module sàng lọc". Chủ động sửa thêm 1 chỗ tương tự không khớp y hệt nhưng cùng lỗi phóng đại "mô phỏng điều kiện thực tế" trong Appendix/tomtat.tex → "mô phỏng một phần điều kiện thực tế" cho nhất quán tinh thần A.6 (không nhận là mô phỏng đầy đủ điều kiện lâm sàng thật). Không đụng đến "Gatekeeper"/"gác cổng"/"mô hình gác cổng" ở các chỗ khác (tên module, tiêu đề mục, các câu dùng như động từ) vì đó là thuật ngữ định danh đã chốt từ B.3/A.4, ngoài phạm vi hẹp của quy tắc E.12. Build sạch, 123 trang, không lỗi.

---

## THỨ TỰ ƯU TIÊN ĐỀ XUẤT (gốc, tham khảo lịch sử)

1. **Kế hoạch lớn B** (lỗi phương pháp đánh giá) — vì đây là lỗi học thuật nghiêm trọng nhất, ảnh hưởng trực tiếp đến tính đúng đắn của số liệu đã công bố.
2. **Kế hoạch lớn A** (hạ mức claim) — sửa nhanh, rủi ro phản biện cao nếu bỏ qua, không cần thêm thực nghiệm.
3. **Kế hoạch lớn D** (tái cấu trúc Chương 4) — cải thiện rõ rệt tính mạch lạc, mức độ ưu tiên cao vì đây là chương trọng tâm.
4. **Kế hoạch lớn E** (lỗi trình bày hình thức) — dễ sửa, nên làm song song, ảnh hưởng điểm hình thức.
5. **Kế hoạch lớn C** (bổ sung thực nghiệm) — tốn thời gian nhất; ưu tiên theo khả năng còn lại: C.1 (kiểm định thống kê) và C.3/C.4 (ablation bổ sung) khả thi nhất trong thời gian ngắn; C.6/C.9 (cross-dataset thật sự, đánh giá liên chuyên gia) có thể ghi vào phần hạn chế nếu không kịp thực hiện.

---

## TÌNH TRẠNG TỔNG QUÁT (cập nhật mới nhất)

- **Kế hoạch lớn A** (A.1–A.6): ✅ **Hoàn tất toàn bộ.**
- **Kế hoạch lớn B** (B.1–B.4): ✅ **Hoàn tất toàn bộ.**
- **Kế hoạch lớn C**: đã rút gọn phạm vi (bỏ C.3/C.5/C.6/C.7/C.9, C.4 đổi hướng, C.8→C.14). **Ablation V1-V8 đã chạy xong thật (cả BTXRD, FracAtlas), đã đưa vào report + Wilcoxon (C.1, C.10, C.16 ✅ HOÀN TẤT).** **C.4 ✅ HOÀN TẤT** (xóa mô tả tiền xử lý YOLOv11/Roboflow + đồng bộ toàn bộ số liệu BTXRD Chapter 4 theo dataset gốc không tiền xử lý; 3 bảng FN chi tiết + lesion-level còn dùng số cũ, đã flag rõ trong report). **C.15 ✅ HOÀN TẤT** (đã export PNG mới, khớp thiết kế triage mềm). Còn cần: C.11/C.12 (còn chờ GPU), C.14 (chưa làm).
- **Kế hoạch lớn D** (D.1–D.9): 🟡 **Gần hoàn tất, còn phần cập nhật số liệu** — D.1/D.2/D.3/D.5/D.6/D.7/D.8/D.9 xong; **D.4 giờ có đủ dữ liệu thật (V1-V8, cả 2 dataset) nhưng chưa đưa vào Chapter 4** — bảng ablation cần mở rộng từ 6 lên 8 hàng, thêm mục ablation cho FracAtlas.
- **Kế hoạch lớn E** (E.1–E.12): Gần như hoàn tất —
  - ✅ Đã làm: E.2, E.3, E.4, E.6, E.8, E.9, E.10, E.11, E.12.
  - 🔁 Đã thay thế theo yêu cầu riêng của trường: E.1 (✅ đã làm phần thay thế — dịch thuật ngữ + phụ lục đối chiếu).
  - ❌ Bỏ hẳn theo quy định trường: E.5 (không gộp danh mục tham khảo, không làm cả phần thay thế).
  - ⏸️ Tạm hoãn: E.7 (đổi tên đề tài) — cần báo/xin phép trường trước, không tự sửa.

## KẾ HOẠCH TRIỂN KHAI TỪNG BƯỚC (chốt sau khi có đủ CSV V1-V8 cả 2 dataset)

Tất cả các bước dưới đây làm được ngay, không cần GPU/thực nghiệm mới — chỉ cần triển khai lần lượt, không bỏ bước nào vì lý do "ưu tiên thấp" (đã thống nhất: bảng + biểu đồ đều làm đủ, không rút gọn):

**Nhóm 1 — Nền dữ liệu (làm trước tiên, độc lập với nhau, có thể song song):**
1. **Chốt lại bộ số liệu chính thức duy nhất** cho V1-V8 (cả 2 dataset, cả 3 kịch bản) — đối chiếu số liệu mới trong CSV với số đang có trong báo cáo hiện tại (lưu ý: **không chỉ V5/V7/V8 mới có số mới** — V1-V4/V6 cũ cũng đã đổi nhẹ so với báo cáo vì được chạy lại toàn bộ cùng một đợt). *Là nền cho bước 3, 4, 5.*
2. **Chạy kiểm định Wilcoxon** cho 6 cặp × 2 dataset × 3 kịch bản (script đã viết sẵn, xem C.1) → bảng 36 kết quả (Δ trung bình + p-value + mức ý nghĩa). *Độc lập với bước 1 (dùng CSV per-image riêng), cần cho bước 7.*

**Nhóm 2 — Cập nhật bảng/biểu đồ (cần bước 1, có thể làm theo bất kỳ thứ tự nào trong nhóm này):**
3. **Cập nhật Bảng ablation Chương 4 (BTXRD, mục 4.3.1)** — mở rộng từ 6 lên 8 hàng (V1-V8), số liệu chốt ở bước 1.
4. **Vẽ lại biểu đồ cột `chart_ablation.png`** — 8 biến thể, số liệu mới (theo `dataviz` skill: 1 hue cố định theo nhóm PSG/không-PSG hoặc theo thứ tự V1-V8, không cycle màu tùy tiện).
5. **Viết mới mục "Ablation trên FracAtlas"** trong Chương 4 (phần FracAtlas hiện chưa có mục ablation) — bảng 8 hàng + biểu đồ cột riêng, cùng cấu trúc như BTXRD (D.8 style).
6. **Thêm so sánh Attention U-Net thuần vs U-Net thuần** (C.16, không câu nhắc, cả 2 dataset) — quyết định vị trí đặt cụ thể khi triển khai (đề xuất mặc định: đặt ngay trước bảng ablation chính như một dòng/bảng phụ "mức 0 câu nhắc", để làm điểm neo mở đầu mạch 3 bậc).

**Nhóm 3 — Viết phân tích + chốt sổ (làm SAU CÙNG, cần toàn bộ nhóm 1+2):**
7. **Viết lại phần phân tích ablation** (văn bản Chương 4) — gộp thành một mạch xuyên suốt 3 bậc dẫn dắt: không câu nhắc (C.16) → concat (V1/V8) → PSG (V2/V7), cộng thêm điều kiện hóa CAD (V8/V3, V7/V6) và loại câu nhắc Gaussian/Binary (V1/V5, V4/V6) — dẫn chứng bằng p-value ở bước 2, đối chiếu với khung giả thuyết đã nêu ở C.1 (viết đúng theo số liệu thật, không ép theo giả thuyết nếu kết quả lệch hướng).
8. **Cập nhật `Xư_ly.md`** — đánh dấu C.1/C.10/C.16/D.4 hoàn tất sau khi xong hết các bước trên.

*Các mục còn lại (đã cập nhật, xem thêm mục "TRẠNG THÁI THẬT SỰ MỚI NHẤT" cuối file):*
- **C.11/C.12** — Gatekeeper/pipeline/4-fold trên FracAtlas, còn chờ GPU/thực nghiệm mới.
- **C.14** — bổ sung ảnh minh họa định tính (chưa bắt đầu).
- **E.7** — chờ xác nhận đổi tên đề tài từ trường.

(E.5 đã bỏ hẳn. C.4 và C.15 đã hoàn tất — xem cập nhật phía trên.)

---

## Cập nhật (phiên "8 pipeline + FracAtlas GPU mới"): C.11/C.12 ĐÃ XONG + fix BTXRD FN tables

User đã tự chạy thêm loạt notebook mới, cung cấp `results/pipeline_detail.csv` (BTXRD + FracAtlas) và các notebook Gatekeeper/pipeline/4-fold CHO CẢ FRACATLAS (trước đây D.8 ghi nhận FracAtlas không có 3 thứ này). Đã xử lý:

1. **BTXRD — dùng `Result/Result_BTXRD/pipeline/pipeline_detail.csv`** (per-image cls_prob/gt_label, xác nhận đúng confusion matrix 167/26/20/162) để tính lại CHÍNH XÁC 2 bảng từng bị flag stale: `tab:fn_prob_dist` (phân bố xác suất 20 ca FN, KHÔNG còn ca "near-miss" nào — khác cấu hình cũ có 2 ca) và `tab:threshold_sweep` (đánh đổi Sensitivity/Specificity theo ngưỡng — phát hiện mới: hạ ngưỡng 0.5→0.3 không cứu được ca FN nào cả vì không còn FN nào trong khoảng [0.3,0.5)). Bảng so sánh diện tích FN/TP (`tab:fn_area_compare`) và bảng lesion-level (Mục 4.7.5) VẪN dùng số liệu cũ (166/24/21/164) vì cần dữ liệu diện tích polygon GT không có trong CSV này — đã ghi chú rõ ràng ngay đầu mục.

2. **FracAtlas — HOÀN TOÀN MỚI (C.11 xong, C.12 xong):** Thêm 3 mục mới vào Chương 4 (mục 4.4.7–4.4.9, trước "Thảo luận"):
   - **Đánh giá chéo 4-fold trên FracAtlas** (`subsec:cross_validation_fa`): Fold1-4 N=89/93/95/90, mean Zoom=0.8144±0.0077, Shift=0.7904±0.0084, Mixed=0.8071±0.0064 — rất gần tập test chính (0.8169/0.7850/0.8129), xác nhận ổn định.
   - **Đánh giá Gatekeeper trên FracAtlas** (`subsec:gatekeeper_fa`): N=409 (72 bệnh+337 lành), TP=51/FP=27/FN=21/TN=310, Sensitivity=70.83% (THẤP hơn nhiều BTXRD 89.30%), Specificity=91.99%, AUC=0.9132. Phát hiện quan trọng: đường gãy xương khó nhận diện ở cấp độ phân loại toàn ảnh hơn khối u BTXRD.
   - **Đánh giá luồng xử lý đầu cuối trên FracAtlas** (`subsec:pipeline_eval_fa`): Pipeline Dice=0.4230 (so với PGA-UNet độc lập 0.8169) — khoảng cách LỚN HƠN NHIỀU so với BTXRD (0.6763), do Sensitivity Gatekeeper thấp kéo theo nhiều ảnh FN bị gán Dice=0.
   - Cập nhật mục "Thảo luận" FracAtlas + chapter5.tex "Hạn chế": thêm phát hiện quan trọng "tổng quát hóa không đồng đều giữa các module — PGA-UNet tổng quát tốt, Gatekeeper thì không", tránh suy rộng tổng quát hóa module phân đoạn ra toàn hệ thống.
   - Sửa câu giới thiệu FracAtlas (đầu Mục 4.4) không còn nói "3 nội dung chưa có tương đương" (đã bổ sung đủ).

3. **Bug tự phát hiện + tự sửa:** Bảng 4.21 (per-fold FracAtlas CV, 5 cột) lúc đầu tràn lề phải do thiếu `\resizebox` — đã phát hiện qua render ảnh trực quan và sửa ngay.

4. **Build:** sạch, 134 trang (từ 130), không lỗi/undefined reference. Đã xem trực quan toàn bộ trang mới (79-82, 90-92).

**Trạng thái C.11/C.12: ✅ HOÀN TẤT.** Việc phụ còn sót của C.4 (bảng diện tích FN/TP + lesion-level) vẫn treo, cần dữ liệu polygon GT area (chưa có).

---

## Cập nhật: C.14 — Bổ sung ảnh minh họa định tính ✅ ĐÃ LÀM (không train gì mới, lục ảnh từ notebook có sẵn)

Trích xuất ảnh PNG nhúng sẵn (base64) trong các notebook đã chạy (không cần GPU/chạy lại): `pipeline/test-pipeline-evaluation.ipynb` (10 ca TP), `pga-vs-unet2d-r512.ipynb` (visualization Shift), `test-subcat-pga-vs-baseline.ipynb` (TOP/BOTTOM-DICE). Đã crop/ghép và thêm 4 hình mới vào Chương 4:

1. **Hình 4.9** (Mục 4.5.2, mới): 6 ca TP tiêu biểu qua toàn bộ pipeline, đa dạng vị trí giải phẫu (đầu gối/cổ tay/lồng ngực/xương chậu/vai). Ban đầu dùng cả 10 ca nhưng ảnh quá cao tràn trang — đã cắt còn 6 ca + validate lại bằng render ảnh.
2. **Hình 4.10** (Mục 4.5.3, mới): 2 ca kịch bản Shift (đầu gối 4 tổn thương Dice=0.851, vai/xương đòn Dice=0.894) — minh chứng trực quan tính bền bỉ trước câu nhắc lệch tâm.
3. **Hình 4.11** (Mục 4.5.3, mới): ca tổn thương kích thước nhỏ ở cẳng chân (Dice=0.769) — minh chứng PGA-UNet định vị được tổn thương rất nhỏ.
4. **Hình 4.12** (Mục 4.6.1, mới): ca chồng lấp giải phẫu phức tạp (vai/xương đòn/lồng ngực, Dice=0.762) — minh họa trực quan cho bullet "vùng chồng lấp đa lớp xương dày đặc" đã có sẵn trong text.

**Đã quyết định KHÔNG cần làm (theo yêu cầu người dùng):** ảnh minh họa "ca sai/ca FN của Gatekeeper/ca FP" — user xác nhận phần liên quan đến pipeline/Gatekeeper chỉ cần số liệu (đã có đầy đủ: confusion matrix, threshold sweep, Sensitivity/Specificity...), không cần ảnh trực quan. Không còn là việc tồn đọng.

**Build:** sạch, 139 trang (từ 134). Tự phát hiện + tự sửa 1 lỗi tràn trang (hình 10-ca gốc quá cao so với khổ giấy) qua render thử trước khi báo hoàn tất.

**Trạng thái C.14: ✅ HOÀN TẤT** (trong phạm vi ảnh có sẵn).

---

## TRẠNG THÁI THẬT SỰ MỚI NHẤT (chốt cuối phiên "8 pipeline + FracAtlas GPU mới")

**Kế hoạch lớn A, B, D:** ✅ Hoàn tất toàn bộ, không còn việc tồn đọng.

## Cập nhật: bổ sung phân tích FN chi tiết cho FracAtlas (dùng lại đúng 2 file pipeline_detail.csv đã có, khai thác thêm phần chưa dùng)

User hỏi lại "2 file csv pipeline cho cả 2 dataset xem giúp được gì không" — rà lại phát hiện: file `Result/Result_FracAtlas/pipeline/pipeline_detail.csv` (đã có sẵn từ trước) chưa được khai thác chi tiết per-image như đã làm cho BTXRD. Đã bổ sung 2 mục mới **hoàn toàn mới** vào Chương 4 (Mục 4.4.10 "Phân tích các ca bỏ sót trên FracAtlas"), dùng đúng file này:
- Bảng phân bố xác suất 21 ca FN trên FracAtlas: khác hẳn BTXRD — **5/21 ca (23,8%) là "near-miss"** thực sự (BTXRD sau khi train lại: 0 ca near-miss).
- Bảng threshold sweep trên FracAtlas: đường cong đánh đổi thuận lợi hơn BTXRD ở đoạn đầu (hạ 0.5→0.3: Sensitivity +13,89 điểm, Specificity chỉ -7,12 điểm), nhưng sụp đổ nhanh hơn ở ngưỡng cực thấp do mất cân bằng lớp nghiêm trọng hơn (72 bệnh/337 lành) — tại ngưỡng 0.01, Specificity chỉ còn 19,58% (so với 60,11% của BTXRD).

**Xác nhận lại phần vẫn CHƯA làm được của C.4:** bảng so sánh diện tích tổn thương FN/TP (`tab:fn_area_compare`) + bảng lesion-level (Mục 4.7.5, BTXRD) vẫn dùng confusion matrix CŨ (166/24/21/164) — đã kiểm tra kỹ lại 2 file `pipeline_detail.csv` (cả 2 dataset) và `seg_samples.csv`, xác nhận KHÔNG có cột diện tích polygon GT nào, chỉ có `n_polygons` (số lượng, không phải diện tích) và chỉ điền cho ảnh TP. Việc này thực sự cần dữ liệu khác (JSON annotation gốc) mà 2 file hiện có không đáp ứng được, dù đã rà soát kỹ theo yêu cầu user.

**Build:** sạch, 141 trang (từ 139).

**Trạng thái C.4:** ✅ Đã khai thác hết mọi thứ có thể từ dữ liệu hiện có. Chỉ còn đúng 1 việc treo (xem bên dưới), cần dữ liệu khác hẳn (JSON annotation), không phải do bỏ sót cách khai thác 2 file csv đã có.

---

## Cập nhật CUỐI: C.4 gần như hoàn tất 100% nhờ user cung cấp JSON annotation gốc

User cung cấp `/home/thongluc/Khóa Luận Tốt Nghiệp/PGA_Unet2D/dataset_json/{BTXRD,FracAtlas}` (JSON labelme gốc, có `imageWidth`/`imageHeight`/`shapes` với `shape_type` polygon/rectangle). Đã xử lý:
1. Thêm `/dataset_json/` vào `.gitignore` (xác nhận không còn xuất hiện trong `git status`).
2. Dọn `dataset_json/BTXRD`: từ 1867 file → còn đúng 187 file khớp với 187 ảnh bệnh lý trong `pipeline_detail.csv` (xóa 1680 file dư thừa không thuộc tập test). `dataset_json/FracAtlas` giữ nguyên (đã đúng 72 file từ đầu, không cần xử lý).
3. Tính diện tích từng polygon bằng công thức shoelace trên tọa độ GT (232 polygon tổng, khớp chính xác N_samples=232 đã dùng xuyên suốt báo cáo) → **cập nhật lại hoàn toàn `tab:fn_area_compare`** trên đúng cấu hình mới (FN n=22 trong 20 ảnh, TP n=210 trong 167 ảnh): trung vị FN=0.186% vs TP=1.005% (tỉ lệ ~18,5%, trước là ~22%), Mann-Whitney p=2,4×10⁻⁵ (mạnh hơn p=0.0001 cũ).
4. **Cập nhật lại phần lớn `tab:lesion_level_metrics`** (Mục 4.7.5): tổng tổn thương 232 (210 TP + 22 FN, đếm trực tiếp từ JSON), Lesion-level Recall=90.52% (từ 90.09%), FNR=9.48% (từ 9.91%). Chỉ còn 2 dòng cuối bảng (Dice trung bình per-polygon, tỉ lệ đạt ngưỡng Dice≥0.5/0.7) vẫn dùng số cũ — đã đánh dấu (*) rõ ràng — vì cần Dice đo riêng từng polygon (mặt nạ dự đoán per-polygon), dữ liệu này JSON annotation không cung cấp được (JSON chỉ có GT, không có prediction).
5. **Build:** sạch, 141 trang, đã xem trực quan cả 2 bảng mới (trang 97, 103-104).

**Trạng thái C.4: ✅ COI NHƯ HOÀN TẤT** — chỉ còn 2 con số rất nhỏ (Dice per-polygon trung bình + 2 tỉ lệ ngưỡng) chưa xác nhận lại được vì cần predicted mask per-polygon (không phải GT, JSON không giúp được nữa); đã ghi chú minh bạch trong report, không phải lỗi tồn đọng do thiếu nỗ lực.

---

**Kế hoạch lớn C — C.11/C.12/C.14 ✅ HOÀN TẤT TOÀN BỘ. C.4 ✅ COI NHƯ HOÀN TẤT (xem cập nhật cuối phía trên) — chỉ còn 2 con số Dice per-polygon rất nhỏ chưa xác nhận được, cần predicted mask chi tiết không có sẵn.**

**Kế hoạch lớn E — chỉ còn 1 mục tạm hoãn:**
- **E.7** — Đổi tên đề tài khóa luận, chờ xác nhận/cho phép từ trường (không tự sửa).

## Cập nhật: Rà soát toàn diện định lượng + ký tự lạ + thuật ngữ (fork review)

Theo yêu cầu user "rà soát report, đặc biệt định lượng chính xác, Anh ngữ và dấu lạ vô nghĩa", đã tự sửa 2 chỗ dấu em-dash "—" dùng sai làm dấu câu (trong nội dung mới thêm ở Chapter4, mục threshold sweep BTXRD), rồi chạy 1 fork đọc toàn bộ main.tex + mọi file include (Chapter1-5, Appendix) đối chiếu số liệu. Fork phát hiện và đã sửa:

1. **[Lỗi số liệu, nghiêm trọng nhất]** ΔDice BTXRD trích sai "+0,3794" (số CŨ trước khi đồng bộ dataset gốc) ở 2 chỗ (Chapter4 dòng ~728, ~1081, phần thảo luận FracAtlas) — đáng lẽ phải là **+0,3867** (0.8607−0.4740, khớp `tab:baseline_comparison`). Đã sửa cả 2.
2. **[Lỗi số liệu do lẫn đơn vị, tự phát hiện thêm khi rà lại]** Câu so sánh "quy mô huấn luyện FracAtlas chỉ bằng ≈49% BTXRD" xuất hiện **3 lần** (dòng 665, 696, 1081) — lỗi vì so sánh nhầm đơn vị: `\NtrainFA`=730 là **mẫu per-polygon**, trong khi `\Ntrain`=1493 là **số ảnh** (khác cột trong `tab:dataset_stats`), 730/1493=49% chỉ là trùng hợp số học từ phép so sánh sai đơn vị. Đã sửa cả 3 chỗ dùng so sánh nhất quán đơn vị: 573 ảnh vs 1493 ảnh = **≈38%** (hoặc 730 vs 1848 mẫu per-polygon = ≈39%).
3. **[Mâu thuẫn nội dung còn sót từ việc xóa tiền xử lý]** 3 chỗ vẫn ngầm ý còn tiền xử lý/ảnh "sạch": `decuong.tex` dòng 118 ("Tập ảnh BTXRD sạch nhiễu kỹ thuật") và dòng 138 (Giai đoạn 2 kế hoạch "Tiền xử lý để loại bỏ nhiễu"); `chapter3.tex` dòng 22 ("Ảnh X-quang sạch..."). Đã sửa cả 3 cho khớp quyết định "không tiền xử lý".
4. **[Rounding nội bộ, mức thấp]** 2 số liệu Wilcoxon (+0.1064→+0.1065, +0.0387→+0.0388) lệch 0.0001 do khác đường tính (trừ trực tiếp bảng đã làm tròn vs tính từ dữ liệu thô) — đã thống nhất theo số của `tab:wilcoxon_ablation` (nguồn chính xác hơn) ở các câu không có phép trừ tường minh đi kèm; giữ nguyên các câu có hiển thị tường minh "X → Y" để không tạo mâu thuẫn toán học ngay trong câu.
5. Cụm "bị loại trong bước tiền xử lý" (nói về lọc polygon lỗi của FracAtlas, khác với tiền xử lý BTXRD đã xóa) đổi thành "bị loại khi lọc dữ liệu" để tránh gây hiểu lầm.

**Không phát hiện thêm vấn đề gì khác** (ký tự encoding lỗi, "---"/"$-$" dùng sai, thuật ngữ Anh-Việt lộn xộn) — báo cáo của fork xác nhận sạch ở các phần còn lại (Chapter2, danh mục thuật ngữ, bảng mới tính từ JSON đều khớp 100% khi kiểm tra thủ công).

**Build:** sạch, 141 trang, không lỗi/undefined reference.

**Mọi mục khác trong toàn bộ file này đều đã ✅ ĐÃ LÀM.**

---

## Cập nhật: tinh gọn toàn bộ report + rà soát lại (phiên "condense")

Theo yêu cầu người dùng, đã cô đặc văn xuôi toàn bộ report (Chapter1-5 + Appendix), cắt các cụm chuyển ý lặp ("Kết quả này cho thấy"...), rút gọn caption bảng/hình, không đụng số liệu/`\ref`/`\cite`/kết luận. Kết quả: 39.472 → 34.943 từ (**-11,5%**), 141 → 134 trang. Đồng thời cập nhật `decuong.tex` khớp phạm vi thực tế (bổ sung FracAtlas), tách trích dẫn đề cương khỏi bibliography chung (dùng số ngoặc vuông cục bộ [1]-[6] để đọc độc lập được), sửa các chỗ tiêu đề/đoạn văn mồ côi qua trang bằng `\needspace` (chỉ trong đề cương, theo đúng yêu cầu phạm vi hẹp của người dùng), xuất riêng `Decuong_KhoaLuan.pdf`.

Rà soát lại toàn diện sau cô đặc (fork đọc lại Chapter1/2/5 toàn văn + đối chiếu số liệu Chapter3/4): **sạch** — không lỗi số liệu, không câu văn gãy/dính do gộp ẩu, không mất ý, không dấu gạch ngang "—" sai quy ước, không `\ref`/`\cite` hỏng. Chỉ có 2 lỗi nhỏ về thuật ngữ (chữ thường "zoom-out"/"shift" lẫn vào giữa các chỗ khác viết hoa "Zoom-out"/"Shift", tại `chapter5.tex` dòng 34 và `chapter3.tex` dòng 244 pseudocode) — đã sửa.

**Lưu ý còn treo (chưa làm, chỉ ghi nhận):** phần FracAtlas trong `chapter4.tex` (Mục 4.4) có cùng kiểu lỗi trình bày "tiêu đề/đoạn văn mồ côi qua trang" (heading rớt xuống cuối trang, để trống nhiều rồi bảng nhảy nguyên khối sang trang sau) như đã phát hiện và sửa trong `decuong.tex` — nhưng lần đó người dùng chỉ yêu cầu sửa phạm vi hẹp "chỉnh mỗi đề cương", nên **chưa áp dụng `\needspace` cho Chapter 4**. Nếu muốn, có thể làm sau bằng đúng kỹ thuật đã dùng cho đề cương.

---

## KẾ HOẠCH LỚN F: Ảnh minh họa so sánh trực quan giữa các mô hình (làm nổi bật claim so sánh)

**Bối cảnh:** Mục 4.5 "Trực quan hóa kết quả" hiện có 4 hình định tính (Hình 4.9-4.12, từ C.14) nhưng **toàn bộ chỉ show dự đoán của riêng PGA-UNet** (ca TP qua pipeline, ca Shift, ca tổn thương nhỏ, ca thất bại) — **chưa có hình nào đối chiếu trực tiếp dự đoán của PGA-UNet cạnh U-Net/SAM-Med2D trên CÙNG một ảnh đầu vào**. Các bảng số liệu (Bảng subcat_baseline, subcat_sam, ablation_arch...) đã chứng minh khoảng cách bằng số, nhưng một người đọc lướt nhanh sẽ bị thuyết phục mạnh hơn nhiều bởi ảnh trực quan cho thấy rõ ràng bằng mắt thường mô hình yếu hơn "sai" như thế nào.

**Nguyên tắc chọn ảnh chung (áp dụng cho mọi mục F.1-F.5 dưới đây):**
- **Dùng CÙNG một ảnh đầu vào** cho các mô hình được so sánh trong một mục — không lấy ảnh khác nhau, để người đọc so trực tiếp cột-đối-cột.
- Ưu tiên lấy ảnh từ **nhóm đã phân loại sẵn độ khó/đặc tính** trong các bảng subcat (TOP-DICE/BOTTOM-DICE, hoặc 3 nhóm Tổn thương nhỏ/Biên giới mờ/Tổn thương rõ nét) — vì đã biết trước ảnh nào sẽ cho kết quả tương phản rõ, không cần dò mù.
- **Tiêu chí "nhìn bằng mắt thường"**: khoảng cách phải thấy được không cần đọc số Dice — ví dụ mặt nạ mô hình yếu hơn trống hoàn toàn/lệch hẳn ra ngoài vùng tổn thương/vỡ vụn nhiều mảnh nhỏ rời rạc, trong khi mô hình mạnh hơn bám sát viền GT liền mạch.
- Bố cục đề xuất mặc định (theo đúng style 5 cột đã dùng ở Hình 4.9): **Ảnh gốc → Ảnh + hộp giới hạn câu nhắc → Ground Truth → Dự đoán mô hình A (yếu hơn) → Dự đoán mô hình B (PGA-UNet)**.
- Mỗi mục nên lấy **1 cặp ảnh "khó"** (khoảng cách lớn, đúng dấu hiệu suy yếu của baseline đã nêu trong bảng số) **+ 1 cặp ảnh "dễ"** (cả hai đều ổn, chênh lệch nhỏ) để đối chiếu — tránh cảm giác cherry-pick cực đoan một chiều.
- Ảnh tổn thương/đường gãy tuy khó/nhỏ nhưng vẫn phải **thấy được bằng mắt thường trên ảnh gốc** khi in ra — tránh chọn ca tổn thương siêu nhỏ đến mức không nhìn ra được kể cả trên GT.

**F.1 — PGA-UNet vs U-Net, nhóm Khó (BTXRD, ứng với Bảng~`tab:subcat_baseline`)**
- Đích minh họa: ΔDice=+0.3867 tổng thể, đặc biệt nhóm \textit{Khó} (bottom-50): U-Net Dice=0.0211 (gần như sụp đổ, HD95=284.72px) trong khi PGA-UNet giữ 0.8261.
- Chọn ảnh: 1 ảnh trong nhóm BOTTOM-DICE nơi mặt nạ U-Net gần như trống/lệch hẳn ra ngoài, PGA bám sát GT; ưu tiên ca có tổn thương đủ lớn để mắt thường nhận ra ngay trên ảnh gốc rằng U-Net "trật lất" chứ không phải do nhìn không rõ. Kèm 1 ảnh nhóm TOP-DICE (dễ) để đối chiếu khoảng cách chỉ nới rộng ở ảnh khó, không phải U-Net luôn tệ.
- Nguồn gợi ý: `Result/Result_BTXRD/test-subcat-pga-vs-baseline.ipynb` (đã tính đúng 2 nhóm TOP/BOTTOM-DICE dùng cho bảng số liệu, nên rất có thể đã có sẵn — hoặc dễ thêm — cell hiển thị ảnh gốc/GT/dự đoán từng ca cụ thể trong 2 nhóm này).

**F.2 — PGA-UNet vs SAM-Med2D, nhóm Tổn thương nhỏ (BTXRD, ứng với Bảng~`tab:subcat_sam`)**
- Đích minh họa: nhóm \textit{Tổn thương nhỏ}, SAM-Med2D chỉ đạt Dice=0.1356 (gần như bỏ sót hoàn toàn ở độ phân giải 256) trong khi PGA-UNet đạt 0.8301 — khoảng cách lớn nhất trong toàn bộ so sánh với SAM.
- Chọn ảnh: ca tổn thương nhỏ nơi SAM gần như không dự đoán được gì (mask trống hoặc vài pixel lẻ tẻ) còn PGA bắt trọn vùng; chọn ca mà tổn thương tuy nhỏ nhưng vẫn nhận ra được bằng mắt thường trên ảnh gốc.
- Nguồn gợi ý: `Result/Result_BTXRD/test-subcat-pga-vs-sam-r256-r512.ipynb` (đã tính 3 nhóm đặc tính tổn thương, cùng input cho cả SAM và PGA).

**F.3 — Ablation kiến trúc: đóng góp của CAD (Bảng~`tab:ablation_arch`)** *(khó thực hiện hơn F.1/F.2, ưu tiên thấp hơn)*
- Đích minh họa: phát hiện trung tâm của ablation — "điều kiện hóa attention (CAD) mới quyết định tính bền bỉ, không phải bản thân attention" (V6 so V7 ở Shift, $+0.1065$, $p<0{,}001$).
- Chọn ảnh: dàn cả 8 biến thể trong 1 hình sẽ rối; đề xuất rút gọn còn **3 cột trên cùng 1 ảnh kịch bản Shift**: U-Net+PSG+Attention gốc (V7, chưa điều kiện hóa) — PGA-UNet đề xuất (V6, đã điều kiện hóa CAD) — GT. Chọn ảnh mà V7 lệch tâm/bám sai vùng do câu nhắc dịch chuyển, còn V6 vẫn bám đúng.
- Lưu ý khả thi: cần notebook test của V6 và V7 chạy suy luận trên **cùng một `img_name`** (kiểm tra thứ tự ảnh test trong `test-v7-psg-attention.ipynb` so với notebook test của V6 `Full_HeatmapPrompt`) — không cần train lại, chỉ cần load 2 checkpoint đã lưu sẵn và suy luận chung 1 ảnh cụ thể nếu thứ tự ảnh giữa 2 notebook không khớp sẵn.

**F.4 — Tính bền bỉ Zoom-out vs Shift, cùng 1 ảnh cùng 1 mô hình (ứng với Bảng~`tab:robustness_comparison`)**
- Khác F.1-F.3 (so giữa các mô hình): mục này so giữa **2 kịch bản câu nhắc** trên cùng PGA-UNet, để chứng minh trực quan mức sụt Dice rất nhỏ giữa Zoom-out và Shift.
- Chọn ảnh: 1 ảnh, 2 hộp giới hạn (Zoom-out đúng tâm vs Shift lệch tâm) qua PGA-UNet — mặt nạ dự đoán gần như không đổi dù hộp câu nhắc dịch chuyển. Nếu lấy được thêm dự đoán U-Net/SAM ở cùng 2 kịch bản đó thì càng thuyết phục (baseline lệch theo hộp rõ hơn).
- Đã có nền sẵn: Hình 4.10 hiện tại (2 ca Shift riêng lẻ, Dice 0.851/0.894) — có thể **mở rộng thêm cột "cùng ảnh ở Zoom-out"** thay vì làm hình mới hoàn toàn.
- Nguồn gợi ý: `pga-vs-unet2d-r512.ipynb` (đã chạy cả 3 kịch bản câu nhắc trong cùng notebook).

**F.5 — FracAtlas: mirror F.1/F.2 trên bộ dữ liệu thứ hai (ứng với Bảng~`tab:fracatlas_subcat_baseline`, `tab:fracatlas_subcat`)**
- Đích minh họa: củng cố phát hiện tổng quát hóa — U-Net gần sụp đổ ở nhóm BOTTOM-DICE FracAtlas (Dice=0.1130) trong khi PGA giữ 0.8015; SAM-Med2D (FT) ở nhóm Tổn thương nhỏ FracAtlas chỉ đạt 0.4395 so với PGA-512 đạt 0.8028.
- Chọn ảnh: cùng tiêu chí F.1/F.2, nhưng lưu ý FracAtlas là ảnh gãy xương (đường nứt mảnh, tuyến tính) — chọn ca mà đường gãy đủ rõ để mắt thường thấy được trên ảnh gốc.
- Nguồn gợi ý: `Result/Result_FracAtlas/test-subcat-pga-vs-baseline.ipynb`, `Result/Result_FracAtlas/test-subcat-pga-vs-sam-r256-r512.ipynb` (song song F.1/F.2).

**Vị trí đặt trong Chapter 4 (đề xuất):**
- F.1, F.2, F.4 (BTXRD) → thêm mục con mới, ví dụ "4.5.4 So sánh trực quan với mô hình cơ sở", ngay sau Hình 4.12 hiện tại trong Mục 4.5/4.6.
- F.3 (ablation) → đặt ngay sau Bảng~`tab:ablation_arch` (Mục 4.3.1), không đặt chung với mục trực quan hóa tổng quát vì gắn chặt với phần ablation.
- F.5 (FracAtlas) → thêm 1 hình trong Mục 4.4 (FracAtlas), gần các bảng subcat tương ứng.

**Mức độ ưu tiên/khả thi:** F.1 và F.2 khả thi nhất và có tác động trực quan mạnh nhất (khoảng cách Dice lớn nhất, notebook nguồn đã có sẵn tính toán per-image). F.5 tương tự nhưng bộ dữ liệu phụ. F.4 là mở rộng nhẹ của hình đã có. F.3 khó nhất (cần khớp `img_name` giữa 2 checkpoint riêng biệt) — có thể làm sau cùng hoặc bỏ nếu không khớp được ảnh.

**Việc cần làm tiếp theo (không phải AI làm — cần người dùng tự chọn ảnh):** người dùng vào từng notebook nguồn gợi ý ở trên, chọn ảnh cụ thể theo đúng tiêu chí (khó/dễ, nhìn rõ bằng mắt thường), export PNG, rồi đưa lại để ghép vào Chapter 4 theo đúng vị trí đề xuất — không cần train/chạy lại gì (trừ F.3 nếu 2 notebook không cùng thứ tự ảnh).

---

## Cập nhật: Kiểm tra dữ liệu 7 biểu đồ cột hiện có + phát hiện 2 bảng thiếu biểu đồ (đã tự vẽ bổ sung)

Theo yêu cầu "kiểm tra lại cần thêm ảnh nữa không, kiểm tra dữ liệu đúng chưa, biểu đồ cột và số liệu đồ", đã đối chiếu từng con số trên cả 7 file `chart_*.png` hiện có trong `Report/images/` với đúng bảng nguồn trong `chapter4.tex`:

- `chart_baseline_sam_comparison.png`, `chart_ablation.png`, `chart_fracatlas_ablation.png`, `chart_subcat_btxrd.png`, `chart_fracatlas_pga_full.png`, `chart_subcat_fracatlas.png`: **khớp chính xác 100%** với bảng nguồn (`tab:baseline_comparison`/`tab:sam_comparison`, `tab:ablation_arch`, `tab:fracatlas_ablation_arch`, `tab:subcat_sam`, `tab:fracatlas_pga_full`, `tab:fracatlas_subcat`).
- `chart_fracatlas_subcat_baseline.png`: khớp, chỉ có 1 chênh lệch hiển thị không đáng kể (PGA-UNet nhóm BOTTOM-DICE: bảng ghi `0.8015` làm tròn 4 chữ số, biểu đồ hiện `0.801` làm tròn 3 chữ số từ số thô chính xác hơn — không phải lỗi số liệu, chỉ khác độ làm tròn).

**Phát hiện thiếu (đã tự vẽ bổ sung, không phải lỗi số liệu mà là thiếu tính nhất quán trình bày):** hai bảng BTXRD sau **không có biểu đồ cột đi kèm**, trong khi bản mirror FracAtlas của chúng ĐỀU có:
1. `tab:subcat_baseline` (U-Net vs PGA-UNet theo độ khó, Dễ/Khó) — FracAtlas có `chart_fracatlas_subcat_baseline.png` nhưng BTXRD thì không.
2. `tab:pga_256_512` (PGA-UNet 256 vs 512) — FracAtlas có `chart_fracatlas_pga_full.png` nhưng BTXRD thì không.

Đã tự vẽ bổ sung 2 biểu đồ mới, đúng style/màu đã dùng xuyên suốt (`YELLOW=#eda100` cho U-Net, `BLUE=#2a78d6` cho PGA-UNet chính, nhạt/đậm cho 256/512), số liệu lấy trực tiếp từ 2 bảng trên:
- `images/chart_subcat_baseline_btxrd.png` — U-Net (0.849/0.021) vs PGA-UNet (0.897/0.826), nhóm Dễ/Khó — chính là biểu đồ hóa cho ví dụ "U-Net gần như sụp đổ" đã nêu ở KẾ HOẠCH LỚN F (F.1), giờ đã có bản biểu đồ số liệu đi kèm ảnh định tính sẽ chọn sau.
- `images/chart_pga_256_512.png` — PGA-UNet 256 (0.843/0.815/0.834) vs 512 (0.861/0.842/0.856), ba kịch bản.

Đã chèn cả 2 vào đúng vị trí trong `chapter4.tex` (ngay sau đoạn "Nhận xét" của mỗi bảng tương ứng, trước khi sang mục con kế tiếp), build lại sạch — **137 trang** (từ 135), không lỗi/undefined reference, đã xem trực quan cả 2 trang render (Hình 4.2 và Hình 4.4 mới, đánh số + tham chiếu bảng đúng).

**Kết luận cho câu hỏi "cần thêm ảnh nữa không":** về **biểu đồ số liệu** (chart) — nay đã đủ, mọi bảng so sánh nhiều nhóm/nhiều mô hình đều có biểu đồ trực quan đi kèm, không còn thiếu chỗ nào. Về **ảnh định tính** (ảnh dự đoán thật) — vẫn còn nguyên danh sách F.1-F.5 ở trên, chưa làm (cần người dùng tự chọn ảnh từ notebook).
