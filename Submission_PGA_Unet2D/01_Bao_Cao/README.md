# 01 — Báo cáo và Tài liệu

## Files cần có trong thư mục này

| File | Trạng thái | Ghi chú |
|------|-----------|---------|
| `Bao_cao_khoa_luan.pdf` | ⏳ Cần compile | Compile từ `Report/main.tex` bằng pdflatex |
| `Slide_Thuyet_Trinh.pptx` | ⏳ Chưa có | Cần tạo slide cho buổi bảo vệ |

## Cách compile PDF

```bash
cd Report/
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

Hoặc dùng Overleaf: upload toàn bộ thư mục `Report/` lên Overleaf và compile.

## Cấu trúc báo cáo

- **Chương 1:** Giới thiệu — bài toán, động lực, đóng góp
- **Chương 2:** Cơ sở lý thuyết — U-Net, SAM, GradCAM, Visual Prompt
- **Chương 3:** Phương pháp đề xuất — PGA-UNet, IPR, GradCAM Rescue, Gatekeeper
- **Chương 4:** Thực nghiệm và đánh giá — so sánh 5 mô hình, phân tích phòng vệ
- **Chương 5:** Kết luận và hướng phát triển
