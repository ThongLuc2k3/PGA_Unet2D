# Hồ Sơ Nộp Xét Duyệt — PGA-UNet

**Đề tài:** Phát triển hệ thống phân đoạn ảnh X-quang xương dựa vào câu nhắc trực quan  
**Tác giả:** Lục Tố Thông | **GVHD:** PGS.TS. Lý Quốc Ngọc & ThS. Đỗ Thị Thanh Hà | **Năm:** 2026  
**Bộ dữ liệu:** BTXRD — Bone Tumor X-Ray Dataset (Nature Scientific Data, 2024)

---

## Cấu Trúc Hồ Sơ

```
Submission_PGA_Unet2D/
├── 01_Dong_Gop_De_Tai/
│   └── 01_Dong_Gop_De_Tai.md       ← Mô tả đóng góp, kiến trúc, kết quả tóm tắt
├── 02_Minh_Chung_So_Lieu/
│   └── 02_Minh_Chung_So_Lieu.md    ← Toàn bộ bảng số liệu thực nghiệm
├── 03_Minh_Chung_Hinh_Anh/
│   ├── 03_Minh_Chung_Hinh_Anh.md   ← Mô tả và hiển thị toàn bộ hình ảnh
│   └── images/                     ← 68 ảnh PNG trích từ Result/ notebooks
├── 04_Tai_Lieu_Tham_Khao/
│   └── 04_Tai_Lieu_Tham_Khao.md    ← Danh mục tài liệu và công cụ
├── 05_Ky_Thuat_Su_Dung/
│   └── 05_Ky_Thuat_Su_Dung.md      ← Phân biệt kỹ thuật kế thừa vs đề xuất mới
└── README.md                        ← File này
```

---

## Hướng Dẫn Đọc Nhanh

| Câu hỏi | Xem tại |
|---|---|
| Đề tài đóng góp gì? | **01_Dong_Gop_De_Tai.md** |
| Số liệu cụ thể PGA vs baseline? | **02_Minh_Chung_So_Lieu.md — Mục C, D, E** |
| Ablation PSG / CAD / loại câu nhắc? | **02_Minh_Chung_So_Lieu.md — Mục G** |
| Kết quả phân lớp EfficientNet_B3? | **02_Minh_Chung_So_Lieu.md — Mục J** |
| Pipeline end-to-end (cascading error)? | **02_Minh_Chung_So_Lieu.md — Mục K** |
| Hình ảnh minh chứng trực quan? | **03_Minh_Chung_Hinh_Anh.md** |
| Điều gì đề xuất mới, điều gì kế thừa? | **05_Ky_Thuat_Su_Dung.md** |

---

## Kết Quả Chính

| Mô hình | Zoom-out Dice | Shift Dice | Mixed Dice | Tham số |
|---|---|---|---|---|
| U-Net (không có prompt) | 0.4534 | — | — | ~7M |
| Attention U-Net (không có prompt) | 0.4159 | — | — | ~8M |
| SAM-Med2D zero-shot | 0.5337 | 0.5184 | 0.5286 | ~100M |
| SAM-Med2D fine-tuned | 0.7350 | 0.7097 | 0.7283 | ~100M |
| **PGA-UNet (đề xuất)** | **0.8524** | **0.8382** | **0.8496** | **~4M** |

**Pipeline end-to-end** (EfficientNet_B3 → PGA-UNet, 375 ảnh hỗn hợp):  
Pipeline Dice = **0.7296**, AUC-ROC phân lớp = **0.9688**

---

## Tài Nguyên Bổ Sung (Google Drive)

| Nội dung | Link |
|---|---|
| Dataset BTXRD | https://drive.google.com/file/d/1fU7KPln7joaa3EZZtGn-VKeg9i4AmPG3 |
| PGA-UNet checkpoint | https://drive.google.com/file/d/1Mv-rUPI7KGmYemd27hmKbJQRHc4ZKB9z |
| SAM-Med2D fine-tuned checkpoint | https://drive.google.com/file/d/1fTEhbgpEzzEqdB8CEW8wH8KnX1YlJJM4 |
| Toàn bộ hồ sơ nộp | https://drive.google.com/drive/folders/1OP8RgnqKwXyYOP_NQf8B_u7E3lpiGJ-m |
