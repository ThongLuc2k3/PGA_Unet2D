# Efficiency: đã có số đo MedSAM / ScribblePrompt

**Quyết định mới:** giữ nguyên các cụm so tham số trong V.D và Kết luận (KHÔNG bỏ).
Notebook efficiency đã chạy đủ 4 model, đặt tại `Result/File_test/test-measure_efficiency_btxrd.ipynb`
(bản canonical sạch: `Source/File_Test/test-measure_efficiency_btxrd.ipynb`, code y hệt).
File nháp cũ ở root đã xóa.

## Số đo thực tế (checkpoint BTXRD, Tesla T4, batch 1)

| Model | Params tổng | Params trainable | GFLOPs | Ckpt | GPU ms | CPU ms |
|---|---|---|---|---|---|---|
| PGA-UNet 256 | 2.955M | 2.955M | 7.74 | 11.4 MB | 8.7 | 93.6 |
| PGA-UNet 512 | 2.955M | 2.955M | 30.97 | 11.4 MB | 18.5 | 341.7 |
| SAM-Med2D 256 | 271.24M | 184.57M | 92.02 | 2443 MB | 50.3 | 1343.6 |
| MedSAM 1024 | 93.74M | 4.06M | 976.48 | 357.7 MB | 381.7 | 12129.4 |
| ScribblePrompt-UNet 128 | 3.99M | 3.99M | 32.81 | 15.2 MB | 6.2 | 187.4 |

## Kiểm tra các claim trong bài

| Claim | Vị trí | Số đo | Kết luận |
|---|---|---|---|
| "1/92 số tham số của SAM-Med2D" | Kết luận, mục efficiency, abstract | 271.24 / 2.955 = 91.8 | ĐÚNG, giữ |
| "12x nhẹ hơn FLOPs, 215x nhỏ hơn storage, 6x nhanh hơn GPU" (vs SAM-Med2D @256) | mục efficiency | 11.9x / 214x / 5.8x | ĐÚNG, giữ |
| **"khoảng 1/90 số tham số của MedSAM"** | **V.D** | **2.955 / 93.74 = 1/31.7** | **SAI. Phải là ~1/32.** Nhiều khả năng copy nhầm từ số "1/92" của SAM-Med2D |
| "ScribblePrompt-UNet số tham số xấp xỉ PGA-UNet" | V.D | 3.99M vs 2.96M (1.35x) | Chấp nhận được (cùng bậc); có thể để "xấp xỉ / cùng cỡ" |
| "ngang cỡ mô hình nhỏ nhất trong ba" | Kết luận | nhỏ nhất trong ba = ScribblePrompt 3.99M; PGA 2.955M còn nhỏ hơn cả ba | Đúng (hơi khiêm tốn), giữ |

## Cần sửa: chỉ 1 con số

### EN - `sections/05-results.tex:129`
HIỆN: `while using about $1/90$ of MedSAM's parameters and a smaller input.`
SỬA:  `while using about $1/32$ of MedSAM's parameters and a smaller input.`

### VN - `vietnam/access_vietnam.tex:375`
HIỆN: `trong khi chỉ dùng khoảng $1/90$ số tham số của MedSAM và một ảnh đầu vào nhỏ hơn.`
SỬA:  `trong khi chỉ dùng khoảng $1/32$ số tham số của MedSAM và một ảnh đầu vào nhỏ hơn.`

## Tùy chọn: có thêm dòng vào tab:efficiency không?

- KHÔNG thêm (giữ bảng gọn, chỉ PGA vs SAM-Med2D): đúng ý ban đầu "efficiency chỉ so SAM-Med2D".
  Số MedSAM/ScribblePrompt vẫn có nguồn là notebook trong Result/, đủ để chống câu "1/32".
- THÊM: bảng 5 dòng, mỗi model ở res gốc, thêm 1 câu caveat res khác nhau.

Khuyến nghị: KHÔNG thêm, chỉ sửa con số 1/90 -> 1/32.

## Sau khi sửa
- grep 2 file: không còn chuỗi `1/90`.
- grep dấu nối câu: không có -- / --- / en/em dash.
- build EN pdflatex + VN xelatex.
