# PGA-UNet: Prompt-Guided Attention U-Net for Bone X-Ray Segmentation

Mã nguồn thực nghiệm cho khóa luận tốt nghiệp:
**"Phát triển hệ thống phân đoạn ảnh X-quang về xương dựa vào câu nhắc trực quan"**

Sinh viên: Nguyễn Hữu Bình (22120031) — Thông Lúc (22120196)
Người hướng dẫn: PGS.TS. Lý Quốc Ngọc — ThS. Đỗ Thị Thanh Hà

---

## Cấu trúc thư mục

```
Source/
├── Prompt-Guided-XRay-Segmentation/   # Package mô hình PGA-UNet
│   ├── dataset.py                      # Dataset loader, augmentation, prompt generation
│   ├── train.py                        # Vòng lặp huấn luyện, early stopping, scheduler
│   ├── models/
│   │   ├── networks/
│   │   │   └── prompt_unet_2D.py       # Kiến trúc PGA-UNet (PSG + CAD)
│   │   ├── layers/
│   │   │   └── grid_attention_layer.py # GridAttentionBlock2D
│   │   └── networks_other.py           # init_weights utility
│   └── REAME.md
│
├── PGA_Unet2D.ipynb                    # Huấn luyện & đánh giá PGA-UNet (chính)
├── Attention_Unet2D.ipynb              # Baseline: Attention U-Net
├── Unet2D.ipynb                        # Baseline: U-Net thuần
├── Finetune_SAMMed2D_test_robust.ipynb # Baseline: SAM-Med2D fine-tuned + robustness
├── SAMMed2D_ZeroShot.ipynb             # SAM-Med2D zero-shot (tham khảo)
├── EfficientNet_B3.ipynb               # Gatekeeper: phân lớp bình thường/bệnh lý
├── Pipeline_Evaluation.ipynb           # Đánh giá pipeline end-to-end
├── SubCat_PGA_vs_Baseline.ipynb        # Phân tích sub-category PGA vs U-Net/AttUNet
├── SubCat_PGA_vs_SAM.ipynb             # Phân tích sub-category PGA vs SAM-Med2D
├── Test_app.ipynb                      # Kiểm tra inference thủ công
│
└── Ablation/                           # Ablation study kiến trúc PGA-UNet
    ├── V1_NoPSG_NoCAD_Concat.ipynb     # V1: không PSG, không CAD (nối kênh đơn giản)
    ├── V2_PSG_Only.ipynb               # V2: chỉ Prompt Spatial Gate
    ├── V3_CAD_Only.ipynb               # V3: chỉ Conditioned Attention Decoder
    ├── V4_Full_BinaryPrompt.ipynb      # V4: PSG + CAD, prompt nhị phân (mask cứng)
    └── V5_Full_HeatmapPrompt.ipynb     # V5: PSG + CAD, prompt Plateau Heatmap (chính thức)
```

---

## Mô hình PGA-UNet

**Kiến trúc:** U-Net nhẹ (~3M tham số), `feature_scale=4`, bộ lọc `[16, 32, 64, 128, 256]`

**Hai thành phần chính:**
- **Prompt Spatial Gate (PSG):** Tại mỗi tầng mã hóa, bản đồ nhiệt câu nhắc được giảm mẫu và nhân có trọng số vào feature map để tăng cường đặc trưng vùng ROI.
- **Conditioned Attention Decoder (CAD):** Tại mỗi tầng giải mã, tín hiệu gating của Attention Gate được điều kiện hóa bằng đặc trưng câu nhắc với trọng số giảm dần `[1.0, 0.7, 0.4, 0.2]`.

**Biểu diễn câu nhắc:** Plateau Heatmap — vùng trong bounding box gán giá trị 1, làm mịn biên bằng Gaussian kernel `31×31`.

**Cài đặt huấn luyện:**

| Tham số | Giá trị |
|---|---|
| Epochs | 100 (early stop patience=15) |
| Batch size | 4 |
| Image size | 512×512 |
| Optimizer | AdamW (lr=1e-4) |
| Scheduler | ReduceLROnPlateau (factor=0.5, patience=5) |
| Loss | Dice + BCE (trọng số bằng nhau) |
| Prompt augmentation | 15% empty, 15% noisy |
| Image augmentation | HFlip 50%, Rotate ±15° (50%) |

---

## Gatekeeper — EfficientNet_B3

Phân lớp nhị phân (bình thường / bệnh lý) đặt trước PGA-UNet trong pipeline.
Tinh chỉnh hai giai đoạn: đóng băng backbone → mở toàn bộ.
Kết quả: **AUC-ROC = 0.9258** trên tập kiểm tra.

---

## Pipeline End-to-End

`Pipeline_Evaluation.ipynb` đánh giá toàn bộ luồng trên tập hỗn hợp (bình thường + bệnh lý):
- Ảnh bình thường → Gatekeeper chặn → không chạy PGA-UNet
- Ảnh bệnh lý → Gatekeeper thông → PGA-UNet phân đoạn với bounding box prompt
- Kết quả: **Pipeline Dice = 0.7296** (226 polygon TP + 38 FP trên 375 ảnh)

---

## Yêu cầu môi trường

Các notebook được thiết kế chạy trên **Google Colab** (GPU T4/A100).

```
torch >= 2.0
torchvision
numpy
opencv-python
scikit-learn
matplotlib
Pillow
tqdm
```

Package PGA-UNet được mount qua:
```python
sys.path.insert(0, '/content/Prompt-Guided-XRay-Segmentation')
```
