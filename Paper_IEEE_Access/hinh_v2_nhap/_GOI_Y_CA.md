# Gợi ý ca (stem) cho từng hình — chọn ca PGA có lợi rõ ràng

Số dưới đây trích từ output notebook hiện có (protocol mới). "z/s" = center_zoom / center_shift.

## F1 — extreme (AttUNet no-prompt / +kênh / +crop / PGA @512)

- **Top-Dice**: `IMG000184` — PGA Dice 0.954. Ca dễ, mọi model tốt (đúng thông điệp "ca dễ thì ngang nhau").
- **Bottom-Dice**: `IMG000791` (bottom #1, AttUNet tệ nhất) — PGA 0.822. Hoặc ca PGA cao hơn ở nhóm bottom:
  `IMG000622` (PGA 0.935), `IMG000258` (0.930), `IMG001263` (0.917) — cần chạy lại để xem channel/crop.
- Giữ IMG000184 + IMG000791 như kế hoạch là ổn. Sau khi chạy cell `f1-figure-rows` sẽ có channel/crop.

## F2 — small-lesion PGA-256 vs SAM (zs / ft) — ĐÃ CÓ SỐ

| Stem | zs | ft | pga256 | Ghi chú |
|---|---|---|---|---|
| **IMG000337** | 0.395 | 0.438 | **0.720** | gradient zs<ft<pga sạch nhất, mọi giá trị có nghĩa |
| **IMG000932** | 0.000 | 0.000 | **0.833** | SAM cả 2 ra 0, PGA rất cao — thông điệp mạnh |
| IMG000360 | 0.154 | 0.649 | 0.714 | gradient rõ, ft đã khá |
| IMG000868 | 0.000 | 0.055 | 0.630 | zs fail, ft gần như fail, pga khá |
| IMG000753 | 0.000 | 0.164 | 0.757 | zs fail, ft yếu, pga tốt |
| IMG000373 | 0.014 | 0.000 | 0.769 | ft < zs (ngược) — không nên |
| IMG000542 | 0.185 | 0.000 | 0.769 | ft < zs (ngược) — không nên |

→ Nên **IMG000337** (gradient đẹp) hoặc **IMG000932** (SAM fail hoàn toàn).

## F3 — small-lesion PGA-512 vs AttUNet baselines — CHỜ CHẠY

Notebook `test-subcat-small-r512` đã sửa để vẽ đúng ảnh nhỏ, cùng thứ tự 10 stem như F2.
Chạy xong xem ca nào AttUNet no-prompt ~0, channel/crop trung bình, PGA cao rõ.

## F4 — small-lesion PGA @128/256/512 — CHỜ CHẠY

Notebook `test-subcat-pga-small-r128-256-512` đã thêm cell `f4-figure-rows` (3 panel, cùng
10 stem). Chạy xong chọn ca mà Dice tăng đều 128 < 256 < 512 (VD từ F2: IMG000337 pga256=0.720).

## F5 — robustness PGA-512 (zoom vs shift), cùng ca — ĐÃ CÓ SỐ

| Stem | z Dice | s Dice | ΔDice | Ghi chú |
|---|---|---|---|---|
| **IMG000020** | 0.942 | 0.942 | **0.000** | tốt nhất — Dice cao, y hệt, hộp dịch rõ |
| IMG000028 | 0.763 | 0.764 | +0.001 | rất ổn định |
| IMG000066 | 0.706 | 0.704 | -0.002 | ổn định |
| IMG000002 | 0.881 | 0.872 | -0.009 | khớp mức TB bảng (-0.008) |
| IMG000052 | 0.823 | 0.721 | -0.102 | tụt nhiều — KHÔNG dùng |

→ Nên **IMG000020**.

## F6 — ablation PGA full-Gaussian vs full-binary @512 — ĐÃ CÓ SỐ (từ CSV per-image)

BTXRD (covering, `center_zoom`):

| Stem | Gaussian | Binary | Δ |
|---|---|---|---|
| **IMG000821** | 0.889 | 0.654 | **+0.235** |
| IMG000643 | 0.724 | 0.531 | +0.193 |
| IMG000369 | 0.669 | 0.488 | +0.181 |
| IMG001342 | 0.708 | 0.542 | +0.165 |
| IMG000438 | 0.831 | 0.677 | +0.155 |

FracAtlas (covering): IMG0002470 (0.760 vs 0.533), IMG0001980 (0.872 vs 0.676), IMG0002533 (0.788 vs 0.600).

→ Nên **IMG000821** (BTXRD, covering): Gaussian 0.889 vs Binary 0.654, khoảng cách rõ, cả hai đều
non-trivial. Thêm stem này vào danh sách vẽ của 2 notebook ablation rồi chạy lại.
(Nếu muốn kịch tính: IMG000648 shift, Gaussian 0.856 vs Binary 0.000 — nhưng là shift + binary sập hẳn.)

## F7 — failure PGA-512 — ĐÃ CÓ SỐ

`IMG000013` (Dice 0.120) — ca ngực, tổn thương ở bờ ngực/sườn, prompt phủ nhưng PGA dự
đoán lệch chỗ. Là ca fail rõ nhất trong 10 ảnh test thường của notebook small-r512. Giữ.
