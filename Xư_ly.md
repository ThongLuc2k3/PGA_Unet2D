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

Phạm vi đã được rút gọn theo quyết định của người dùng: bỏ C.3, C.5, C.6, C.7 (ban đầu), C.9 (xem lý do ở mục "Đã bỏ khỏi phạm vi" bên dưới); C.4 đổi hướng thành sửa report thay vì thêm ablation; C.8 sau đó được khôi phục lại thành C.14. **Còn lại 9 mục active: C.1, C.2 ✅, C.4 (dạng mới), C.10, C.11, C.12, C.13 ✅, C.14 (mới), C.15 (mới).** Khác với A/B/D/E (chủ yếu sửa văn bản), phần lớn nhóm C còn lại là **thực nghiệm thật** — cần chạy notebook, GPU (Kaggle/Colab). Xếp theo độ sẵn sàng (dễ → khó) để tiện ước lượng công sức trước khi bắt đầu.

### Nhóm 1 — Chỉ chạy lại code có sẵn, đổi dataset (dễ nhất)

**C.10 — Chạy Ablation (V1→V5 tương đương) trên FracAtlas** *(ưu tiên cao nhất toàn nhóm C)*
Hiện thư mục `Result/Result_FracAtlas/Ablation/` đang trống (đã xác nhận lại), trong khi BTXRD đã có đủ ablation V1–V5. Chạy lại đúng bộ biến thể kiến trúc (U-Net / +PSG / +CAD / +PSG+CAD binary / +PSG+CAD Gaussian) trên FracAtlas để chứng minh đóng góp của PSG/CAD/Gaussian không chỉ đúng trên BTXRD mà còn giữ nguyên trên domain khác — trực tiếp củng cố claim tổng quát hóa của kiến trúc (A.3).
*Chuẩn bị:* không cần code mới — copy 4 notebook trong `Result/Result_BTXRD/Ablation/` (test-v1 đến v4) + notebook PGA gốc, đổi đường dẫn dataset sang FracAtlas, chạy trên GPU. Mỗi biến thể vài chục phút train + test (573 ảnh train FracAtlas), 5 lần chạy.

**C.11 — Train Gatekeeper + đánh giá Pipeline end-to-end trên FracAtlas** *(ưu tiên cao thứ hai)*
BTXRD có `efficientnet-b3.ipynb` (Gatekeeper) và `test-pipeline-evaluation.ipynb` (pipeline end-to-end); FracAtlas hiện chưa có notebook tương đương. Đây là bổ sung trả lời trực tiếp điểm yếu bị phê bình nặng nhất: pipeline/Gatekeeper mới chỉ được validate trên một dataset (A.3 và mục B toàn bộ).
*Chuẩn bị:* copy `efficientnet-b3.ipynb` + `test-pipeline-evaluation.ipynb` từ Result_BTXRD, đổi dataset. **Điều kiện tiên quyết cần kiểm tra trước:** FracAtlas gốc (trước khi cắt ra làm bài toán segmentation) có nhãn "fracture/no-fracture" ở cấp ảnh hay không — nhiều khả năng có vì FracAtlas gốc là bộ phân loại gãy xương; nếu không có sẵn thì phải tự gán nhãn.

**C.12 — Chạy 4-fold cross-validation trên FracAtlas** *(ưu tiên thấp nhất trong nhóm 1, chỉ làm nếu còn thời gian)*
BTXRD có `test-pga-dataset-1234.ipynb` (4-fold CV, tương ứng Bảng 4.8/4.9); FracAtlas chưa có. Vì train set FracAtlas khá nhỏ (573 ảnh) và mục tiêu chính của 4-fold là củng cố độ ổn định của claim chính (đã chứng minh trên BTXRD), làm thêm trên FracAtlas là "có thì tốt" chứ không bắt buộc — chỉ nên làm sau khi đã hoàn thành C.10 và C.11.

**C.1 — Kiểm định thống kê chính thức** 🔁 THU HẸP PHẠM VI
Ban đầu định làm Wilcoxon cho toàn bộ bảng so sánh chính (4.2–4.7, 4.14, 4.18), nhưng đã quyết định: **chỉ đáng làm cho cặp có chênh lệch sát nhau** — các cặp PGA vs SAM-Med2D/U-Net chênh lệch quá lớn (10-30 điểm % Dice), kiểm định chỉ xác nhận lại điều đã rõ, không cần làm.
*Phát hiện quan trọng:* rà lại toàn bộ CSV kết quả hiện có (test-pga-samzs-samft-r256.ipynb, Ablation V1-V4, pga-vs-unet2d-r512.ipynb...) thì **chỉ lưu số liệu trung bình theo kịch bản, không lưu Dice/IoU từng ảnh** — không đủ để chạy Wilcoxon (cần dữ liệu ghép cặp per-image). Máy hiện tại cũng không có sẵn dataset/checkpoint để tự chạy lại suy luận.
*Kế hoạch mới:* kiểm định Wilcoxon chính thức **chỉ chạy cho 1 cặp — U-Net+Concat (Gaussian) vs U-Net+Binary** (xem ghi chú mới ở D.4), đây là cặp "sát nhau, đáng ngờ" thay cho V4 cũ. Đã xác nhận riêng: **PGA-UNet vs U-Net (Δ=38 điểm % Dice) và PGA-UNet vs SAM-Med2D (Δ=10-30 điểm %) không cần kiểm định** — chênh lệch quá lớn so với N=187, kiểm định chỉ xác nhận lại điều đã rõ.

*Cập nhật đánh số (xem D.4):* biến thể mới không còn tên "V4" nữa — đã đổi thành **V5** (V4 gốc giữ nguyên, không đụng). File cần chạy giờ là `test-v5-nopsg-nocad-binary.ipynb`, không phải `test-v4-nopsg-nocad-binary.ipynb`.

**Đã bổ sung xong export CSV per-image** (`results/..._per_image.csv`) — không chỉ V1-V3 + PGA@512 như dự tính ban đầu, mà **toàn bộ V1, V2, V3, V4 gốc** (thêm cả V4 để phòng khi cần) + V5 mới, ở **cả 2 dataset** (BTXRD và FracAtlas) và **cả 3 folder test** (`Source/File_Test/Ablation`, `Result/Result_BTXRD/Ablation`, `Result/Result_FracAtlas/Ablation`):
- test-v1-nopsg-nocad-concat.ipynb (đã có checkpoint sẵn)
- test-v2-psg-only.ipynb (đã có checkpoint sẵn)
- test-v3-cad-only.ipynb (đã có checkpoint sẵn)
- test-v4-full-binaryprompt.ipynb (đã có checkpoint sẵn — V4 gốc, giữ nguyên)
- test-v5-nopsg-nocad-binary.ipynb (mới — **cần train trước**, xem D.4)
- `Result/Result_BTXRD/pga-vs-unet2d-r512.ipynb` (đã có checkpoint sẵn, chỉ export phần PGA-UNet)

Lý do thêm cả V2/V3/V4/PGA@512 dù hiện tại chỉ kiểm định V1 vs V5: dữ liệu per-image có sẵn phòng khi cần kiểm định thêm cặp khác sau này (PSG-alone, CAD-alone, PGA vs CAD-only...) mà không phải sửa notebook lại từ đầu — chi phí thêm gần như bằng 0 vì đã có checkpoint, chỉ tốn thời gian chạy lại suy luận (không train).

**Việc còn lại của người dùng:** (1) train `V5_NoPSG_NoCAD_Binary.ipynb` (BTXRD) và `V5_NoPSG_NoCAD_Binary_FracAtlas.ipynb` (FracAtlas) trên Colab/Kaggle → upload checkpoint lên Drive → điền `CKPT_ID` vào `test-v5-nopsg-nocad-binary.ipynb` tương ứng; (2) chạy lại các notebook test còn lại (chỉ cần chạy lại suy luận, không train) để có đủ file `*_per_image.csv`; (3) đưa file CSV cho tôi — tôi viết đoạn `scipy.stats.wilcoxon` và cập nhật lại Bảng ablation + Hình 4.x trong Chapter 4.

### Đã bỏ khỏi phạm vi (quyết định của người dùng)

**C.3, C.5, C.6, C.7, C.8, C.9 — BỎ, không làm.** Lý do từng mục:
- **C.3** (ablation prompt ngẫu nhiên/sai vị trí): bỏ — PGA-UNet vận hành trong phạm vi câu nhắc cho phép (thiết kế đã giới hạn phạm vi sai lệch câu nhắc hợp lý), không cần chứng minh với 2 kịch bản cực đoan này.
- **C.5** (baseline U-Net+bbox channel...): bỏ — **đã có sẵn**, chính là biến thể U-Net+Concat (V1 cũ) trong ablation hiện tại (Bảng ablation kiến trúc, D.4), không cần làm thêm.
- **C.6** (cross-dataset generalization thật, train 1 dataset → test thẳng dataset kia): bỏ — BTXRD (u xương) và FracAtlas (gãy xương) là hai loại tổn thương khác biệt về hình thái, phép thử zero-shot liên miền kiểu này không phù hợp/không có ý nghĩa giữa 2 domain quá khác nhau.
- **C.7** (confidence interval, external validation): bỏ — chưa cần thiết ở mức độ khóa luận đại học.
- **C.8** (bổ sung nhiều ảnh minh họa định tính): bỏ — chưa cần thiết ở mức độ khóa luận đại học.
- **C.9** (đánh giá liên chuyên gia): bỏ — cần người thật (nhiều bác sĩ), ngoài khả năng thực hiện.

**C.4 — Ablation tiền xử lý** 🔁 ĐỔI THÀNH: **Xóa nội dung tiền xử lý ảnh khỏi báo cáo**
Không làm ablation tiền xử lý nữa. Lý do: hướng thực nghiệm mới sẽ chạy trực tiếp trên **dataset gốc, không qua bước tiền xử lý xóa nhiễu/xóa ký hiệu R/L** (YOLOv11s + Roboflow) như trước. Vì vậy nhiệm vụ C.4 đổi thành: rà soát và **xóa/viết lại mọi nội dung mô tả bước tiền xử lý này** trong báo cáo (Chapter3 — mục tiền xử lý, `fig:preprocessing_pipeline`, `subsec:preprocessing_pipeline`; Chapter1 — nếu có nhắc; Appendix/decuong.tex — Giai đoạn 2 "Gán nhãn hộp giới hạn vùng nhiễu qua Roboflow, tinh chỉnh YOLOv11s..."), vì bước này không còn phản ánh đúng quy trình thực nghiệm mới. **Đây là việc sửa report + chạy lại thực nghiệm trên dataset gốc, không phải bổ sung ablation — chỉ thực hiện sau khi có kết quả train lại trên dataset gốc.**

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

**C.15 — Cập nhật lại ảnh sơ đồ pipeline (`pipeline_pga_app_inference`)** *(nhiệm vụ mới)*
Ảnh `Report/images/pipeline_pga_app_inference.png` hiện dùng trong report đang **lỗi thời**, vẽ theo thiết kế "bộ chặn cứng tự động" cũ (Gatekeeper tự động rẽ nhánh, không có bước bác sĩ xác nhận) — mâu thuẫn trực tiếp với văn bản Chapter 3 đã mô tả thiết kế "triage mềm" hiện tại. File nguồn `diagrams/pipeline_pga_app_inference.drawio` đã được cập nhật đúng logic mới (bác sĩ luôn xác nhận, bbox chỉ vẽ sau khi xác nhận có bệnh, **và có thêm nhánh cho phép bác sĩ override khi Gatekeeper báo "Không bệnh" nhưng bác sĩ vẫn nghi ngờ muốn tự thử phân đoạn** — đã sửa lại phần nối dây bị đứt gãy trong file drawio để nhánh này hoạt động đúng).
*Việc cần làm:* mở file `.drawio` bằng draw.io/diagrams.net, kiểm tra lại trực quan (máy hiện không có công cụ export drawio→PNG), Export as PNG đè lên `Report/images/pipeline_pga_app_inference.png`, rồi rebuild PDF để kiểm tra khớp với văn bản Chapter 3.

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

**Trạng thái: ⏳ CHỜ THỰC NGHIỆM MỚI** — V5 "U-Net+Binary" chưa từng được train (cả BTXRD và FracAtlas), cần train trước khi sửa Bảng~`tab:ablation_arch`, Hình~`fig:chart_ablation` (sẽ thành 6 cột thay vì 5), và văn bản phân tích liên quan trong chapter4.tex. Notebook cần chạy:
- `Source/File_Train/Ablation/V5_NoPSG_NoCAD_Binary.ipynb` (BTXRD) và `V5_NoPSG_NoCAD_Binary_FracAtlas.ipynb` (FracAtlas) — train từ đầu, 100 epoch, patience 15, cùng hyperparameter với V1.
- `Result/Result_BTXRD/Ablation/test-v5-nopsg-nocad-binary.ipynb` và `Result/Result_FracAtlas/Ablation/test-v5-nopsg-nocad-binary.ipynb` — test sau khi có checkpoint (điền `CKPT_ID`).

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
- **Kế hoạch lớn C**: đã rút gọn phạm vi — bỏ C.3/C.5/C.6/C.7/C.8/C.9, đổi hướng C.4 thành sửa report. ❌ **Còn lại 7 mục active, chưa làm mục nào (0/7): C.1, C.2, C.4 (dạng mới), C.10, C.11, C.12, C.13.** C.1 đã chuẩn bị sẵn code/notebook (5 notebook đã thêm export CSV per-image), chỉ còn chờ người dùng train + chạy lại trên GPU.
- **Kế hoạch lớn D** (D.1–D.9): 🟡 **Gần hoàn tất, còn 1 phần treo** — D.1/D.2/D.3/D.5/D.6/D.7/D.8/D.9 xong; **D.4 phát sinh việc mới** (thay V4 cũ bằng biến thể "U-Net+Binary", cần train lại rồi mới sửa Bảng~`tab:ablation_arch`/Hình~`fig:chart_ablation` — xem chi tiết ở D.4 và C.1).
- **Kế hoạch lớn E** (E.1–E.12): Gần như hoàn tất —
  - ✅ Đã làm: E.2, E.3, E.4, E.6, E.8, E.9, E.10, E.11, E.12.
  - 🔁 Đã thay thế theo yêu cầu riêng của trường: E.1 (✅ đã làm phần thay thế — dịch thuật ngữ + phụ lục đối chiếu).
  - ❌ Bỏ hẳn theo quy định trường: E.5 (không gộp danh mục tham khảo, không làm cả phần thay thế).
  - ⏸️ Tạm hoãn: E.7 (đổi tên đề tài) — cần báo/xin phép trường trước, không tự sửa.

**Việc còn lại của toàn bộ kế hoạch, tổng hợp lại:**
1. **D.4 (việc mới phát sinh)** — train biến thể "V5 U-Net+Binary" cho cả BTXRD (`V5_NoPSG_NoCAD_Binary.ipynb`) và FracAtlas (`V5_NoPSG_NoCAD_Binary_FracAtlas.ipynb`), test bằng `test-v5-nopsg-nocad-binary.ipynb` tương ứng, rồi cập nhật lại bảng/hình ablation trong Chapter 4 (bảng sẽ có 6 hàng thay vì 5, V4 gốc vẫn giữ).
2. **C.1** — sau khi có V5 ở trên, chạy lại các notebook test còn lại (V1, V2, V3, V4, PGA@512 — chỉ suy luận, không train) để lấy đủ CSV per-image, đưa cho tôi tính Wilcoxon (U-Net+Concat vs U-Net+Binary).
3. **C.2 + C.13** — khảo sát related work + tìm bài báo có kiến trúc giống PSG/CAD/PGA (đọc/viết, làm được bất cứ lúc nào, không cần GPU).
4. **C.10** — chạy ablation (6 biến thể, gồm cả V5 U-Net+Binary mới) trên FracAtlas.
5. **C.11** — train Gatekeeper + đánh giá pipeline end-to-end trên FracAtlas.
6. **C.12** — 4-fold CV trên FracAtlas (ưu tiên thấp nhất, làm sau cùng nếu còn thời gian).
7. **C.4 (dạng mới)** — chờ có kết quả train lại trên dataset gốc (không tiền xử lý) rồi mới xóa nội dung tiền xử lý khỏi report.
8. **E.7** — chờ xác nhận đổi tên đề tài từ trường, sau đó mới sửa `\tenKL` trong main.tex.

(E.5 đã bỏ hẳn, không còn là việc tồn đọng.)
