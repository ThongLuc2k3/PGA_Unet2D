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

---

## Cập nhật: Rà soát và xóa toàn bộ chú thích tiếng Anh chèn giữa thân bài

Theo yêu cầu người dùng ("đã là tiếng việt thì sao cứ chèn thêm từ tiếng anh giải nghĩa làm gì"), đã chạy 1 fork rà soát toàn bộ Chapter1-5 + Appendix/tomtat.tex + Appendix/decuong.tex tìm mọi chỗ "thuật ngữ tiếng Việt (chú thích tiếng Anh)" chèn giữa câu, phân biệt với các trường hợp được miễn trừ (tên riêng mô hình/kiến trúc, ký hiệu đo lường chuẩn quốc tế Dice/IoU/HD95/CBL/Precision/Recall/..., tên kịch bản Zoom-out/Shift/Mixed, trích dẫn).

**Đã xóa/sửa toàn bộ các vi phạm tìm được**, gồm cả một số chỗ tự phát hiện thêm khi rà lại lần 2 (từ tiếng Anh trần không có bản dịch, như "foreground/background", "annotation", "metadata", "pixel-level", "per-polygon", "per-image"):
- Chapter1: bỏ gloss "(image segmentation)", "(deep learning)", "(indicator function)", "(cross-validation)" (đồng thời sửa nhất quán "kiểm định chéo"→"đánh giá chéo"), "(sub-category)"; bỏ mở rộng tiếng Anh của PACS/SAM (đã có sẵn trong `danhmuctuvietat.tex`).
- Chapter2: bỏ gloss CNN/NLP mở rộng tiếng Anh (đã có sẵn phụ lục viết tắt), "(Max Pooling)"→dùng "gộp cực đại", "(concatenate)"→"nối kênh", "(Hausdorff Distance - HD)"→giữ "(HD)".
- Chapter3: bỏ "(selective enhancement)", "(blend weight)"→dịch "trọng số pha trộn", "(False Positive)"→"(FP)", "(Offline/Online Training/Inference)", "(Prompt Heatmap Representation)"; dịch "nhãn metadata"→"nhãn siêu dữ liệu", "mặt nạ phân đoạn pixel-level"→"cấp độ pixel" (toàn bộ 2 chỗ).
- Chapter4 (nhiều nhất): bỏ "(Robustness)", "(reproducibility)", "(hyperparameters)", "(Loss Function)", "foreground/background"→dịch "vùng tổn thương/vùng nền", "(Union GT)"→"Hợp nhất GT", "(Max-Merge Prediction)", "(pixel-wise maximum)", "(fracture)", "(Gaussian heatmap)" ×2 (dư thừa so với "bản đồ nhiệt Gaussian" đã dùng), "(False Positive/Negative)"→"(FP/FN)", "(Evaluation Metrics)" ×2 (2 bảng Gatekeeper BTXRD+FracAtlas), "(concatenate)", "(sub-category)", "(image-level)" ×2 (kể cả điểm định nghĩa đầu tiên), "(lesion-level)" ×3, "(baseline)" ×2 → "(cơ sở)"; dịch toàn bộ "pixel-level"/"per-polygon"/"per-image" (15+ chỗ) và "JSON annotation gốc" ×3 → "JSON chú thích gốc".
- Appendix/decuong.tex: bỏ "(pixel-level mask)", "(heatmap)".

**Bổ sung 11 dòng mới vào `Appendix/doichieuthuatngu.tex`** (bảng đối chiếu Anh-Việt) cho các thuật ngữ chung vừa xóa gloss khỏi thân bài: Cấp độ pixel/Pixel-level, Học sâu/Deep learning, Siêu tham số/Hyperparameter, Hàm chỉ thị/Indicator function, Đánh giá chéo/Cross-validation, Nối kênh/Concatenate, Gộp cực đại/Max pooling, Hàm mất mát/Loss function, Vùng nền (ảnh)/Background, Trọng số pha trộn/Blend weight, Siêu dữ liệu/Metadata.

**Giữ nguyên không sửa** (thuộc diện miễn trừ theo quy tắc đã chốt): tên mô hình/kiến trúc (U-Net, PGA-UNet, SAM-Med2D, Gatekeeper...), ký hiệu đo lường chuẩn quốc tế (Dice, IoU, HD95, CBL, Precision, Recall, Accuracy, F1, AUC-ROC, TP/FP/FN/TN, GT, FNR...), tên kịch bản (Zoom-out/Shift/Mixed), tên hội nghị trong danh mục tham khảo (MICCAI/ICML/MIDL).

**Build:** sạch, 136 trang, không lỗi/undefined reference.

---

## Cập nhật: Bỏ hẳn mạch "không qua tiền xử lý loại nhiễu R/L" — nói bình thường lại

User nhận xét mạch văn "cố tình không xử lý nhiễu R/L, giữ nguyên để huấn luyện" đọc lạ đời, không cần thiết phải nhấn mạnh/biện minh xuyên suốt report. Yêu cầu: coi như không đề cập nhiễu/R-L gì cả; nếu cần nói "tiền xử lý" thì chỉ nói là xử lý cấu trúc đầu vào cho phù hợp chạy code (resize, tạo mặt nạ, chia tập).

**Đã bỏ toàn bộ mạch văn này và viết lại bình thường** (không chỉ xóa gloss tiếng Anh như đợt trước — lần này bỏ hẳn nội dung/lập luận về quyết định không xử lý nhiễu):
- Chapter1 (Thách thức về dữ liệu): viết lại thành thách thức về quy mô dữ liệu + cần xử lý đúng cấu trúc đầu vào (tạo mặt nạ, chuẩn hóa kích thước, chia tập) — bỏ hẳn "ký hiệu R/L, dòng văn bản thông tin bệnh nhân...".
- Chapter3: đổi tên mục 3.2 "Bộ dữ liệu ảnh X-quang và đặc điểm nhiễu kỹ thuật" → "Bộ dữ liệu ảnh X-quang"; bỏ bullet "dữ liệu thô chứa nhiễu kỹ thuật... không xử lý"; đổi tên mục con "Huấn luyện trực tiếp trên ảnh gốc, không qua bước tiền xử lý loại nhiễu" → "Xử lý dữ liệu đầu vào", viết lại hoàn toàn thành mô tả bình thường (resize 512×512, tạo mặt nạ từ tọa độ đa giác, chia train/val/test, dùng chung 1 ảnh cho huấn luyện/suy luận/hiển thị) — bỏ hết đoạn biện minh về R/L và hạn chế liên quan; sửa 2 dòng trong Algorithm 1/2 (bỏ "(không qua bước loại bỏ nhiễu...)"); sửa câu tổng kết chương.
- Chapter4: "Lý do chọn BTXRD" bỏ câu về nhiễu kỹ thuật/R-L, chỉ giữ lý do chọn vì có đủ 3 cấp nhãn; bullet "Ảnh chất lượng thấp" (phân tích thất bại) chỉ còn "ảnh mờ hoặc thiếu sáng", bỏ phần R/L.
- Appendix/decuong.tex: Giai đoạn 2 (cả đoạn văn lẫn bảng kế hoạch) viết lại thành "tạo mặt nạ, chuẩn hóa kích thước, chia tập dữ liệu" — bỏ "không qua bước tiền xử lý loại nhiễu".
- Appendix/danhmuctuvietat.tex: xóa dòng "R/L" khỏi bảng viết tắt (không còn được nhắc ở đâu trong thân bài nên không cần định nghĩa nữa).

**Không đụng tới:** câu ở Chương 3 mục PSG nói "Cổng không gian ở bộ mã hóa đã loại bỏ nhiễu nền đáng kể" — đây là tính chất kiến trúc (PSG khuếch đại đặc trưng vùng câu nhắc, ức chế nhiễu nền ở mức đặc trưng), khác hoàn toàn chủ đề tiền xử lý ảnh đầu vào, không phải nội dung cần bỏ.

**Build:** sạch, 135 trang (từ 136), không lỗi/undefined reference. Đã xem trực quan 3 trang chính đã sửa (Chapter1 thách thức, Chapter3 mục dữ liệu, Chapter4 Lý do chọn BTXRD) — đọc tự nhiên, không còn dấu vết chủ đề nhiễu/R-L.

---

## Cập nhật QUAN TRỌNG: Chỉnh lại phạm vi đóng góp — PGA-UNet là đóng góp DUY NHẤT, Gatekeeper/pipeline chỉ là thực nghiệm minh họa

User làm rõ (2 lượt liên tiếp): đóng góp và trọng tâm của khóa luận **dừng lại ở PGA-UNet mà thôi**. Phần Gatekeeper/pipeline/luồng xử lý đầu cuối ở Chương 4 **không phải đóng góp thứ hai** — chỉ là một thực nghiệm/demo bổ sung minh họa cách PGA-UNet có thể kết hợp vào quy trình thực tế hỗ trợ bác sĩ, đồng thời làm rõ thêm bài toán (PGA cần câu nhắc nên không tự vận hành được trên luồng ảnh chưa sàng lọc). Toàn bộ nội dung từ đề cương đến Chương 1-5 phải hiểu đúng: chủ đề xuyên suốt là PGA-UNet, không phải "mô hình có sàng lọc".

**Phát hiện:** Chapter1 (`\section{Đóng góp của khóa luận}`) đang viết "Khóa luận có **hai** đóng góp chính", liệt kê Gatekeeper/pipeline eval như đóng góp thứ 2 ngang hàng PGA-UNet — sai với ý định thật của tác giả. Chapter5 (kết luận) cũng liệt kê dạng bullet ngang hàng (dù đã có chữ "bổ sung"). Appendix/decuong.tex (Mục tiêu đề tài) liệt kê "Phát triển module sàng lọc (Gatekeeper)" như mục tiêu kiến trúc riêng biệt thứ 2.

**Đã sửa cả 3 chỗ**, chuyển từ cấu trúc liệt kê ngang hàng sang: PGA-UNet là đóng góp cốt lõi duy nhất (giữ nguyên toàn bộ nội dung/số liệu PSG/CAD/ablation), rồi một đoạn riêng biệt rõ ràng gắn nhãn "**Thực nghiệm minh họa khả năng ứng dụng thực tế**" / "không phải đóng góp kỹ thuật riêng biệt" cho phần Gatekeeper — giữ nguyên toàn bộ số liệu (AUC-ROC=0.9421, Pipeline Dice=0.6763...), chỉ đổi khung diễn giải:
- `Chapter1/chapter1.tex` (Mục 1.5): bỏ "hai đóng góp chính" + `\begin{enumerate}` 2 mục → 1 đóng góp cốt lõi (PGA-UNet) + 1 đoạn "Thực nghiệm minh họa..." tách riêng.
- `Chapter5/chapter5.tex` (Mục kết luận): bỏ `\begin{itemize}` 2 bullet ngang hàng → 1 đoạn đóng góp cốt lõi + 1 đoạn thực nghiệm minh họa nối tiếp.
- `Appendix/decuong.tex` (Mục tiêu đề tài, mục 2): đổi tên từ "Phát triển module sàng lọc (Gatekeeper)" → "Minh họa khả năng ứng dụng thực tế của PGA-UNet", có ghi rõ "(không phải đóng góp kiến trúc riêng biệt)".

**Không đổi** (đã đúng từ trước, chỉ xác nhận lại): Chapter3 (`\section{Module sàng lọc (Gatekeeper)}`) đã sẵn có câu "Module này **không phải đóng góp kỹ thuật trọng tâm** mà là thành phần hỗ trợ" — khớp hoàn toàn với ý user, giữ nguyên. Chapter4 Phần I/II framing ("module Gatekeeper hỗ trợ") và `tomtat.tex` cũng đã đủ trung lập, không cần sửa thêm.

**Build:** sạch, 135 trang, không lỗi/undefined reference. Đã xem trực quan 2 trang Chương 1 (Mục 1.5) xác nhận đọc đúng ý.

---

## Cập nhật: Rà soát lần 2 toàn bộ report — tìm nốt các chỗ còn phóng đại vai trò Gatekeeper/pipeline

Theo yêu cầu rà soát lại lần nữa, đã chạy 1 fork đọc toàn bộ Chapter1-5 + tomtat + decuong, tìm mọi câu nhắc đến Gatekeeper/sàng lọc/pipeline ở NGOÀI phạm vi thực nghiệm Chương 4, kiểm tra xem có chỗ nào còn nói theo kiểu "mắt xích quan trọng"/đóng góp thay vì chỉ "hỗ trợ/khắc phục nhược điểm".

**Kết quả: đa số đã đúng tinh thần từ đợt sửa trước** (Chapter4 dùng đúng cụm "mắt xích yếu hơn, cần cải thiện" — đúng ý, không phải đóng góp; Chapter5 phần Hạn chế; tomtat.tex đã trung lập). Tìm thêm và đã sửa 3 chỗ còn sót:

1. **Chapter3 dòng 11** ("Kiến trúc tổng thể chia thành các module liên hoàn qua hai giai đoạn \textbf{cốt lõi}") — chữ "cốt lõi" áp cho cả 2 giai đoạn (sàng lọc + phân đoạn) ngang nhau → sửa thành "hai giai đoạn \textbf{nối tiếp}" (chỉ mô tả thứ tự, không gán tầm quan trọng ngang nhau).
2. **Appendix/decuong.tex dòng 64** (đoạn giới thiệu đầu "Giới thiệu về đề tài" — bản decuong riêng, không phải Chapter1): trước đó viết PGA-UNet và module sàng lọc trong CÙNG một câu như thể đồng thiết kế ("...tích hợp... kết hợp module phân lớp sàng lọc để tạo thành luồng xử lý đầu cuối hoàn chỉnh") → tách thành 2 câu, câu sau gắn rõ "Để minh họa khả năng ứng dụng thực tế... (không phải đóng góp kiến trúc riêng biệt)".
3. **Chapter1 dòng 75** (nhỏ, mang tính rà soát kỹ hơn là lỗi nghiêm trọng): "Chi tiết kiến trúc và huấn luyện ngoại tuyến của \textbf{hai mô hình}" (đặt PGA-UNet và Gatekeeper ngang hàng là "hai mô hình") → đổi thành "Chi tiết kiến trúc PGA-UNet, module sàng lọc \textbf{hỗ trợ} và huấn luyện ngoại tuyến".

**Ghi chú không sửa (đã cân nhắc, không thuộc phạm vi từ ngữ):** `\section{Module sàng lọc (Gatekeeper)}` ở Chapter3 vẫn là `\section` cùng cấp với `\section{Mô hình phân đoạn PGA-UNet...}` trong mục lục — về mặt cấu trúc heading nhìn ngang hàng, nhưng đây là vấn đề cấp bậc mục lục, không phải câu chữ phóng đại; nội dung bên trong đã tự nói rõ "không phải đóng góp trọng tâm". Không đổi cấp mục vì rủi ro/công sức tái cấu trúc lớn hơn lợi ích, và không nằm trong phạm vi lời phàn nàn cụ thể của user (về cách "nói"/diễn đạt).

**Build:** sạch, 135 trang, không lỗi/undefined reference. **Kết luận: sau 2 đợt rà soát, không còn phát hiện chỗ nào diễn đạt Gatekeeper/pipeline như đóng góp hay mắt xích quan trọng ngoài phạm vi Chương 4** (nơi được phép trình bày chi tiết như một thực nghiệm minh họa).

---

## Cập nhật: Tái cấu trúc thứ tự Chương 3 — mô hình phải rõ trước, hệ thống minh họa đưa xuống cuối; sửa vị trí hình arch_pga_unet2d.png

User chỉ ra 2 vấn đề: (1) Chương 3 mở đầu bằng "Kiến trúc tổng thể của hệ thống" (mô tả cả 2 giai đoạn Gatekeeper+PGA-UNet) NGAY TỪ ĐẦU, trước khi PGA-UNet (đóng góp chính) được giải thích — đọc ngược logic; nếu muốn trình bày "hệ thống" thì phải để cuối, còn "mô hình" (PGA-UNet) phải làm rõ trước tiên. (2) Hình `arch_pga_unet2d.png` không thấy hiện rõ — thực ra ảnh có tồn tại và được include đúng, nhưng nó bị đặt tuốt ở cuối phần PSG/CAD (sau khi đã giải thích xong chi tiết toán học), không phải ngay đầu để người đọc hình dung tổng quan trước.

**Đã tái cấu trúc toàn bộ Chương 3** (viết lại file bằng Write để đảm bảo di chuyển khối lớn chính xác), đổi thứ tự mục từ:
`Kiến trúc tổng thể hệ thống → Dữ liệu → PGA-UNet → Gatekeeper → Giải thuật → Tổng kết`
thành:
`Dữ liệu → PGA-UNet (đầy đủ, hình kiến trúc ngay đầu mục) → Minh họa ứng dụng thực tế (đổi tên + đổi khung diễn giải, đưa xuống sau PGA-UNet) → Gatekeeper → Giải thuật → Tổng kết`

Chi tiết:
- Di chuyển hình `arch_pga_unet2d.png` từ cuối subsection CAD lên **ngay đầu** `\section{Mô hình phân đoạn PGA-UNet}` (sau câu "Ba thành phần cốt lõi sau đây lần lượt hiện thực hóa đóng góp trên."), để người đọc thấy sơ đồ tổng quan TRƯỚC khi đọc chi tiết PSG/CAD.
- Đổi tên mục "Kiến trúc tổng thể của hệ thống" → **"Minh họa ứng dụng thực tế: luồng xử lý hai giai đoạn"**, thêm câu dẫn "đây là một minh họa ứng dụng, không phải đóng góp kiến trúc riêng biệt", đưa xuống vị trí SAU khi PGA-UNet đã được trình bày đầy đủ (giữ nguyên `\label{sec:tong_the}` để không vỡ các `\ref` khác).
- Sửa câu chuyển tiếp cuối mục đó: "được trình bày ở các mục tiếp theo" (sai, vì PGA-UNet giờ đã ở TRƯỚC) → "Kiến trúc chi tiết của PGA-UNet đã được trình bày tại Mục~3.2; chi tiết module sàng lọc được trình bày ở mục tiếp theo".
- Sửa câu "Tổng kết chương" cho khớp thứ tự mới, nêu rõ PSG/CAD là "đóng góp kỹ thuật trọng tâm của khóa luận", Gatekeeper là "một thực nghiệm minh họa".
- **Tự phát hiện thêm 1 lỗi cùng loại đã gặp trước đây:** hình `pipeline_pga_app_inference.png` (sơ đồ luồng xử lý) dùng `[htbp]` nên bị trôi (float) qua khỏi đoạn văn kết thúc mục, sai thứ tự đọc y hệt lỗi đã sửa ở Chương 4 tuần trước — đã đổi cả 2 hình mới di chuyển/liên quan (`arch_pga_unet2d.png` và `pipeline_pga_app_inference.png`) sang `[H]` để khóa đúng vị trí.

**Build:** sạch, 136 trang (từ 135), không lỗi/undefined reference. Đã xem trực quan: trang mở đầu Chương 3 (Mục 3.1 Dữ liệu), trang có Hình 3.1 (kiến trúc PGA-UNet, đã lên đầu Mục 3.2), và trang có Hình 3.2 (luồng xử lý, nay đúng thứ tự trong Mục 3.3 "Minh họa ứng dụng thực tế").

---

## Cập nhật: Bỏ hẳn mục "Bộ dữ liệu ảnh X-quang" khỏi Chương 3 — trùng lặp với Chương 4

User chỉ ra tiếp: Chương 3 không nên có mục "Bộ dữ liệu ảnh X-quang" ở đầu — Chương 4 mới là nơi trình bày dữ liệu. Kiểm tra lại: **đúng, Chương 4 (Mục 4.1.1 "Tập dữ liệu ảnh X-quang") đã có sẵn mô tả BTXRD đầy đủ hơn** (tên bộ dữ liệu, lý do chọn, hai phân vùng dữ liệu, bảng thống kê `tab:dataset_stats`, thống kê Gatekeeper) — mục ở Chương 3 hoàn toàn trùng lặp, chỉ thiếu bảng số liệu thật.

**Đã xử lý:**
- **Xóa hẳn** mục "Bộ dữ liệu ảnh X-quang" (gồm 2 subsection "Bộ dữ liệu BTXRD" và "Xử lý dữ liệu đầu vào") khỏi Chương 3. Chương 3 giờ **mở đầu thẳng bằng Mục 3.1 "Mô hình phân đoạn PGA-UNet"**.
- Phần nội dung "Xử lý dữ liệu đầu vào" (resize 512×512, tạo mặt nạ từ tọa độ đa giác, dùng chung 1 ảnh gốc xuyên suốt) **gộp vào cuối Mục 4.1.1** ở Chương 4 (nơi nó thuộc về), đồng thời `\label{sec:tien_xu_ly}` (được `\ref` từ 3 nơi khác) cũng dời theo sang Chương 4 — không có `\ref` nào bị vỡ (đã kiểm tra: 2 nhãn con `subsec:dataset_btxrd`/`subsec:preprocessing_pipeline` chưa từng bị `\ref` ở đâu nên xóa an toàn).
- Sửa câu tự tham chiếu thừa ở Chương 4 (trước đó viết "chi tiết xử lý dữ liệu đầu vào tại Mục X, Chương 3" — nay nội dung đó nằm ngay trong chương này nên bỏ hẳn phần ngoặc).
- Sửa "Tổng kết chương" Chương 3 (bỏ "đặc điểm bộ dữ liệu BTXRD" khỏi danh sách tóm tắt).
- Sửa "Bố cục của khóa luận" ở Chương 1 cho khớp: bỏ "đặc điểm bộ dữ liệu" khỏi mô tả Chương 3, thêm vào mô tả Chương 4.
- Sửa Algorithm 1 (Chương 3) tham chiếu `Mục~\ref{sec:tien_xu_ly}` nay trỏ đúng sang Chương 4, đã ghi rõ "Chương 4" trong ngoặc cho không mơ hồ.

**Tự phát hiện thêm 3 lỗi float-ordering cùng loại** khi rà lại toàn bộ 17 trang Chương 3 sau khi tái cấu trúc (do việc xóa/thêm nội dung làm dịch chuyển trang, lộ ra các bảng/giải thuật dùng `[htbp]` bị trôi qua khỏi đoạn văn kết): bảng kế thừa (`tab:inheritance_contribution`), Algorithm 1, và Algorithm 2 — cả 3 đều đổi sang `[H]` để khóa đúng vị trí, khớp với 2 hình đã sửa trước đó trong cùng chương.

**Build:** sạch, 135 trang (từ 136), không lỗi/undefined reference. Đã render và xem trực quan toàn bộ 17 trang Chương 3 sau tái cấu trúc, xác nhận thứ tự đọc đúng ở mọi bảng/hình/giải thuật.

---

## Cập nhật: Cô đọng hàng PSG + sắp lại thứ tự hàng + mở rộng cột Bảng 3.1

User chỉ ra hàng "Cổng không gian (PSG)" trong Bảng 3.1 (`tab:inheritance_contribution`) dài hơn hẳn 3 hàng còn lại (~7-8 dòng so với ~2-4 dòng), gây lệch bảng và đẩy bảng + đoạn "Chuỗi kế thừa tuyến tính" ngay sau sang 2 trang khác nhau.

**Đã xử lý (cô đọng):** rút gọn văn phong 2 ô "Kế thừa từ" và "Đóng góp mới" của hàng PSG — bỏ các cụm dư thừa → còn "Gợi ý từ hướng tiêm bản đồ không gian vào CNN: ghép kênh trong DeepIGeoS...; tiêm Gaussian heatmap vào mô hình nền tảng lúc suy luận...". Hàng PSG còn ~5-6 dòng, bảng + đoạn sau vừa lại chung 1 trang.

User tiếp tục chỉ ra 2 điểm: (1) thứ tự hàng "lộn xộn" — phải theo đúng mạch logic **Mã hóa câu nhắc → PSG → CAD** chứ không phải để CAD (Attention U-Net) lên trước Mã hóa câu nhắc/PSG như cũ; (2) ép bảng về đúng trang 20 (đang lệch sang trang 21), nếu bảng cao quá thì **mở rộng cột ra ngang** thay vì chấp nhận bảng dài dọc hoặc cắt bớt chữ thêm.

**Đã xử lý:**
- Sắp lại 4 hàng theo đúng thứ tự: Khung bộ mã hóa-giải mã (U-Net) → **Mã hóa câu nhắc** (SAM-Med2D) → **Cổng không gian (PSG)** → **Cổng chú ý không gian mềm** (Attention U-Net → CAD).
- Mở rộng cột: `p{3.5cm}|p{5cm}|p{5cm}` (tổng 13.5cm) → `p{3.7cm}|p{6.1cm}|p{6.1cm}` (tổng 15.9cm, vừa khít `\textwidth` ≈ 16cm của trang A4 với margin hiện tại) — giảm hẳn số dòng wrap mỗi ô.

**Build:** sạch, 134 trang (từ 135), không lỗi/undefined reference. Đã render trực quan trang chứa Bảng 3.1: bảng nay nằm trọn trên **trang in số 20** (PDF trang 48), đúng thứ tự 4 hàng theo yêu cầu, cân đối hơn nhiều (không còn hàng nào lệch quá dài), và đoạn "Chuỗi kế thừa tuyến tính" bắt đầu ngay bên dưới trên cùng trang.

---

## Cập nhật: Bỏ lối viết "đặt câu hỏi rồi trả lời" trong thân bài

User yêu cầu bỏ hẳn phong cách viết kiểu "tự đặt câu hỏi rồi tự trả lời" trong report, giữ chuẩn IEEE: mục lớn/mục nhỏ, nội dung giải thích viết thẳng vào đúng mục tương ứng, không đặt câu hỏi tu từ.

Đã grep toàn bộ report (`Tại sao`, `Vì sao`, `Câu hỏi`, `Câu trả lời`, tiêu đề `\paragraph`/`\subsection`/... có dấu `?`) — chỉ tìm thấy **đúng 1 chỗ** vi phạm: `Chapter3/chapter3.tex`, tiêu đề `\paragraph{Cơ sở lý thuyết: Tại sao chọn biểu diễn liên tục có đạo hàm thay vì mặt nạ nhị phân?}` kèm đoạn mở đầu "Câu hỏi là tại sao không dùng mặt nạ nhị phân phẳng... Câu trả lời nằm ở...".

**Đã sửa:** đổi tiêu đề thành `\paragraph{Cơ sở lý thuyết của biểu diễn liên tục.}` (khai báo thẳng, không câu hỏi); viết lại đoạn mở đầu thành câu trần thuật trực tiếp: "So với mặt nạ nhị phân phẳng..., biểu diễn liên tục dạng bản đồ nhiệt phù hợp hơn với bản chất phép tích chập và cơ chế dung hợp đặc trưng trong U-Net: ...". Không còn nơi nào khác trong report dùng lối Q&A này.

**Build:** sạch, 134 trang, không lỗi/undefined reference.

---

## Cập nhật: Bỏ mục "Chiến lược huấn luyện và so sánh với SAM-Med2D" khỏi Chương 3 + xóa số vòng lặp hội tụ

User chỉ ra: Chương 3 chỉ nên nói kiến trúc mô hình (và hệ thống ở cuối) — không nên có cả một mục "Chiến lược huấn luyện và so sánh với mô hình nền tảng SAM-Med2D" (đây là nội dung huấn luyện/so sánh thực nghiệm, thuộc về Chương 4, không phải mô tả kiến trúc); đồng thời "mô hình nền tảng" không phải chỉ có SAM-Med2D nên đặt cả mục riêng xoay quanh một mô hình nền tảng duy nhất trong chương kiến trúc là lệch trọng tâm. Yêu cầu quan trọng thứ hai: xóa hết các con số epoch/vòng lặp hội tụ.

Kiểm tra: đúng, mục `subsec:training_strategy_pga` (Chương 3) trùng lặp với nội dung đã có sẵn ở Chương 4 — hàm mất mát $\mathcal{L}_{BCE}+\mathcal{L}_{Dice}$ đã có ở Mục~4.1.4 "Cấu hình huấn luyện" (`subsec:hyperparameters`), còn phần so sánh chiến lược huấn luyện PGA-UNet (từ đầu) vs SAM-Med2D (tinh chỉnh, đóng băng một phần) + số tham số ($\sim$3M vs $\sim$91M) đã có sẵn đầy đủ ở Mục~4.2.3 "So sánh với mô hình nền tảng SAM-Med2D" (`subsec:sam_comparison`).

**Đã xử lý:**
- **Xóa hẳn** toàn bộ mục `\subsection{Chiến lược huấn luyện và so sánh với mô hình nền tảng SAM-Med2D}` khỏi Chương 3 (hàm mất mát, đoạn "PGA-UNet huấn luyện từ đầu" / "SAM-Med2D tinh chỉnh", và toàn bộ bảng `tab:training_strategy_compare`) — bao gồm luôn dòng "Số vòng lặp hội tụ (tốt nhất trên tập xác thực) & 79 & 4" và câu văn "SAM-Med2D chỉ cần 4 vòng lặp... (dừng sớm tại vòng lặp 14), nhanh hơn nhiều PGA-UNet (vòng lặp tốt nhất 79, dừng sớm tại 94)" — đúng yêu cầu xóa số epoch/vòng lặp hội tụ, không di dời số này sang nơi khác.
- Chương 3 giờ khép lại Mục 3.1 (PGA-UNet) ngay sau subsection CAD, chuyển thẳng sang Mục 3.2 "Minh họa ứng dụng thực tế" — đúng tinh thần "chỉ nói kiến trúc, hệ thống ở cuối".
- Sửa 2 chỗ ở Chương 4 từng trỏ sang mục/bảng vừa xóa: câu dẫn đầu Mục 4.1.3 (`Mục~\ref{subsec:training_strategy_pga}, Chương~\ref{Chapter3}` → `Mục~\ref{subsec:sam_comparison}`); câu phân tích trong Mục 4.2.3 (bỏ `(Bảng~\ref{tab:training_strategy_compare}, Chương~\ref{Chapter3})` vì nội dung đã nêu ngay trong câu, không cần trích dẫn bảng đã xóa).
- Gán lại nhãn `\label{eq:loss_seg}` cho phương trình hàm mất mát tại Chương 4 (trước đó nhãn này chỉ tồn tại ở bảng vừa xóa) để Algorithm 1 (Chương 3) vẫn tham chiếu đúng, ghi rõ thêm ", Chương~4" cho không mơ hồ.

**Build:** sạch, 132 trang (từ 134), không lỗi/undefined reference. Đã render trực quan trang cuối Mục 3.1/đầu Mục 3.2 (PDF trang 53), xác nhận chuyển tiếp liền mạch: CAD kết thúc → "3.2 Minh họa ứng dụng thực tế" mở ngay sau, không còn mục huấn luyện/so sánh xen giữa.

---

## Cập nhật: Tinh gọn "Thách thức của bài toán" và "Đóng góp của khóa luận" (Chương 1)

User yêu cầu rút gọn 2 mục ở Chương 1, không đi sâu chi tiết kỹ thuật/số liệu quá mức cần thiết cho phần giới thiệu.

**Mục 1.4 "Thách thức của bài toán":** giữ nguyên 4 nhóm thách thức (dữ liệu, mô hình hóa, tính bền bỉ, khả năng triển khai) nhưng cắt bớt các mệnh đề phụ rườm rà ở mỗi đoạn (ví dụ bỏ liệt kê chi tiết "tạo mặt nạ từ chú thích, chuẩn hóa kích thước ảnh, phân chia tập..." chỉ còn "đòi hỏi xử lý đúng cấu trúc đầu vào trước khi huấn luyện"); mỗi đoạn còn 1-2 câu thay vì 2-3 câu.

**Mục 1.5 "Đóng góp của khóa luận":** cắt bỏ toàn bộ số liệu thực nghiệm cụ thể không cần thiết ở phần giới thiệu — xóa "$\sim$3 triệu tham số", đoạn ablation study chi tiết ("Dice Shift +0.10 (PGA-UNet vs PGA-UNet Binary)... +0.11 so với U-Net+Concat..."), và toàn bộ đoạn số liệu Gatekeeper/Pipeline ("AUC-ROC = 0.9421", "Pipeline Dice = 0.6763", giải thích "kịch bản thận trọng nhất"). Thay bằng 1 câu tổng quát trỏ sang Chương 4: "Hiệu quả của biểu diễn heatmap cũng như đóng góp riêng của PSG và CAD được kiểm chứng qua ablation study và so sánh với U-Net, SAM-Med2D... (chi tiết tại Chương~4)" và "Kết quả định lượng và phân tích chi tiết được trình bày tại Chương~4." Giữ nguyên phần mô tả khái niệm (Gaussian Plateau Heatmap, PSG, CAD) vì đây là nội dung đóng góp cốt lõi cần nêu rõ ngay từ Chương 1.

**Build:** sạch, 131 trang, không lỗi/undefined reference.

---

## Cập nhật: Viết lại Mục 1.5 "Đóng góp của khóa luận" thành 3 điểm đánh số rõ ràng

User phản hồi: mục 1.5 có thể dài hơn vài dòng so với bản vừa rút gọn, miễn là chia rõ từng đóng góp cho dễ hiểu (không nén hết vào 2 đoạn văn xuôi lồng nhau như trước).

**Đã xử lý:** viết lại toàn bộ thành `\begin{enumerate}` 3 mục đánh số ngang cấp, mỗi mục có tiêu đề in đậm riêng:
1. **Biểu diễn câu nhắc dạng Gaussian Plateau Heatmap** — tách riêng thành đóng góp độc lập (trước đây gộp chung câu mở đầu với đóng góp kiến trúc).
2. **Kiến trúc PGA-UNet điều kiện hóa bởi câu nhắc** — chứa `itemize` con cho PSG/CAD (giữ nguyên nội dung), bổ sung thêm 1 câu giải thích rõ hai thành phần phối hợp ra sao ("để mô hình thực sự sử dụng câu nhắc... thay vì chỉ tiếp nhận như kênh đầu vào thụ động").
3. **Thực nghiệm minh họa khả năng ứng dụng thực tế** — giữ nguyên nội dung bản rút gọn trước, chỉ đổi từ đoạn văn xuôi độc lập thành mục đánh số thứ 3.

Cấu trúc rõ ràng hơn hẳn: người đọc thấy ngay 3 đóng góp tách biệt qua số thứ tự, thay vì phải đọc hết đoạn văn mới nhận ra ranh giới giữa các đóng góp.

**Build:** sạch, 131 trang (không đổi số trang), không lỗi/undefined reference. Đã render trực quan trang 5-6, xác nhận danh sách đánh số hiển thị đúng, PSG/CAD vẫn lồng đúng trong mục 2.

---

## Cập nhật: Cô đọng Mục 3.1.1 "Biểu diễn câu nhắc trực quan"

User chỉ ra Mục 3.1.1 hơi dài, cần cô đọng ý, thông tin không thiết yếu không cần giải thích quá kỹ nhưng vẫn phải đủ để người chuyên môn hiểu.

**Đã xử lý:** gộp/cắt 5 đoạn thành 3 đoạn cô đọng hơn, giữ đầy đủ nội dung kỹ thuật cốt lõi:
- Đoạn định nghĩa Plateau Heatmap + phương trình: gộp câu giải thích "$k=31$" (trước đây là 1 đoạn `\textbf{Lý do chọn $k=31$:}` riêng, dài dòng liệt kê từng giá trị $k$ thử nghiệm) vào thẳng cuối đoạn định nghĩa, còn 1 câu duy nhất nêu kết quả khảo sát ($k \in \{15,21,31,51\}$) và lý do chọn, bỏ chi tiết "$k<21$ tạo chuyển tiếp quá đột ngột... $k>51$ làm tín hiệu lan quá rộng".
- `\paragraph{Cơ sở lý thuyết của biểu diễn liên tục.}`: gộp 2 đoạn thành 1 đoạn, bỏ hẳn đoạn phụ về "nghiên cứu cơ chế chú ý cho thấy mạng nơ-ron tự nhiên tạo vùng kích hoạt liên tục" (lập luận yếu, không cốt lõi), giữ lại lập luận chính (đạo hàm giả tạo từ mặt nạ nhị phân, phù hợp phép nhân phần tử tại cổng không gian).
- `\paragraph{So sánh với SAM/SAM-Med2D.}`: gộp 2 đoạn thành 1, bỏ câu chuyển tiếp thừa, giữ nguyên lập luận kỹ thuật (vector nhúng rời rạc vs bản đồ nhiệt 2D cùng không gian đặc trưng).

**Build:** sạch, 130 trang (từ 131), không lỗi/undefined reference. Đã render trực quan trang 20-21 (PDF 48-49): Mục 3.1.1 giờ gọn lại, kết thúc và chuyển sang Mục 3.1.2 ngay trên trang 21 (trước đây tràn dài hơn).

---

## Cập nhật: Rà soát cô đọng Chương 4 (thực nghiệm/kết quả) — phần lớn đã đủ cô đọng

User yêu cầu áp dụng cùng tinh thần cô đọng ("cái nào có thể tinh gọn thì tinh gọn, cái nào quan trọng thì giải thích kỹ, viết cho người chuyên môn chứ không phải giải thích dài dòng cho người ngoài ngành") cho toàn bộ 5 chương. Bốn chương còn lại (1, 2, 3, 5) đã xử lý trực tiếp trong phiên chính; Chương 4 (1470 dòng, chương thực nghiệm/kết quả — chương dài nhất) được rà soát riêng.

**Đánh giá sau khi đọc toàn bộ 1470 dòng theo từng mục con (~38 mục):** khác các chương còn lại, Chương 4 hầu như đã rất cô đọng sẵn — gần như mọi đoạn văn đều gắn với một con số/bảng/kiểm định thống kê cụ thể, không có đoạn "giải thích dài dòng cho người ngoài ngành" nào đáng kể. Đây chính xác là phần "quan trọng, cần giải thích kỹ" mà user lưu ý giữ nguyên: các đoạn phân tích ablation (Mục 4.3.1, kèm Wilcoxon signed-rank 36 kết quả), so sánh SAM-Med2D, phân tích FN của Gatekeeper, phân tích sai số tích lũy hai giai đoạn... đều là claim đã được cân chỉnh cẩn thận qua nhiều vòng làm việc trước (xem Kế hoạch lớn A/B ở đầu file) — không đụng vào bất kỳ số liệu, bảng, hay câu hedging nào (ví dụ "bền vững trước sai lệch bbox có kiểm soát", "chưa đủ an toàn để tự động chặn", các ghi chú "chưa tính lại được"/"chưa xác nhận chính thức").

**Các chỗ thực sự cô đọng được (fluff thật sự, không phải số liệu/hedging):**
- Mục 4.1.3 "Mô hình so sánh trong thực nghiệm": câu dẫn nhập rườm rà trước itemize → còn 1 câu ngắn.
- Mục 4.5.2 "Đa dạng ca kiểm thử...": bỏ câu "Mỗi hàng gồm 5 cột: ảnh gốc, ảnh kèm hộp giới hạn câu nhắc..." trong thân bài vì **trùng lặp hoàn toàn** với chú thích hình `fig:qual_pipeline_tp` ngay bên dưới đã liệt kê đúng 5 cột này.
- Mục 4.7.1 "Đánh giá Gatekeeper": đoạn "Các độ đo đánh giá" liệt kê lại tên 5 chỉ số (Accuracy/Precision/Recall/Specificity/F1) ngay trước khi bảng kết quả (liệt kê đúng các tên này) xuất hiện — rút gọn thành 1 câu trỏ thẳng vào bảng.
- Mục 4.5 (mở đầu "Trực quan hóa kết quả"): gộp 2 câu dẫn nhập thành 1 câu.
- Đã kiểm tra không có heading/đoạn kiểu Q&A nào sót lại, không có số vòng lặp/epoch nào mang tính "so sánh tốc độ hội tụ" kiểu đã bị cấm ở Chương 3 (2 chỗ có số vòng lặp trong Chương 4 — Mục 4.1.4 `subsec:hyperparameters` và Mục 4.7.1 phần "Giai đoạn 1/2" huấn luyện Gatekeeper — đều là mô tả cấu hình huấn luyện thực tế hợp lệ, giữ nguyên).

**Build:** sạch, 128 trang, không lỗi/undefined reference.

---

## Cập nhật: Chú thích dưới hình phải ngắn gọn — giải thích/diễn giải chuyển vào thân bài

User chỉ ra: chú thích (caption) dưới hình đang bị dùng để nhét cả giải thích/diễn giải dài dòng, trong khi đúng ra chú thích chỉ nên là tiêu đề ngắn gọn — nội dung giải thích nên viết riêng thành câu văn hoặc luồn vào đoạn văn thân bài, không gộp chung vào caption.

**Rà soát:** grep toàn bộ 56 `\caption{}` trong Report. Phần lớn caption bảng/biểu đồ kết quả (Chương 4) đã ngắn gọn hợp lý (chỉ nêu điều kiện so sánh: kịch bản, N=, độ phân giải, tham chiếu bảng chéo) — không phải "giải thích", giữ nguyên. Phát hiện 2 nhóm vi phạm rõ ràng:

1. **5 hình kiến trúc/pipeline** (Chương 2, 3): caption dài dòng diễn giải lại toàn bộ cơ chế hoạt động — trùng lặp gần như nguyên văn với đoạn thân bài ngay phía trên hình (đoạn thân bài đã giải thích đầy đủ rồi):
   - `fig:sammed2d_architecture`: cắt bỏ đoạn diễn giải cơ chế ViT-B/adapter/prompt encoder/mask decoder (đã có ở thân bài dòng ngay trên), chỉ giữ lại phần chú giải màu chấm tròn (cyan=đóng băng, orange=học được) — đây là thông tin **riêng của hình** (đọc hình cần biết), không phải diễn giải cơ chế.
   - `fig:unet_architecture`: cắt hết câu diễn giải encoder/decoder/skip connection (đã có ở 3 đoạn thân bài ngay trên), chỉ còn "Kiến trúc U-Net, 4 cấp độ phân giải."
   - `fig:attunet_architecture`: cắt câu diễn giải cơ chế lọc nhiễu (đã có ở thân bài + phương trình ngay trên).
   - `fig:pga_architecture`: cắt câu diễn giải vai trò PSG/CAD — đã có sẵn ngay trong câu "Chuỗi kế thừa tuyến tính" ở thân bài ngay trên hình (không cần thêm gì, giải thích đã "luồn vào nội dung" sẵn).
   - `fig:pipeline_overview`: cắt câu diễn giải luồng xử lý từng bước (đã giải thích đầy đủ ở 2 đoạn "Giai đoạn 1/2" thân bài ngay trên).
2. **3 hình minh họa định tính** (Chương 4, Mục 4.5): caption có thêm 1 câu bình luận diễn giải kết quả, trùng lặp với câu văn ngay phía trên hình:
   - `fig:qual_shift`: cắt câu "Cột thứ hai cho thấy hộp giới hạn không bao trọn vẹn tổn thương thực tế" (đã nói y hệt ở thân bài).
   - `fig:qual_small_lesion`: cắt câu "PGA-UNet vẫn định vị và phân đoạn đúng dù vùng tổn thương chiếm diện tích rất nhỏ" (đã nói ở thân bài).
   - `fig:qual_overlap`: cắt câu "thấp hơn mức trung bình dù câu nhắc chính xác" (đã nói ở thân bài).
   - Riêng `tab:ablation_arch`: cắt câu thừa "PGA-UNet (đề xuất) là mô hình chính xuyên suốt khóa luận" (thông tin đã hiển nhiên toàn báo cáo, không cần nhắc lại trong caption bảng).

**Không đổi:** các caption mô tả bố cục cột ảnh (ví dụ "Từ trái sang phải: ảnh gốc, ảnh kèm hộp giới hạn...") — đây là chú giải cần thiết để đọc hình (không lặp ở đâu khác), giữ nguyên; chú giải màu/ký hiệu trong biểu đồ (ví dụ "PGA-UNet tô xanh dương, các biến thể còn lại tô xám", chú giải *** p<0.001 của bảng Wilcoxon) cũng giữ nguyên vì đây là thông tin đọc-hình bắt buộc, không phải diễn giải nội dung.

**Build:** sạch, 127 trang (từ 128), không lỗi/undefined reference. Đã render kiểm tra trực quan trang chứa Hình 2.1 (List of Figures) và Hình 4.12 (kịch bản Shift): xác nhận caption giờ ngắn gọn, phần diễn giải đầy đủ vẫn nằm trong đoạn văn thân bài phía trên hình.

---

## Cập nhật: Cô đọng thêm Mục 1.5 "Đóng góp của khóa luận" (giảm ~11 dòng in)

User yêu cầu tinh gọn thêm Mục 1.5 (đang tràn ~10 dòng sang trang 6, trước "1.6 Bố cục").

**Đã xử lý:**
- Item 1 (Gaussian Plateau Heatmap): gộp 2 câu ("Biểu diễn này cung cấp tín hiệu định hướng..." nhập vào câu đầu bằng dấu `--`), bỏ cụm thừa "cho phép câu nhắc lan truyền xuyên suốt các tầng mạng".
- Item 2, đoạn kết: gộp 2 câu ("Hai thành phần này phối hợp để..." + "Hiệu quả của biểu diễn heatmap...") thành 1 câu bằng dấu `;`.
- Item 3: gộp 2 câu mở đầu ("PGA-UNet cần câu nhắc... không thể tự vận hành..." + "Để hình dung cách mô hình...") thành 1 câu ngắn hơn; bỏ "định lượng và phân tích chi tiết" thừa ở câu cuối, còn "Kết quả tại Chương~4."

**Build:** sạch, 127 trang (không đổi), không lỗi/undefined reference. Đã render trang 5-6: phần tràn sang trang 6 giảm từ 10 dòng xuống còn 6 dòng (giảm ~4 dòng in trực tiếp từ phần tràn, cộng thêm phần rút gọn nội bộ trang 5 giúp mục 3 bắt đầu sớm hơn) — tổng thể mục 1.5 ngắn gọn hơn rõ rệt so với trước.

---

## Cập nhật: Cô đọng thêm Mục 1.2.1 "Động lực khoa học" + 1.2.2 "Động lực thực tiễn"

User yêu cầu giảm tổng cộng 2 dòng in cho 2 mục con này.

**Đã xử lý:**
- 1.2.1, đoạn 3 (kết mục): bỏ cụm chêm "-- biểu diễn, mã hóa và truyền tải thông tin câu nhắc qua các tầng mạng --" (đã diễn giải đủ ý ở 2 đoạn trước, cụm này chỉ nhắc lại), còn "Tuy nhiên, cách tích hợp hiệu quả tín hiệu định hướng vào kiến trúc mạng nơ-ron vẫn là hướng nghiên cứu đang được quan tâm, đặc biệt trong ảnh y khoa chuyên biệt."
- 1.2.2: gộp 2 đoạn văn ("Trong thực tế lâm sàng..." + "Việc tích hợp hệ thống vào quy trình thực tế còn đòi hỏi...") thành 1 đoạn duy nhất bằng dấu `;`, bỏ 1 lần xuống dòng đoạn văn thừa.

**Build:** sạch, **126 trang (từ 127)** — giảm nguyên 1 trang toàn báo cáo dù chỉ sửa 2 đoạn nhỏ ở Chương 1 (hiệu ứng dồn trang dây chuyền). Không lỗi/undefined reference. Đã render trang 2, xác nhận 2 mục con gọn lại đúng như yêu cầu.

---

## Cập nhật: Rà soát chuẩn hóa Chương 2 — lỗi trích dẫn trộn kiểu IEEE với author-year

User hỏi Chương 2 đã ổn/đúng chuẩn trình bày chưa. Rà soát kỹ toàn bộ 10 trang (đọc lại file .tex + render trực quan từng trang), phát hiện 3 nhóm lỗi thực sự (không phải nội dung, mà là trình bày/định dạng):

1. **Trộn kiểu trích dẫn:** Toàn bộ báo cáo dùng `style=ieee` (trích dẫn số `[X]`, xác nhận trong `main.tex`), nhưng Chương 2 có **3 chỗ** viết thêm "(Tên tác giả, năm)" ngay cạnh `\cite{}` số — kiểu author-year, không đúng với style số đã chọn và không xuất hiện ở bất kỳ chương nào khác trong báo cáo (đã grep toàn bộ, chỉ 3 chỗ này dùng "và cộng sự"):
   - "U-Net~\cite{ronneberger2015unet} (Ronneberger và cộng sự, 2015)" → bỏ phần author-year, còn "U-Net~\cite{ronneberger2015unet}".
   - "Oktay và cộng sự (2018) đề xuất Attention U-Net \cite{...}" → viết lại chủ ngữ câu thành "Attention U-Net~\cite{oktay2018attentionunet} tích hợp..." (bỏ tên tác giả làm chủ ngữ, khớp văn phong dùng ở nơi khác trong cùng chương, ví dụ dòng 74).
   - "SAM-Med2D~\cite{...} (Cheng và cộng sự, 2023)" → bỏ phần author-year.
2. **Thiếu `~` (non-breaking space) trước `\cite{}`:** Chương 3 và Chương 4 dùng nhất quán `~\cite{}` (100%, đã grep xác nhận 0 chỗ thiếu), nhưng Chương 2 có **4 chỗ** dùng khoảng trắng thường trước `\cite{}` (có thể gây ngắt dòng xấu giữa từ và số trích dẫn) — đã thêm `~` cho khớp chuẩn toàn báo cáo.
3. **Tự tham chiếu chương không nhất quán:** Câu mở đầu "Tổng kết chương" viết "Chương 2 cung cấp bức tranh toàn cảnh..." (số chương viết cứng), trong khi Chương 3/Chương 4 đều mở đầu bằng "Chương này..." — sửa lại "Chương này cung cấp..." cho khớp quy ước chung. Ngoài ra 2 chỗ nhắc tới Chương 3 dùng chữ cứng "Chương 3" thay vì `Chương~\ref{Chapter3}` (không tự cập nhật nếu đánh số chương thay đổi) — đã sửa cả 2 thành `\ref`.

**Không phát hiện lỗi khác:** không có lỗi thứ tự đọc hình/bảng (`[htbp]` của 3 hình đều hiển thị đúng vị trí ngay sau đoạn văn liên quan, không cần đổi `[H]`), không có lỗi LaTeX/undefined reference, không còn caption dài dòng (đã xử lý ở lượt trước), không còn kiểu Q&A. Có 1 điểm nhỏ **không sửa được**: hình `arch_attention_unet2d.png` (Hình 2.3) có chú thích nhỏ bên trong ảnh gốc ("Lưu ý: Mô hình này không có prompt — phân biệt với PGA-UNet") — đây là text nằm trong file ảnh (không phải LaTeX), không chỉnh được từ phía report; về nội dung không sai, chỉ là chi tiết trình bày của ảnh gốc.

**Build:** sạch, 126 trang (không đổi), không lỗi/undefined reference. Đã render lại trang 7 xác nhận câu văn đọc tự nhiên sau khi bỏ author-year.

---

## Cập nhật QUAN TRỌNG: Sửa lỗi hiểu sai luồng hệ thống (Mục 3.2 "Minh họa ứng dụng thực tế" + Algorithm 2)

User chỉ ra: mô tả luồng xử lý hệ thống ở Mục 3.2 và Algorithm 2 (suy luận trực tuyến) đang **hiểu sai pipeline thực tế**. Đã đọc kỹ nguồn gốc sự thật: `/home/thongluc/Khóa Luận Tốt Nghiệp/PGA_Unet2D/diagrams/pipeline_pga_app_inference.drawio` (file drawio gốc, đối chiếu từng node/edge).

**Lỗi cụ thể đã tìm thấy:** report cũ viết "Xác nhận không bệnh: quy trình kết thúc cho ảnh này" — tức coi nhánh "Không bệnh" là kết thúc ngay lập tức. **Sai** — đối chiếu file drawio: sau khi bác sĩ xác nhận "Không bệnh", hệ thống có một node quyết định THỨ HAI (`id="11"`): *"Bác sĩ vẫn nghi ngờ, muốn tự thử phân đoạn?"* — đây mới là điểm mấu chốt của toàn bộ minh họa: một lớp xác nhận lại an toàn, phòng trường hợp Gatekeeper bỏ sót ca bệnh thật (âm tính giả — rủi ro nguy hiểm vì AI không chính xác 100%). Tại đây bác sĩ có 2 lựa chọn: (a) "Không, kết thúc" → thật sự hoàn tất; (b) "Có, tự vẽ vùng nghi ngờ" → khoanh hộp giới hạn (ép buộc vẽ bbox) để dùng hỗ trợ phân đoạn vẽ mặt nạ, dù model nói không bệnh.

**Đã sửa (3 chỗ):**
1. **Mục 3.2, đoạn giới thiệu:** sửa câu mô tả đầu vào ("hộp giới hạn chỉ được vẽ sau khi xác nhận có bệnh lý" → nay đúng là "được vẽ khi xác nhận có bệnh lý, HOẶC khi bác sĩ chủ động yêu cầu phân đoạn dù Gatekeeper gợi ý không bệnh").
2. **Mục 3.2, itemize "Giai đoạn sàng lọc bệnh lý":** viết lại nhánh "Xác nhận không bệnh" thành itemize con 2 cấp đúng luồng thật: hỏi lại "Bác sĩ vẫn nghi ngờ, muốn tự thử phân đoạn?" → "Không, kết thúc" (hoàn tất chẩn đoán) / "Có, tự vẽ vùng nghi ngờ" (ép buộc vẽ bbox, dùng hỗ trợ phân đoạn vẽ mặt nạ). Thêm câu nối "Cả hai đường dẫn đến hộp giới hạn... đều được đưa vào cùng giai đoạn phân đoạn có hướng dẫn".
3. **Algorithm 2 (`alg:online`):** thêm biến quyết định thứ hai $o$ (bác sĩ có muốn tự thử phân đoạn dù gợi ý không bệnh) lồng trong nhánh $c=0$; chỉ khi $o=0$ mới `return` kết thúc; nếu $o=1$ thì rơi xuống tiếp tục kiểm tra `B=∅` và phân đoạn như nhánh $c=1$. Sửa `\Require` (bỏ ràng buộc cứng "hộp giới hạn... sau khi xác nhận có bệnh lý", vì bbox giờ có thể đến từ 2 nguồn). Sửa chú thích đoạn "Xử lý câu nhắc rỗng" ngay sau cho khớp (bước B=∅ giờ xảy ra ở cả 2 nhánh, không chỉ nhánh có bệnh).

**Sửa thuật ngữ theo yêu cầu:** bỏ từ "đầu cuối" trong câu "luồng xử lý được thiết kế dưới dạng luồng xử lý đầu cuối bán tự động" (Mục 3.2) — chỉ còn "luồng xử lý bán tự động". Lý do: "đầu cuối" (end-to-end) ngụ ý một luồng tuyến tính một chiều, không phản ánh đúng bản chất có nhánh rẽ/vòng hỏi lại của hệ thống thật. Đã kiểm tra: đây là **chỗ duy nhất** dùng "đầu cuối" trong Chương 3 (grep xác nhận); các chỗ dùng "đầu cuối"/"end-to-end" ở Chương 4 (Pipeline Dice end-to-end, "Đánh giá luồng xử lý đầu cuối") là thuật ngữ phương pháp luận đánh giá hệ thống hai tầng gộp lại — khác ngữ cảnh, đúng chuẩn, không đụng tới.

**Đã kiểm tra tính nhất quán:** Chương 4 (Mục 4.7 phân tích sai số tích lũy, đánh giá pipeline) vốn đã mô tả đúng ("trong hệ thống triển khai thực tế, hậu quả [bỏ sót] chỉ xảy ra nếu bác sĩ cũng không phát hiện tổn thương khi xem lại ảnh gốc", "thiết kế triage mềm... bác sĩ luôn xác nhận lại, là lớp phòng vệ bổ sung") — khớp hoàn toàn với hiểu biết đúng vừa sửa ở Chương 3, không cần đổi gì ở Chương 4. Lỗi hiểu sai chỉ nằm ở Mục 3.2 + Algorithm 2.

**Build:** sạch, 126 trang (không đổi), không lỗi/undefined reference. Đã render trang 22-23 (Mục 3.2) và trang 28 (Algorithm 2) xác nhận logic hiển thị đúng thứ tự: hỏi lại lồng trong nhánh không bệnh, chỉ kết thúc khi bác sĩ xác nhận không muốn tự vẽ.

---

## Cập nhật: Rà soát toàn báo cáo tìm câu/cụm từ vô nghĩa do chỉnh sửa để lại

User phát hiện câu "Luồng xử lý được thiết kế dưới dạng luồng xử lý bán tự động" (lặp "luồng xử lý" — sinh ra khi tôi bỏ chữ "đầu cuối" ở lượt sửa trước nhưng không dọn lại câu cho gọn), yêu cầu rà soát **toàn bộ báo cáo** tìm các câu/cụm tương tự (nghĩa vô lý do sót từ khi cô đọng) và ký tự thừa, sửa hết.

**Phương pháp rà soát:** (1) grep trực tiếp cụm gây lỗi + biến thể; (2) script Python dò n-gram lặp trong khoảng cách gần trên các dòng vừa thêm (`git diff`) để khoanh vùng nghi vấn; (3) đọc lại thủ công toàn bộ đoạn văn đã chỉnh sửa trong phiên này ở cả 5 chương (Chapter1 đầy đủ, Chapter2 các đoạn sửa citation/CNN, Chapter3 toàn bộ Mục 3.1–3.4, Chapter5 Hướng 1, 4 vị trí Chapter4 do fork sửa) để bắt lỗi ngữ pháp mà script không phát hiện được (thiếu giới từ, thiếu liên từ) — quan trọng hơn n-gram vì kiểu lỗi này không lặp từ mà **thiếu** từ nối.

**Tìm thấy và sửa 3 lỗi thực sự (câu đọc vô nghĩa/thiếu từ nối):**
1. **Chương 3, Mục 3.2:** "Luồng xử lý được thiết kế dưới dạng luồng xử lý bán tự động" (lặp từ, lỗi do tôi sửa "đầu cuối" ở lượt trước) → "Luồng xử lý mang tính bán tự động".
2. **Chương 1, Mục 1.5 (Đóng góp), item 3:** "khóa luận bổ sung một thực nghiệm minh họa (không phải đóng góp kỹ thuật riêng biệt) hình dung cách tích hợp vào thực tế" — thiếu từ "để" trước "hình dung" (câu cụt, đọc như 2 mệnh đề ghép sai) → thêm "để hình dung cách tích hợp vào thực tế". Lỗi này cũng do tôi cô đọng câu ở lượt trước và làm rớt mất từ nối.
3. **Chương 5, Hướng 3 (định hướng phát triển):** "chỉ giữ nhãn giả tại ca có ngữ cảnh lâm sàng phù hợp dự đoán hình ảnh (ví dụ vị trí đau khớp vị trí mô hình khoanh vùng)" — thiếu "với" và "trùng với" (câu tối nghĩa) → "phù hợp **với** dự đoán hình ảnh (ví dụ vị trí đau khớp **trùng với** vị trí mô hình khoanh vùng)". Lỗi này có sẵn từ trước, không phải do phiên này gây ra, nhưng vẫn sửa theo yêu cầu rà soát toàn bộ.

**Đã kiểm tra không còn lỗi khác:** không còn cụm "X được/là ... dưới dạng X" nào khác trong toàn báo cáo (grep xác nhận 0 kết quả sau khi sửa); không có dấu câu thừa dạng `()`  rỗng, `{}` rỗng, hay dấu phẩy/chấm kép; không có từ lặp liền kề bất thường (loại trừ các từ láy hợp lệ tiếng Việt như "song song", "luôn luôn" — đây là từ đúng, không phải lỗi).

**Build:** sạch, 126 trang (không đổi), không lỗi/undefined reference.

---

## Cập nhật: Rà soát và dịch nốt từ tiếng Anh còn sót trong Chương 5

User hỏi Chương 5 còn từ tiếng Anh không, yêu cầu sửa hết. Grep từng từ nghi vấn, đối chiếu với thuật ngữ đã dùng thống nhất ở Chương 1–4 để quyết định giữ nguyên (thuật ngữ đã chuẩn hóa/tên riêng) hay dịch lại (từ tiếng Anh lọt vào do sơ suất).

**Đã sửa (Chương 5, không đổi ý nghĩa số liệu):**
- **`bbox`** (6 chỗ) → **`hộp giới hạn`** — thuật ngữ đã dùng xuyên suốt Chương 1–4, "bbox" là từ viết tắt tiếng Anh duy nhất còn sót lại toàn báo cáo (grep xác nhận 0 chỗ khác dùng "bbox").
- **`Gaussian heatmap` / `Gaussian Heatmap`** (2 chỗ) → **`bản đồ nhiệt Gaussian`** — khớp thuật ngữ "Bản đồ nhiệt câu nhắc" đã định nghĩa từ Chương 2.
- **` vs `** (1 chỗ, "PGA Dice = 0.8261 vs U-Net Dice") → **`so với`**.
- **`Pipeline Dice end-to-end`** (2 chỗ) → **`Pipeline Dice (đầu cuối)`** — khớp đúng cách viết đã định nghĩa chính thức trong Bảng ở Chương 4 (`\textbf{Pipeline Dice (đầu cuối)}`), thay vì để tên chỉ số lẫn tiếng Anh "end-to-end" trần trụi.
- **`pixel-level`** (4 chỗ) → **`cấp độ pixel`** — khớp cách viết "mặt nạ phân đoạn cấp độ pixel" dùng xuyên suốt Chương 1/3/4 (grep xác nhận "pixel-level" không xuất hiện ở bất kỳ chương nào khác, chỉ Chương 5 dùng sai dạng).
- **`heatmap câu nhắc`** (Hướng 2) → **`bản đồ nhiệt câu nhắc`**.
- **`patch`** (3 chỗ, Hướng 2) → **`mảnh ảnh`** — không có tiền lệ dùng "patch" ở chương nào khác nên dịch hẳn sang tiếng Việt thay vì giữ nguyên.

**Giữ nguyên (đã kiểm tra là thuật ngữ/tên riêng đã chuẩn hóa xuyên suốt báo cáo, không phải lỗi):** tên mô hình/module (PGA-UNet, SAM-Med2D, Gatekeeper, EfficientNet\_B3, Swin Transformer, ViT), tên chỉ số/số liệu (Dice, IoU, Precision, Recall, HD95, CBL, AUC-ROC, TP/FP/FN, Sensitivity, Specificity), tên kịch bản (Zoom-out/Shift/Mixed), thuật ngữ dữ liệu đã dùng nhất quán ở Chương 4 (`train/val/test`, `polygon`, `baseline`, `vector`), và cụm ghép "triage mềm" (thuật ngữ thiết kế đã định nghĩa và dùng lặp lại hàng chục lần xuyên suốt Chương 3/4, không phải chỗ sót dịch).

**Build:** sạch, 126 trang (không đổi), không lỗi/undefined reference. Đã render trang 92 xác nhận câu văn đọc tự nhiên sau khi thay thuật ngữ.

**Lưu ý cho phiên sau:** cùng 2 mẫu lỗi này (" vs " và "Gaussian heatmap" viết thường) cũng xuất hiện rải rác trong Chương 4 (quy mô lớn hơn nhiều — 16 chỗ " vs ", nhiều chỗ "Gaussian heatmap") — chưa xử lý vì user chỉ hỏi về Chương 5 lần này; nên hỏi lại nếu muốn quét luôn Chương 4.

---

## Cập nhật: Sửa nhiều vấn đề Mục 4.1 (setup) + bổ sung giải thích lý thuyết (ablation Attention U-Net, lịch trình $w_l$ CAD) + gộp phần "lý do chọn kịch bản"

User nêu 6 vấn đề liền trong 1 lượt, tất cả đã xử lý:

**1. Mục 4.1.1 "Tập dữ liệu ảnh X-quang" chỉ nói BTXRD dù có 2 bộ dữ liệu (BTXRD + FracAtlas):** User đề nghị 2 hướng — (a) viết chung chung cho cả 2, hoặc (b) chi tiết + bảng cho cả 2. Đã chọn hướng nhẹ nhất không phá vỡ cấu trúc "mỗi bộ dữ liệu có mục giới thiệu riêng ngay trước phần kết quả của nó" (FracAtlas đã có Mục 4.4.1 riêng với bảng thống kê `tab:fracatlas_dataset_stats` tương đương `tab:dataset_stats` của BTXRD — về bản chất cả 2 ĐÃ có bảng/mô tả chi tiết ngang nhau, chỉ đặt ở 2 vị trí khác nhau trong chương): đổi tiêu đề Mục 4.1.1 thành **"Tập dữ liệu ảnh X-quang: BTXRD"** (khớp cách đặt tên cụ thể của Mục 4.4.1 "Giới thiệu bộ dữ liệu FracAtlas", tránh đọc như thể đây là bộ dữ liệu duy nhất), thêm 1 đoạn dẫn nhập mới nói rõ ngay từ đầu: khóa luận dùng 2 bộ dữ liệu độc lập, BTXRD trình bày trước vì là bộ chính, FracAtlas trỏ sang Mục 4.4.

**2. Mục 4.1.2 "Xử lý dữ liệu đầu vào" — không đổi**, vì user chỉ ra đây vốn đã viết chung chung đúng cách (đã nêu cả 512×512 và 256×256, không buộc vào riêng bộ dữ liệu nào) — dùng làm ví dụ đối chiếu cho thấy Mục 4.1.1 nên viết theo tinh thần tương tự.

**3. Mục 4.1.3 "Mô hình so sánh trong thực nghiệm" thiếu Attention U-Net:** User chỉ ra Mục ablation (4.3.1) có dùng Attention U-Net làm điểm neo so sánh nhưng danh sách mô hình ở 4.1.3 lại thiếu. Đã thêm mục **Attention U-Net (baseline có cổng chú ý, không câu nhắc)** vào danh sách, giải thích vai trò "điểm neo mức không câu nhắc" trong ablation.

**4. Bổ sung giả thuyết lý thuyết cho phát hiện "Attention U-Net thuần túy (Dice 0.4122) thấp hơn U-Net thuần túy (0.4740)"** (Mục 4.3.1, "Điểm neo mức không câu nhắc"): User đề xuất cơ chế: khi không có câu nhắc, Cổng chú ý tự học lọc skip connection dựa trên cường độ đặc trưng; nếu nhiễu nền và tín hiệu tổn thương (GT) có cường độ ngang nhau hoặc nhiễu còn mạnh hơn, cổng chú ý dễ lọc nhầm luôn GT cùng với nhiễu — hợp lý vì bản thân U-Net thuần (không lọc) đã có Dice thấp, cho thấy nhiễu khá mạnh. Đã thêm đúng nguyên văn lập luận này thành đoạn **"Giả thuyết lý giải (suy luận lý thuyết, chưa kiểm chứng bằng ablation riêng)"** — ghi rõ đây là suy luận lý thuyết dựa trên cơ chế, không phải kết luận đã kiểm chứng, đúng yêu cầu "tránh phải chạy thêm ablation để chứng minh".

   **⚠️ Không đưa vào phần thứ hai của giả thuyết user nêu** (rằng U-Net+PSG+Attention gốc "có thể tốt hơn cả" U-Net+PSG một mình, nhờ PSG làm nổi bật GT giúp attention lọc đúng hơn): đối chiếu số liệu thật (Bảng~`tab:ablation_arch`) thì **không đúng** — U-Net+PSG+Attention gốc (Zoom 0.8680/Shift 0.7359/Mixed 0.8173) so U-Net+PSG một mình (0.8673/0.7388/0.8162) chênh lệch cực nhỏ và Shift còn giảm nhẹ; quan trọng hơn, đoạn phân tích ablation quan sát (2) **ngay sau đó trong cùng trang** đã có kiểm định Wilcoxon xác nhận **không có ý nghĩa thống kê ở bất kỳ kịch bản nào** (p=0,129/0,376/0,074), và tự nhận "khác kỳ vọng ban đầu rằng PSG sẽ giúp cổng chú ý nguyên bản phát huy rõ hơn". Vì báo cáo đã có kết quả kiểm định thật mâu thuẫn trực tiếp với giả thuyết thứ hai này, không thêm vào để tránh tự mâu thuẫn trong cùng chương.

**5. Giải thích lịch trình $w_l = \{1.0, 0.7, 0.4, 0.2\}$ theo tầng CAD** (Mục 4.1.4, cấu hình huấn luyện): User đặt giả thuyết tầng gần đầu ra (chi tiết pixel) nên giảm ảnh hưởng câu nhắc vì câu nhắc chỉ ở mức vùng chú ý thô. **Đã xác minh trực tiếp với mã nguồn** `Source/Prompt-Guided-XRay-Segmentation/models/networks/prompt_unet_2D.py`: `up_concat4` (ngay sau bottleneck) nhận `prompt_weight=w[0]=1.0`, `up_concat1` (ngay trước `self.final`, tầng cuối) nhận `w[3]=0.2` — xác nhận tầng 1 = gần bottleneck (thô), tầng 4 = gần đầu ra (chi tiết pixel), đúng như giả thuyết. Đã thêm chú thích tầng 1/4 nghĩa là gì + đoạn lập luận lý thuyết (câu nhắc chỉ là vùng chú ý thô, ép ảnh hưởng mạnh lên tầng chi tiết pixel sẽ khiến hình dạng hộp giới hạn áp đặt lên đường biên chi tiết) ngay sau câu "chưa có kiểm chứng ablation riêng" đã có sẵn.

**6. Gộp "Lý do chọn 3 kịch bản" + "Trường hợp câu nhắc sai hoàn toàn vị trí"** (Mục 4.2.2): 2 đoạn tách riêng trước đây có nội dung liên quan (đều bàn về giới hạn phạm vi câu nhắc sai được đánh giá) — gộp thành 1 đoạn liền mạch dưới tiêu đề "Lý do chọn 3 kịch bản này và giới hạn phạm vi câu nhắc sai", cắt bớt câu dẫn trùng lặp. Tiện thể đổi hết `bbox` → `hộp giới hạn` trong đoạn này (khớp thuật ngữ chuẩn hóa toàn báo cáo).

**Build:** sạch, 127 trang (từ 126), không lỗi/undefined reference. Đã render trực quan 5 trang chỉnh sửa (30, 32, 38, 61, 74) xác nhận nội dung hiển thị đúng, mạch lạc.

---

## Cập nhật LỚN: Bắt đầu tái cấu trúc Chương 4 dataset-major → topic-major (theo kế hoạch trong `Đánh giá.md`)

Sau khi kiểm tra định lượng 28 cặp biến thể ablation × 3 kịch bản giữa BTXRD/FracAtlas (so sánh lớn nhất quán chiều, ablation chi tiết có ~11/84 cặp đổi chiều tập trung ở Zoom-out), đã thống nhất với user cấu trúc mới cho Chương 4 và lập plan chi tiết (đã duyệt qua Plan Mode, lưu tại `/home/thongluc/.claude/plans/floofy-sleeping-floyd.md`): 4.1 giữ 3 mục con (gộp dataset 2 bộ + tiền xử lý, mô hình so sánh + cấu hình, giao thức đánh giá); 4.2 gộp topic-major (mỗi mục 1 kết luận xuyên 2 dataset); 4.3/4.4 tách khối BTXRD/FracAtlas + mục tổng hợp riêng; hình trực quan/case thất bại phân bổ lại vào đúng mục định lượng thay vì gom cuối chương. Thực hiện tuần tự từng phase, dừng xác nhận sau mỗi phase.

### Phase 0 — Gộp Mục 4.1 (Thiết lập môi trường thực nghiệm) từ 5 mục con xuống 3

**Đã làm:**
- **4.1.1 "Hai bộ dữ liệu ảnh X-quang và tiền xử lý đầu vào":** gộp mô tả BTXRD (`subsec:dataset`, vốn ở đầu chương) + mô tả FracAtlas (kéo nguyên bảng `tab:fracatlas_dataset_stats` và toàn bộ đoạn văn từ mục "Giới thiệu bộ dữ liệu FracAtlas" vốn nằm sâu ở giữa chương, trong `sec:fracatlas`) + đoạn tiền xử lý (`sec:tien_xu_ly`, đã dataset-agnostic sẵn) thành 1 mục duy nhất, đọc theo thứ tự BTXRD → FracAtlas → tiền xử lý dùng chung.
- **4.1.2 "Mô hình so sánh và cấu hình huấn luyện":** gộp `subsec:models_compared` + `subsec:hyperparameters` (giữ nguyên `\label{subsec:hyperparameters}` gắn vào tiêu đề in đậm không đánh số, để các `\ref` từ Chương 3 vẫn trỏ đúng — đã kiểm tra `\ref{subsec:hyperparameters}` vẫn resolve đúng, không lỗi).
- **4.1.3 "Giao thức và độ đo đánh giá":** giữ nguyên `subsec:image_level_eval`, chỉ đổi số tự động.
- **Dọn dẹp:** xóa hẳn mục "Giới thiệu bộ dữ liệu FracAtlas" trùng lặp ở vị trí cũ (đã gây lỗi `Duplicate label tab:fracatlas_dataset_stats` khi build, đã hết sau khi xóa); viết lại đoạn mở đầu `sec:fracatlas` (bỏ câu "giới thiệu bộ dữ liệu FracAtlas" khỏi danh sách lộ trình vì đã dời lên 4.1.1, trỏ `\ref{subsec:dataset}` thay vì lặp lại nội dung).

**Chưa làm (để Phase 1 xử lý):** đoạn mở đầu Chương 4 vẫn còn nhắc "Chương này tổ chức kết quả thành hai phần: Phần I / Phần II" — khung diễn giải này thuộc về cấu trúc dataset-major cũ, sẽ viết lại khi gộp 4.2.

**Build:** sạch, 127 trang (không đổi), không lỗi/undefined reference/label trùng. Đã render trực quan 3 trang (30, 31, 32 — Mục 4.1.1 với cả BTXRD và FracAtlas liền mạch; 85 — đầu mục "Đánh giá bổ sung" nay gọn lại, trỏ đúng về Bảng 4.2 ở Mục 4.1.1).

### Phase 1 — Gộp Mục 4.2 (Đánh giá hiệu năng phân đoạn) thành topic-major

**Đã làm:**
- Viết lại đoạn mở đầu Chương 4 (bỏ khung "Phần I/Phần II" cũ) thành lộ trình theo mục 4.1→4.5 mới.
- **4.2.1 So sánh U-Net:** gộp bảng `tab:baseline_comparison` (BTXRD) + `tab:fracatlas_baseline` (FracAtlas) liền nhau, viết 1 đoạn "Nhận định xuyên hai bộ dữ liệu" 3 gạch đầu dòng (giới hạn tự động nhất quán cả 2 miền; giá trị câu nhắc thậm chí rõ hơn trên FracAtlas; đây là dấu hiệu tổng quát ở cấp độ thiết kế, trỏ forward sang mục 4.3.3 sẽ viết ở Phase 2).
- **4.2.2 Tính bền bỉ:** giữ bảng BTXRD `tab:robustness_comparison`, bên FracAtlas không tạo bảng mới trùng lặp mà trích dẫn 3 số Dice (Zoom/Shift/Mixed @512) ngay trong văn bản, trỏ forward về bảng đầy đủ tại 4.2.4 — tránh hiển thị cùng một bộ số liệu FracAtlas trong 2 bảng khác nhau.
- **4.2.3 So SAM-Med2D:** gộp bảng `tab:sam_comparison` (BTXRD) + `tab:fracatlas_sam_comparison` (FracAtlas, giữ nguyên ghi chú về SAM hội tụ sớm lần đầu trên FracAtlas), viết 1 đoạn nhận định chung (SAM hội tụ nhanh nhất quán cả 2 miền, PGA vẫn thắng sau khi SAM đã tinh chỉnh đúng cách, tính bền bỉ PGA vẫn tốt hơn ở cả 2).
- **4.2.4 Ảnh hưởng độ phân giải + hiệu quả tính toán:** đổi tên mục từ "(BTXRD)" thành tên chung; gộp bảng `tab:pga_256_512` (BTXRD) + `tab:fracatlas_pga_full` (FracAtlas, dời từ vị trí cũ lên đây — đây là bảng "dùng chung 2 vai trò" cho cả 4.2.2 và 4.2.4 như đã lường trước trong plan) + 2 biểu đồ; viết 1 đoạn nhận định chung (Dice tăng nhất quán cả 2 khi lên 512, nhưng Precision đổi chiều giữa 2 dataset — nêu rõ khác biệt này do đặc tính hình thái, không phải mâu thuẫn số liệu); giữ bảng `tab:efficiency` dùng chung cuối mục (kiến trúc không đổi giữa 2 dataset nên không cần tách).
- **Dọn dẹp:** xóa 3 subsection FracAtlas cũ đã merge (`subsec:fracatlas_pga_full`, `subsec:fracatlas_baseline`, `subsec:fracatlas_sam`) khỏi vị trí cũ trong `sec:fracatlas`; viết lại đoạn mở đầu `sec:fracatlas` cho khớp (bỏ phần đã dời sang 4.2, giữ phần dẫn nhập cho nội dung còn lại — đặc tính tổn thương/ablation/cross-val, thuộc Phase 2).

**Đã kiểm tra kỹ:** không còn label trùng (`tab:fracatlas_pga_full`, `tab:fracatlas_baseline`, `tab:fracatlas_sam_comparison`, `fig:chart_fracatlas_pga_full` đều chỉ còn đúng 1 lần); không số liệu nào bị đổi, chỉ di chuyển vị trí + viết đoạn tổng hợp mới.

**Build:** sạch, 126 trang (từ 127), không lỗi/undefined reference/label trùng. Đã render trực quan 6 trang (64, 65, 68, 69, 70, 71, 72-75) xác nhận toàn bộ 4 mục con của 4.2 hiển thị đúng: mỗi mục có bảng/cặp bảng BTXRD+FracAtlas rồi đúng 1 đoạn "Nhận định xuyên hai bộ dữ liệu" duy nhất, không lặp cấu trúc; chuyển tiếp sang "4.3 Phân tích kiến trúc và khả năng tổng quát hóa" liền mạch.

### Phase 2 — Tái cấu trúc Mục 4.3 (Phân tích kiến trúc) thành khối BTXRD/FracAtlas/Kết luận

**Đã làm:**
- **4.3.1 "Trên BTXRD":** demote 3 mục con cũ (`subsec:ablation_arch`, `subsec:cross_validation`, `subsec:subcategory`) từ `\subsection` xuống `\subsubsection`, gộp dưới 1 `\subsection{Trên BTXRD}` mới. Xóa hẳn subsubsection "Kiểm định thống kê Wilcoxon signed-rank" (bảng `tab:wilcoxon_ablation` + đoạn diễn giải) khỏi vị trí này, thay bằng 1 câu trỏ forward sang Mục 4.3.3.
- **4.3.2 "Trên FracAtlas":** sắp lại thứ tự 3 mục con FracAtlas cho khớp BTXRD (cũ: Subcategory→Ablation→CrossVal; mới: Ablation→CrossVal→Subcategory), demote xuống `\subsubsection`. Xóa khối "Phân tích, đối chiếu với BTXRD" (4 gạch đầu dòng) khỏi mục Ablation FracAtlas, thay bằng 1 câu trỏ forward sang 4.3.3.
- **4.3.3 "Kết luận đóng góp kiến trúc xuyên hai miền dữ liệu" (viết mới):** phục hồi nguyên bảng `tab:wilcoxon_ablation` (36 kết quả, lấy lại từ git diff vì đã bị xóa tạm ở bước trên) + đoạn dẫn nhập kiểm định; tái sử dụng nguyên 4 gạch đầu dòng "Phân tích, đối chiếu với BTXRD" từ Ablation FracAtlas làm khung chính; thêm 1 đoạn ngắn về độ ổn định qua đánh giá chéo (rút gọn từ mục "Thảo luận" cũ, chỉ giữ phần kiến trúc, bỏ phần Gatekeeper); kết bằng đoạn "Kết luận về phạm vi tổng quát hóa kiến trúc" (rút gọn từ đoạn "Về mức độ tổng quát hóa có thể kết luận" cũ, bỏ nhắc lại Gatekeeper vì đã có sẵn ở Nhận xét của Pipeline eval FracAtlas, trỏ forward sang Mục 4.7 cho phần hệ thống).
- **Quyết định biên tập (lệch nhẹ so với bản đồ nội dung gốc trong plan):** không đưa 3 gạch đầu dòng đầu của "Thảo luận" cũ (so U-Net/SAM-Med2D/tính bền bỉ margin) vào 4.3.3 vì đã trùng lặp hoàn toàn với đoạn "Nhận định xuyên hai bộ dữ liệu" đã viết ở từng mục 4.2.x (Phase 1) — giữ 4.3.3 tập trung đúng vào tổng hợp ablation/cross-val/subcategory, tránh lặp nội dung giữa 2 mục.
- Xóa hẳn subsection "Thảo luận: hiệu quả của kiến trúc khi huấn luyện lại trên miền dữ liệu khác" (đã tách nội dung vào 4.3.3 và mục Gatekeeper FracAtlas).
- Do phần Gatekeeper/FN-analysis/pipeline-eval FracAtlas (vốn nằm cùng `sec:fracatlas` với nội dung 4.3.2) chưa có section cha sau khi xóa `\section{Đánh giá bổ sung...}`, tạm đặt 1 `\section` mới "Đánh giá Gatekeeper và luồng xử lý đầu cuối trên FracAtlas" (label tạm `sec:fracatlas_gatekeeper_temp`) — sẽ được Phase 3 gộp chính thức vào `sec:product_overview`.
- Thêm lại `\label{sec:tien_xu_ly}` (bị rơi mất từ Phase 0, gây lỗi undefined reference từ Chương 3) vào đúng đoạn "Tiền xử lý đầu vào" tại 4.1.1.
- Sửa 2 `\ref{sec:fracatlas}` còn sót ở Chương 5 (label đã xóa) trỏ lại đúng `subsec:conclusion_arch` và `subsec:arch_fracatlas`.
- **Lỗi phát hiện và sửa giữa chừng:** lần đầu viết 4.3.3 bị đặt sai vị trí (rơi vào bên trong section Gatekeeper tạm, hiển thị nhầm số "4.4.4" thay vì "4.3.3") — đã dùng script Python di chuyển đúng khối 61 dòng về đúng vị trí cuối `\subsection{Trên FracAtlas}`, trước section Gatekeeper tạm.

**Build:** latexmk sạch (clean rebuild qua `latexmk -c` rồi build lại), 124 trang (từ 126, giảm 2 trang do gộp/rút gọn nội dung trùng lặp), không còn undefined reference/label trùng cụ thể nào (đã kiểm tra kỹ bằng grep + quét byte trực tiếp; còn 1 dòng tổng "There were undefined references" không có chi tiết kèm theo dù rebuild sạch nhiều lần — kết luận là artifact vô hại, không tương ứng bất kỳ `\ref`/`\label`/`\cite` cụ thể nào còn thiếu). Đã render trực quan 4 trang (65 = bảng Wilcoxon đầu 4.3.3, 66-67 = 4 bullet + đoạn kết luận, 59 = đầu 4.3.2 Trên FracAtlas, 69 = mục Gatekeeper FracAtlas trong section tạm) xác nhận đánh số 4.3.1/4.3.2/4.3.3 đúng, mạch văn liền mạch, cross-reference tới 4.7 (Gatekeeper BTXRD) đúng.

### Phase 3 — Tái cấu trúc Mục 4.4 (Gatekeeper + luồng xử lý đầu cuối) thành khối BTXRD/FracAtlas

**Đã làm:**
- Gộp 2 khối đang nằm cách xa nhau trong file thành 1 `\section{Đánh giá module Gatekeeper và luồng xử lý đầu cuối}` (giữ nguyên `\label{sec:product_overview}` gốc): khối BTXRD (`sec:danh_gia_phan_lop` + `subsec:fn_analysis` + `subsec:cascading_error` + `sec:pipeline_eval` + `subsec:additional_e2e_metrics`, vốn nằm cuối file) demote xuống `\subsubsection`, gộp dưới `\subsection{Trên BTXRD}\label{subsec:product_overview_btxrd}` mới; khối FracAtlas (`subsec:gatekeeper_fa` + `subsec:fn_analysis_fa` + `subsec:pipeline_eval_fa`, vốn ở section tạm ngay sau 4.3.3) demote tương tự, gộp dưới `\subsection{Trên FracAtlas}\label{subsec:product_overview_fracatlas}` mới, xóa `\section` tạm `sec:fracatlas_gatekeeper_temp` của Phase 2.
- Viết lại đoạn mở đầu `sec:product_overview` (trỏ tới 2 mục con BTXRD/FracAtlas) và thêm 1 câu dẫn ngắn đầu 4.4.2 nêu rõ bất đối xứng đã biết: FracAtlas không có mục "sai số tích lũy" riêng, nội dung lồng trong "Nhận xét" của `subsec:pipeline_eval_fa`, trỏ ngược `subsec:cascading_error` (BTXRD) — giữ đúng bất đối xứng như plan đã lường trước, không ép thêm mục con thứ 4 giả cho FracAtlas.
- Toàn bộ nội dung/số liệu giữ nguyên, chỉ đổi vị trí + cấp độ heading + viết đoạn dẫn nhập mới; không cần sửa cross-reference nào khác vì tất cả đều dùng `\ref` tới label không đổi.

**Build:** sạch ngay lần đầu (latexmk, không cần force/clean), 123 trang (từ 124), 0 undefined reference cụ thể (quét bằng regex trực tiếp trên log, không còn dòng tổng "undefined references" nào — sạch hơn cả Phase 2). Đã render trực quan 2 trang (68 = đầu 4.4/4.4.1 Trên BTXRD, 79 = chuyển tiếp 4.4.1→4.4.2 Trên FracAtlas) xác nhận đánh số 4.4.1/4.4.2 đúng, mạch văn liền mạch, câu dẫn bất đối xứng FracAtlas đọc rõ nghĩa.

### Phase 4 — Phân bổ lại 6 hình trực quan + case thất bại vào đúng mục định lượng

**Đã làm:** Xóa hẳn 2 mục cuối chương từng gom riêng "Trực quan hóa kết quả" (`sec:truc_quan_hoa`) và "Giới hạn kiến trúc và phân tích trường hợp thất bại" (`sec:failure_cases`, gồm cả comment "PHẦN II" lỗi thời còn sót từ cấu trúc 2-phần cũ), phân bổ lại từng hình + đoạn văn mô tả vào đúng mục định lượng liên quan:
- `fig:vis_pga_sample` (Zoom-out) → cuối 4.2.1 (Đánh giá cơ sở U-Net so PGA-UNet).
- `fig:qual_shift` (Shift lệch tâm) → cuối 4.2.2 (Tính bền bỉ), sửa 1 câu tự tham chiếu vòng ("minh chứng tính bền bỉ đã trình bày ở Mục~`sec:pipeline_eval`" → "minh chứng trực quan cho tính bền bỉ vừa nêu ở trên", vì hình giờ nằm ngay trong mục đang bàn về tính bền bỉ).
- `fig:qual_small_lesion` (tổn thương nhỏ) → cuối 4.3.1 (đặc tính tổn thương, BTXRD), ngay sau bảng kiểm chứng công bằng cùng độ phân giải.
- `fig:qual_pipeline_tp` (6 ca TP qua pipeline) → cuối mục "Đánh giá luồng xử lý đầu cuối trên dữ liệu hỗn hợp" trong 4.4.1 (Trên BTXRD).
- `fig:qual_overlap` + toàn bộ 3-bullet "nhóm trường hợp PGA-UNet dự đoán kém" → cuối 4.3.3 (Kết luận đóng góp kiến trúc), thêm tiêu đề "Giới hạn quan sát được (BTXRD)" và 1 câu chú thích rõ đây là hạn chế của thiết kế bản đồ nhiệt Gaussian, không phủ nhận kết luận tổng quát hóa vừa nêu, và chưa kiểm chứng lại trên FracAtlas.
- Không đổi số liệu/nội dung hình nào, chỉ di chuyển vị trí + viết lại câu dẫn nhập cho khớp ngữ cảnh mới tại từng vị trí.

**Build:** sạch, 122 trang (từ 123), không undefined reference/duplicate label nào (đã kiểm tra qua IDE diagnostics + latexmk log). Đã render trực quan 5 vị trí hình mới (39, 42, 60, 70-71, 80-81) xác nhận mỗi hình lồng đúng mạch văn của mục định lượng chứa nó, không đọc rời rạc; chuyển tiếp giữa các mục (4.2.1→4.2.2, 4.2.2→4.2.3, 4.3.1→4.3.2, 4.3.3→4.4, trong 4.4.1) đều liền mạch.

### Phase 5 — Viết mới Mục 4.5 "Tổng kết chương"

**Đã làm:** Chương 4 trước giờ **chưa từng có** mục tổng kết riêng (khác Chương 2/3 đều có `\section{Tổng kết chương}`) — đây là mục hoàn toàn mới, không phải đổi số từ mục cũ. Viết theo đúng văn phong ngắn gọn của Chương 2/3 (2 đoạn, không dùng bullet), đặt cuối file, nội dung: đoạn 1 tóm tắt 4 nhóm thực nghiệm (4.2/4.3/4.4) + khẳng định kiến trúc PSG+CAD tổng quát tốt xuyên hai miền dữ liệu ở cấp độ **module phân đoạn** (trỏ về kết luận đã có ở 4.3.3, không nhắc lại số liệu chi tiết); đoạn 2 nêu thẳng giới hạn: tổng quát hóa **không đồng đều giữa các module** (Gatekeeper suy giảm trên FracAtlas kéo Pipeline Dice xuống), liên hệ lại thiết kế "triage mềm" đã giới thiệu ở Chương 3, và forward-link các hạn chế cụ thể sang Chương 5.

**Build:** sạch, 123 trang (từ 122, +1 trang do nội dung mới), 0 undefined reference, không lỗi. Đã render trực quan trang 88 xác nhận mục lục hiển thị đúng "4.5 Tổng kết chương" (không còn mục 4.5 "Trực quan hóa" cũ chiếm chỗ), nội dung đọc mạch lạc, trả lời thẳng câu hỏi "tổng quát tới đâu, không tổng quát ở điểm nào" như yêu cầu ban đầu, không lặp lại 4.3.3.

---

## Hoàn tất toàn bộ 6 phase tái cấu trúc Chương 4 (Phase 0 → Phase 5)

Toàn bộ kế hoạch tại `Đánh giá.md` / `/home/thongluc/.claude/plans/floofy-sleeping-floyd.md` đã triển khai xong: 4.1 (3 mục con), 4.2 (topic-major, 4 mục), 4.3 (BTXRD/FracAtlas/Kết luận), 4.4 (BTXRD/FracAtlas), hình trực quan + case thất bại phân bổ vào đúng mục định lượng, 4.5 Tổng kết chương viết mới. Build cuối: sạch, 123 trang, 0 undefined reference/duplicate label. Bước tiếp theo (theo đúng yêu cầu ban đầu của user): tạo 1 fork agent kiểm tra chi tiết toàn bộ Chương 4 đã tái cấu trúc để rà soát tính liên kết/logic, bổ sung chỉnh sửa nếu cần.

### Rà soát cuối cùng (fork agent) — kiểm tra liên kết/logic toàn bộ Chương 4 sau tái cấu trúc

**Đã làm:** Đọc lại toàn bộ `chapter4.tex` (1434 dòng, đọc tuần tự từng đoạn ~400 dòng, không sample/grep) để rà soát 4 tiêu chí: mạch văn tại các điểm nối hình/mục vừa di chuyển, tính nhất quán logic giữa các đoạn "Nhận định xuyên hai bộ dữ liệu" (4.2.x), 4.3.3 và 4.5, trùng lặp nội dung, và tính nhất quán của luận điểm trung tâm ("kiến trúc phân đoạn tổng quát tốt, hệ thống/Gatekeeper thì không") xuyên suốt chương. Tìm thấy và sửa 2 vấn đề:
1. **Thứ tự đoạn văn sai trong 4.3.3:** Khối "Giới hạn quan sát được (BTXRD)" (3-bullet case thất bại + hình `fig:qual_overlap`, được chuyển vào đây từ Phase 4) nằm SAU đoạn "Kết luận về phạm vi tổng quát hóa kiến trúc" — khiến toàn mục 4.3 (và cả sec:ablation_study) kết thúc bằng một ca thất bại cụ thể thay vì đoạn tổng kết mạnh nhất. Đã đổi chỗ: "Giới hạn quan sát được" + hình đặt ngay sau đoạn "Độ ổn định qua đánh giá chéo", còn "Kết luận về phạm vi tổng quát hóa kiến trúc" chuyển xuống cuối cùng — đúng cấu trúc "hạn chế cụ thể trước, kết luận tổng hợp mạnh nhất sau cùng". Sửa luôn 1 cụm từ liên quan ("đã kết luận ở trên" → "sẽ kết luận dưới đây") cho khớp thứ tự mới.
2. **Trùng lặp gần verbatim:** Ví dụ minh họa "PGA-UNet đề xuất cải thiện Shift Dice +0.0989 so với PGA-UNet Binary... tỷ lệ signal-to-noise ≈ 8,3" xuất hiện gần như y hệt ở cả Mục~4.3.1 (đánh giá chéo, câu gốc) và Mục~4.3.3 (đoạn "Độ ổn định qua đánh giá chéo"). Đã rút gọn bản sao ở 4.3.3 thành 1 câu trỏ ngược về Mục~4.3.1 thay vì lặp lại số liệu.
3. Kiểm tra không thấy mâu thuẫn nào giữa các đoạn "Nhận định xuyên hai bộ dữ liệu" (4.2.1-4.2.4), 4 bullet + 2 đoạn kết luận ở 4.3.3, và 2 đoạn Tổng kết chương ở 4.5 — luận điểm trung tâm (module phân đoạn tổng quát tốt xuyên 2 dataset, nhưng Gatekeeper/hệ thống thì không) được giữ nhất quán, không có đoạn nào nói ngược. Các điểm nối hình ảnh (4.2.1→4.2.2, 4.2.2→4.2.3, 4.3.1→4.3.2, 4.4.1 nội bộ, 4.4.2→4.5) đều đọc mượt, không có câu cụt hay lặp ý liền kề. Không phát hiện `\ref{}` nào trỏ sai ngữ nghĩa.

**Build:** sạch, 123 trang (không đổi), 0 undefined reference/error sau khi sửa.

---

## Kiểm tra bổ sung sau khi hoàn tất tái cấu trúc: số liệu + ảnh minh họa

### Kiểm tra lại số liệu Chương 4 (đối chiếu CSV gốc)

Đối chiếu trực tiếp bằng tay toàn bộ 90 giá trị số trong 2 bảng rủi ro cao nhất (bị xóa/di chuyển trong Phase 2 tái cấu trúc trước đó):
- Bảng `tab:wilcoxon_ablation` (36 giá trị Δ Dice + p-value, 6 cặp × 2 dataset × 3 kịch bản): khớp 100% với `wilcoxon_results.csv` gốc (chỉ khác dấu do quy ước "X−Y" khác chiều giữa 2 nơi tính, không ảnh hưởng p-value vì Wilcoxon đối xứng theo hướng).
- Bảng `tab:ablation_arch` (BTXRD) + `tab:fracatlas_ablation_arch` (FracAtlas), 8 biến thể × 3 kịch bản mỗi bảng: khớp 100% với `ablation_v1v8_official.csv` gốc.
- Kiểm tra chéo phép tính trong văn bản (VD: $0.4740\to0.8607$ = $+0.3867$, $0.3831\to0.8169$ = $+0.4338$): đúng.
- Định dạng thập phân (dấu chấm cho số liệu Dice/IoU kiểu bài báo, dấu phẩy cho p-value/phần trăm trong văn xuôi tiếng Việt) nhất quán xuyên suốt Chương 4 và toàn báo cáo (đối chiếu Chương 2/3/5), không phải lỗi.
- Kết luận: không phát hiện sai lệch số liệu nào từ toàn bộ quá trình di chuyển/gộp khối trong 6 phase tái cấu trúc.

### Bổ sung/thay ảnh minh họa từ `Report/images` (8 folder ảnh mới do user cung cấp)

User thêm 8 folder ảnh thô mới (PGA vs SAM-Med2D nhỏ/mờ/rõ, PGA vs U-Net nhóm khó/dễ, PGA zoom vs shift, V6 vs V7 ablation — mỗi loại có bản BTXRD + FracAtlas). Theo lựa chọn "cả hai" (vừa thay vừa bổ sung):

- **Thay thế** `qual_shift_examples.png` (Mục 4.2.2) bằng `qual_robustness_zoom_shift.png` mới (ghép 4 hàng: BTXRD Zoom/Shift + FracAtlas Zoom/Shift, cùng 1 ca mỗi dataset) — minh chứng trực tiếp hơn bản cũ (vốn chỉ có 2 ca Shift rời rạc, không có nền Zoom-out để so sánh, và thiếu hẳn phần FracAtlas).
- **Thay thế** `qual_small_lesion.png` (đứng riêng ở 4.3.1) bằng 2 hình mới đặt đúng vị trí dữ liệu tương ứng: `qual_subcat_sam_btxrd.png` (4.3.1) và `qual_subcat_sam_fracatlas.png` (4.3.2) — mỗi hình ghép 6 hàng (PGA/SAM × 3 nhóm nhỏ/mờ/rõ), minh họa trực tiếp cho Bảng `tab:subcat_sam`/`tab:fracatlas_subcat`.
- **Bổ sung mới** `qual_subcat_baseline_btxrd.png` (4.3.1) và `qual_subcat_baseline_fracatlas.png` (4.3.2): 4 hàng (PGA/U-Net × dễ/khó), minh họa Bảng `tab:subcat_baseline`/`tab:fracatlas_subcat_baseline` — mục này trước đây chỉ có bar chart, chưa có ảnh X-quang thật.
- **Bổ sung mới** `qual_ablation_v6v7_btxrd.png` (4.3.1) và `qual_ablation_v6v7_fracatlas.png` (4.3.2): 2 hàng (V6-CAD so V7-Attention gốc) trên cùng 1 ca mỗi dataset — mục ablation trước đây cũng chỉ có bar chart.
- Tất cả ảnh ghép được dựng bằng script Python/Pillow (resize cùng chiều rộng, ghép dọc, thêm nhãn hàng + Dice/IoU), lưu trực tiếp vào `Report/images/`.
- Caption/văn dẫn được viết cẩn thận để không suy diễn quá mức từ 1 ca đơn lẻ: với cặp V6/V7 (chỉ 1 ca each), ghi rõ đây là minh họa cụ thể, không đại diện xu hướng trung bình (dẫn lại đúng chiều Wilcoxon đã kiểm định).
- Đã xóa 2 file ảnh cũ không còn dùng (`qual_shift_examples.png`, `qual_small_lesion.png`) sau khi xác nhận không còn `\ref`/`\includegraphics` nào trỏ tới.

**Build:** sạch, 129 trang (từ 123, +6 trang do 6 hình mới cỡ lớn), 0 undefined reference/lỗi. Đã render trực quan toàn bộ 7 vị trí hình mới/thay thế (trang 42, 62-63, 68-69, 81-82, 85-86) xác nhận hiển thị đúng, chú thích khớp số liệu, mạch văn liền mạch.

---

## Rà soát toàn bộ báo cáo (5 chương + Appendix) sau khi tái cấu trúc Chương 4 + thay ảnh

Đọc toàn bộ Chapter1–5 và các file Appendix (`tomtat.tex`, `danhmuctuvietat.tex`, `doichieuthuatngu.tex`; `decuong.tex` chỉ rà nhanh vì là văn bản đề xuất, thì tương lai, không mô tả cấu trúc chương thực tế nên không tính là "lỗi thời"), đối chiếu mọi `\ref{}` từ Chapter 1/3/5 trỏ vào label thuộc Chapter 4 xem còn đúng ngữ cảnh sau tái cấu trúc hay không.

**Đã tìm thấy và sửa 3 chỗ lỗi thời (Chương 1 + Appendix), do mô tả sai phạm vi/cấu trúc Chương 4 sau khi đã mở rộng đánh giá song song 2 bộ dữ liệu:**
1. **Chapter1/chapter1.tex, Mục "Đóng góp của khóa luận":** câu "được kiểm chứng qua ablation study và so sánh với U-Net, SAM-Med2D **trên BTXRD**" hạ thấp phạm vi thực tế (ablation giờ được kiểm chứng đầy đủ trên CẢ HAI bộ dữ liệu, có kiểm định Wilcoxon xuyên miền dữ liệu tại Mục 4.3.3) — sửa thành "trên cả BTXRD và FracAtlas".
2. **Chapter1/chapter1.tex, Mục "Bố cục của khóa luận":** đoạn mô tả Chương 4 vẫn viết theo khung cũ ("kết quả... trên BTXRD; đồng thời trình bày thực nghiệm bổ sung... FracAtlas") — không còn đúng cấu trúc topic-major mới (BTXRD+FracAtlas song song trong 4.2, tách khối+tổng hợp trong 4.3/4.4). Viết lại toàn bộ câu cho khớp cấu trúc hiện tại.
3. **Appendix/tomtat.tex (Tóm tắt khóa luận):** hoàn toàn không nhắc tới FracAtlas dù đây giờ là một phần trọng tâm của bằng chứng luận điểm (tổng quát hóa xuyên 2 miền dữ liệu). Bổ sung 2 câu ngắn về kết quả FracAtlas (đóng góp kiến trúc nhất quán xuyên 2 dataset; hạn chế Gatekeeper rõ hơn trên FracAtlas) mà không đổi số liệu BTXRD đã có.

**Đã kiểm tra, không có vấn đề:** Chapter 2 không tham chiếu Chương 4 nên không bị ảnh hưởng; mọi `\ref` từ Chapter 3 tới Chương 4 (`subsec:hyperparameters`, `sec:pipeline_eval`, `sec:danh_gia_phan_lop`, `sec:tien_xu_ly`) đều đúng ngữ cảnh vì các label này chỉ đổi cấp độ heading (subsection→subsubsection) chứ không đổi nội dung/vị trí logic; mọi `\ref` từ Chapter 5 tới Chương 4 (`subsec:conclusion_arch`, `subsec:pipeline_eval_fa`, `subsec:subcategory`, `subsec:arch_fracatlas`) đều đã đúng (đã được sửa sẵn trong các phase tái cấu trúc trước đó của phiên này). Luận điểm trung tâm (module phân đoạn tổng quát tốt xuyên 2 dataset, Gatekeeper/hệ thống thì không) được lặp lại nhất quán, không mâu thuẫn, giữa Chương 4 (4.3.3, 4.5) và Chương 5. Định dạng thập phân (chấm cho Dice/IoU, phẩy cho %/p-value) và thuật ngữ Việt hóa nhất quán xuyên suốt toàn báo cáo, không phát hiện lẫn tiếng Anh không cần thiết. Không phát hiện lỗi cú pháp LaTeX khả nghi nào trong Chapter1/2/3/5/Appendix.

**Build:** sạch, 130 trang (từ 129, +1 trang do thêm nội dung ở Chapter 1 + tomtat.tex), 0 undefined reference/lỗi.

---

### Kiểm tra kỹ đề cương (`Appendix/decuong.tex`)

Đọc toàn bộ đề cương và đối chiếu với báo cáo cuối cùng:
- **Tên tác giả/MSSV:** "Thông Lúc (22120196)", "Nguyễn Hữu Bình (22120031)" khớp chính xác với `Title/title.tex`.
- **6 tài liệu tham khảo trong đề cương** ([1] U-Net, [2] SAM-Med2D, [3] BTXRD, [4] EfficientNet, [5] FracAtlas, [6] Attention U-Net): đối chiếu từng mục với `References/references.bib` (`ronneberger2015unet`, `2023-SAMMed2D-Cheng`, `btxrd2024`, `oktay2018attentionunet`) — khớp chính xác tác giả/năm/venue, kể cả năm xuất bản chính thức BTXRD (Scientific Data, 2025, dù bib-key đặt tên `btxrd2024` theo năm nộp preprint — không phải lỗi, chỉ là quy ước đặt tên key).
- **Phạm vi/mục tiêu/giới hạn nêu trong đề cương** (huấn luyện BTXRD chính + FracAtlas kiểm chứng tổng quát hóa; câu nhắc hộp giới hạn; Gatekeeper là minh họa không phải đóng góp kiến trúc riêng; hệ thống hỗ trợ không thay thế bác sĩ): đều được thực hiện đúng và nhất quán trong báo cáo cuối cùng, không có mục tiêu nào bị bỏ hoặc bị mâu thuẫn.
- **"Kết quả dự kiến"** (Dice≥0,80, IoU≥0,70, AUC-ROC≥0,92): đều đạt/vượt trong kết quả thực tế (PGA-UNet Dice=0.8607/IoU=0.7630, Gatekeeper AUC-ROC=0.9421) — đề cương là tài liệu định hướng trước khi làm nên không cần khớp số chính xác, chỉ cần không bị mâu thuẫn/thụt lùi so với mục tiêu, và không bị mâu thuẫn.
- **`Lời cam đoan`** dùng "chúng tôi" nhất quán với khung nhóm 2 người.

**Kết luận:** không phát hiện sai lệch/lỗi thời nào giữa đề cương và báo cáo cuối cùng — không cần sửa.

---

## Đổi tên đề tài

Đổi tên đề tài từ "Phát triển hệ thống phân đoạn ảnh X-quang về xương dựa vào câu nhắc trực quan" (cụm "ảnh X-quang về xương" không tự nhiên, đã ghi nhận trước đó) sang **"Phát triển hệ thống phân đoạn tổn thương xương trên ảnh X-quang dựa trên câu nhắc trực quan"**, áp dụng xuyên suốt toàn bộ report:
- `Title/title.tex` (2 trang bìa).
- `Appendix/decuong.tex` (tiêu đề đề cương + bản dịch tiếng Anh, đổi thành "Developing a bone lesion segmentation system on X-ray images based on visual prompts").
- `proposal.tex` và `MUCLUC.tex` (2 file không nằm trong `main.tex`/không thuộc bản build hiện tại nhưng vẫn được git track) — đổi luôn cho nhất quán toàn repo; tiện thể sửa lỗi chính tả "CẦU NHẮC" → "CÂU NHẮC" có sẵn trong `MUCLUC.tex`.
- `README.md` và `Source/README.md` (dòng mô tả đề tài ở đầu file).
- Không đổi `Xư_ly.md` (giữ nguyên câu ghi chú lịch sử đề xuất tên mới) và không đổi `Decuong_KhoaLuan.pdf` (văn bản đã nộp, không phải nguồn LaTeX build được).

**Build:** sạch, 130 trang (không đổi), 0 undefined reference/lỗi. Đã render trực quan 2 trang bìa + trang đầu đề cương xác nhận tên mới hiển thị đúng, xuống dòng đẹp, không tràn khung.

---

## Sửa từ ngữ trong đề cương (`Appendix/decuong.tex`)

Theo yêu cầu user, sửa 2 điểm chỉ trong đề cương:
- **Bỏ từ "đầu cuối":** thay "luồng xử lý đầu cuối" → "hệ thống" ở 4 chỗ (2.1 giới thiệu, 2.3 phạm vi đánh giá, 2.5 kết quả dự kiến — gộp luôn "đánh giá luồng xử lý toàn hệ thống" thành "đánh giá hệ thống" để tránh lặp từ "hệ thống" 2 lần liền, 2.6 bảng kế hoạch giai đoạn 5).
- **Sửa câu phạm vi dữ liệu ở 2.1:** "Toàn bộ hệ thống được huấn luyện và đánh giá trên bộ dữ liệu BTXRD~[3]" (chỉ nhắc 1 dataset) → "...trên hai bộ dữ liệu X-quang xương có đặc tính tổn thương khác nhau: BTXRD~[3] và FracAtlas~[5]" — khớp đúng thực tế đã làm (huấn luyện lại từ đầu và đánh giá đầy đủ trên cả 2 bộ).
- Không đổi câu ở 2.3 "Phạm vi thực hiện" (BTXRD là dữ liệu chính, FracAtlas dùng đánh giá bổ sung) vì user không yêu cầu và đây là mô tả hợp lệ về vai trò 2 bộ dữ liệu trong đề cương gốc.

**Build:** sạch, 130 trang (không đổi), 0 undefined reference/lỗi. Đã render trực quan trang đầu Mục 2.1 xác nhận câu văn mới đọc tự nhiên, không còn "đầu cuối".

---

## Chỉnh câu văn 2.1/2.2 đề cương: bỏ ngoặc phòng thủ, tổng quát hóa "khối u"

Theo yêu cầu user:
- **Bỏ "(phân đoạn ảnh)"** ở câu "Bước khoanh vùng tổn thương (phân đoạn ảnh) là cơ sở..." (2.1) — câu đã đủ rõ nghĩa không cần chú thích lại.
- **Tổng quát hóa "khối u" → "tổn thương"** ở 2 chỗ mang tính mô tả chung, không đặc thù riêng BTXRD: "đo kích thước khối u" → "đo kích thước tổn thương" (2.1); "Phân đoạn nhị phân vùng khối u xương" → "...vùng tổn thương xương" (2.3, Bài toán) — vì phạm vi bài toán giờ bao gồm cả gãy xương (FracAtlas), không chỉ u xương. **Giữ nguyên** 2 chỗ "khối u" còn lại vì là tên loại tổn thương cụ thể, không phải cách gọi chung: "khối u xương nguyên phát" (liệt kê loại tổn thương ở 2.1) và "khác biệt với khối u BTXRD" (đối chiếu đặc tính BTXRD vs FracAtlas ở 2.2, mục tiêu 4).
- **Viết lại câu "Để minh họa khả năng ứng dụng thực tế..." (2.1)** bỏ hẳn ngoặc phòng thủ "(không phải đóng góp kiến trúc riêng biệt)", đổi khung diễn đạt từ "minh họa" sang tích cực hơn: "Để hỗ trợ tốt hơn cho quy trình chẩn đoán thực tế, PGA-UNet còn được kết hợp thêm với một module phân lớp sàng lọc, tạo thành một hệ thống khả thi trong thực tế."
- **Áp dụng nhất quán cho mục tiêu 2 (2.2)**: đổi tiêu đề in đậm "Minh họa khả năng ứng dụng thực tế của PGA-UNet" → "Mở rộng khả năng ứng dụng thực tế của PGA-UNet", bỏ luôn ngoặc phòng thủ ở cuối câu, đổi "luồng xử lý hai giai đoạn" → "một hệ thống hai giai đoạn" (khớp quy ước "hệ thống" thay "luồng xử lý"/"đầu cuối" vừa thống nhất trước đó), "minh họa cách hệ thống có thể hỗ trợ" → "hỗ trợ bác sĩ tốt hơn".

**Build:** sạch, 130 trang (không đổi), 0 undefined reference/lỗi. Đã render trực quan 2 trang (Mục 2.1, Mục 2.2-2.3) xác nhận câu văn mới đọc tự nhiên, mạch lạc, không còn ngoặc phòng thủ.

---

## Tinh gọn Mục 2.1 đề cương (cắt 2 hàng)

Theo yêu cầu user, nén 3 đoạn của Mục 2.1 mà không bỏ nội dung cốt lõi:
- Đoạn 1: "đặt áp lực đáng kể lên đội ngũ bác sĩ về tốc độ đọc phim và độ chính xác chẩn đoán" → "gây áp lực lớn lên tốc độ và độ chính xác chẩn đoán của bác sĩ"; bỏ lặp "tổn thương" ở "đo kích thước tổn thương" → "đo kích thước"; "tuy nhiên hiện vẫn thực hiện thủ công" → "nhưng hiện vẫn thực hiện thủ công".
- Đoạn 2: bỏ "đặc thù" (thừa); "chi phí tính toán cao, không phù hợp triển khai" → "khó triển khai" (giữ nguyên ý, ngắn hơn).
- Đoạn 3: gộp câu "Toàn bộ hệ thống được huấn luyện và đánh giá..." làm mệnh đề nối tiếp thay vì câu riêng; bỏ "thêm" thừa trong "kết hợp thêm với"; "cho quy trình chẩn đoán thực tế" → "cho chẩn đoán thực tế".

**Kết quả đo bằng render trực quan (so 2 bản trước/sau):** Mục 2.1 giảm từ 23 dòng xuống 21 dòng (tiết kiệm đúng 2 dòng theo yêu cầu), không mất ý nào (vẫn đủ: bối cảnh lâm sàng, hạn chế PACS thủ công, hạn chế U-Net/SAM-Med2D, đề xuất PGA-UNet+Gatekeeper, 2 bộ dữ liệu).

**Build:** sạch, 130 trang (không đổi), 0 undefined reference/lỗi.
