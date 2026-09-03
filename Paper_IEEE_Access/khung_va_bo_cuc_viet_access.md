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

| # | Claim | So sánh cụ thể | File bằng chứng | Trạng thái số | Nằm ở mục |
|---|---|---|---|---|---|
| C9 | Điểm ước lượng chất lượng mask mức polygon (QualityHead) | Toàn tập test: MAE/RMSE/Pearson/Spearman giữa điểm QualityHead và Dice thật, `center_zoom` và `center_shift` riêng | `test-auxiliary-signals-r512-{btxrd,fracatlas}` Phần A (bọc `evaluate_quality_head.py`) | **notebook đã tạo 2026-09-03**, chạy được ngay với checkpoint `00`; thành Mode B sau khi chạy | V-L |
| C10 | Gợi ý vùng box cho bác sĩ | Mỗi ảnh: 50 box ứng viên, QualityHead chấm điểm, lấy top-5 (kèm @3); chấm theo độ phủ tổn thương của box (bao trọn = 1.0, một phần = tỉ lệ), không dùng mask mô hình. Báo Độ phủ trung bình, Độ phủ trung bình tốt nhất, Tỉ lệ ảnh khoanh trọn (>= 1 ô bao trọn 100% tổn thương) | `test-auxiliary-signals-r512-{btxrd,fracatlas}` Phần B | **notebook đã tạo 2026-09-03**, chạy được ngay với checkpoint `00`; thành Mode B sau khi chạy | V-L |
| C-fail | Failure modes | Tổn thương dài/phân nhánh, vùng giải phẫu chồng lấn, tương phản yếu | `Paper_IEEE_Access/images/failure/` | định tính | V-K |

### Thay đổi so với bản sổ claim trước

Nhóm 0 đến 4: không đổi (claim, so sánh, file, mục đều giữ nguyên).

Nhóm 5:

- **C9** trước ghi "định tính; muốn số phải chạy `evaluate_quality_head.py`". Nay đã có
  notebook định lượng `test-auxiliary-signals-r512-{btxrd,fracatlas}` Phần A: MAE, RMSE,
  Pearson, Spearman giữa điểm QualityHead và Dice thật mức polygon, `center_zoom` và
  `center_shift` riêng, kèm hình reliability theo bin. Vẫn ở V-L, thành Mode B sau khi chạy.
- **C10** trước ghi "định tính". Nay đã có notebook định lượng, Phần B cùng file. Chấm theo
  **độ phủ box với tổn thương GT** (bao trọn = 1.0, một phần = tỉ lệ diện tích), **không
  dùng mask mô hình**. K = 5, kèm @3. Số báo: Độ phủ trung bình, Độ phủ trung bình tốt nhất,
  Tỉ lệ ảnh khoanh trọn (>= 1 ô bao trọn 100% tổn thương). Vẫn ở V-L, thành Mode B sau khi chạy.

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
     F. Auxiliary outputs: prompt-use score and QualityHead   [nền cho C9, C10]
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
     L. Interactive demonstration and auxiliary quality signal   [C9, C10]  (dinh tinh)

VI.  DISCUSSION
     dien giai 4 truc; thu hep pham vi; han che
     (do phan giai co dinh, prompt mo phong, train tach 2 dataset, patient-level,
      protocol heuristic, loss chua nham vung nho/tam + loss thay the da thu khong cai thien,
      ablation mot split, Monte Carlo = on dinh khong phai vuot troi, chua probing feature-level,
      QualityHead chua hieu chuan, chua them baseline prompt hien dai ngoai SAM-Med2D vong nay)

VII. CONCLUSION
     PGA-UNet la gi, da danh gia gi, khong thiet lap dieu gi, future work

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
- Discussion và Conclusion giữ khung hiện tại, thêm 1 dòng cho kết quả loss âm tính.

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

### I.1. C9 và C10: gộp 1 notebook định lượng (đã chốt cách làm 2026-09-03)

Một notebook cho mỗi dataset: `test-auxiliary-signals-r512-{btxrd,fracatlas}.ipynb`, 5 cell,
dùng đúng checkpoint `00` (đã có QualityHead) và tập test. Chạy Kaggle được ngay, không train
thêm.

- Cell 1: setup (clone, tải checkpoint `00`, tải dataset)
- Cell 2: load model + hàm dùng chung (`run_prompt`, tiền xử lý, độ phủ)
- Cell 3, Phần A (C9): bọc logic `evaluate_quality_head.py`, chạy `center_zoom` và
  `center_shift`. Xuất bảng: Dataset, Prompt, Số polygon, MAE, RMSE, Pearson, Spearman
  (giữa điểm QualityHead và Dice thật mức polygon). Xuất hình: scatter điểm dự đoán vs Dice
  thật + đường theo bin (Dice trung bình mỗi bin điểm).
- Cell 4, Phần B (C10): mỗi ảnh test lấy 50 box ứng viên (kích thước 0.15 đến 0.55 khung),
  QualityHead chấm điểm, sắp xếp, lấy **top-5** (K chốt = 5). Với mỗi box top-5 tính
  **độ phủ** = tỉ lệ diện tích tổn thương nằm trong box (bao trọn thì 1.0, bao một phần
  thì theo tỉ lệ, không chạm thì 0). Không dùng mask mô hình để chấm, chỉ xét hình học box
  với tổn thương GT.
  - Mỗi ảnh: `độ phủ trung bình nhóm 5` và `độ phủ box tốt nhất nhóm 5`.
  - Toàn dataset: trung bình 2 số đó qua tất cả ảnh, gọi là **Độ phủ trung bình** (trung
    bình qua ảnh của độ phủ trung bình nhóm 5) và **Độ phủ trung bình tốt nhất** (trung
    bình qua ảnh của độ phủ box tốt nhất nhóm 5).
  - **Tỉ lệ ảnh khoanh trọn** = tỉ lệ ảnh mà trong nhóm 5 ô có ít nhất một ô bao trọn
    100% diện tích tổn thương (độ phủ ô tốt nhất = 1.0). Bao thiếu dù chỉ một phần nhỏ
    cũng không tính.
  - Bảng xuất: Dataset, Độ phủ trung bình, Độ phủ trung bình tốt nhất, Tỉ lệ ảnh khoanh trọn.
- Cell 5 (tuỳ chọn): 1 hình định tính, 1 ảnh với 3 box gợi ý điểm cao nhất + điểm QualityHead.

Trong bài: cả A và B nằm mục V-L, mỗi phần một bảng nhỏ. Câu chữ cho C10: "xếp hạng vùng
box ứng viên cho bác sĩ duyệt", không gọi là detection, không nói recall như một bộ phát hiện.
Câu chữ cho C9: nêu MAE và Spearman, kèm câu cấm "không phải xác suất hiệu chuẩn".

Demo giữ `top_k=5` cho khớp bài. Chưa có file kết quả nào trong `Result/`.

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

1. Giữ bản sửa file đuôi kép (mục H). [Đã chốt: giữ nguyên]
2. Viết `test-auxiliary-signals-r512-{btxrd,fracatlas}.ipynb` cho C9 + C10 (theo mục I.1),
   bản canonical trong `Source/File_Test/{btxrd,fracatlas}/`. **[Đã tạo 2026-09-03]**
   User tự chạy trên Kaggle, điền lại `CKPT_ID` nếu ID checkpoint `00` thay đổi.
3. Gộp số loss vào notebook `00` (theo mục G). [Chưa làm, chờ]
4. Trong lúc user chạy notebook: viết trước các mục KHÔNG phụ thuộc kết quả đó (II Related
   Work, III Method, IV Experimental Setup, và phần khung V, VI, VII). Có kết quả C9/C10
   thì viết tiếp V-L. Mỗi mục viết `.md` nháp cho user duyệt trước khi sửa `.tex`, rồi
   đồng bộ `access_vietnam.tex`.

## K. Trạng thái quyết định (2026-09-03)

- File đuôi kép: đúng là bug `qualitative_visualization.py`, giữ bản sửa hiện có.
- Gộp số loss: chờ duyệt khung.
- Checkpoint PGA-512: thư mục `00` là chính thức. FracAtlas 0.727 / 0.713.
- Baseline prompt hiện đại thêm (MedSAM/ScribblePrompt): future work, không làm vòng này.
- C9 + C10: gộp 1 notebook `test-auxiliary-signals-r512-*` mỗi dataset. C10 dùng **K = 5**,
  chấm theo **độ phủ tổn thương của box** (không dùng mask), báo Độ phủ trung bình + Độ phủ
  trung bình tốt nhất + Tỉ lệ ảnh khoanh trọn (ít nhất 1 ô bao trọn 100% tổn thương). Demo
  giữ `top_k = 5`.
