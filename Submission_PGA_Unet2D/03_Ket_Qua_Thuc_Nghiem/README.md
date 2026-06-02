# 03 — Kết quả thực nghiệm

## Files

| File | Nội dung |
|------|----------|
| `Metrics_Detail.csv` | Bảng số liệu đầy đủ: Dice, IoU, Precision, Recall, HD95, CBL cho tất cả mô hình và prompt modes |
| `images/vis_pga_*.png` | Visualization PGA-UNet trên 3 ảnh test đại diện |
| `images/vis_sam_*.png` | Visualization SAM-Med2D |
| `images/vis_unet_*.png` | Visualization U-Net baseline |
| `images/vis_attunet_*.png` | Visualization Attention U-Net |

## Tóm tắt kết quả (Mixed 70/30, N=248)

| Mô hình | Dice | HD95 | Ghi chú |
|---------|------|------|---------|
| U-Net (no prompt) | 0.5090 | 125.12px | Blind segmentation |
| Attention U-Net | 0.4110 | 141.23px | Attention khuếch đại nhiễu khi không có prompt |
| SAM-Med2D zero-shot | 0.5289 | 114.31px | Foundation model, no fine-tune |
| SAM-Med2D fine-tuned | 0.7554 | 51.84px | SOTA prompt-based |
| **PGA-UNet (ours)** | **0.8558** | **12.79px** | **+13.3% vs SAM, ~4M params** |

## Kết quả GradCAM Rescue (N=174 ảnh có prompt xấu)

- Tỷ lệ phát hiện: **174/174 = 100%** (cả PGA và SAM)
- PGA GradCAM CBL: 0.298 → Rescue thành công (D≥0.7): 38/174 = 21.8%
- SAM GradCAM CBL: 0.497 (tốt hơn) nhưng **không có rescue mechanism**

## Kết quả MobileNetV4 Gatekeeper

| Metric | Giá trị |
|--------|---------|
| Accuracy | 85.77% |
| Precision | 83.11% |
| Recall / Sensitivity | 89.64% |
| Specificity | 81.91% |
| F1-score | 86.25% |
| **AUC-ROC** | **0.9514** |

## Result notebooks (Kaggle)

Toàn bộ kết quả có thể reproduce bằng các notebook trong `Source/`:
- Chạy trên Kaggle T4 GPU
- Dataset tải tự động từ Google Drive
- Thời gian chạy: UNet~3h, AttUNet~4h, PGA~6h, SAM~5h
