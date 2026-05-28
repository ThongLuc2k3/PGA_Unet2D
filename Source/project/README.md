# Prompt-Guided X-Ray Segmentation

Dự án khóa luận tốt nghiệp — Phân đoạn vùng xương tổn thương trên ảnh X-quang dùng Prompt-Guided Attention U-Net.

## Cấu trúc thư mục

```
project/
├── dataset.py            # Dataset JSON-polygon (dùng cho PGA-UNet)
├── dataset_simple.py     # Dataset mask-PNG (dùng cho UNet / Att-UNet baseline)
├── clean_data.py         # Tiền xử lý: xóa ICC profile khỏi PNG
├── train_unet.py         # Huấn luyện U-Net 2D (baseline)
├── train_attunet.py      # Huấn luyện Attention U-Net 2D (baseline)
├── train_pga.py          # Huấn luyện PGA-UNet 2D (đề xuất)
├── app.py                # Demo Gradio
└── models/
    ├── networks_other.py           # Hàm khởi tạo trọng số
    ├── layers/
    │   ├── grid_attention_layer.py # Grid Attention Block
    │   └── loss.py                 # Các hàm loss bổ sung
    └── networks/
        ├── utils.py                # unetConv2, unetUp, ...
        ├── unet_2D.py              # U-Net 2D gốc
        ├── attention_unet_2D.py    # Attention U-Net 2D
        └── prompt_unet_2D.py      # PGA-UNet 2D (đề xuất)
```

## Dataset

| Model | Định dạng dataset | Tham số |
|-------|-------------------|---------|
| UNet / Att-UNet | PNG masks (`train/masks/`) | `IMG_SIZE=256` |
| PGA-UNet | JSON polygon (`train/annotations/`) | `IMG_SIZE=512` |

## Chạy nhanh (Google Colab)

Xem file `All_Models.ipynb` — notebook duy nhất chứa đủ 3 model.

## Các thí nghiệm PGA-UNet

| Thí nghiệm | `EXPERIMENT` | `prompt_mode` |
|------------|-------------|---------------|
| Exp A | `'A'` | `zoom_out` only |
| Exp B | `'B'` | `mixed_7_3` (70% zoom-out + 30% shift) |
