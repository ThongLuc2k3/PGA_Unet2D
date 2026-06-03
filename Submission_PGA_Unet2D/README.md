# Hồ Sơ Gửi Giảng Viên — PGA-UNet

**Đề tài:** Phát triển hệ thống phân đoạn ảnh X-quang xương dựa vào câu nhắc trực quan  
**Tác giả:** Lục Tố Thông | **Năm:** 2026

---

## Cấu Trúc Hồ Sơ

| File | Nội dung |
|---|---|
| `01_Dong_Gop_De_Tai.md` | Đóng góp 1 (kiến trúc PGA-UNet) và Đóng góp 2 (pipeline lâm sàng) — với công thức toán học |
| `02_Minh_Chung_So_Lieu.md` | Toàn bộ bảng số liệu: phân đoạn, phân lớp, phòng vệ, đặc tính tổn thương |
| `03_Minh_Chung_Hinh_Anh.md` | Mô tả các ảnh minh chứng kèm đường dẫn (ảnh trong thư mục `images/`) |
| `04_Tai_Lieu_Tham_Khao.md` | Danh mục 6 tài liệu tham khảo chính |
| `05_Ky_Thuat_Su_Dung.md` | Phân biệt kỹ thuật kế thừa vs đề xuất mới — tránh đạo văn |
| `images/` | Ảnh visualization + sơ đồ kiến trúc (14 file PNG) |

---

## Kết Quả Chính

| Mô hình | Dice (Mixed 70/30) | Tham số |
|---|---|---|
| U-Net | 0.5090 | ~7M |
| Attention U-Net | 0.4110 | ~8M |
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
