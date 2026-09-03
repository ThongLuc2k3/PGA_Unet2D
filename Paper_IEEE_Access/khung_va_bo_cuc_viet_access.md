# Khung lập luận và bố cục viết lại bài IEEE Access (bản để duyệt)

Ngày 2026-09-03. Chưa đụng `.tex`. Đây là bản đọc hiểu, đánh giá hiện trạng, và đề xuất
bố cục để anh duyệt trước khi bắt đầu viết.

## A. Đã đọc những gì

- `Paper_IEEE_Access/manuscript_writing_guardrails.md` (toàn bộ 15 mục)
- `Paper_IEEE_Access/claims_to_validate.md` (13 claim + claim robustness xuyên suốt)
- `Paper_IEEE_Access/ke_hoach_chinh_sua_bai_bao.md`
- `PGA-UNet_IEEE_Access_Redline_Revision_VI.pdf` (13 trang + bảng ưu tiên + checklist biên tập)
- Toàn bộ `Paper_IEEE_Access/sections/00..08`
- `README.md` gốc + `Source/README.md`
- Số liệu mới trong `Result/` (train + test, BTXRD + FracAtlas, gồm ablation, Monte Carlo,
  và 3 nhánh loss `00` / `01` / `10`)

## B. Bài đang ở đâu

### B.1. Phần đã ổn định, chỉ cần rà nhỏ

Method, Related Work, Experimental Setup, và khung Discussion/Conclusion đã bám đúng guardrails:

- Logic hai tầng so sánh đã tách rõ: Attention U-Net là tham chiếu tự động (đo độ khó
  khu trú), SAM-Med2D là so sánh khớp prompt. Không còn câu nào đọc như "PGA-UNet thắng
  Attention U-Net nên kiến trúc tốt hơn".
- Khung "thắt vòng vây" đã có trong Introduction và Related Work.
- Protocol mô tả đúng: `center_mixed` 80/20, scale x3, shift 0.5, kernel 31, seed
  22120196, 150 epoch, chọn checkpoint theo image-level merged val Dice ở `center_shift`.
- Đã có 2 baseline prompt-matched (`concat-prompt-attunet`, `crop-prompt-attunet`), đúng
  AUTHOR ACTION số 1 của thầy.
- QualityHead và CAD prompt-confidence được tách rõ là 2 tín hiệu khác nhau, không cái nào
  bị gọi là xác suất hiệu chuẩn.

### B.2. Phần đang treo

- `sections/05-results.tex` vẫn để nguyên bảng số cũ (protocol trước) kèm "Status note".
  Toàn bộ bảng trong thân bài hiện là legacy.
- Theo quyết định của anh ngày 2026-09-01: train lại PGA cả 2 dataset để chọn checkpoint
  tốt nhất, chạy lại toàn bộ ablation multi-seed, chạy lại FracAtlas. Nên Claim
  1, 2, 3, 4, 5, 7, 11, 12 quay lại pending; mục Ablation chỉ nên ghi 1 câu "đang chạy lại".
- Efficiency (Claim 8) là số kiến trúc, không bị chặn, viết được ngay.

### B.3. Điểm cần anh chốt trước khi viết số

1. **FracAtlas 512 đã đổi số.** [Đã chốt 2026-09-03] Thư mục `Result/File_train/{btxrd,fracatlas}/pga 512/00/`
   là checkpoint PGA-512 chính thức mới nhất. Số canonical: BTXRD test zoom/shift
   0.7817 / 0.7740, FracAtlas 0.7271 / 0.7134. Bỏ hẳn số cũ 0.666 / 0.657.
2. **Ablation: full PGA không phải cấu hình tốt nhất** trên BTXRD trong đợt chạy hiện tại
   (vài biến thể hơn nhẹ, nằm trong độ lệch Monte Carlo). Đây là lý do anh quyết chạy lại
   multi-seed. Bài viết mục Ablation ở Mode A cho tới khi có số mới.
3. **Bảng Top/Bottom-Dice, SAM, small-lesion** trong `Result/` đã có số mới nhưng phụ thuộc
   checkpoint PGA "best" anh đang chọn lại. Nếu PGA chọn theo "best" thì AttUNet x2 và
   SAM-Med2D phải cùng cách chọn (cùng multi-seed hoặc cùng một seed cố định), nếu không sẽ
   dính AUTHOR ACTION số 3 của thầy.

## C. Bộ claim chính, gom gọn để khỏi lan man

13 claim quy về 4 trục. Bài nên bám đúng 4 trục này.

**Trục 1: Prompt là thiết yếu, không phải kiến trúc thắng kiến trúc.**
Bằng chứng: Attention U-Net tự động (Dice khoảng 0.52 BTXRD, 0.34 FracAtlas) so với
PGA-UNet có prompt; cộng subset Top-Dice / Bottom-Dice. Đọc đúng: bài toán không-prompt rất
khó, không phải PGA-UNet giỏi kiến trúc hơn.

**Trục 2: Đã có prompt rồi thì khai thác thế nào cho tốt.**
Bằng chứng: PGA-UNet vs SAM-Med2D @256 (cùng box, cùng độ phân giải); PGA-UNet vs 2 baseline
AttUNet prompt-matched @512. Đọc đúng: PSG và CAD giữ tín hiệu tổn thương nhỏ xuyên suốt
mạng, khác cách SAM chỉ dùng box để chỉ vùng ở mask decoder.

**Trục 3: Tổn thương nhỏ là nơi thiết kế này ăn tiền nhất.**
Bằng chứng: subset 50 ảnh diện tích tổn thương nhỏ nhất. SAM-Med2D-FT gần như không tạo
được mask (Dice khoảng 0.19 BTXRD), PGA-256 khoảng 0.76, PGA-512 khoảng 0.85. Đây là bằng
chứng mạnh nhất của bài. Cộng hiệu ứng độ phân giải 512 > 256 > 128.

**Trục 4: Ổn định và chi phí.**
Monte Carlo 4 split (std < 0.012) cho độ ổn định mức chia dữ liệu. Efficiency: 2.95M tham
số, khoảng 92x nhỏ hơn SAM-Med2D. Đọc đúng: ổn định không phải vượt trội thống kê; chi phí
thấp không phải sẵn sàng lâm sàng.

Ablation (Gaussian vs binary, PSG, CAD) là bằng chứng hỗ trợ Trục 2, viết theo "consistent
with complementary contributions".

## D. Khung lập luận xuyên suốt

Một câu: *Bài toán tổn thương nhỏ trên X-quang xương khó chủ yếu ở bước khu trú; PGA-UNet
nhảy cóc qua bước detection bằng box của bác sĩ, rồi thiết kế PSG và CAD để tín hiệu vùng
nhỏ không bị suy hao qua downsampling; đóng góp thật nằm ở cách khai thác prompt, rõ nhất
trên tập tổn thương nhỏ, chứ không phải ở việc thắng một baseline không-prompt.*

Mỗi mục Results phải quay về đúng một mắt xích của câu này.

## E. Sổ claim đầy đủ, sắp theo thứ tự đọc mạch lạc

Mọi claim trong `claims_to_validate.md` cộng thí nghiệm loss của thầy. Cột "Nằm ở mục" trỏ
sang mục lục IEEE ở phần F. Không claim nào bị bỏ hoặc gộp chìm vào đoạn văn.

### Nhóm 0: Nền tảng

| # | Claim | So sánh cụ thể | File bằng chứng | Trạng thái số | Nằm ở mục |
|---|---|---|---|---|---|
| C13 | Đánh giá độc lập trên 2 dataset, xu hướng lặp lại | Mọi claim dưới đây chạy song song BTXRD và FracAtlas | tất cả notebook `Result/*` | có số mới | xuyên suốt V, chốt lại 1 câu ở VI |
| C11 | Ảnh hưởng độ phân giải 128 / 256 / 512 | PGA-UNet 3 độ phân giải, 2 điều kiện prompt, mỗi dataset | test cell nhúng trong `pga-train-{128,256,512}` (`Result/File_train/*/pga 128,256,512`) | có số mới (`00` là 512 chính thức); cần đối chiếu lại 128/256 với `Result/` | V-A |

### Nhóm 1: Prompt có thiết yếu không (tầng tham chiếu tự động)

| # | Claim | So sánh cụ thể | File bằng chứng | Trạng thái số | Nằm ở mục |
|---|---|---|---|---|---|
| C1a | Bài toán không-prompt khó tới đâu | PGA-UNet vs Attention U-Net ảnh-only (không box) | `test-pga-vs-attunet-variants-r512-{btxrd,fracatlas}` | có số mới (AttUNet 0.52 / 0.34) | V-B |
| C1b | Có box rồi thì kiến trúc có còn quan trọng, hay chỉ cần "có box" | PGA-UNet vs Attention U-Net + prompt-channel (box nhị phân ghép kênh 2) vs Attention U-Net + prompt-crop (cắt ảnh theo box) | cùng notebook trên, cùng tập ảnh 4 model | có số mới (channel 0.768/0.754 BTXRD, crop 0.741/0.733; PGA hơn nhẹ BTXRD, hơn rõ FracAtlas) | V-B |
| C2 | Lợi ích tập trung ở đâu | Top-50 và Bottom-50 ảnh theo Dice của Attention U-Net; chạy lại PGA-UNet, prompt-channel, prompt-crop trên đúng các ảnh đó | `test-subcat-pga-vs-attunet-variants-r512-{btxrd,fracatlas}` | có số mới | V-C |

### Nhóm 2: Đã có prompt thì khai thác thế nào cho tốt (tầng khớp prompt)

| # | Claim | So sánh cụ thể | File bằng chứng | Trạng thái số | Nằm ở mục |
|---|---|---|---|---|---|
| C3 | PGA-UNet vs mô hình nền tảng dùng prompt, cùng box cùng độ phân giải | PGA-UNet-256 vs SAM-Med2D zero-shot vs SAM-Med2D fine-tuned, @256, cả zoom và shift | `test-pga-samzs-samft-r256-{btxrd,fracatlas}` | có số mới (SAM-ZS 0.255/0.262, SAM-FT 0.630/0.563, PGA-256 0.762/0.629) | V-D |
| C6 | Thành phần nào đóng góp | CAD-only, PSG-only, PSG + vanilla attention gate, full + binary prompt, full + Gaussian (PGA-UNet đầy đủ) | `Source/File_Test/{btxrd,fracatlas}/Ablation/` + `test-full-pga-heatmap-reference-*` | có số nhưng anh quyết chạy lại multi-seed | V-H (Mode A, 1 câu, chưa đưa số) |

### Nhóm 3: Tổn thương nhỏ, nơi thiết kế ăn tiền nhất

| # | Claim | So sánh cụ thể | File bằng chứng | Trạng thái số | Nằm ở mục |
|---|---|---|---|---|---|
| C4 | Tổn thương rất nhỏ: PGA-UNet vs SAM-Med2D | Subset 50 ảnh diện tích GT nhỏ nhất: PGA-UNet-256 vs SAM-Med2D ZS/FT, @256, khung metric 512 chung | `test-subcat-small-r256-{btxrd,fracatlas}` | có số mới (SAM-FT 0.19 BTXRD / 0.37 FracAtlas, PGA-256 ~0.76) | V-E.1 |
| C5 | Tổn thương rất nhỏ: PGA-UNet vs baseline prompt-matched thường | Cùng subset nhỏ: PGA-UNet-512 vs Attention U-Net + prompt-channel vs Attention U-Net + prompt-crop, @512 | `test-subcat-small-r512-{btxrd,fracatlas}` | có số mới | V-E.2 |
| C12 | Hiệu ứng độ phân giải rõ hơn khi tổn thương nhỏ | Cùng 50 stem nhỏ trong mỗi dataset: PGA-UNet @128 / 256 / 512, 2 điều kiện prompt, kèm mức tụt so với 512 | `test-subcat-pga-small-r128-256-512-{btxrd,fracatlas}` (đã sửa bug N=0 ngày 2026-09-01) | có số mới sau khi sửa bug | V-E.3 |

### Nhóm 4: Ổn định, chi phí, và các thử nghiệm phụ

| # | Claim | So sánh cụ thể | File bằng chứng | Trạng thái số | Nằm ở mục |
|---|---|---|---|---|---|
| Cross | Nhạy cảm với dịch prompt | Với mọi claim C1-C6, C11-C12: chênh lệch giữa `center_zoom` và `center_shift` (Dice, CBL, HD95, mức tụt tương đối) | mọi notebook trên (đều báo 2 điều kiện riêng) | có số mới | V-F (gom lại), và 2 cột trong mọi bảng |
| C7 | Ổn định qua các lần chia ngẫu nhiên mức ảnh | 4 checkpoint PGA-UNet-512 với split seed 1-4, seed train cố định 22120196; mean ± std | `test-pga-dataset-1234-{btxrd,fracatlas}` | có số mới (std < 0.012 mọi hàng) | V-G |
| C8 | Chi phí tính toán | PGA-UNet 256/512 vs SAM-Med2D 256: params, FLOPs, size, latency GPU/CPU | `test-measure_efficiency_btxrd.ipynb` | **Mode B, viết ngay** (2.955M vs 271M, ~92x) | V-I |
| E1 | Thí nghiệm loss theo gợi ý của thầy (redline 3.5) | PGA-UNet-512 `00` Dice+BCE vs `01` Focal Dice vs `10` size Tversky, 2 dataset, 2 điều kiện prompt | `Result/File_train/{btxrd,fracatlas}/pga 512/{00,01,10}` (test cell nhúng đã chạy) | **Mode B, viết ngay**, kết quả âm tính | V-J |

### Nhóm 5: Sử dụng tương tác và tín hiệu phụ trợ

| # | Claim | Trạng thái | Nằm ở mục |
|---|---|---|---|
| C9 | Điểm ước lượng chất lượng mask (QualityHead) | **GẠT SANG 1 BÊN 2026-09-04.** Đã chạy `test-auxiliary-signals-r512-*`: QualityHead ra gần như hằng số (~0.69 BTXRD, ~0.72 FracAtlas), Pearson −0.05 đến 0.16, Spearman 0.04 đến 0.19. Không phân biệt được tốt/tệ. Không đưa vào Results. | không có mục Results; 1 câu ở VI Discussion + 1 câu future work ở VII |
| C10 | Gợi ý vùng box cho bác sĩ | **GẠT SANG 1 BÊN 2026-09-04.** Cùng notebook Phần B: vì QualityHead hằng số nên xếp hạng vô nghĩa, "top-5" = 5 box tùy tiện. BTXRD 38% khoanh trọn, FracAtlas 87% nhưng chỉ do hình học (vết nhỏ + box to). Không đo được gì về phương pháp. Không đưa vào Results. | như C9 |
| C-fail | Failure modes | định tính | V-K |

### Thay đổi so với bản sổ claim trước

Nhóm 0 đến 4: không đổi (claim, so sánh, file, mục đều giữ nguyên).

Nhóm 5, chốt 2026-09-04:

- **C9 và C10 gạt sang một bên**, không đưa vào phần kết quả. Đã chạy
  `test-auxiliary-signals-r512-{btxrd,fracatlas}` (kết quả nằm ở `Result/File_test/*`):
  QualityHead sập về đoán hằng số, không có tín hiệu phân biệt; C10 do đó cũng không đo
  được gì. Notebook và số giữ lại trong repo làm bằng chứng, không trích vào bài.
- Trong bài: bỏ mục V-L. Method III-F vẫn định nghĩa QualityHead và điểm prompt-use của CAD
  (chúng có thật trong kiến trúc), nhưng đóng khung là "chưa cho tín hiệu dùng được".
  Discussion thêm 1 câu hạn chế, Conclusion thêm 1 câu kết mở (hướng nghiên cứu sau).
- Demo Gradio (`test-Demo_Interactive_PGA_Unet-*`) giữ nguyên làm minh hoạ giao diện, đã
  cập nhật checkpoint sang `00`. User tự chạy và chụp 1 ảnh minh hoạ luồng vẽ box -> mask
  (không chụp phần "Suggest prompts").

## F. Mục lục IEEE (mọi tiểu mục ghi rõ claim)

```
I.   INTRODUCTION
     nút thắt khu trú, 2 hướng giải, câu hỏi trung tâm, đóng góp
     [khớp C1, C3, C6, C7, C8, và nhóm nhỏ C4/C5/C12]

II.  RELATED WORK
     A. Automatic segmentation and the Attention U-Net lineage
     B. Interactive and prompt-based segmentation
     C. Promptable medical foundation models
     Bảng: prior work + khoảng trống
     [không mang claim, khung hoá gap]

III. METHOD
     A. Offline and online framework
     B. Problem setting
     C. Prompt representation (Gaussian plateau, center_zoom/shift/mixed, phạm vi box mô phỏng)
     D. Prompt Spatial Gate (PSG)
     E. Conditional Attention Decoder (CAD)
     F. Auxiliary outputs: prompt-use score and QualityHead
        [mô tả kiến trúc; đóng khung "chưa cho tín hiệu dùng được", trỏ sang VI]
     Hình 1: kiến trúc

IV.  EXPERIMENTAL SETUP
     A. Datasets (BTXRD, FracAtlas; chia mức ảnh; hạn chế patient-level)   [C13]
     B. Training details (seed, 150 epoch, center_mixed 80/20, chọn checkpoint, fine-tune SAM-Med2D, split seed MC)
     C. Baselines and metrics (AttUNet tự động; SAM-Med2D; prompt-channel + prompt-crop AttUNet; Dice/CBL/HD95; công thức CBL; HD95 chuẩn hoá)
     D. Scope of analysis (box một phần / âm / vùng lạ nằm ngoài phạm vi)

V.   RESULTS
     Status note: mục nào Mode A pending, mục nào Mode B refreshed
     A. Main results across datasets and resolutions          [C11, C13]
     B. Comparison against automatic and prompt-matched Attention U-Net
        doan 1: vs image-only Attention U-Net                 [C1a]
        doan 2: vs prompt-channel va prompt-crop Attention U-Net   [C1b]
     C. Behavior on automatic-baseline top-Dice / bottom-Dice subsets   [C2]
     D. Matched comparison against SAM-Med2D                  [C3]
     E. Small-lesion analysis
        E.1 vs SAM-Med2D at 256                               [C4]
        E.2 vs prompt-channel and prompt-crop Attention U-Net at 512   [C5]
        E.3 PGA-UNet at 128 / 256 / 512                       [C12]
     F. Sensitivity to prompt displacement                    [cross-cutting robustness, tong hop C1-C6/C11-C12]
     G. Monte Carlo cross-validation                          [C7]
     H. Ablation study                                        [C6]  (Mode A vong nay)
     I. Efficiency analysis                                   [C8]  (Mode B)
     J. Exploratory comparison of segmentation losses         [E1]  (Mode B, ket qua am tinh)
     K. Failure modes                                         [C-fail]
     (khong con muc L. C9/C10 gat sang mot ben, xem VI + VII)

VI.  DISCUSSION
     dien giai 4 truc; thu hep pham vi; han che
     (do phan giai co dinh, prompt mo phong, train tach 2 dataset, patient-level,
      protocol heuristic, loss chua nham vung nho/tam + loss thay the da thu khong cai thien,
      ablation mot split, Monte Carlo = on dinh khong phai vuot troi, chua probing feature-level,
      chua them baseline prompt hien dai ngoai SAM-Med2D vong nay)
     + 1 cau: QualityHead da thu nhung sap ve gan hang so, khong cho tin hieu phan biet
       theo tung prompt (Spearman 0.04 den 0.19); coi nhu chua hoat dong.

VII. CONCLUSION
     PGA-UNet la gi, da danh gia gi, khong thiet lap dieu gi, future work
     + 1 cau ket mo: mot huong tiep theo la mot tin hieu tu danh gia dang tin cay hon
       (hieu chuan / loss xep hang) va tu do la goi y vung nghi ngo

BACK MATTER
     Data availability, Author contributions, Ethics statement,
     Acknowledgment (khai bao dung AI), References, Biographies
```

### Ghi chú phân bổ

- **C1 giữ nguyên 1 mục (V-B) nhưng 2 đoạn tách bạch**: đoạn tự động và đoạn prompt-matched,
  đúng guardrails "không gộp 2 tầng vào 1 câu", mà vẫn không giấu 2 baseline prompt-channel /
  prompt-crop.
- **prompt-channel và prompt-crop xuất hiện 3 lần**: toàn tập (V-B), subset top/bottom (V-C),
  subset nhỏ (V-E.2). Mỗi lần là một câu hỏi khác nhau.
- **Small-lesion tách 3 mục con** để C4, C5, C12 đều hiện rõ, không dồn thành 1 đoạn.
- **V-F** là mục mới gom claim robustness xuyên suốt lại một chỗ, đồng thời chuyển hình
  `fig:robust` (đang nằm nhầm dưới Monte Carlo) về đây.
- **V-J** là mục mới cho thí nghiệm loss, để thể hiện rõ "đã thử theo gợi ý thầy".
- **Không còn V-L**. C9/C10 chạy ra âm tính (2026-09-04), gạt sang một bên: chỉ còn III-F
  mô tả kiến trúc + 1 câu hạn chế ở VI + 1 câu kết mở ở VII. Xem mục I.1.
- Discussion và Conclusion giữ khung hiện tại, thêm 1 dòng cho loss âm tính và 1 dòng cho
  QualityHead chưa hoạt động.

## F. Số liệu

### F.1. Dùng được ngay

- Efficiency: bảng đầy đủ (2.955M params, 7.74 GFLOPs @256 / 30.97 @512, ckpt 11.4 MB, GPU
  8.6ms @256 / 18.8ms @512, CPU 100ms / 335ms; SAM-Med2D 271.24M, 92 GFLOPs, 2443 MB).
- So sánh loss: xem mục G, kết quả âm tính sạch.
- Attention U-Net tự động: Dice 0.52 BTXRD / 0.34 FracAtlas (nếu anh chốt các `00` là chính thức).

### F.2. Pending tới khi anh chốt checkpoint

- Bảng chính resolution, Monte Carlo, baseline, top/bottom, SAM, small-lesion, ablation.

## G. So sánh loss (điểm anh nhờ rà, số 1)

3 nhánh đã chạy xong test nhúng trong chính notebook train, không cần chạy test riêng.

| Loss | BTXRD zoom / shift | FracAtlas zoom / shift |
|---|---|---|
| Dice + BCE (`00`, mặc định) | **0.7817 / 0.7740** | **0.7271 / 0.7134** |
| Focal Dice (`01`) | 0.7725 / 0.7653 | 0.6421 / 0.5784 |
| size Tversky (`10`) | 0.7776 / 0.7665 | 0.7086 / 0.6796 |

Kết luận: mặc định Dice + BCE tốt nhất hoặc ngang bằng ở cả 2 dataset và cả 2 điều kiện
prompt. Focal Dice làm hỏng nặng FracAtlas (HD95 nhảy lên khoảng 105 pixel). Đây là kết quả
âm tính sạch, khớp guardrails ("default có thể đã đủ mạnh dưới protocol hiện tại").

Đề xuất xử lý:

1. Gộp 3 số này vào notebook `00` (thêm 1 cell markdown + 1 bảng nhỏ), bỏ ý định làm
   notebook test loss riêng.
2. Trong bài: 1 đoạn ngắn nói rõ đã thử theo gợi ý của thầy (mục 3.5 redline), không cải
   thiện, nên giữ Dice + BCE. Vị trí cụ thể cần anh chọn (xem câu hỏi cuối file).

## H. File đuôi kép (điểm anh nhờ rà, số 2)

Lỗi: `Source/Prompt-Guided-XRay-Segmentation/qualitative_visualization.py`, hàm
`export_qualitative_rows`. Tên ảnh xuất ra bị `IMG000184.png.png` vì `_record_name` trả về
tên đã có đuôi `.png` rồi code còn nối thêm `.png`.

Trạng thái: đã có bản sửa trong cây làm việc (chưa commit), strip đuôi ảnh
(`png/jpg/jpeg/bmp/tif/tiff`) trước khi ghép `.png`. `re` đã import sẵn. Bản sửa đúng và đủ.
Chỉ cần anh xác nhận đây đúng là file anh nói, rồi commit chung khi commit `Source/`.

## I. Thông tin còn thiếu để viết IEEE

### I.1. C9 và C10: đã chạy, kết quả âm tính, gạt sang một bên (chốt 2026-09-04)

Notebook `test-auxiliary-signals-r512-{btxrd,fracatlas}.ipynb` đã chạy xong, output ở
`Result/File_test/{btxrd,fracatlas}/`.

**C9 (QualityHead):**

| dataset | prompt | MAE | RMSE | Pearson | Spearman |
|---|---|---|---|---|---|
| BTXRD | zoom | 0.148 | 0.186 | −0.046 | 0.060 |
| BTXRD | shift | 0.151 | 0.189 | −0.049 | 0.037 |
| FracAtlas | zoom | 0.103 | 0.133 | 0.160 | 0.186 |
| FracAtlas | shift | 0.112 | 0.152 | 0.060 | 0.097 |

QualityHead ra gần như hằng số (~0.69 BTXRD, ~0.72 FracAtlas) cho mọi ca. Tương quan gần 0.
Head học đoán về mức trung bình để tối thiểu MSE (đầu vào bị detach, head nhỏ, trọng số loss
nhỏ). Không phải bug test, không phải bug train, là điểm yếu thiết kế.

**C10 (gợi ý vùng box):** BTXRD top-5 độ phủ trung bình 0.223 / tốt nhất 0.688 / khoanh trọn
38%. FracAtlas 0.608 / 0.953 / 87.5%. Nhưng vì QualityHead hằng số nên top-5 = 5 box tùy
tiện; FracAtlas cao chỉ do hình học (vết gãy nhỏ nằm giữa + box ứng viên to). Không đo được
gì về phương pháp.

**Xử lý trong bài:**

- Bỏ mục V-L. Không trích số C9/C10.
- Method III-F: giữ định nghĩa QualityHead + điểm prompt-use của CAD (có thật trong kiến
  trúc). Câu cuối đổi thành "we find this head does not yet provide a usable signal, see
  Limitations".
- Discussion: thêm 1 câu "the auxiliary QualityHead collapsed toward a near-constant estimate
  and did not provide a discriminative per-prompt signal (Spearman 0.04 to 0.19); it should
  be treated as non-functional under the current training".
- Conclusion: thêm 1 câu kết mở, hướng nghiên cứu sau là một tín hiệu tự đánh giá đáng tin
  hơn và từ đó là gợi ý vùng.
- Làm nhẹ chỗ nhắc QualityHead ở abstract/introduction (abstract đã hedge "does not establish
  calibrated confidence", chỉ cần bỏ chỗ nào ngụ ý nó hoạt động).
- Demo Gradio giữ nguyên làm minh hoạ giao diện, đã cập nhật checkpoint sang `00`. User chụp
  1 ảnh luồng vẽ box -> mask (không chụp "Suggest prompts").

Notebook + số C9/C10 giữ lại trong repo làm bằng chứng, không đưa vào manuscript.

**Cập nhật 2026-09-04, thử cứu bằng điểm training-free (Cách A):**
`test-auxiliary-signals-r512-*` đã viết lại: bỏ đọc QualityHead, thay bằng
`Q = mean(S_sharp, S_fill, S_size, S_stab)` tính thẳng từ output suy luận, không train
lại. S_stab (IoU giữa mask gốc và mask khi nhích box) là tín hiệu đặt cược. Part A so
Spearman của Q và từng thành phần với Dice thật; Part B xếp hạng 50 box theo Q so với theo
QualityHead. User chạy. Nếu Spearman của Q lên tầm 0.4+ thì C9/C10 quay lại bài dưới dạng
"training-free self-assessment", cập nhật demo + chụp ảnh. Nếu không, giữ future work như
trên. Commit `b6f98f4`.

### I.2. Các mục còn thiếu khác

1. **Số của 2 bài gốc BTXRD và FracAtlas** (thầy yêu cầu, mục 3.8 redline): cần trích
   Dice/segmentation từ `\cite{b7}` và `\cite{b8}` làm điểm đối chiếu bối cảnh. Chưa có
   trong bài.
2. **AUTHOR ACTION số 2 redline**: thêm ít nhất 1 baseline prompt hiện đại nữa (MedSAM /
   ScribblePrompt / Med-SA). [Đã chốt 2026-09-03] Đưa vào future work, không làm vòng này.
   Vòng này giữ SAM-Med2D + 2 baseline AttUNet prompt-matched, ghi rõ trong hạn chế +
   hướng phát triển.
3. **AUTHOR ACTION số 3 redline**: thống kê theo cặp (paired bootstrap / 95% CI) cho PGA vs
   baseline và cho ablation chính. Chưa làm.
4. **AUTHOR ACTION số 4/5 redline**: test prompt khó hơn (bao phủ một phần, box âm).
   Guardrails đã đặt ngoài phạm vi. Cần anh xác nhận giữ nguyên "ngoài phạm vi" trong bài.
5. **Placeholder**: affiliation tác giả 2, tiểu sử + ảnh Lý Quốc Ngọc, DOI, footer
   template. Thầy tự điền.

## J. Việc

1. File đuôi kép (mục H): giữ bản sửa, đã commit `cfef8ba`.
2. Notebook C9 + C10: đã tạo và đã chạy. Kết quả âm tính, gạt sang một bên (mục I.1).
3. Demo: đã đổi checkpoint sang `00` ở 2 file `test-Demo_Interactive_PGA_Unet-*`. User chạy
   Kaggle, chụp 1 ảnh luồng vẽ box -> mask.
4. Gộp số loss vào notebook `00` (mục G). [Chưa làm]
5. Viết nháp `.md` (đã có `nhap_method_setup.md` cho III + IV, cần chỉnh theo quyết định
   C9/C10). Tiếp: II Related Work, khung V/VI/VII. Mỗi mục `.md` nháp trước khi sửa `.tex`.

## K. Trạng thái quyết định

**2026-09-03**
- File đuôi kép: bug `qualitative_visualization.py`, giữ bản sửa. Đã commit.
- Checkpoint PGA-512: thư mục `00` là chính thức. BTXRD 0.782/0.774, FracAtlas 0.727/0.713.
- Baseline prompt hiện đại thêm (MedSAM/ScribblePrompt): future work, không làm vòng này.

**2026-09-04**
- C9 + C10: đã chạy, **âm tính** (QualityHead sập về hằng số, Spearman 0.04 đến 0.19).
  **Gạt sang một bên**: bỏ mục V-L, giữ III-F mô tả kiến trúc, thêm 1 câu hạn chế ở
  Discussion + 1 câu kết mở ở Conclusion. Demo giữ làm minh hoạ giao diện, đã đổi checkpoint
  sang `00`.
- Gộp số loss vào `00`: chưa làm.
