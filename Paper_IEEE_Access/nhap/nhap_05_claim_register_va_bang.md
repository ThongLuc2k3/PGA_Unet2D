# Results: sổ đăng ký claim + bảng — ĐÃ ÁP VÀO .tex (2026-09-04)

Trạng thái: `sections/05-results.tex` + `sections/04-experimental-setup.tex` (EN) và
`vietnam/access_vietnam.tex` (VI) đã viết lại theo sổ này, build sạch (EN 12 trang,
VI 24 trang). **Chưa commit.** Số Claim gốc `claims_to_validate.md` (1-13), không đánh lại.

Bộ độ đo chuẩn mọi bảng so sánh: **Dice, IoU, HD95, CBL** (small-lesion vẫn có IoU nhưng
prose ghi Dice là overlap chính). `tab:selfassess` / `tab:suggest` dùng độ đo riêng.
Số image-level merged, prompt bao phủ trừ khi ghi rõ z/s. Nguồn: notebook trong `Result/`.

4 trụ: **P1** có prompt > không prompt · **P2** cách tận dụng prompt (Gaussian+PSG+CAD) ·
**P3** thắng SAM-Med2D, biên rộng nhất ở prompt lệch + tổn thương nhỏ · **P4** độ phân giải cao hơn thì tốt hơn.

---

## Bảng trong bài (số thứ tự cuối cùng từ .aux)

| # | Label | Mục | Claim / trụ | So sánh | Notebook nguồn |
|---|---|---|---|---|---|
| 1 | `tab:related` | II | — | công trình trước + khoảng trống | — |
| 2 | `tab:splits` | IV-A | — | train/val/test: BTXRD 1493/187/187 ảnh (1848/238/232 poly), FracAtlas 573/72/72 (730/95/92) | dataset split |
| 3 | `tab:resolution` | V-A | 11 / P4 | PGA @128/256/512, z/s — Dice,IoU,HD95px,HD95n,CBL | `pga-train-{128,256,512}` |
| 4 | `tab:baseline` | V-B | 1 / P1,P2 | PGA vs AttUNet no-prompt / +kênh / +crop @512, covering — **có cột $\Delta$Dice** | `test-pga-vs-attunet-variants-r512` |
| 5 | `tab:extreme` | V-C | 2 / P1,P2 | cùng 4 model, top-50 / bottom-50 theo Dice AttUNet @512 (bảng RIÊNG ngay sau V-B) | `test-subcat-pga-vs-attunet-variants-r512` |
| 6 | `tab:sam` | V-D | 3 / P3 | PGA vs SAM-Med2D zs/ft @256, covering | `test-pga-samzs-samft-r256` |
| 7 | `tab:small-sam` | V-E.1 | 4 / P3 | nhỏ: PGA-256 vs SAM zs/ft @256 (khung 512) | `test-subcat-small-r256` |
| 8 | `tab:small-att` | V-E.2 | 5 / P3 | nhỏ: PGA-512 vs AttUNet no-prompt / +kênh / +crop @512 | `test-subcat-small-r512` |
| 9 | `tab:small-res` | V-E.3 | 12 / P4 | nhỏ: PGA @128/256/512 (50 stem cố định), z/s | `test-subcat-pga-small-r128-256-512` |
| 10 | `tab:robust` | V-F | cross-cutting / P3 | 5 model (AttUNet no-prompt / +kênh / +crop / SAM-ft / PGA), z vs s + $\Delta$Dice | dùng lại số #4, #6 |
| 11 | `tab:ablation` | V-G | 6 / P2 | CAD-only / PSG-only / PSG+attn thường / full+hộp nhị phân / full PGA @512, z/s — **1 split** | `Result/File_test/*/ablation/*` |
| 12 | `tab:mccv` | V-H | 7 | PGA-512, 4 split ngẫu nhiên, mean±sd — + cột IoU | `test-pga-dataset-1234` |
| 13 | `tab:efficiency` | V-I | 8 | PGA-256 / PGA-512 / SAM-256 | `test-measure_efficiency_btxrd` |
| 14 | `tab:loss` | V-J | E1 | Dice+BCE (mặc định) / size-Tversky / Focal Dice @512, z/s | `pga 512/{00,01,10}` |
| 15 | `tab:selfassess` | V-L | 9 | Spearman của S_sharp, S_stab, Q vs Dice thật | `test-auxiliary-signals-r512` A |
| 16 | `tab:suggest` | V-L | 10 | shortlist top-3/top-5 xếp theo Q | `test-auxiliary-signals-r512` B |

Claim 13 (hai dataset): mọi bảng tách BTXRD / FracAtlas. Failure modes: `fig:failure` + văn.

## Con số then chốt đã đưa vào (đối chiếu nhanh)

- `tab:baseline` $\Delta$Dice (dòng − PGA): BTXRD no-prompt −0.265, +kênh −0.022, +crop −0.041 · FracAtlas −0.385, −0.134, −0.137.
- `tab:ablation` 1-split: BTXRD covering full PGA 0.782 vs binary 0.788 (binary nhỉnh Dice/IoU, full dẫn HD95 22.8 + CBL 0.918). FracAtlas full PGA thắng mọi cấu hình mọi độ đo. center_shift full PGA thắng cả 2 dataset. → prose đóng khung "tốt nhất 3/4 ô Dice; Gaussian rõ nhất ở off-center + FracAtlas; đa seed đang chạy".
- `tab:mccv` IoU: BTXRD 0.647±.006 / 0.639±.007 ; FracAtlas 0.595±.007 / 0.590±.010.
- `tab:resolution` HD95n (z/s): BTXRD 0.032/0.029, 0.030/0.035, 0.031/0.034 ; FracAtlas 0.044/0.053, 0.029/0.032, 0.015/0.014.
- small-lesion IoU đã thêm vào cả 3 bảng (#7,#8,#9): xem `Result/File_test/test-subcat-small-r256/-r512` và `test-subcat-pga-small-r128-256-512`.

## Prose đã sửa kèm

- Contribution bullet (`01-introduction.tex` + VI): "dùng Dice và IoU cho overlap, CBL cho định vị, HD95 cho biên".
- `04-experimental-setup.tex` Baselines-and-Metrics (+ VI): mọi bảng có Dice/IoU/CBL/HD95; Dice+IoU tương quan mạnh để cạnh nhau để đối chiếu; small-lesion IoU thấp + nhạy biên nên Dice là overlap chính; precision/recall trong log. Bỏ câu cũ "paper emphasizes Dice/CBL/HD95".
- `04` Datasets: đoạn văn split → `tab:splits`.
- V-B: đoạn 2 rút còn 1 câu (số vào cột $\Delta$Dice).
- V-I Efficiency: bỏ số trùng bảng, giữ tỉ lệ 92×/12×/215×/6×.
- `06-discussion.tex`: 1 câu ablation (single-split table + đa seed đang chạy).
- Bản VI: 8 pseudo-figure `\textit{[Hình N...]}` → `\includegraphics` thật (`../images/...`) + `\label/\ref`; thêm `\usepackage{graphicx}`. Bảng chuyển hết sang `\label/\ref` (bỏ "Bảng N." thủ công).

## CÒN TREO

- `tab:ablation` mới 1 split. Khi chạy xong multi-seed: chỉ thay số trong bảng + bỏ câu "rerun in progress" (caption + prose V-G + 06-discussion). Không đổi cấu trúc.
- Chưa commit (user chưa dặn).
- `khung_va_bo_cuc_viet_access.md` mục G (gộp số loss vào notebook `00`): chưa làm, số loss đã viết thẳng từ output `01`/`10`.
