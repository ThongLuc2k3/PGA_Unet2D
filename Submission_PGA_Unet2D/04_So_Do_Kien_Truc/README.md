# 04 — Sơ đồ kiến trúc

## Files có sẵn

| File | Nội dung |
|------|----------|
| `arch_pga_unet2d.drawio` | Kiến trúc PGA-UNet (đề xuất) |
| `arch_unet2d.drawio` | Kiến trúc U-Net baseline |
| `arch_attention_unet2d.drawio` | Kiến trúc Attention U-Net |
| `arch_sammed2d.drawio` | Kiến trúc SAM-Med2D (ViT-B + Adapter) |
| `pipeline_pga_app_inference.drawio` | Toàn bộ inference pipeline app.py |
| `diagram_pga.png` | PGA-UNet — ảnh PNG chất lượng cao |
| `diagram_unet.png` | U-Net — ảnh PNG |
| `diagram_attunet.png` | Attention U-Net — ảnh PNG |
| `diagram_sammed2d.png` | SAM-Med2D — ảnh PNG |

## Mở file .drawio

Dùng [draw.io](https://app.diagrams.net/) (miễn phí, online) hoặc VS Code extension "Draw.io Integration".

## Còn thiếu (cần vẽ thêm)

- `system_architecture.png` — Sơ đồ tổng thể toàn bộ hệ thống (MobileNetV4 → PGA → IPR → GradCAM)
- `preprocessing_pipeline.png` — 6 bước tiền xử lý dữ liệu
- `classification_pipeline.png` — Pipeline MobileNetV4 Gatekeeper
