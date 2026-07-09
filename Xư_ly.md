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

**A.1 — Sửa claim Gatekeeper "an toàn"**
Hiện diễn giải Recall 88.77% (bỏ sót 21/187 ca) là "đảm bảo an toàn sàng lọc", NPV 88.65% là "đủ tin cậy làm bộ lọc sơ cấp" — kết luận quá mạnh so với yêu cầu an toàn lâm sàng. Sửa: chỉ nói Gatekeeper có hiệu năng ban đầu khá tốt, **chưa đủ an toàn** để tự động chặn ảnh âm tính; cần ưu tiên tăng sensitivity và có cơ chế không cho Gatekeeper loại bỏ ca nghi ngờ.

**A.2 — Sửa claim "bền bỉ trong lâm sàng thực tế" → "bền vững trong kịch bản mô phỏng có kiểm soát"**
Chỉ đánh giá qua Zoom-out/Shift/Mixed (bbox mô phỏng), chưa có bbox từ nhiều bác sĩ, bbox quá nhỏ/quá lớn/sai hoàn toàn, nhiều tổn thương trong cùng ảnh. Sửa câu chữ ở mọi nơi xuất hiện (đặc biệt phần kết luận): "bền vững trước sai lệch bbox có kiểm soát trong các kịch bản Zoom-out/Shift/Mixed", không viết "bền bỉ trong lâm sàng thực tế".

**A.3 — Sửa claim "tổng quát hóa liên miền" trên FracAtlas**
FracAtlas có train/val/test riêng (573/72/72) → mô hình đã được huấn luyện lại trên FracAtlas, không phải test trực tiếp mô hình train-trên-BTXRD. Sửa cách viết: "đánh giá bổ sung trên bộ dữ liệu thứ hai sau khi huấn luyện/tinh chỉnh trên FracAtlas", không dùng "cross-dataset generalization" theo nghĩa external domain generalization trừ khi bổ sung thí nghiệm ở A.3.1.

**A.4 — Sửa mâu thuẫn "pipeline phản ánh sát điều kiện lâm sàng" vs. thiết kế human-in-the-loop**
Thiết kế hiện tại: Gatekeeper âm tính → dừng, không qua PGA-UNet, bác sĩ không có cơ hội vẽ bbox. Điều này mâu thuẫn với mô tả "human-in-the-loop" vì ở nhánh âm tính con người bị loại khỏi vòng quyết định. Sửa mô tả kiến trúc: Gatekeeper không nên là bộ chặn cứng, chỉ nên là module cảnh báo/triage mềm (xem B.3).

**A.5 — Hạ mức claim novelty của PSG/CAD**
Hiện mô tả PSG là "thành phần mới hoàn toàn", CAD là mở rộng Attention Gate, nhưng khảo sát liên quan còn hẹp (chủ yếu U-Net, Attention U-Net, SAM-Med2D). Cần bổ sung khảo sát (xem C.2) trước khi giữ nguyên mức claim "mới hoàn toàn".

**A.6 — Viết lại phần kết luận chung ở mức thận trọng**
Kết luận hiện tại viết "tính bền bỉ cao trong điều kiện lâm sàng thực tế" — dễ bị phản biện. Sửa thành: một hệ thống **thử nghiệm/tiền lâm sàng** có tiềm năng hỗ trợ phân đoạn tương tác, chưa đủ bằng chứng khẳng định an toàn hoặc sẵn sàng triển khai lâm sàng.

---

## KẾ HOẠCH LỚN B: Sửa lỗi phương pháp đánh giá (nghiêm trọng nhất)

**B.1 — Sửa công thức Pipeline Dice**
Hiện tại: FN (ảnh có bệnh nhưng Gatekeeper dự đoán âm) không qua PGA-UNet và "không tính" — mẫu số Pipeline Dice chỉ gồm TP+FP, FN không bị đưa vào với Dice=0. Điều này làm chỉ số pipeline "đẹp" hơn thực tế vì ca bị bỏ sót hoàn toàn không bị phạt. Sửa: tính lại Pipeline Dice trong đó **mọi FN bệnh lý được gán Dice = 0** trong mẫu số/tử số end-to-end.

**B.2 — Bổ sung các chỉ số end-to-end phản ánh đúng rủi ro lâm sàng**
Báo cáo thêm riêng: sensitivity bệnh lý (ở cấp độ ảnh), lesion-level recall, false negative rate, và một metric end-to-end đã tính FN=0 Dice như B.1 — không chỉ dựa vào Pipeline Dice hiện tại.

**B.3 — Đổi thiết kế Gatekeeper từ "bộ chặn cứng" sang "module triage mềm"**
Vì Gatekeeper bỏ sót 21/187 ca và đang được mô tả như một bước chặn cứng trước phân đoạn, cần đề xuất/chỉnh sửa thiết kế: Gatekeeper chỉ đưa ra cảnh báo/độ ưu tiên, bác sĩ vẫn có thể kiểm tra và chủ động kích hoạt phân đoạn ngay cả khi Gatekeeper dự đoán âm tính — giữ đúng tinh thần human-in-the-loop (liên kết A.4).

**B.4 — Phân tích định lượng các ca FN của Gatekeeper**
Bổ sung: confusion matrix đầy đủ, phân tích đặc điểm của 21 ca bị bỏ sót (loại tổn thương, kích thước, độ mờ), thử nghiệm chọn ngưỡng (threshold) ưu tiên sensitivity cao thay vì ngưỡng mặc định, và đánh giá hậu quả khi Gatekeeper chặn nhầm ảnh có bệnh.

---

## KẾ HOẠCH LỚN C: Bổ sung thực nghiệm còn thiếu

**C.1 — Kiểm định thống kê chính thức**
Hiện chưa có kiểm định thống kê cho các so sánh chính: PGA-UNet vs SAM-Med2D, V5 vs V4 (ablation). Bổ sung Wilcoxon signed-rank test cho so sánh cặp ở cấp độ ảnh (image-level paired comparison) cho toàn bộ các bảng so sánh chính (4.2–4.7, 4.14, 4.18).

**C.2 — Khảo sát liên quan (related work) rộng hơn để bảo vệ claim novelty**
Bổ sung khảo sát các phương pháp đưa prompt/bbox/mask/click vào CNN, attention U-Net có điều kiện, interactive segmentation y khoa, MedSAM, SAM-based adapters, nnU-Net-based prompt variants — làm nền cho A.5.

**C.3 — Ablation kiến trúc đầy đủ hơn (gần full factorial)**
Hiện đã có V1–V5 nhưng thiếu: biến thể binary+concat, kiểm định thống kê cặp ảnh cho từng cặp so sánh, và đặc biệt **prompt ngẫu nhiên hoặc prompt sai vị trí** để chứng minh mô hình thực sự dùng prompt đúng cách (không chỉ học overfit theo phân bố heatmap).

**C.4 — Ablation tiền xử lý (YOLOv11s xóa nhiễu + xóa ký hiệu R/L)**
Pipeline tiền xử lý hiện tại (YOLOv11s phát hiện nhiễu trên 3.746 ảnh PNG, tô vùng nhiễu bằng màu nền/đen, xóa ký hiệu R/L) là thao tác mạnh trên ảnh y khoa nhưng chưa có ablation. Bổ sung: so sánh ảnh gốc vs ảnh đã xóa nhiễu; so sánh xóa R/L bằng inpainting vs tô màu vs không xóa; kiểm tra tiền xử lý có làm sai lệch vùng giải phẫu hoặc gây artifact ảnh hưởng model không.

**C.5 — Baseline công bằng hơn để tách bạch đóng góp kiến trúc vs lợi ích của prompt**
PGA-UNet nhận thêm bbox/heatmap còn U-Net baseline hoàn toàn tự động — nên việc PGA-UNet vượt U-Net chủ yếu chứng minh "có thêm thông tin định hướng không gian giúp bài toán dễ hơn", chưa tách bạch được đóng góp kiến trúc thuần túy. Bổ sung baseline: U-Net + bbox channel, U-Net + binary mask prompt, Attention U-Net + prompt, và nếu khả thi: nnU-Net, UNet++, TransUNet/Swin-UNet, hoặc các mô hình interactive segmentation nhẹ khác.

**C.6 — Thí nghiệm cross-dataset generalization thật sự (bổ trợ A.3)**
Để có thể giữ claim tổng quát hóa liên miền theo đúng nghĩa, cần thêm: train trên BTXRD → test trực tiếp trên FracAtlas (không fine-tune), hoặc train trên FracAtlas → test trên BTXRD (zero-shot theo cả hai chiều).

**C.7 — Mở rộng quy mô/độ tin cậy thống kê của tập kiểm thử**
187 ảnh test BTXRD, 72 ảnh test FracAtlas — chấp nhận được cho khóa luận đại học nhưng chưa đủ cho claim mạnh về ổn định/triển khai/hiệu quả lâm sàng. Bổ sung khoảng tin cậy (confidence interval), phân tích theo ca khó, và nếu khả thi, external validation từ dataset/bệnh viện độc lập khác.

**C.8 — Bổ sung trực quan hóa kết quả và phân tích lỗi định tính**
Hiện chỉ có một ca tiêu biểu (Hình 4.7). Bổ sung nhiều ví dụ: ca đúng, ca sai, ca FN của Gatekeeper, ca FP, ca tổn thương nhỏ, ca prompt lệch, ca gãy/khối u khó, ca có nhiễu ảnh — để phần phân tích lỗi có sức thuyết phục.

**C.9 — Đánh giá liên chuyên gia (nếu khả thi trong thời gian còn lại)**
Đo độ nhạy của mô hình với bbox do nhiều bác sĩ/nhiều người vẽ khác nhau — hiện hoàn toàn chưa có. Ghi rõ trong hạn chế nếu không kịp thực hiện, thay vì bỏ qua.

**C.10 — Chạy Ablation (V1→V5 tương đương) trên FracAtlas** *(giá trị cao nhất, ưu tiên làm trước trong nhóm C.10–C.12)*
Hiện thư mục `Result/Result_FracAtlas/Ablation/` đang trống, trong khi BTXRD đã có đủ ablation V1–V5. Chạy lại đúng bộ biến thể kiến trúc (U-Net / +PSG / +CAD / +PSG+CAD binary / +PSG+CAD Gaussian) trên FracAtlas để chứng minh đóng góp của PSG/CAD/Gaussian không chỉ đúng trên BTXRD mà còn giữ nguyên trên domain khác — trực tiếp củng cố claim kiến trúc đang bị đánh giá là chưa đủ full factorial (C.3) và claim tổng quát hóa (A.3/C.6).

**C.11 — Train Gatekeeper + đánh giá Pipeline end-to-end trên FracAtlas** *(giá trị cao thứ hai)*
BTXRD có `efficientnet-b3.ipynb` (Gatekeeper) và `test-pipeline-evaluation.ipynb` (pipeline end-to-end); FracAtlas hiện chưa có notebook tương đương. Cần kiểm tra FracAtlas có nhãn fracture/no-fracture ở cấp ảnh (nhiều khả năng có, vì FracAtlas gốc là dataset phân loại gãy xương) để train lại Gatekeeper và dựng lại pipeline evaluation. Đây là bổ sung trả lời trực tiếp điểm yếu bị phê bình nặng nhất: pipeline/Gatekeeper mới chỉ được validate trên một dataset (A.3, C.6, và mục B toàn bộ).

**C.12 — Chạy 4-fold cross-validation trên FracAtlas** *(ưu tiên thấp nhất trong nhóm C.10–C.12)*
BTXRD có `test-pga-dataset-1234.ipynb` (4-fold CV, tương ứng Bảng 4.8/4.9); FracAtlas chưa có. Vì train set FracAtlas khá nhỏ (573 ảnh) và mục tiêu chính của 4-fold là củng cố độ ổn định của claim chính (đã chứng minh trên BTXRD), làm thêm trên FracAtlas là "có thì tốt" chứ không bắt buộc — chỉ nên làm sau khi đã hoàn thành C.10 và C.11 nếu còn thời gian.

---

## KẾ HOẠCH LỚN D: Tái cấu trúc Chương 4 theo đúng nguồn dữ liệu thực nghiệm

Vấn đề chung: các bảng trong Chương 4 hiện chưa theo một trật tự logic rõ ràng, có phần trùng lặp ý và không phản ánh đúng cách các notebook kết quả đã được tổ chức.

**D.1 — Thiết lập lại trật tự trình bày tổng thể của Chương 4**
Trình bày lại theo mạch: thiết lập dữ liệu → mô hình so sánh → chỉ số đánh giá → kết quả chính → ablation → phân tích lỗi → đánh giá pipeline. Đây là khung sườn để sắp xếp lại toàn bộ các mục con bên dưới.

**D.2 — Gộp/làm rõ mục 4.2.3 và 4.2.4 (đang bị trùng ý)**
4.2.3 "So sánh với SAM-Med2D" và 4.2.4 "Kiểm chứng công bằng tại cùng độ phân giải 256×256" hiện đọc như lặp lại cùng một ý (cả hai đều là so sánh PGA-UNet vs SAM-Med2D ở 256). Nguồn dữ liệu của cả hai là cùng một notebook: `Result/Result_BTXRD/test-pga-samzs-samft-r256.ipynb`. Gộp lại thành một mục duy nhất (hoặc làm rõ 4.2.4 là phần mở rộng phân tích riêng biệt, không lặp lại số liệu đã trình bày ở 4.2.3).

**D.3 — Chuẩn hóa lại bảng so sánh SAM-Med2D (mục 4.2.3)**
Bảng hiện tại đang chuẩn hóa cả HD95 và chỉ có một kích thước (256) — không cần thiết phải đưa HD95 vào, và nên trình bày theo format đẹp/gọn giống bảng FracAtlas (mục 4.14/4.18) thay vì format hiện tại.

**D.4 — Đổi tên biến thể trong ablation kiến trúc (mục 4.3.1)**
Thay vì gọi V1/V2/V3/V4/V5, đặt tên theo kiến trúc để người đọc hiểu ngay đây là ablation kiến trúc: U-Net, U-Net+PSG, U-Net+CAD, U-Net+PSG+CAD (PGA đầy đủ), v.v. — khớp với cách đã dùng ở phần đóng góp (liên kết C.3).

**D.5 — Sửa caption bảng 4.8 và 4.9 để mạch lạc theo tầng bậc**
Bảng 4.8 nên có caption: "Dice Score từng fold trong đánh giá chéo 4-fold PGA-UNet (kịch bản Zoom-out/Shift/Mixed)"; Bảng 4.9 nên có caption: "Kết quả đánh giá chéo 4-fold PGA-UNet trên 3 kịch bản prompt (trung bình 4 fold)". Cách đặt tên này giúp người đọc thấy ngay bảng sau là tổng hợp/trung bình của bảng trước.

**D.6 — Ánh xạ rõ vai trò từng notebook kết quả vào đúng mục của Chương 4**
Làm rõ trong văn bản (ví dụ ở đầu mỗi mục, hoặc trong phụ lục mô tả nguồn số liệu) vai trò của từng notebook, tránh người đọc nhầm lẫn các bảng có vẻ trùng nhau:
- `pga-vs-unet2d-r512.ipynb` → so sánh PGA-UNet vs U-Net **cùng kích thước 512**.
- `test-pga-samzs-samft-r256.ipynb` → so sánh PGA-UNet vs SAM-Med2D **chưa fine-tune (zero-shot)** và **đã fine-tune**, cùng kích thước 256.
- `test-subcat-pga-vs-baseline.ipynb` → so sánh PGA-UNet vs U-Net theo **subcategory** (ảnh U-Net tin cậy nhất/kém nhất), ở 512.
- `test-subcat-pga-vs-sam-r256-r512.ipynb` → so sánh PGA-UNet vs SAM-Med2D fine-tuned theo 3 loại tổn thương (nhỏ/mờ/rõ): SAM-Med2D chỉ ở 256 (để so cùng cấp), PGA-UNet có cả 256 và 512 (để chứng minh lợi thế train tùy ý kích thước không bị resize quá mức, khác với SAM-Med2D vốn cố định 256 và rất khó mở lên 512).

**D.7 — Bổ sung so sánh PGA-256 vs PGA-512**
Hiện không có notebook riêng cho so sánh này, nhưng dữ liệu đã có sẵn trong `pga-vs-unet2d-r512.ipynb` (PGA-512) và `test-pga-samzs-samft-r256.ipynb` (PGA-256) — có thể cắt/khớp số liệu từ hai file này để dựng một bảng so sánh PGA-256 vs PGA-512, làm rõ luận điểm: PGA-UNet có thể train lại tùy ý ở độ phân giải cao hơn (512) mà không bị giới hạn kiến trúc như SAM-Med2D (vốn cố định 256, khó mở rộng).

**D.8 — Áp dụng cùng cấu trúc mapping notebook cho phần FracAtlas (mục 4.4.2–4.4.5)**
Thư mục `Result/Result_FracAtlas/` chứa đúng 4 notebook cùng tên với BTXRD: `pga-vs-unet2d-r512.ipynb`, `test-pga-samzs-samft-r256.ipynb`, `test-subcat-pga-vs-baseline.ipynb`, `test-subcat-pga-vs-sam-r256-r512.ipynb`. Vì vậy phần FracAtlas (mục 4.4) nên chia thành 4 mục con 4.4.2–4.4.5, mirror đúng logic đã áp dụng cho BTXRD ở D.6:
- 4.4.2 PGA-UNet vs U-Net cùng kích thước 512 (từ `pga-vs-unet2d-r512.ipynb`).
- 4.4.3 PGA-UNet vs SAM-Med2D (zero-shot & fine-tuned) cùng kích thước 256 (từ `test-pga-samzs-samft-r256.ipynb`) — áp dụng luôn D.3 (bỏ HD95, format gọn) cho bảng này.
- 4.4.4 PGA-UNet vs U-Net theo subcategory (ảnh tin cậy nhất/kém nhất), ở 512 (từ `test-subcat-pga-vs-baseline.ipynb`).
- 4.4.5 PGA-UNet vs SAM-Med2D fine-tuned theo 3 loại tổn thương (nhỏ/mờ/rõ): SAM-Med2D chỉ ở 256, PGA-UNet có cả 256 và 512 (từ `test-subcat-pga-vs-sam-r256-r512.ipynb`) — cùng luận điểm về lợi thế train tùy ý kích thước như D.6.

Lưu ý khác biệt: FracAtlas **không có** notebook tương đương cho đánh giá chéo 4-fold (`test-pga-dataset-1234.ipynb`), Gatekeeper (`efficientnet-b3.ipynb`), hay pipeline end-to-end (`test-pipeline-evaluation.ipynb`) — thư mục `Result_FracAtlas/Ablation/` hiện cũng đang trống. Ba phần này (4-fold CV, Gatekeeper, pipeline) chỉ tồn tại ở BTXRD và không cần ép vào phần trình bày FracAtlas; nếu muốn có ablation trên FracAtlas thì đây là hạng mục thực nghiệm còn thiếu (bổ sung vào Kế hoạch lớn C nếu còn thời gian).

**D.9 — Rà soát toàn bộ Chương 4 sau khi tái cấu trúc**
Sau khi áp dụng D.1–D.8, đọc lại toàn chương để đảm bảo không còn mục nào lặp ý (như tình trạng 4.2.3/4.2.4 ban đầu), cấu trúc 4.4.x (FracAtlas) phản ánh đúng song song với 4.2.x (BTXRD), và mỗi bảng/mục đều có thể truy ngược về đúng notebook nguồn.

---

## KẾ HOẠCH LỚN E: Sửa lỗi trình bày hình thức toàn khóa luận

**E.1 — Chuyển đề cương khóa luận vào phụ lục**
Phần "ĐỀ CƯƠNG KHOÁ LUẬN TỐT NGHIỆP" hiện nằm ngay sau lời cảm ơn, trước mục lục — không nên xuất hiện như một chương/phần chính. Chuyển toàn bộ vào phụ lục.

**E.2 — Sửa ngôi xưng trong lời cam đoan**
Hiện ghi "Tôi xin cam đoan..." dù khóa luận do hai sinh viên thực hiện. Sửa thành "Chúng tôi xin cam đoan đây là công trình nghiên cứu của nhóm...".

**E.3 — Thống nhất thuật ngữ "khóa luận" (bỏ "luận văn")**
Lời cam đoan hiện dùng "luận văn" — dễ gây nhầm với luận văn thạc sĩ. Rà soát toàn văn bản, thống nhất dùng "khóa luận".

**E.4 — Chuẩn hóa đánh số trang phần đầu**
Trang bìa thứ hai hiện hiển thị số trang "2" (trang bìa thường không đánh số hiển thị), sau đó chuyển sang số La Mã cho lời cam đoan/cảm ơn/đề cương/mục lục. Chuẩn hóa lại theo quy ước: trang bìa không số, phần mở đầu số La Mã, nội dung chính số Ả Rập.

**E.5 — Gộp hệ thống tài liệu tham khảo thành một danh mục duy nhất**
Phần đề cương hiện có danh mục tài liệu tham khảo riêng (chỉ vài mục, đánh số lại từ [1]) tách biệt với danh mục đầy đủ ở cuối khóa luận — gây rối trích dẫn (đề cương trích [7][8][9] nhưng danh mục ngay sau chỉ có [1]-[4]). Bỏ danh mục riêng trong đề cương (đã chuyển vào phụ lục theo E.1), chỉ giữ một danh mục thống nhất ở cuối.

**E.6 — Sửa lỗi encoding/ký tự lạ toàn văn bản**
Nhiều chỗ lỗi font: "X￾quang", "PGA￾UNet", "end-to￾end", "256Ö256", "512Ö512", "PGAö512". Kiểm tra lại font, LaTeX encoding, gói tiếng Việt, ký hiệu nhân "×", và cách ngắt dòng/gạch nối.

**E.7 — Sửa tên đề tài khóa luận**
Tên hiện tại "Phát triển hệ thống phân đoạn ảnh X-quang về xương dựa vào câu nhắc trực quan" — cụm "ảnh X-quang về xương" không tự nhiên. Đề xuất: "Phát triển hệ thống phân đoạn tổn thương xương trên ảnh X-quang dựa trên câu nhắc trực quan" (hoặc ngắn hơn: "Phân đoạn tổn thương xương trên ảnh X-quang dựa trên câu nhắc trực quan").

**E.8 — Rút gọn caption hình/bảng**
Nhiều caption dài như một đoạn văn và lồng cả kết luận nhân quả (ví dụ Hình 4.7: "Đường biên bám sát GT nhờ cơ chế Prompt Spatial Gate và Conditioned Attention"). Viết lại caption ngắn gọn, chỉ mô tả nội dung hình/bảng; phần diễn giải nhân quả để trong văn bản phân tích.

**E.9 — Chuẩn hóa thuật ngữ Anh–Việt**
Các cụm Gatekeeper, pipeline end-to-end, image-level, baseline comparison, robustness, sub-category, cross-dataset, prompt-guided, zero-shot, fine-tuned xuất hiện dày đặc và lẫn lộn. Quy tắc: lần đầu xuất hiện ghi tiếng Việt kèm tiếng Anh trong ngoặc, sau đó dùng nhất quán một cách gọi. Ví dụ: "đánh giá liên bộ dữ liệu" thay cho "cross-dataset", "đánh giá theo ảnh" thay cho "image-level", "đường ống xử lý đầu cuối" (hoặc thống nhất "pipeline đầu cuối").

**E.10 — Viết lại tiêu đề mục Chương 4 theo văn phong khóa luận**
Nhiều tiêu đề hiện mang dáng dấp bài báo (Baseline Comparison, Robustness, SOTA Prompt-based, Cross-dataset, Sub-Category). Viết lại theo mạch logic khóa luận (liên kết D.1): thiết lập dữ liệu → mô hình so sánh → chỉ số → kết quả chính → ablation → phân tích lỗi → đánh giá pipeline.

**E.11 — Chuẩn hóa định dạng danh mục tài liệu tham khảo**
Hiện có URL tách kiểu "https : / / …", một số mục ghi "Truy cập năm 2025", một số ghi phiên bản, arXiv, DOI không đồng nhất. Chọn một chuẩn trích dẫn cụ thể (IEEE/ACM/APA) và áp dụng thống nhất cho toàn bộ danh mục.

**E.12 — Sửa văn phong một số cụm từ chưa chuẩn học thuật**
"module gác cổng" → "module sàng lọc"; "đánh giá toàn diện" → "đánh giá trên nhiều khía cạnh"; "mô phỏng điều kiện lâm sàng thực tế" → "mô phỏng một phần luồng xử lý lâm sàng"; "hệ thống đủ thông minh" → "hệ thống có khả năng hỗ trợ tương tác".

---

## THỨ TỰ ƯU TIÊN ĐỀ XUẤT

1. **Kế hoạch lớn B** (lỗi phương pháp đánh giá) — vì đây là lỗi học thuật nghiêm trọng nhất, ảnh hưởng trực tiếp đến tính đúng đắn của số liệu đã công bố.
2. **Kế hoạch lớn A** (hạ mức claim) — sửa nhanh, rủi ro phản biện cao nếu bỏ qua, không cần thêm thực nghiệm.
3. **Kế hoạch lớn D** (tái cấu trúc Chương 4) — cải thiện rõ rệt tính mạch lạc, mức độ ưu tiên cao vì đây là chương trọng tâm.
4. **Kế hoạch lớn E** (lỗi trình bày hình thức) — dễ sửa, nên làm song song, ảnh hưởng điểm hình thức.
5. **Kế hoạch lớn C** (bổ sung thực nghiệm) — tốn thời gian nhất; ưu tiên theo khả năng còn lại: C.1 (kiểm định thống kê) và C.3/C.4 (ablation bổ sung) khả thi nhất trong thời gian ngắn; C.6/C.9 (cross-dataset thật sự, đánh giá liên chuyên gia) có thể ghi vào phần hạn chế nếu không kịp thực hiện.
