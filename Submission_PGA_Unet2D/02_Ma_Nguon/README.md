# 02 — Mã nguồn và Mô hình

## Cấu trúc

```
02_Ma_Nguon/
├── models/
│   ├── networks/
│   │   ├── prompt_unet_2D.py      # PGA-UNet (đề xuất chính)
│   │   ├── unet_2D.py             # U-Net baseline
│   │   ├── attention_unet_2D.py   # Attention U-Net baseline
│   │   └── utils.py               # Utilities
│   └── layers/
│       ├── grid_attention_layer.py  # Attention Gate layer
│       └── loss.py                  # Loss functions (BCE + Dice)
├── dataset_pga.py     # Dataset cho PGA-UNet (JSON polygon, 3 prompt modes)
├── dataset_simple.py  # Dataset cho U-Net/AttUNet (mask PNG)
├── train_pga.py       # Script train PGA-UNet
├── train_unet.py      # Script train U-Net
├── train_attunet.py   # Script train Attention U-Net
├── app.py             # Demo Gradio UI
└── requirements.txt   # Thư viện

checkpoints/           # Trọng số (download từ Drive)
  ├── pga_unet_expB_best.pth   # PGA-UNet best checkpoint
  └── best_mobilenetv4.pth     # MobileNetV4 Gatekeeper
```

## Mô hình đề xuất: PGA-UNet (`models/networks/prompt_unet_2D.py`)

**Kiến trúc:** U-Net encoder-decoder + 2 module mới:
- `PromptSpatialGate`: nhân feature map với Gaussian heatmap → tập trung vào vùng prompt
- `ConditionedAttention`: attention gate được điều kiện hóa bởi heatmap → loại bỏ noise ngoài vùng quan tâm

**Tham số:** ~4M trainable params (nhỏ hơn SAM-Med2D ~25×)

## Cách chạy training

```bash
# Train PGA-UNet
python train_pga.py \
    --img_dir dataset_BTXRD/train/images \
    --json_dir dataset_BTXRD/train/annotations \
    --val_img_dir dataset_BTXRD/val/images \
    --val_json_dir dataset_BTXRD/val/annotations

# Train U-Net baseline
python train_unet.py

# Train Attention U-Net baseline
python train_attunet.py
```

## Cài đặt môi trường

```bash
pip install -r requirements.txt
```

**Yêu cầu:** Python 3.9+, CUDA GPU (≥8GB VRAM khuyến nghị), PyTorch ≥2.0

## Checkpoints (Google Drive)

| Mô hình | Link Drive | Dice test |
|---------|-----------|-----------|
| PGA-UNet Exp B | [drive.google.com/...1Mv-rUPI7KGmYemd27hmKbJQRHc4ZKB9z] | 0.8558 |
| MobileNetV4 | [Điền link] | AUC=0.9514 |
