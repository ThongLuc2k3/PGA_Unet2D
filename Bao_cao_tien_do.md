# Báo cáo tiến độ — PGA-UNet2D
**Ngày cập nhật:** 04/06/2026 | **Deadline nộp báo cáo:** 12/06/2026

---

## Hai đóng góp chính của đề tài

| | **Đóng góp 1 — Nghiên cứu** | **Đóng góp 2 — Sản phẩm** |
|---|---|---|
| **Nội dung** | PGA-UNet: kiến trúc phân đoạn mới dùng Gaussian heatmap prompt | Pipeline lâm sàng hoàn chỉnh end-to-end |
| **Kết quả chính** | Dice=0.8558 > SAM-Med2D Dice=0.7554 (+13.3%), 25× ít tham số | App hỗ trợ bác sĩ: sàng lọc → phân đoạn → tự sửa lỗi prompt |
| **Đánh giá** | 248 test samples, 3 kịch bản prompt, so sánh SAM fine-tuned + zero-shot | Hệ thống bán tự động, bác sĩ xác nhận trước khi phân đoạn |
| **Hạn chế thừa nhận** | Chỉ test trên 1 dataset (BTXRD) | Cascading error: MobileNet 88% × PGA 86% ≈ 66% tổng thể |

> **Tại sao tách 2 đóng góp?** Đóng góp 1 đánh giá PGA-UNet thuần túy (không qua MobileNet) → Dice 0.86 là số sạch, có thể so sánh công bằng với SAM. Đóng góp 2 mô tả hệ thống thực tế và thừa nhận giới hạn pipeline minh bạch.

---

## Phản hồi từ Meeting giảng viên (01/06/2026)

### ✅ Vấn đề 1 — Cơ sở lý thuyết heatmap (ĐÃ XỬ LÝ)
**GV hỏi:** *"Khái niệm bên trong quan trọng hơn bên ngoài không ở đâu có, tại sao tự nghĩ ra?"*

Đã bổ sung vào Chapter 3 (sec 3.3.1) hai đoạn:
- **Lý thuyết:** Binary mask tạo step edge → gradient giả tạo → mạng học cạnh hộp, không học đặc trưng tổn thương. Plateau Heatmap tạo transition mượt → phù hợp cơ chế tích chập.
- **So sánh SAM:** SAM dùng positional embedding rời rạc (2 vector 256d) → phù hợp Transformer. PGA dùng heatmap 2D → phù hợp U-Net feature map (nhân theo phần tử trực tiếp, không mất thông tin không gian).

---

### ✅ Vấn đề 2 — Fine-tune clarity (ĐÃ XỬ LÝ)
**GV hỏi:** *"Em fine-tune ở chỗ nào? Nếu chỉ fine-tune decoder thì không học được gì."*

Đã thêm subsection 3.3.4 vào Chapter 3 + bảng so sánh:

| | PGA-UNet | SAM-Med2D |
|---|---|---|
| Chiến lược | Huấn luyện **từ đầu** (không đóng băng gì) | Fine-tune từ pretrained ViT-B |
| Encoder | U-Net CNN — toàn bộ học từ BTXRD | ViT-B pretrained 4M+ ảnh y tế |
| Tham số | ~4M (tất cả tham gia backprop) | ~100M |
| Epoch hội tụ | 60 | 12 |

---

### ✅ Vấn đề 3 — So sánh SAM "khập khiễng" (ĐÃ XỬ LÝ)
**GV chỉ ra:** *"So sánh model đã fine-tune với SAM zero-shot là không công bằng."*

Đã chạy `SAMMed2D_ZeroShot.ipynb` → bảng so sánh 3 hàng công bằng:

| Model | Dice (mixed_7_3) |
|---|---|
| **PGA-UNet** | **0.8558** |
| SAM-Med2D fine-tuned | 0.7554 |
| SAM-Med2D zero-shot | 0.5289 |

---

### ⚡ Vấn đề 4 — Cascading error (GIẢI PHÁP: Tách 2 đóng góp)
**GV chỉ ra:** *"MobileNet sai 12%, độ chính xác cuối chỉ còn 0.86 × 0.88 ≈ 66%."*

Giải pháp áp dụng:
- **Chapter 4 (Đóng góp 1):** Đánh giá PGA-UNet độc lập trên 248 mẫu *đã có bệnh* → Dice=0.8558 (không qua MobileNet, số sạch).
- **Chapter 4 (Đóng góp 2):** MobileNetV4 đạt AUC-ROC=0.9514, Accuracy=85.77%. Ghi nhận giới hạn pipeline và đề xuất cải thiện classifier là hướng phát triển tương lai.

---

### ✅ Vấn đề 5 — Báo cáo, code, dữ liệu (ĐÃ NỘP 01/06/2026)
- Báo cáo đúng format, ghi rõ đóng góp / kế thừa
- Source code + documentation đã gửi
- Google Drive: `https://drive.google.com/drive/folders/1OP8RgnqKwXyYOP_NQf8B_u7E3lpiGJ-m`

---

## Trạng thái nhiệm vụ

### ✅ Đã hoàn thành
| Nhiệm vụ | Ghi chú |
|---|---|
| Nộp hồ sơ GV | 01/06/2026 |
| Số liệu 4 mô hình | Dice/IoU/HD95/CBL đầy đủ |
| SAM zero-shot comparison | 248 samples, 3 modes |
| MobileNetV4 evaluation | AUC-ROC=0.9514, ảnh confusion matrix có sẵn |
| Lý thuyết heatmap (Chapter 3) | Cơ sở + so sánh SAM — sec 3.3.1 |
| Fine-tune clarity (Chapter 3) | Subsection 3.3.4 + bảng chiến lược |

### ✅ Mới hoàn thành (02/06/2026)
| Nhiệm vụ | Ghi chú |
|---|---|
| 3 sơ đồ diagrams | PNG export xong, đã `\includegraphics` trong chapter3.tex |
| `SubCat_PGA_vs_SAM.ipynb` fix | Sửa lỗi `ImportError: build_sam` trên Kaggle (sys.modules cache clear) |

### ✅ Mới hoàn thành (03/06/2026)
| Nhiệm vụ | Ghi chú |
|---|---|
| `subsec:cascading_error` — Phân tích sai số tích lũy | Lý thuyết: 89.64%×85.58%≈76.7%; thực nghiệm đang chuẩn bị — chapter4.tex |
| Chapter 5 — Viết lại toàn bộ kết luận + hướng phát triển | 4 hướng cụ thể: cải thiện gác cổng, Unified Model, Multi-prompt, đa tập — chapter5.tex |
| Extract + đặt tên ảnh từ Result notebooks | 41 ảnh → Report/images/, xóa trùng/orphaned, còn 54 files sạch |
| Fix 5 ablation notebooks | Xóa `verbose` (PyTorch≥2.2), `leave=True`, print mỗi epoch, lưu Drive, visualization cell 5 cột |

### 🖼️ Chính sách ảnh trong báo cáo (chốt 03/06)
- **KHÔNG thêm ảnh minh chứng mới** vào report — đã đủ `vis_pga/attunet/unet/sam` hiện có
- **CHỈ thêm** sơ đồ kiến trúc hoặc workflow mới nếu cần giải thích kỹ thuật
- Report dùng khoảng **15–20 ảnh** (số liệu + 2–3 vis đại diện mỗi mô hình + biểu đồ tổng hợp)

### 📚 Bổ sung tài liệu tham khảo (chờ bạn cung cấp PDF/link)
| Tên | Trạng thái | Ghi chú |
|---|---|---|
| **SAM** — Segment Anything, Kirillov 2023 | ⏳ Chờ PDF | Nhắc tên trong Ch.1, Ch.3 chưa có cite |
| **YOLOv11** — Ultralytics 2024 | ⏳ Chờ link | Dùng Ch.3, Ch.4 chưa có cite |
| **Roboflow** | ⏳ Chờ link | Dùng Ch.3 chưa có cite |
| **BTXRD** | ⏳ Chờ bổ sung | Đã có entry placeholder trong bib |

### ✅ Mới hoàn thành (03/06/2026 — tối)
| Nhiệm vụ | Ghi chú |
|---|---|
| Fix references.bib — tác giả đúng từ PDF | SAM-Med2D: Junlong Cheng; BTXRD: Shunhan Yao et al. |
| Thêm YOLOv11 + Roboflow vào bib + cite trong tex | Link chính thức |
| **main.pdf compile không lỗi** | 3.8 MB — LaTeX sạch |
| Submission tái cấu trúc 5 folder + .tex + main.tex | Sẵn sàng compile ra PDF gửi thầy |
| GVHD điền đúng: PGS.TS. Lý Quốc Ngọc & ThS. Đỗ Thị Thanh Hà | Trong Report + Submission |
| V1–V5 ablation notebooks fix hoàn chỉnh | 3-mode eval, vis inline, không Drive |

### ✅ Mới hoàn thành (04/06/2026)
| Nhiệm vụ | Ghi chú |
|---|---|
| **Dataset ID** sửa toàn bộ 31 notebooks | ID mới: `1X1SY8T63pdBPIdrv_3P0gKVwoLxCa5sW` |
| **02_Minh_Chung_So_Lieu** reset về ⏳ | Toàn bộ số liệu chờ chạy lại với dataset mới |
| **chapter4.tex** reset ablation V1–V5 về \textit{chờ} | Chờ kết quả mới |
| **03_Minh_Chung_Hinh_Anh** tái cấu trúc | 25 ảnh, chia Phần I/II, ảnh nhúng inline |

---

## 🔴 NHIỆM VỤ CẦN CHẠY NGAY (deadline 12/6 — còn 8 ngày)

> Dataset đổi sang `1X1SY8T63pdBPIdrv_3P0gKVwoLxCa5sW` — tất cả số liệu cũ không còn hợp lệ, chạy lại toàn bộ.  
> **Tổng cộng 18 notebooks** trong `Source/`, chia 3 nhóm theo thứ tự phụ thuộc.

---

### 🟢 Nhóm 1 — Chạy song song ngay, không phụ thuộc nhau (10 notebooks)

| # | Notebook | Mục đích | Output cần lấy |
|---|---|---|---|
| 1 | `Unet2D.ipynb` | Train + test U-Net baseline (không prompt) | Dice/IoU/HD95/CBL × 1 mode, epoch dừng, best val Dice |
| 2 | `Attention_Unet2D.ipynb` | Train + test Attention U-Net baseline (không prompt) | Dice/IoU/HD95/CBL × 1 mode, epoch dừng, best val Dice |
| 3 | `PGA_Unet2D.ipynb` | **Train + test PGA chính (V5)** — bao gồm cross-validation seed mới | Dice × 3 mode, epoch dừng, best val Dice |
| 4 | `Finetune_SAMMed2D_test_robust.ipynb` | Fine-tune SAM-Med2D trên BTXRD + test 3 mode | Dice × 3 mode, epoch dừng |
| 5 | `SAMMed2D_ZeroShot.ipynb` | Test SAM-Med2D zero-shot (không fine-tune) | Dice × 3 mode |
| 6 | `Ablation/V1_NoPSG_NoCAD_Concat.ipynb` | Train + test V1: concat heatmap đơn giản, không PSG không CAD | Dice × 3 mode, best val Dice |
| 7 | `Ablation/V2_PSG_Only.ipynb` | Train + test V2: chỉ có PSG ở encoder, decoder thường | Dice × 3 mode, best val Dice |
| 8 | `Ablation/V3_CAD_Only.ipynb` | Train + test V3: chỉ có CAD ở decoder, encoder thường | Dice × 3 mode, best val Dice |
| 9 | `Ablation/V4_Full_BinaryPrompt.ipynb` | Train + test V4: PSG+CAD đầy đủ nhưng dùng binary bbox thay heatmap | Dice × 3 mode, best val Dice |
| 10 | `MobileNetV4_BTXRD_dataset.ipynb` | Train + test MobileNetV4 phân lớp gác cổng (có bệnh / không bệnh) | Accuracy/Recall/Precision/F1/AUC-ROC |

> **Lưu ý #3 và #6–#9:** `Ablation/V5_Full_HeatmapPrompt.ipynb` là bản ablation reference của PGA_Unet2D — kiến trúc giống hệt nhau. Dùng checkpoint từ `PGA_Unet2D.ipynb` (#3) làm V5, **không cần chạy V5 riêng**.

---

### 🟡 Nhóm 2 — Chờ checkpoint PGA từ #3 xong (2 notebooks)

| # | Notebook | Mục đích | Phụ thuộc |
|---|---|---|---|
| 11 | `PGA_Ablation.ipynb` | Ablation loại câu nhắc: empty / noise / hard bbox / plateau heatmap / oracle GT | PGA checkpoint (#3) |

> `PGA_Extended_Test.ipynb` — load checkpoint PGA và chạy test + visualization bổ sung. Chạy sau #3 nếu cần ảnh minh chứng thêm, **không bắt buộc** cho số liệu báo cáo.

---

### 🔵 Nhóm 3 — Chờ đủ checkpoint PGA + baseline + SAM (#1–#5 xong) (3 notebooks)

| # | Notebook | Mục đích | Phụ thuộc |
|---|---|---|---|
| 13 | `SubCat_PGA_vs_Baseline.ipynb` | So sánh PGA vs U-Net/AttUNet theo nhóm dễ/khó | PGA (#3) + UNet (#1) + AttUNet (#2) ckpt |
| 14 | `SubCat_PGA_vs_SAM.ipynb` | So sánh PGA vs SAM theo nhóm nhỏ/mờ/rõ nét | PGA (#3) + SAM (#4) ckpt |

> `Test_app.ipynb` — test end-to-end app.py Gradio với tất cả checkpoints. Chạy **sau cùng** khi đã có đủ mọi checkpoint, mục đích demo sản phẩm, không lấy số liệu báo cáo.

### Đóng góp 2 — Ghi chú
- **Ảnh không bệnh** (GV hỏi): Thuộc Đóng góp 2 — xử lý bởi MobileNetV4 gatekeeper (AUC-ROC=0.9514). PGA chỉ nhận ảnh có bệnh đã qua lọc. Ghi rõ trong chapter4.tex là đủ.
- **Cascading error**: 89.64%×85.58%≈76.7% tổng thể — đã thừa nhận, tách rõ Đóng góp 1 (Dice=0.8606 số sạch) và Đóng góp 2 (pipeline end-to-end).

---

## Kết quả thực nghiệm chốt

### Phân đoạn

| Model | Mode | Dice↑ | IoU↑ | HD95↓ | CBL↑ | N |
|---|---|---|---|---|---|---|
| U-Net 2D | — | 0.5090 | 0.4125 | 125.12px | 0.6457 | 187 |
| Att U-Net 2D | — | 0.4110 | 0.3212 | 141.23px | 0.5917 | 187 |
| **PGA-UNet** | zoom_out | **0.8606** | **0.7619** | **12.16px** | **0.9558** | 248 |
| **PGA-UNet** | mixed_7_3 | **0.8558** | **0.7552** | **12.79px** | **0.9532** | 248 |
| SAM-Med2D (fine-tuned) | mixed_7_3 | 0.7554 | 0.6325 | 51.84px* | 0.8997 | 248 |
| SAM-Med2D (zero-shot) | mixed_7_3 | 0.5289 | 0.3853 | 114.31px* | 0.8125 | 248 |

> `*` HD95 trên 256px. HD95/imgsize: PGA≈0.025 vs SAM fine-tuned≈0.204 → PGA chính xác biên **~8×** hơn.

### Phân lớp (MobileNetV4 Gatekeeper)

| Accuracy | Precision | Recall | F1 | AUC-ROC |
|---|---|---|---|---|
| 85.77% | 83.11% | 89.64% | 86.25% | **0.9514** |


nội dung cuộc họp trò chuyện:
Dưới đây là 100% toàn bộ nội dung cuộc họp được trích xuất nguyên bản từ đoạn ghi âm, không qua bất kỳ sự chỉnh sửa nào về văn phong hay ngữ pháp, và được trình bày trong định dạng Markdown (giống như 1 file .md) theo đúng yêu cầu của bạn:
dụng form á. [1]

Dạ. [1]

Thì như vậy sẽ mã hóa cái rồi em mã hóa cái chưa đúng không? Dạ đúng. [1]

Rồi mã hóa cái from này có gì khác trước không? [1]

Ờ được cái from nó sẽ là nó sẽ tạo một thành một cái headm càng vào sau bên bên trong chính giữa from thì nó headm nó càng càng mạnh để nó có thể ghép vào được trong cái [1]

bây giờ cái là nó chấm điểm hoặc là đánh vào [1]

rồi nó làm gì nữa? Nó sẽ tạo một cái headm headmap trên cái phone đó. Cái form nó dán giống như kiểu một ảnh nhưng mà nó là kiểu một headm [1]

headm là ở đâu ra cái người dùng á họ đưa cái from đó bằng cách nào [1]

họ đưa cái from là cái bao box từ baox đó nó sẽ là một cái headp là [2]

đúng không? Dạ đúng không là càng sâu vô trong cái form đó nó head càng sáng bên ngoài rìa của headmap bên ngoài rìa của from thì nó headmap nó càng yếu để nó add vô được cái map của đầu [2]

để em đầu Tôi [2]

em có ảnh [2]

bây giờ đang muốn biết nè thì gửi giúp em từ từ nè. [2]

Dạ đưa ảnh vô thì nó encoder thì thôi cái đó cũng dễ hiểu đi cho nó có nhiều khách encoder. Bây giờ chuyện thứ hai là đưa cái prom vô đưa cái vision prom vô thì nó mã hóa làm sao đó hiểu không chưa? Em em gửi những cái này đi để kiểm tra giờ nha. Em em gửi những cái cái này là nó nằm trong thực nghiệm hả? [2]

Dạ. [3]

Đâu thí dụ cái from của em [3]

dạ đây cái from đây khi from thì thì nó sẽ là tạo một cái headm thì càng xong [3]

không cái prom là em em người ta chỉ đóng b rồi làm sao em tạo ra hitmap hit map ý nghĩa nói gì [3]

dạ ban đầu người dùng sẽ chấm hai điểm như là hai điểm khúc này cái khúc này để [3]

rồi cái hit map này khác cái của sam chỗ nào cái cách mà mã hóa vision prom á của sam thế nào hiểu không em mã hóa sao [3]

em mà ban ban đầu á thì em ghép vô thì em thấy nó là [3]

không mà em em mã hóa sao nó khác cái của Sam với Sam 2D rồi đó [3]

mã hóa nó khác gì [4]

khác thì em không rõ tại Sam2D là bạn thấy đâu phương tán này [4]

tại vì ban đầu em muốn ghép vô thì nó sẽ gặp lỗi nên là em thấy khi mà cái ảnh nó tạo face map á thì nó sẽ face map giống kiểu headmap nên cái form nó không phải headmap chạm [4]

không có [4]

để em gửi cái báo cáo hôm nay với lại cái sụ tốt nè nha cái này cái sụ tốt đúng không [4]

dạ [4]

nó chứa những cái dữ liệu này nè để kiểm tra Tùng chắc ba tắt được ba cái bảo vệ là chết nó em gửi sự code với những cái hình ảnh vậy để kiểm tra XM tự em tạo ra là em dựa vào cái gì để ra XM? Dựa vào bài báo nào phí xuống vào bài báo nào để ra em thấy sai tới cái đó. [4]

Tại vì ban ban đầu là em tự nghĩ cũng một phần là em tự nghĩ ra tại vì ban đầu cái cái ảnh nó tạo ra f map nó kiểu tương tự vậy thầy. Kiểu [5]

đó là cái gì? Cái đó là cái [5]

cái map [5]

cái à cái này là của cái red cam nhưng mà cái này em để mình hỏa cái map của ảnh á khi mà ảnh nó [5]

của em là cái nào [5]

em? Trên đây tại của em [5]

từ ba box em ra em ra cái hit map ha. [5]

Dạ thì giống giống như kiểu là nó sẽ à cái h cái face map của ảnh nó sẽ là một cái headm nó mạnh ở vùng nào thì nó sẽ m cái vùng đó. [5]

Nhưng mà quan điểm của em hitmap là cái gì hiểu không? [5]

Dạ hitm là vùng chú ý mạnh. [6]

Ủa em đóng box. [6]

Dạ [6]

rồi trong đó em cái để tính ra được cái hitm truyền cái hàm nào. [6]

Ờ [6]

em nói hitm hit map là sao ai góp ý được phả không? [6]

Tại vì nó nhiều công thức để Tính hitmap mà không hiểu quan điểm hitmap của em là sao á. [6]

Kiểu càng sẽ ờ em cho nó là kiểu càng sau bên trong nó càng mạnh là kiểu tầm [6]

tại sao tại sao lại cái màu nóng thì nó lại ứng với thằng bên trong đâu có ai nói vậy đâu. [6]

Đâu đâu có làm sao mình chắc này mà để làm gì mới được. [6]

Ừ tại vì map để làm gì cho giai đoạn kế [6]

tại để cho nó lên được cái cái cái map của cái ảnh visual map [7]

ờ lộ được trên cái ph map là cái ảnh là cái ảnh khi mà kết thúc mà nó bắt đầu dự đoán rồi là nó sẽ dựa vào cái vùng mà cái vùng à map mạnh này để nó dự đoán ra. [7]

Nhưng mà khi ông bác sĩ ổ gợi ý ổng ổng nó quanh quẩn trong khu vực đóạ [7]

thì em lại từ cái đó em chuyển sang X map. [7]

Dạ. [7]

Và X map em quan điểm là cái thằng ở bên trong thì nó lại là quan trọng hơn thằng bên ngoài [7]

à quan trọng nhiều hơn nhưng mà thì cái khái niệm đó không ở đâu có tại sao l ra vậy? [7]

Còn cái thằng Sam nó làm sao [8]

nó nó lấy cái visual pro nó mã hóa làm sao em có nắm không nhớ không sao. em không coi trước những cái phương pháp mạnh trước. Thí dụ như nó thằng SAM gì đó nó cũng là Visom á thì nó lấy cái vùng đó nó mã hóa sao hiểu không? Hoặc là có những cái bài nó cũng dùng vis không có dùng Sam gì hết có cái bài nó dùng vis from riêng là ban đầu em dùng from á mà không có head map hoặc là head map có yếu thì cái nó dự đoán thì nó vẫn dự đoán theo cái mô hình ban đầu của cái góc [8]

nhưng mà em phải có cơ sở tự nhiên em đưa cái hệ pháp này Thì ra là cái ý nói muốn nói cái gì [9]

để để như mà khi bác sĩ [9]

là cái ý tự nhiên em bảo là cái vùng trung tâm là xem như là cái vùng quan trọng thì cái đó người ta bán ngay chỗ nhỏ [9]

không không phải vùng tâm là ý là càng cái prom á càng sâu vô bên trong thì nó càng hít mắt mạnh hơn thôi [9]

để cho nó [9]

để cho nó hiểu được cái tâm cái tâm cái tâm cần chú ý cái tâm chú ý nhiều hơn là những vùng lan lộ bên ngoài [9]

thì em phải nói cho ra câu chuyện chứ nói rồi bây giờ nó dùng cái đó đi nó làm gì tiếp [9]

bây giờ ảnh n đã mã hóa ra rồi Bây giờ prom thì nó chuyển sang BM chỉ là ảnh thôi. [10]

Dạ. Dạ. [10]

Rồi nó mã hóa rồi sao nữa? Rồi nó quyện lại như thế nào? [10]

Dạ nó quyện là nó trồng lớp lên nhau để cho cái bộ mình chữ đoán nó chú ý vùng này hơn để nó dự đoán nó tạo ra [10]

không có em lấy [10]

rồi em có một cái kết quả nếu mà em không dùng với em có dùng thì nó nhau gì có giống như cái của chưa em sử dụng như là của Unet m Unet khi không sử dụng from nó tự động thì nó chỉ có di 0.5 IU 0.4 và [10]

em thử trên tập nào [10]

em thử trên tập BTXRD đã xử lý những cái chữ C những cái nhà dở rồi. [11]

Dạ rồi còn an unit thì nó nó yếu hơn [11]

nhưng mà em vẫn scale ảnh xuống đúng không? [11]

Dạ keo xuống 5 4 ngàn mấy ba ngàn mấy keo xuống 200 mấy thôi. [11]

512 [11]

phải không? [11]

Dạ [11]

em tự ke xuống còn cái ngoài kia nó là 2 4 số 512 còn cái mô hình S2D á thì ban đầu là nếu như chen theo góc tác giả thì cái form nó vừa sát cái m quá hay là cái kết quả nó chen bị ảo nhưng mà khi test lên trên cái tập mà zom out rồi các thứ của em á kết quả nó 95 [11]

là à cái cái bao bao kích thước nó không có bị bung ra quá nhiều Sao em lên được hơn nó nhiều mà em có thể cho thấy một cái kết quả được sế này nó hơn là [12]

chắc là chắc là do domain map hoặc là cái tác giả sử dụng mô hình transformer hoặc mạnh quá kiểu nó không có [12]

tức là của em là có huấn luyện [12]

còn của tác giả là có huấn luyện vô chạy luôn có lại là là chân tập BTSRD và form [12]

không nhưng mà em vô tun hệ thống là chỗ nào tham số [12]

đóng đóng bảng chỉnh số của encoder chỉ tin decoder [12]

à có cái [12]

nếu mà em em chỉ file tool decoder thì không có file tun được cái gì [12]

giờ đây đóng đóng bằng chọm số file tun từ cái M deoder trở đi [13]

nhưng mà cái cách mà mã hóa R của ST M 2D là nó khác đúng không [13]

mã hóa của SAM R mã R á dạ của 2D là nó khác rồi. Chắc cái đó em sẽ tin kiểu là hiểu hiểu hiểu chưa? [13]

Dạ. [13]

Thành ra bây giờ khi em so này em muốn so cái gì đó là nó hơi [13]

so đầu tiên là so về [13]

của em là cái mã cái cái mã khóa prom nó khác nè. [13]

Dạ. [13]

Rồi cái deput rồi cái lúc em trộn cái chỗ email coder với cái prom á với prometer xong á thì em trộn bằng cách nào? Có giống như cái trộn vương này không? Dạ. Hiểu không? Dạ. [13]

Rồi cái decoder mình có giống không? Tại vì nếu á em nó tới ba công đoạn đúng không? Nó mã hóa nè bốn luôn main coder, pr coder rồi là fusion hai đng đó với nhau. Dạ [14]

rồi decoder để ra cái mas. [14]

Dạ. [14]

Đó thì mỗi cái đó nếu em soi với sum 2D với cái của em thì mỗi cái là kỹ thuật nó khác nhau. Dạ. [14]

Thì như vậy khi em ra mà hơn á thì thí dụ như là người ta sẽ thắc mắc không hiểu là công đoạn nào hiểu không? Công đoạn nào thật sự là nó đóng góp. Hiểu không? [14]

Dạ. [14]

Đây để em x [14]

thật ra nó hiện nay nó Nó nó nó hơi về cái mặt logic á nó hơi lộn xộn phải không? Em gửi đi em gửi cái báo cáo mới nhất với lại cái sụt code. Bây giờ phải kiểm tra sụt code luôn. Gửi cái sụt code vào mấy cái file ảnh mà chủ nghiệm á gửi hết cái gửi đi gửi liền đi giờ gửi có hai to tiếng chụ trước từ. [14]

Ờ [15]

rồi sao rồi giờ cuối cùng em ra bảo vệ cái gì? Cái kỹ của mình bảo vệ cái gì trong cái hệ thống của mình [15]

bảo vệ cái gì? Để là đầu tiên là chứng minh được là cái khi mà không sử dụng ch mình sử dụng ch đó có [15]

tại vì mình phải nộp cho chính xác tại vì 15 tâ này là phải báo khoa xác định cho những cái nào ra bảo vệ cái nào không đúng [15]

thành ra nếu cái nào mà mình không chấp thì tốt nhất là để làm sao không ra rớt là chết mất hết cái em tích lũy nó phải không [15]

chứ không phải ra rớt rồi là bảo vệ lại không có đâu nha [15]

thành ra phải nộp cho kỹ để coi lại nha đừng có nộp tèm lem cái báo cáo rồi sụt code rồi một cái file mô tả sụ code làm sao rồi những cái hình ảnh lúc nãy á nha để coi coi có ra bảo vệ được không để 15 này là phải báo cho khoa thì nếu mà cảm thấy không ổn thì là cứ để được sau để được sao ban đầu là em sẽ chứng minh là khi mà mô hình không [16]

bây giờ trong hệ thống của em đi thì em thấy em muốn rằng minh chứng cái gì nào tôi đưa vô tôi làm cho nó lên 0.86 Đầu tiên là khi mà kỹ thuật sự có sử dụng là cái quan trọng nhất. Khi mà không sử dụng mà có sử dụng phone kết quả nó sẽ khác biệt. Cái thứ hai là cái mô hình Sam 2D khi mà so sánh với mô hình Samm 2D á thì nó nó là mô hình lớn của luyện trinh [16]

Sam 2D là lấy từ bài nào tại vì nó nhiều bài [17]

mở cái bài báo xem là bài nào [17]

em gửi lại cái reference đó nha. Tại nó có hai ba á em mở đi em xem bài nào [17]

trời đó không có một cái bài sẵn Nữ tại em bỏ hết vô trong Google ray có nhóm á thầy mất kết đối mạng. Emp cái bài đó đưa đó m là m 2d [17]

à m sam là mô hình trên 2 á mô hình y tế nhưng mà là mô hình được file tin trên y tế nhưng mà sam m 2d là mô hình chỉ file tin riêng trên data 2D thôi m sam đó vừa có 3D vậ cái đó [17]

cái này thấy Tên của thầy nên nghĩ chắc có đúng [17]

chứ em xài bài nào rồi [18]

thầy nhiều nhiều bài [18]

bài nào em phải có [18]

dạ [18]

em phải chốt lại nha bây giờ hôm nay chốt lại để mà 15 báo cáo với khoa nè thứ nhất là cái thư mục reference của em những tài liệu nào em dùng cho luận văn em phải bỏ và không có vớ vẩn thấy không hiện nay là vớ vẩn nha hiện nay là không rõ em dùng tài liệu nào tại vì nếu mà mình xài phương pháp người ta mà mình không sai tới á là luận văn là ngay đây là cái li chính ph hợp là nó vẽ rớp dữ hiểu không là nó phạm vô cái lỗi đạo văn hiểu chưa thành ra cái thư vậc reference là để kiểm tra cái đậu văn hiểu không mình xài mình có sai tới của người ta không rồi thứ hai cái báo cáo của em nha báo cáo và cái sục cod hiểu không và file mô tả sụ cod em g chứ phải vứt cái code đó sao rồi những cái file bức ảnh giống nãy để kiểm tra vào mô tả Thôi em tự phát đi có dạ em tự phát anh ba đâu chỗ nào em coi nó chỗ nào xem coi nó chỗ nào em em hiểu nó như thế nào nó mã hóa r như thế nào có biết không biết nó mã hóa tại bạn cộng với em nó sẽ tìm hiển về cái thôi không được em nói chung là lộn xộn quá bây giờ dậy nha để góp ý với em rồi á em về phải làm thầy em phải gửi ngay cho nay nhé nh để 15 là Phải báo cáo với nhức khoa rồi đó. Nhất khoa cái nào không rõ là là thôi rồi là đợ sau đó v ba với bẩn cả cả hơn cả năm rồi giờ bớ bẩn là được. Chuyện thứ nhất nè là nộp cái báo cáo đúng không? [18]

Trong cái báo file báo cáo dĩ nhiên rồi nó có một cái file là mô tả cái phần đóng góp nha. Báo cáo là phải thay cái format của trường không phải viết với ba vẫn theo cái format của trường. Cái phần đóng góp là em đóng góp cái gì nói rõ ràng nha. Thứ hai là cái thư mục reference thì em chốt lại những cái tài liệu này em dùng cho luận vang nha. Theo đúng cái format là 5 nè. Tên bài bảo nè nha. Và trong cái này á em phải reference em dùng cái này em phải reference đúng lại nha. Hiểu không? [19]

Dạ. [19]

Thí dụ em có dùng cái ph gì đó thế kia mà cái kỹ thuật đó là em lấy đâu em phải sai tới. [19]

Nếu như có nhiều cái mình tự nghĩ ra thì [20]

thì nghĩ ra thì mình ghi là đóng góp. Mình ghi đóng góp nhưng mà đóng góp mình nó kế thừa hay là nó được cảm sinh từ cái gì thì phải ghi ra. Còn không là nó là gọi là đạo văn. Nhiều cách đạo văn. Đạo văn là chết nguyên si hoặc là ăn cấp ý tưởng. [20]

L mình kạp sinh nhưng mà cũng có người làm như vậy thì mình có bị coi [20]

mình vẫn cứ sai tới để người ta sẽ so sánh cái chuyện để người ta đánh giá hiểu không mà mình cảm sinh từ cái ý của người ta mình cũng phải ghi chứ chứ không người ta gọi là ăn cấp ý tưởng là em sợ em cắp ý tưởng [20]

em sợ em tưởng kiểu em tự nghĩ ra nhưng mà lỡ có người có cái giống như em tới trước thì em biết coi là đạo vă với người ta không thì như vậy em phải so cái của em với cái của người ta coi khác cái gì cái đó chuyện của em hiểu không em nghĩ ra chỗ này mà em không hoàn toàn xem cái tài liệu kia nhưng mà sau đó em xem lại em thấy này nó cũng có cái giống giống mình Thì như vậy cái chuyện của em là em ngồi em phải trà soát lại coi là mình khác nó thứ gì. Hiểu không? Đó chỉ vậy thôi. Hiểu chưa? Rồi thứ ba là sụt code nha. Sột code thì dĩ nhiên là gửi code. Rồi cái file mô tả nha. [21]

File file gọi là nó documentation đó. Documentation thì mô tả sụ code em tổ chức là sao? Rồi data nữa nha. Có data [22]

data là sau khi xử lý [22]

data thì em Em phải cho biết cái dữ liệu em em dĩ nhiên Google TR có cái link [22]

để bấm cho thôi ha. Thì dĩ nhiên là dữ liệu góc ha. Dữ liệu góc rồi sau đó dữ liệu mà em để tổ chức trend à rồi test gì đó valid gì đó ha. Rồi cái kha trước nữa hiểu không? Cái cái cái kha kha khao trước nữa. Hiểu chưa? Đó thì về chuẩn bị cái này ấy gửi đi thì mới góp ý được chứ giờ nói tèm lem quá. Thì bây giờ em ra kết quả Em thấy nó có hơn. Dạ. Nhưng mà bây giờ em phải rà soát lại cái hơn đó là như thế nào ha. Rồi trong này thì dĩ như nó có cái phần quan trọng là thực nghiệm phải không? Thực nghiệm á thì em phải minh chứng những gì em nói cái chỗ đóng góp á thì em cố gắng em minh chứng. Em minh chứng cho cái đóng góp này nè. Đó. Còn hiện nay em ra một con số nhưng mà em không lý giải được. Em hơn nó là vì sao? Là vì nhờ Cái PR cái cách mã hóa PR hay là nhờ công đoạn decoder hay công đoạn encoder hay công đoạn Fusion không rõ thấy không? Chứ đâu phải mình ra con số hơn chứ là ấy được đâu. [22]

Dạ. [23]

Hiểu không? [23]

Dạ. [23]

Tại vì cái thằng Sam m là cái Sam là nó lớn và lý giải ở cái tình huống này thì mình hơn nó là vì sao? [23]

Tại vì nó chưa file tool lại à đầy đủ hay là tại sao? Còn nếu nó tool lại thì như thế nào đó chứ còn tự nhiên em em nhào vô Em hơn nó như vậy là người ta sẽ đặt ghi vấn ngay nó tại vì nó là một cái foundation model em không thể địch lại hiểu không? Nó huấn luyện em chỉ thắng nó ở những cái ngõ ngách nào đó em phải khôn ngoan em thắng nó ở những ngõ ngách nào đó hiểu chưa và em thử á thì em sẽ thử trên nhiều tập chút. Ban đầu BTXRD để cho mình đỡ phải đợi chờ cài đặt ha. Thì sau đó em thử thêm trên cái thành ph nhá. Dạ. [23]

Em thử thêm trên cái thành ph xem hiểu không? [24]

Dạ. [24]

Chứ còn mình thử trên một tập thì thì ra người ta không ra biết đánh giá là sao. Được chưa? Đó. Rồi à rồi thử thì cũng chấp được thử. Tức là cho mình học thống kê rồi đó. Thứ là khi thử cái này em tìm cách em a tái lấy mẫu. Resembling, tái lấy mẫu để mà chứ còn em chỉ làm một một một đợt thôi em lấy cái tập mà học rồi tập kiểm tra vậy thì đâu có đánh giá phải không hiểu không phải tái lấy mẫu để cho nó có giống như là cross validation đó phả không vâng chứ còn đưa tự nhiên đưa con số ra thì là khó lắm em thực nghiệm em phải nói cho rõ ha mô tả cái thực nghiệm của em đúng không trong thực nghiệm em phải mô tả đó cái em xài hệ thống thế nào thông số siêu thập số các thứ vân cái đó rất quan trọng để ảnh hưởng tới toàn bộ hệ thống đó Rồi nó có những cái module là là email encoder nè. Bây giờ viết báo cáo lại Rome Encoder nè ha. Rồi Fusion đúng không? Nó kết lại đúng không? Rồi decoder đúng không? [24]

Rồi thì trong những cái này người ta thắc mắc nè em ra cái con số 0.7 à 7 70% thì là trong này là người ta muốn biết là cái nào nó đóng góp chứ còn ha. Rồi em em em saw cái này là là phương pháp của em our approach rồi em đi em so với thằng S2D đúng không? [25]

Thì em phải coi cái này cái đám này của Sams S2D dùng kỹ thuật gì phải lý giải ra rồi có thể em hơn nó ở cái tình huống nào chứ còn em không để vậy gì ha đó là một cái foundation model nó không có đơn giản hơn đó là cái cái gì có em bảo em a Em em khóa cái này hết em chỉ decoder thì xem như là đâu có tại vì muốn decoder tốt là phải nhờ mấy thằng này trong khi mình phi thằng này mình lấy này được cái gì đâu đem hơn nó vậy xem như là thằng này nó gặp tập mới là nó xem như nó thực hiện zero short rồi hiểu chưa em đi em lấy cái thằng lượng học đầy đủ muốn đầy đủ em em thắng cái thằng zeros nó hiểu khôngos là lấy cái mẫu chưa được học á em phải tool kiểu này xong chưa học [25]

em có fan tin lại cái mẫu bxd cho X M [26]

nhưng mà tun chỗ nào? F công đoạn nào? [26]

Fight công đoạn là từ nói chung là phân cái trọng số nó học ban đầu của encoder kiểu nó phải kiểu nó thấy [26]

đó thì đây nè trong bốn này phun công đoạn nè to từ công đoạn này trở đi tại vì encoder thì cái nó lớn nó không thể học [26]

từ công đoạn form thì chỉ có encoder là nó bị khoán lại tại vì [26]

em á em phải làm sao thực hiện ban đầu á thằng này zero là chưa có làm gì hết chưa có làm gì [26]

rồi sau đó em mới phải to Dạ [26]

đúng không? Sau đó mới file tool [26]

thì coi coi thằng này khi f tool á thằng này nó hơn được cái gì không? [27]

Rồi sau đó em mới so cái của em với thằng V tool hiểu không? Em phải up một cái kịch bản phải vẽ ra kịch bản rõ ràng chứ cái này nó có vẻ tèm l quá nha. Rồi một cái nữa là em về cái câu prom này của em cái phần mà hit map á em nói cho rõ cái x map này cái mục đích nó là gì nghĩ nó không rõ lắm ha. X map này gì và em phải so sánh với cái mã hóa prom vis encoder của mấy mấy thằng kia. [27]

Dạ. [27]

Thấy không? Em phải nắm chứ em cái này là quan trọng. [27]

Dạ [28]

cái bài của mình là quan trọng là chỗ này chứ đâu có cái gì khác đâu. [28]

Dạ. [28]

Hiểu không? Và cái của em là em muốn minh chứng cái gì phải cho rõ. Hiện nay nói tùm lum quá. Tức là mình muốn build firm stretch đúng không? Để mà mình có một cái mô hình hôm nọ nói rồi đó. L model đúng không? Mô hình bộ tham số nó bé hơn. Đó thì em phải nắm cái bản chất này [28]

hiểu chưa? Mô hình mình bé nhưng mà vì sao mà nó nhỏ nhưng mà nó có vỏ thấy không? Là nhờ những cái kỹ thuật nào đó thì nó nhấn nhá vô. Ủa em làm trên cái tập BTSD mà đạt tới tám mấy phần trăm di á là cao lắm đó nha. Em có hiểu con số đó không? Em có lấy những cái mẫu nhỏ không? Cái mẫu mà cái vùng tổn thương nhỏ không? Sau đó lấy coi kết quả. [28]

Em có hiểu con số đâu. Tại không rõ tập học tập test như thế nào em phải về reset. Em link lại chút để em sáo trộn cái tập để mà em thử á chứ em thử có một đợt thì vậy là em fan wifi không? Dạ em có cái file đi nó bị [29]

thì về sưu tập lại cái này cho rõ nha để thầy có gửi qua cái quyết định n cái vùng nhỏ vùng tổ thương nhỏ coi đâu phát hiện được Cái này em có nên lập ra được cái vùng tổng thương nhỏ không? [29]

Ờ hình như em show em chỉ show chung chung kiểu là show [29]

em về nè. Đó thành ra em làm nó tèm lem tèm lem nhớ không? [29]

Dạ. [30]

Bây giờ em về em cái tập dữ liệu á em phải xem nó có những cái thách thức nào. Tập dữ liệu thì thách thức được chưa? Em a em chia ra những cái thư mục. Thí dụ thư mục cái nhóm thứ nhất là những cái vùng mà tổn thương nhỏ. Hiểu không? Tổn thương nhỏ. Em thử riêng coi tổn thương nhỏ cái đài nó cỡ nhiều rồi. Thứ nhất là cái vùng mà cái biên mờ hiểu không? Cái vùng tổn thương mà cái biên nó mờ nhạc nó không rõ ha. Thì nó nhiều rồi còn cái vùng mà mà tổn thương lớn thấy không nó rõ rõ nét tổn thương lớn rõ nét đó thì nó chính xác cỡ bao nhiêu. Rồi thứ hai là cái ảnh mà không bệnh ảnh không có vùng tổn thương ảnh không bệnh thì nó làm sao nó ra nhiêu thì em xem những nhóm này độ chính xác bao nhiêu. [30]

Dạ giờ nói chính tới anh không bệ thì đầu tiên tại cái đó là ch mất thì thì đầu tiên sẽ là điện quang khi đưa vào đạo vào thì sẽ có một mô hình mobile n v4 của t em là sử dụng của chỉ chạy lại của tác giả thôi tác giả người khác thôi chứ không được đó cái đó là nó sẽ phân loại tổn thư là có bệnh hay không bệnh [31]

thì em lấy cái tập đó gì nó có cái hai tập á nó tập bệnh nhất [31]

thì trước khi sử dụng á thì nó sẽ đưa ra một cái thông báo cho bác sĩ bác sĩ sẽ xét lại một lần nữa là nó có bệnh hay không có bệnh tại cái mô hình phân đoạn nó nó đâu phải chính xác 100% đâu nên cũng phải thông báo cho bác sĩ để bác sĩ nhật lại thì nó sẽ thông báo là ờ anh này có bệnh. Nếu bác sĩ xác nhận là ờ có bệnh thì nó bắt đầu xử lý cái phân đoạn tiếp theo. Còn nếu như vậy là cái công đợ này của em là bán bán tự động em em phân loại xong rồi là phải có bác sĩ ngồ nó coi [31]

ờ bác sĩ xác nhận lại được nữa tại vì [32]

xác nhận ở công đoạn [32]

xác nhận ở công đoạn là có bệnh ảnh có bệnh hay không bệnh từ vậy là như vậy cái mẫu [32]

ý là không có không có xác định là vùng nào nhưng mà [32]

tức là giai đoạn học hay là test [32]

à test ạ [32]

giai đoạn test [32]

dạ test thực thi [32]

còn giai đoạn học đâu [32]

giai đoạn loại không lấy cái bàn đấy. [32]

Ờ giai đoạn học là chỉ lấy tin ảnh có bệnh chứ không có sử dụng phân loại. [32]

Ủa nếu em không học phân loại thì sao mà em test giai đoạn online? Em test [32]

ờ tại giai đoạn online là thằng này nó đâu có làm trên cái mẫu của bạn xương tại vì kiểu đề sai không cũng được nó luôn em lấy đại cái [32]

đây mô hình đây nó chỉ chính xác ở mức 88 8% nếu bỏ vô thì nó sẽ có hành không hạnh công bệnh bỏ vô đây để học luôn. người ta thắc mắc là tại vì em lấy cái mô hình này nè khi cái miệng mình nói lấy mô hình nào thì người ta quan quan trọng là cái bộ tham số và trong ruột của nó đó [33]

đã được tin chẩn cho cái bộ dữ liệu nào [33]

dụ em bảo mobile v4 [33]

thì em có đã huấn luyện nó cho cái bộ d chưa [33]

có có huấn luyện lại ta thắc mắc tại sao anh không huấn luyện luôn mà đi anh lấy một cái bộ đâu đâu đó huấn luyện như vậy hiểu không rất là thắc mắc bạn Cái này tắt xong tắt cái này đó [33]

thì tại vì ban đầu là cái này là cái mô hình phân đoạn của em ban đầu là chữ liệu chân tập là có nhãn tập ảnh có bệnh [34]

không cái đó là phân đoạn còn bây giờ đang nói phân lớp em muốn phân lớp để em tách ra cái mẫu có bệnh để mà em đem xuống thằng dưới. [34]

Dạ. Tại vì [34]

người ta thắc mắc là bây giờ em lấy cái mô hình phân lớp đó ở đâu và tại sao em không huấn luyện với cái tập dữ liệu mình đang có. thấy cái mô hình phân lớp này trên tìm hiểu và có file t lại trên có chen lại trên cái mô hình BTSD là nó để bổ sung cái khuyết thiếu là mô hình của em chỉ phân đoạn trên ảnh có bệnh tại vì những cái ảnh mà không bệnh nhân bỏ vô cái mô hình của em thì nó vẫn phân đoạn [34]

thì đúng rồi thì bởi vậy mình phải phân lớp trước nhưng mà đã hỏi là trong cái phân lớp của em á [35]

dạ [35]

thì tại sao ông đưa cái bộ dữ liệu có bệnh không bệnh vô để mình phân lớp mình đang nói phân lớp chứ có phân đoạn mà tại sao em đi em lấy cái mobile v là nó đã huấn luyện đâu rồi? Tại sao kỳ vậy? Tại sao mình không phân lớp mà mình không huấn luyện lại? Thắc mắc bạn huấn luyện lại nó tốt hơn không? [35]

Là [35]

ví dụ em lấy mobile net em đưa cái tập BTXRD vô. [35]

Dạ [35]

em có cái nhóm bệnh và không bệnh em đem vô em huấn luyện để có bộ tăng số. [35]

Dạ. [36]

Còn hiện nay của em á là em đi em lấy em xài luôn [36]

không? Cái này em lấy trên trang lại trên file BTSD giờ em lại bảo em không lấy mobile n. P đó trend lại trên dạ [36]

để phân lớp. [36]

Dạ [36]

đúng không? [36]

Dạ. [36]

Và và trong đó là offline. [36]

Dạ. [36]

Thì khi đó trong online thì mình lấy ra mình xài. [36]

Dạ đúng. [36]

Thì nếu mà không có bác sĩ can thiệp thì độ chính xác nó bao nhiêu? Nó ra sao? [36]

Dạ đúng rồi. [36]

Thì như vậy là 12% là sai. Tức là có bệnh. [36]

Bây giờ muốn biết là có bệnh không bệnh mà nó nói là có bệnh. [36]

Dạ. [37]

Thì khi đó cái thằng đó sẽ phải đem xuống thằng sau. M. Dạ. [37]

Đúng không? [37]

Dạ. [37]

Nên mới có [37]

chứ còn nếu mà nó có bệnh có bệnh mà nó bảo là không bệnh là mình lại không nên đi [37]

tại sao như mình không có mas. [37]

Dạ [37]

thì ngay từ đầu em đã phải chịu sai số 12% rồi. [37]

Dạ. [37]

Nên em mới có thêm cái [37]

s 12% phân lớp. Dạ. [37]

Nên em mới có thêm [37]

nhưng mà nhưng mà trong tập học em học thì độ chính xác được bao nhiêu? [37]

Trong tập học á hình như bạn không có gửi giắc cỡ của tầm à 90 mặt tác thì nó chỉ tổng như vậy thì mình xem coi có cách nào mình tăng lên thêm không. Tại vì nếu vậy là em mất hết 12%. Mà tại sao xuống dưới xuống dưới thì em lại thêm được bảy mấy? Bảy mấy là trên như vậy là trung cuộc là em chưa thấy được kết quả trung cuộc nói hiểu không? [37]

Tại vì em chỉ là vậy. 86% trên cái [38]

cái mà đem ra đúng không? [38]

Còn chung cuộc là bao nhiêu? Nó hiểu không? Đó em em làm người ta bị rất là conf người ta cứ nghĩ rằng cái đồ chính xác em 86 em ban đầu nghĩ là cái mô [38]

bây giờ mình nói đơn giản đi. 0.86 nhân với thằng kia là 88 86 nh 88 là có sá mấy [38]

rồi nó hiểu không? Tích hai cái xác suất á [38]

dạ đơn giản vậy xác dịch tại b đầu nếu mô hình không có sử dụng cái này. Thì bắt buộc bác sĩ phải xác định cái ảnh đó có bệnh mới sự vậy trong tại vì trong thực tế đưa bức ảnh vô thì bệnh hay không bệnh là nếu mà biết chắc cần ai nó cố vấn đ quái hiểu không thì bác sĩ cũng đang cần ai nó cố vấn có những cái bệnh tổn thương mà nó giai đoạn sớm á thì người ta hay bị sót hay bị nis còn nếu ông bác sĩ gì cũng biết hết thôi đâu cần ai ch không [38]

vậy cái này sẽ chuyển thành tự động hết luôn [39]

chuyển thành tự động chứ còn bác sĩ chỗ đó thì không cần thiết hoặc là hoặc là có thể nếu em muốn á thì trong phân lớp này em phải có thêm cái exprâm sàn thì nó sẽ giúp cho mình ví dụ nè ví dụ trong BTSCD nó có một cái ảnh nó có nhiều nhãn nó có nhiều nhãn thì có thể lấy cái nhãn đó qua L để mà nó sinh ra một số cái câu mô tả vân vân thì những câu mô tả đó thực chất khi khám bệnh á là bác sĩ biết là tại vì ông khám lm sạn biết Th không thì khi ổng đưa thêm những cái câu lâm sàn đó kết hợp với cái ảnh thì đưa vô phân lớp á nó sẽ tốt hơn là bắt nó nhìn cái anh không [39]

có btd thì nó có kết quả à không có cái cái test [40]

có ra nhãn là label em lấy cái label đó em bỏ vô em em kêu nó xin cho em một số con mô tả nó nó xin được không thằng nào về mình suy nghĩ coi là V với là một cái nữa là tại vì vậy nè em bị vậy nè. Thật ra thật ra em làm chung cái segmentation cũng được. Tức là đối với cái mẫu không bệnh nè không bệnh thì cái m của em là đen hết black hết đúng không? Rồi còn mẫu có bệnh nè. Đó thì cái m của em là trắng qu Tại vì cái hàm loss của em á trong lúc decoder á em thiếu cái hàm loss cho cái thằng thông vị. Tại vì mẫu này có mà cái hàm loss của em là chủ yếu là di loss PC gì đó. Cái hàm los sao mở ra coi cái hàm los của cái mobile [40]

biết trong mô hình của em á khi em phân đoạn thì em phải có cái hàm loss để mà em cực tiểu chứ phân đoạn [41]

hiểu không? [41]

Dạ [41]

thì trong cái hàm L của em không hề đá động gì đến thằng này. Nếu như em em đưa thêm nó đá động đến thằng này á ha đưa thêm cái loss đó thì xem kết quả thế nào thì em khỏi phải bằng lớp. Tại vì hai cái mô hình riêng vì cái mô hình mobile unit á chỉ là hỗ trợ trong phần thi thôi chứ không có liên quan tới huấn luyện. Huấn luyện là đi tập trung vô cái đại tiến [41]

không thì đúng rồi. Tức là trong cái mô hình phân đoạn của em nè. [41]

Trong mô hình phân đoạn của em nè. Trong cái decoder muốn hỏi em là cái hàm loss. Hiểu chưa? phục thì em có thể khắc phục bằng hai cách và em thử thì có chuyện cho mình thử. Chuyện thứ nhất là em vẫn phân lớp bình thường và em tính chung cuộc cho rõ ràng em tính kiểu như thấy không? Và thứ hai là em sửa bằng cách không dùng phân l mà em sửa cái hàm loss. Trong hàm loss nó có tính đến cái này nó có tính đến cái mẫu không bình em về em hỏi ch nó chỉ liền thôi. Và có một cách cải tiến nữa là khi em sửa hàm loss em hỏi nó cái loss để mà khắc phục những cái mẫu tổn thương bé, những cái mẫu pin mểu không? Rồi những cái mẫu thông bình thì nó sẽ đưa ra cho em một loạt những những cái cái ló hiểu không? Chứ còn hiện nay là không rõ cái lo. Thành ra cái lúc mà người ta hỏi là đối với tổn thương nhỏ đâu anh L anh sao chỉ phóng chế này? Đi bên m đâu l nào đúng không? Rồi ảnh không bệnh đâu là l nào? Đâu thấy cái đâu là cái quan trọng nhất. đâu chỗ nào mở cái xốt lại gửi nha để thầy xác định với khoa là có ra bảo vệ được hay không có làm tiếp để ra bảo vệ được hay không tại thời gian còn ngắn quá còn mà không chắc thì cứ dời lại đợt sau còn không là em những cái học phần em tích lũy là mất hết á ra bảo vệ mà rớt là nó đã mất hết á không tích lũy được đâu hiểu không em em không có lưu lại được cái kết quả tập Không được về viết vô báo cáo thèm l quá có sụt có rồi thì bây giờ chịu khó về viết ngược lại báo cáo đi ha rồi hỏi hầm l không thấy hầm l gì hết thì đây là cái thế mạnh của mình em á cái chắc nghiên cứu của em lạ lắm người ta a r tức là mình đâu có biết cái gì đâu ai chỉ mình cái gì rõ ràng để mình đi đâu nếu chỉ rỗi thôi anh nghĩ là chi thì bây giờ em em mới thử cái này em thử là classification rồi sau đóation là một hướng đúng không rồi sau đó em tiếp tục em a đi em em thử chỉ có segmentation thôi nhưng mà em cộng với cái loss hiểu không cái loss này mà l tính cả đối với mẫu không bệnh với cái mậy phải hỏi phải nói ra thôi vô rồi hỏi chỉ luôn thì em đưa ra hai bản nhiệm vụ của em ai đi cứ nghiên cứu rồi em đưa ra kết quả thôi còn em á là em cứ lành nhất dương chỉ đưa ra một đưa rau Em nói hãy giới thiệu cho tôi cái hàm má a cái hàm đó trong bài toán phân đoạn ảnh chí khoa nhằm đáp ứng nhằm khắc phục các phách thức sau. Rồi mấy em có công cụ mấy em biết sai thứ nhất một xà thứ nhất cái vùng tổn thương vùng tổn thương. có cái thứ bé thứ hai phục tổn thương có bi mời nhà thứ ba là ảnh không có bệnh tôi nói thí dụ vậy rồi vậy em coi nó còn thách thức gì thì em nói cái đó nó khống chế mình ra rồi cái số mẫu mất cân bằng mất mất tập dữ liệu mất cân bằng mất cân bằng dữ liệu rồi mất cân bằng dữ liệu Th không và trong cái tập nếu em phân lớp thì em kẹt nó nha. Tại vì trong tập này là multilabel thì em phải phân lớp dạng multilabel hay là em chỉ cần có bệnh thôi, không bệnh còn lớp gì kệ nữa. Thấy không? Đó thì là cái chuyện v nói [42]

nếu như nếu như mà thời gian gấp quá chắc sẽ bỏ đi chứ còn [43]

chỉ là không bệnh hay không bệnh thôi. [43]

Dạ là bệnh mà dạng có tổn thương á chứ còn nhiều Khi cái bệnh mà nó không có rõ cái tổn thương dạ thì cũng không phân đoạn để làm gì đó em nhớ mấy thằng đó hiểu không? Dạ [43]

bim mờ nhạc đó rồi khoảng cách bên vậy hỏi kỹ biểu thức toán ha. Dạ [43]

rồi nhất là đó một tổn thương nhỏ vộc đi mờ nhạc kìa. Ờ anh không có bệnh kìa. Hiểu chưa? Hiểu không? [43]

Tại vì em em không có phạt em không có cái hàm phạt cái chỗ mà cái thằng không bệnh. [43]

Em phạt thì là em đưa mẫu vô thì có thể làm đó. B đó bị thiếu sót quá. Còn cái hàm của của em hiện nay là chắc là em xài cái di loss hoặc là PCE thôi. Xài đơn giản quá xài cái băng hiểu không? [44]

Xài đơn giản quá chưa? Thôi về học nó kêu nó viết biểu thức toán ra rồi giải thích cho em ghi đi. Viết biểu thức toán của cái hàm L và giải thích ý nghĩa của từng hàm L. Rồi rồi bây giờ em rồi em bảo nó trích chọn trích chọn các hàm L tiêu biểu nhất cho mỗi nhóm ha. đó thì coi nó chọn sao rồi về tử em mới chọn nhá. Với lại một cái nữa là thầy có đề xuất là cái rá cam khi mà m như một cái không phải khối u á thì nó sẽ đưa ra một cái mát chống mát rẫm rồi sẽ đưa ra một cái nhện toán thì em cũng có thực nghĩ như là thực nghiệm ý ban đầu nếu như m trên cái vùng mà bộ phận thì Tất nhiên nó sẽ tự phân đoạn mặc dù nó không có có cái u nhưng mà cái đó hơi khó nên là em chuyển qua là Nó như 70% là vùng đen chỉ nó mùng đoạn nhỏ như này thì nó sẽ ra mát trống và nó sẽ đưa ra một cái cam dữ gợi ý thì cái điện Ram này em tính là đưa ra một cái from luôn tạo cái form này để nó chử đoán thêm một lần nữa thì em phải giải xức cho báo cáo cho rõ để biết cho rõ để sắp nộp rồi [44]

dạ nói b quên và cái chuyện của em nếu có chù visom prom nếu như ông bác sĩ ông đánh visum crom sai thì hệ thống xử lý thế nào [45]

dạ đúng chưa ch được ha nếu mà ổng đánh nếu mà ổng đã visual sai thì dẫn đến hệ thống xử lý thế nào đó nó có cái gì nó biết không hay là ổ đánh sao nó làm vậy chưa rồi đó chuyện em về thấy rồi mở ra coi mở ra coi sơ chú thôi thì về lo trâu chuốc lại cái đó đi đó thì về coi hỏi nó nó giải thích cho cái hàm toán này sao sao rồi so với cái lot của em coi thêm cái gì được vô để mà làm hai hướng nè ha hiểu không Thì coi thằng nào mèo nào cắn nào em anh đi thôi mà đó hiểu không chứ em là em thứ nhất chương chỉ em đưa một phương pháp đưa một phương pháp thì đâu phải vậy sao em đưa ra được người ta đâu có đánh giá được phải không biết nó tốt xấu là sao rồi thôi được [45]

thằng này là mình có phải trả phí phải hả [46]

ờ có nếu free thì xài free thì không ổn nhưng mà trả phí được 22 đô tháng Em cũng đang kiểu làm thêm mấy cái phus khác để bỏ vậ đó rồi lên liền nhá. Nộ góp cho một trễ quá là không sát nha. Tức là thời gian ngắn quá không có ngồi trà đó đợt ngay đây t 15 báo cáo với ta rạo cái thư mục cho rõ ràng em nợ cái luậng văn theo cái cấu trúc chẩn đồ án á hiểu không? Em bỏ dần vào đó đi rồi em gửi cái link em ghi rõ cái cái title nha. Kiểm tra ha kiểm tra ra bảo vệ tra khóa luận tra bảo vệ nha tạo cái cấu trúc thư thục giống như mã cũng học á tạo đúng bỏ vô đặt chưa vớ vẫn vài file rồi nay xuất chiế thầy cần cái chỗ em là cái đường cao là bảo vệ cho [46]
Lý do vì sao kết quả Dice của Unet chỉ đạt 0.5?
Phân tích thêm về cách SAM mã hóa vision prompt
Các hàm Loss nào giúp khắc phục lỗi biên mờ nhạt?


