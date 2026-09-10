# Sửa: kiểm định thống kê + HD95 không so được + mâu thuẫn "so sánh khớp 256"

Không chạy thêm thực nghiệm. Chỉ dùng dữ liệu per-image đã có trong `Result/File_test/*/ablation/`
và `Result/File_test/*/test-auxiliary-signals-*`.

## Dữ liệu per-image có sẵn (đủ để kiểm định)
- Ablation: 5 cấu hình x 2 dataset x 2 prompt mode, Dice từng ảnh (n=187 BTXRD, n=72 FracAtlas).
  Trung bình khớp chính xác Bảng ablation trong bài -> đúng nguồn.
- Self-assessment: Q vs true_dice từng đa giác (n=232 BTXRD, n=92 FracAtlas).
- KHÔNG có per-image cho tab:baseline / tab:sam / tab:extreme / tab:robust / tab:resolution / MCCV.

## Kết quả kiểm định (đã tính, script scratchpad/stats.py)

Kiểm định hoán vị bắt cặp (đổi dấu ngẫu nhiên 20000 lần, hai phía) trên Dice từng ảnh;
khoảng tin cậy bootstrap 95% cho chênh trung bình. Δ = Dice(đầy đủ) − Dice(biến thể).

| Biến thể | BTXRD phủ | BTXRD lệch | FracAtlas phủ | FracAtlas lệch |
|---|---|---|---|---|
| Chỉ CAD (bỏ PSG) | +0.010 (p=.11) | +0.015 (p=.03)* | +0.031 (p=.01)* | +0.028 (p=.01)* |
| Chỉ PSG (bỏ CAD) | +0.002 (p=.67) | +0.003 (p=.61) | +0.092 (p<.001)* | +0.102 (p<.001)* |
| PSG + attention thường (bỏ CAD) | +0.012 (p=.08) | +0.017 (p=.02)* | +0.038 (p=.02)* | +0.022 (p=.16) |
| Đầy đủ + hộp nhị phân | −0.006 (p=.24) | +0.004 (p=.64) | +0.059 (p<.001)* | +0.056 (p<.001)* |

Tóm tắt trung thực:
- BTXRD: phần lớn chênh KHÔNG đạt ý nghĩa trên một tập chia (kể cả +0.006 của hộp nhị phân,
  CI bootstrap [−0.017, +0.004] chứa 0). Chỉ prompt lệch tâm: đầy đủ > "chỉ CAD" và > "PSG+attention thường".
- FracAtlas: đầy đủ vượt CẢ 4 biến thể ở prompt phủ (p ≤ .02); vượt 3/4 ở lệch tâm.
  Chênh lớn nhất là so với "chỉ PSG" (bỏ CAD): +0.09 đến +0.10 Dice, p<.001 -> CAD đóng góp mạnh trên FracAtlas.

Self-assessment Spearman(Q, true Dice), permutation p + bootstrap 95% CI:
| | rho | 95% CI | p |
|---|---|---|---|
| BTXRD phủ | 0.70 | [0.61, 0.77] | <.001 |
| BTXRD lệch | 0.60 | [0.50, 0.69] | <.001 |
| FracAtlas phủ | 0.65 | [0.51, 0.76] | <.001 |
| FracAtlas lệch | 0.48 | [0.29, 0.63] | <.001 |

## HD95 các frame khác nhau (xác nhận từ code notebook)

| Nguồn | frame HD95 |
|---|---|
| PGA-UNet 512 / 256 / 128 | 512 / 256 / 128 px |
| AttUNet + 2 biến thể (512) | 512 px |
| SAM-Med2D | 256 px |
| MedSAM | **độ phân giải ảnh GỐC (thay đổi từng ảnh)** |
| ScribblePrompt | độ phân giải ảnh gốc |

=> HD95 trong `tab:sam` và `tab:robust` trộn 4 loại frame, KHÔNG chuẩn hóa được bằng một S
(thiếu per-image gốc của MedSAM/ScribblePrompt). Dice, IoU, CBL đều bất biến theo frame.
Bảng khác (tab:baseline, tab:extreme, tab:resolution) đều cùng frame 512 hoặc đã có HD95_n -> giữ nguyên.

## CÁC THAY ĐỔI (EN + VN)

### 1. Thêm đoạn "Statistical analysis" vào Mục IV (sau Baselines and Metrics)
Nói: bảng so sánh chính là ước lượng điểm trên một tập chia (không chạy lại mọi baseline qua
nhiều split); độ ổn định của PGA-UNet qua split = MCCV (SD Dice ≤ 0.011); nơi có per-image
(ablation, self-assessment) dùng kiểm định hoán vị bắt cặp 20000 lần + bootstrap 95% CI; hệ số
tương quan Q báo p hoán vị + CI bootstrap.

### 2. Mục V.H (Ablation): thêm 1 đoạn + bảng con Δ/p (bảng ở trên)
Giữ nguyên tab:ablation. Thêm `tab:ablation-sig`. Thêm câu tóm tắt trung thực (BTXRD phần lớn
không ý nghĩa / FracAtlas có ý nghĩa, CAD mạnh trên FracAtlas).

### 3. Mục V.J + tab:selfassess: thêm p + CI (1 câu, hoặc thêm cột CI vào bảng)

### 4. tab:sam: BỎ cột HD95. Thêm dòng PGA-UNet @256.
Cột còn: Dataset | Model | Res. | Dice | IoU | CBL.
PGA-UNet 256: BTXRD 0.762 / 0.633 / 0.902 ; FracAtlas 0.629 / 0.470 / 0.895 (số phủ từ tab:resolution).
Caption thêm: HD95 bỏ vì mỗi model chấm trong frame gốc riêng, không so trực tiếp được;
Dice/IoU/CBL bất biến frame.

### 5. §V.D text: viết lại
- Nêu rõ so sánh KHỚP độ phân giải: PGA@256 (0.762 / 0.629) vs SAM-Med2D-ft@256 (0.630 / 0.563),
  chênh 0.13 / 0.07 Dice.
- PGA@512 là cấu hình tốt nhất của mô hình.
- MedSAM@1024, ScribblePrompt@128 ở frame gốc; so Dice/IoU/CBL, bỏ HD95.
- BỎ cụm "dẫn về HD95 ở hầu hết ô".

### 6. §IV Baselines (EN dòng 41 / VN 236): thêm MedSAM + ScribblePrompt vào danh sách,
   nói tab:sam trình bày PGA ở cả 256 (khớp) lẫn 512 (tốt nhất).

### 7. tab:robust: BỎ cột HD95 z/s. Caption bỏ nhắc HD95, thêm lý do.
Cột còn: Dataset | Model | Dice z/s | ΔDice | IoU z/s | CBL z/s.

### 8. Thảo luận (VN 751 / EN 06 dòng 7): đổi
"Thí nghiệm ablation hiện vẫn đang trong giai đoạn chuyển từ một lần chia sang nhiều lần chia."
-> "Thí nghiệm ablation chỉ dựa trên một tập chia; chúng tôi định lượng độ chắc chắn bằng kiểm
định bắt cặp trên Dice từng ảnh (Mục V.H) thay cho việc lặp lại qua nhiều seed."

### 9. Kết luận future work (VN 756): "hoàn tất thí nghiệm ablation với nhiều seed"
-> "mở rộng ablation và đánh giá qua nhiều tập chia" (giữ là future work, không ngụ ý đã bắt đầu).

## Sau khi sửa: build EN + VN, grep 1/90 / SAM2 / em-dash, kiểm ref.
