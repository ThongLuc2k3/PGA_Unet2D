# Hồ Sơ Gửi Giảng Viên — PGA-UNet

**Đề tài:** Phát triển hệ thống phân đoạn ảnh X-quang xương dựa vào câu nhắc trực quan  
**Tác giả:** Lục Tố Thông | **GVHD:** PGS.TS. Lý Quốc Ngọc & ThS. Đỗ Thị Thanh Hà | **Năm:** 2026

---

## Cấu Trúc Hồ Sơ

```
Submission_PGA_Unet2D/
├── main.tex                        ← compile ra PDF (pdflatex main.tex × 2)
├── 01_Dong_Gop_De_Tai/             ← Đóng góp PSG, CAD, GradCAM+IPR, MobileNetV4
│   ├── 01_Dong_Gop_De_Tai.tex
│   └── 01_Dong_Gop_De_Tai.md
├── 02_Minh_Chung_So_Lieu/          ← Số liệu phân đoạn, phân lớp, phòng vệ
│   ├── 02_Minh_Chung_So_Lieu.tex
│   └── 02_Minh_Chung_So_Lieu.md
├── 03_Minh_Chung_Hinh_Anh/         ← Mô tả + 21 ảnh PNG
│   ├── 03_Minh_Chung_Hinh_Anh.tex
│   ├── 03_Minh_Chung_Hinh_Anh.md
│   └── images/  (21 ảnh PNG)
├── 04_Tai_Lieu_Tham_Khao/          ← 8 tài liệu (có PDF hoặc link)
│   ├── 04_Tai_Lieu_Tham_Khao.tex
│   └── 04_Tai_Lieu_Tham_Khao.md
└── 05_Ky_Thuat_Su_Dung/            ← Phân biệt kế thừa vs đề xuất mới
    ├── 05_Ky_Thuat_Su_Dung.tex
    └── 05_Ky_Thuat_Su_Dung.md
```

---

## Kết Quả Chính

| Mô hình | Dice (Mixed 70/30) | Tham số |
|---|---|---|
| U-Net (không có câu nhắc) | 0.5090 | ~7M |
| Attention U-Net (không có câu nhắc) | 0.4110 | ~8M |
| SAM-Med2D zero-shot | 0.5289 | ~100M |
| SAM-Med2D fine-tuned | 0.7554 | ~100M |
| **PGA-UNet (đề xuất)** | **0.8558** | **~4M** |

---

## Tài Nguyên Bổ Sung (Google Drive)

| Nội dung | Link |
|---|---|
| Dataset BTXRD | https://drive.google.com/file/d/1fU7KPln7joaa3EZZtGn-VKeg9i4AmPG3 |
| PGA-UNet checkpoint | https://drive.google.com/file/d/1Mv-rUPI7KGmYemd27hmKbJQRHc4ZKB9z |
| SAM-Med2D fine-tuned | https://drive.google.com/file/d/1fTEhbgpEzzEqdB8CEW8wH8KnX1YlJJM4 |
| MobileNetV4 Gatekeeper | [Điền link Drive] |
| Toàn bộ hồ sơ nộp | https://drive.google.com/drive/folders/1OP8RgnqKwXyYOP_NQf8B_u7E3lpiGJ-m |
