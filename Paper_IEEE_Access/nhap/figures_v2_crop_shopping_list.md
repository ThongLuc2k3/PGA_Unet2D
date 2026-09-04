# Figure V2: danh sách hàng ảnh cần crop (bản chốt, 7 hình / 23 hàng)

Cách làm:
- Anh chạy các notebook bên dưới (bản trong `Result/`, hoặc chạy lại `Source/File_Test/...`
  trên Kaggle), crop **nguyên hàng ngang** của đúng stem — lấy **hết các cột** + phần chữ
  metric của hàng, chừa lề rộng, **không cắt cột**.
- Đặt tên file theo cột "Tên file gửi". Mỗi file kèm ghi chú: hình nào / model gì / ca gì /
  prompt zoom hay shift.
- Tôi lo: cắt cột, căn đều lên lưới lớn, dán nhãn hàng + tiêu đề section + header cột y như
  7 ảnh hiện tại, xuất `<tên>_V2.png`.

Quy ước prompt: `center_zoom` = bao phủ / "Zoom-out"; `center_shift` = lệch tâm / "Shift".
Trừ F5, mỗi hàng chỉ 1 điều kiện — anh chọn zoom hay shift tùy ảnh nào đẹp, khác nhau giữa
các hình cũng được. Nếu chọn shift, tôi thêm chữ vào caption cho khớp bảng (bảng ghi "covering").

Nếu stem cần không nằm trong lưới notebook đang vẽ, sửa danh sách stem hiển thị của notebook
rồi chạy lại đúng cell vẽ.

---

## F1 — `unet_extreme_groups_btxrd_V2.png`   (mục V-B Claim 1 + V-C Claim 2)

Mirror `tab:baseline` / `tab:extreme`. Notebook:
`Result/File_test/btxrd/test-subcat-pga-vs-attunet-variants-r512-btxrd.ipynb`.

4 model @512, trên 2 ca: IMG000184 (AttUNet tốt nhất) + IMG000791 (AttUNet tệ nhất).
= **8 hàng**.

| # | Model / section | Stem | Prompt | Tên file gửi |
|---|---|---|---|---|
| 1 | Attention U-Net (no prompt) | IMG000184 | (không prompt) | `F1_184_attunet.png` |
| 2 | AttUNet + kênh prompt | IMG000184 | anh chọn | `F1_184_channel.png` |
| 3 | AttUNet + crop theo prompt | IMG000184 | anh chọn | `F1_184_crop.png` |
| 4 | PGA-UNet | IMG000184 | anh chọn | `F1_184_pga.png` |
| 5 | Attention U-Net (no prompt) | IMG000791 | (không prompt) | `F1_791_attunet.png` |
| 6 | AttUNet + kênh prompt | IMG000791 | anh chọn | `F1_791_channel.png` |
| 7 | AttUNet + crop theo prompt | IMG000791 | anh chọn | `F1_791_crop.png` |
| 8 | PGA-UNet | IMG000791 | anh chọn | `F1_791_pga.png` |

Tiêu đề section: "Top-Dice case (IMG000184)" / "Bottom-Dice case (IMG000791)".
Nhãn hàng: "Attention U-Net" / "AttUNet + kênh" / "AttUNet + crop" / "PGA-UNet".

---

## F2 — `small_lesion_sam_pga256_pga512_V2.png`   (mục V-D Claim 3 + V-E.1 Claim 4)

Mirror `tab:sam` / `tab:small-sam`. Notebook:
`Result/File_test/btxrd/test-subcat-small-r256-btxrd.ipynb`. Stem IMG000868 (vai, 2 tổn
thương nhỏ). = **3 hàng**.

| # | Model | Stem | Prompt | Tên file gửi |
|---|---|---|---|---|
| 1 | SAM-Med2D zero-shot $256$ | IMG000868 | anh chọn | `F2_868_sam_zs.png` |
| 2 | SAM-Med2D fine-tuned $256$ | IMG000868 | anh chọn | `F2_868_sam_ft.png` |
| 3 | PGA-UNet $256$ | IMG000868 | anh chọn | `F2_868_pga256.png` |

Nhãn hàng: "SAM-Med2D zero-shot 256" / "SAM-Med2D fine-tuned 256" / "PGA-UNet 256".

---

## F3 — `small_lesion_pga_vs_attunet_V2.png`   (mục V-E.2 Claim 5)

Mirror `tab:small-att`. Notebook:
`Result/File_test/btxrd/test-subcat-small-r512-btxrd.ipynb`. 1 ca tổn thương nhỏ (anh
chọn ca đẹp trong subset). = **4 hàng** @512.

| # | Model | Prompt | Tên file gửi |
|---|---|---|---|
| 1 | Attention U-Net (no prompt) | (không prompt) | `F3_attunet.png` |
| 2 | Attention U-Net + kênh prompt | anh chọn | `F3_channel.png` |
| 3 | Attention U-Net + crop theo prompt | anh chọn | `F3_crop.png` |
| 4 | PGA-UNet | anh chọn | `F3_pga.png` |

Ghi kèm tên stem anh dùng.

---

## F4 — `small_lesion_pga_128_256_512_V2.png`   (mục V-A Claim 11 + V-E.3 Claim 12)

Mirror `tab:small-res` (+ `tab:resolution`). Notebook:
`Result/File_test/btxrd/test-subcat-pga-small-r128-256-512-btxrd.ipynb` — notebook này
hiện KHÔNG vẽ ảnh, cần thêm 1 cell vẽ (hoặc lấy IMG000868 từ 3 notebook `pga-train-128/256/512`).
Stem IMG000868. = **3 hàng**.

| # | Model | Stem | Prompt | Tên file gửi |
|---|---|---|---|---|
| 1 | PGA-UNet $128$ | IMG000868 | anh chọn | `F4_868_pga128.png` |
| 2 | PGA-UNet $256$ | IMG000868 | anh chọn | `F4_868_pga256.png` |
| 3 | PGA-UNet $512$ | IMG000868 | anh chọn | `F4_868_pga512.png` |

Nhãn hàng: "PGA-UNet 128x128" / "256x256" / "512x512".

---

## F5 — `prompt_robustness_examples_V2.png`   (mục V-F robustness)

Mirror `tab:robust` (thông điệp: dịch prompt gần như không đổi kết quả). Notebook:
`Result/File_test/btxrd/test-pga-vs-attunet-variants-r512-btxrd.ipynb` (section PGA-UNet
chạy cả center_zoom lẫn center_shift). PGA-UNet @512, **1 ca, 2 hàng** (cùng ca).

| # | Model | Prompt | Tên file gửi |
|---|---|---|---|
| 1 | PGA-UNet $512$ | center_zoom | `F5_pga_zoom.png` |
| 2 | PGA-UNet $512$ | center_shift | `F5_pga_shift.png` |

Ghi kèm tên stem (nên là ca nhiều polygon, Dice trung bình). Nhãn hàng: "Bao phủ
(center\_zoom)" / "Lệch tâm (center\_shift)".

---

## F6 — `ablation_gaussian_vs_binary_case_V2.png`   (mục V-G Claim 6)

Mirror `tab:ablation` (chỉ nhánh full Gaussian vs full binary). Notebook:
`Result/File_test/btxrd/ablation/test-full-pga-heatmap-reference-btxrd/...ipynb` (Gaussian)
+ `.../test-full-binary-prompt-btxrd/...ipynb` (binary). Stem IMG001464. = **2 hàng** @512.

2 notebook này trước vẽ IMG000013, KHÔNG có IMG001464 — anh thêm `'IMG001464'` vào danh
sách stem hiển thị của cả 2 rồi chạy lại cell vẽ. (Muốn đổi stem khác có ở cả hai thì báo.)

| # | Model | Stem | Prompt | Tên file gửi |
|---|---|---|---|---|
| 1 | PGA-UNet full (Gaussian + PSG + CAD) | IMG001464 | anh chọn | `F6_1464_gaussian.png` |
| 2 | PGA-UNet full + hộp nhị phân | IMG001464 | anh chọn | `F6_1464_binary.png` |

Nhãn hàng: "PGA-UNet (Gaussian)" / "PGA-UNet (Binary)". Số Dice/IoU tôi điền từ metric
trên hàng.

---

## F7 — `failure_case_overlap_V2.png`   (mục V-K Failure modes)

Notebook: `Result/File_test/btxrd/test-pga-vs-attunet-variants-r512-btxrd.ipynb`
(section PGA-UNet). PGA-UNet @512, **1 hàng**, 1 ca thất bại (tổn thương dài/phân nhánh
hoặc ở vùng giải phẫu chồng lấn: ngực/sườn/vai/xương đòn, Dice thấp dù prompt phủ đúng).

| # | Model | Prompt | Tên file gửi |
|---|---|---|---|
| 1 | PGA-UNet $512$ | anh chọn | `F7_failure_pga.png` |

Ghi kèm tên stem.

---

## Tổng kết cần gửi

| Hình | Số file | Ghi chú |
|---|---|---|
| F1 | 8 | `F1_*` |
| F2 | 3 | `F2_868_*` |
| F3 | 4 | `F3_*` + tên stem |
| F4 | 3 | `F4_868_*` (cần thêm cell vẽ) |
| F5 | 2 | `F5_pga_zoom/shift` + tên stem |
| F6 | 2 | `F6_1464_*` (thêm IMG001464 vào 2 notebook) |
| F7 | 1 | `F7_failure_pga` + tên stem |

**23 file hàng ảnh.** Crop rộng đủ mọi cột + chữ metric. Tôi lo cắt cột, căn lưới, dán
nhãn/tiêu đề như 7 ảnh hiện tại.

Screenshot anh tự chụp riêng (không thuộc list này): `demo_segmentation` (III-A),
`demo_suggestion` (V-L). Sơ đồ `architecture_pga_unet` giữ nguyên.
