# PGA-UNet: Prompt-Guided Attention U-Net for Bone X-Ray Segmentation

Mã nguồn thực nghiệm cho khóa luận tốt nghiệp:
**"Phát triển hệ thống phân đoạn tổn thương xương trên ảnh X-quang dựa trên câu nhắc trực quan"**

Sinh viên: Nguyễn Hữu Bình (22120031) — Thông Lúc (22120196)
Người hướng dẫn: PGS.TS. Lý Quốc Ngọc — ThS. Đỗ Thị Thanh Hà

---

## Cấu trúc thư mục

```
Source/
├── Prompt-Guided-XRay-Segmentation/   # Package mô hình PGA-UNet (branch TN_B_ON)
│   ├── dataset.py                      # BTXRD_Dataset: load ảnh/polygon, sinh prompt (zoom_out/shift/mixed_7_3), augmentation
│   ├── train.py                        # Vòng lặp huấn luyện PGA-UNet, early stopping, scheduler
│   ├── models/
│   │   ├── networks/
│   │   │   └── prompt_unet_2D.py       # Kiến trúc PGA-UNet (PromptSpatialGate + Conditioned Attention Decoder)
│   │   ├── layers/
│   │   │   └── grid_attention_layer.py # GridAttentionBlock2D (kế thừa từ Attention U-Net)
│   │   └── networks_other.py           # init_weights và tiện ích khởi tạo trọng số
│   └── REAME.md
│
├── File_Train/                         # Notebook HUẤN LUYỆN (chạy trên Colab/Kaggle GPU)
│   ├── PGA_Unet2D.ipynb                # Huấn luyện PGA-UNet (mô hình chính, Thí nghiệm B)
│   ├── Unet2D.ipynb                    # Huấn luyện baseline U-Net thuần (không prompt)
│   ├── Finetune_SAMMed2D_test_robust.ipynb  # Fine-tune SAM-Med2D + test 3 kịch bản prompt
│   ├── EfficientNet_B3.ipynb           # Huấn luyện Gatekeeper (phân lớp bình thường/bệnh lý)
│   └── Ablation/                       # Huấn luyện 5 biến thể kiến trúc PGA-UNet
│       ├── V1_NoPSG_NoCAD_Concat.ipynb    # V1: không PSG, không CAD (nối kênh đơn giản)
│       ├── V2_PSG_Only.ipynb              # V2: chỉ Prompt Spatial Gate
│       ├── V3_CAD_Only.ipynb              # V3: chỉ Conditioned Attention Decoder
│       ├── V4_Full_BinaryPrompt.ipynb     # V4: PSG + CAD, prompt nhị phân (mask cứng)
│       └── V5_Full_HeatmapPrompt.ipynb    # V5: PSG + CAD, prompt Gaussian Heatmap (mô hình đề xuất)
│
└── File_Test/                          # Notebook ĐÁNH GIÁ / SO SÁNH (copy từ Result/Result_BTXRD, đã xóa output)
    ├── pga-vs-unet2d-r512.ipynb            # So sánh PGA-UNet vs U-Net (baseline), 3 kịch bản prompt, 512×512
    ├── test-pga-samzs-samft-r256.ipynb     # PGA-UNet vs SAM-Med2D zero-shot vs SAM-Med2D fine-tuned, 256×256
    ├── test-pga-dataset-1234.ipynb         # Kiểm định chéo (Cross-validation) PGA-UNet trên 4 fold
    ├── test-subcat-pga-vs-baseline.ipynb   # Phân tích sub-category: PGA-UNet vs U-Net (nhóm Dễ/Khó theo Dice U-Net)
    ├── test-subcat-pga-vs-sam-r256-r512.ipynb  # Phân tích sub-category: SAM-Med2D vs PGA-UNet (256 & 512)
    ├── test-pipeline-evaluation.ipynb      # Đánh giá pipeline end-to-end (Gatekeeper → PGA-UNet)
    ├── efficientnet-b3.ipynb               # Đánh giá Gatekeeper (Accuracy/Recall/Precision/AUC-ROC)
    ├── Test_app.ipynb                      # Kiểm tra inference thủ công (Gradio app demo)
    └── Ablation/                       # Test 4 biến thể ablation (V1–V4; V5 được test ở các notebook trên)
        ├── test-v1-nopsg-nocad-concat.ipynb
        ├── test-v2-psg-only.ipynb
        ├── test-v3-cad-only.ipynb
        └── test-v4-full-binaryprompt.ipynb
```

> **Quy ước:** `File_Train/` chứa notebook huấn luyện từ đầu (sinh checkpoint `.pth`); `File_Test/` chứa notebook tải checkpoint đã huấn luyện về để đánh giá/so sánh/trực quan hóa — không huấn luyện lại. Các file trong `File_Test/` được đồng bộ từ `Result/Result_BTXRD/` (nơi lưu kết quả chạy thật) nhưng đã xóa toàn bộ output (số liệu, biểu đồ) để giữ mã nguồn gọn nhẹ.

---

## Mô hình PGA-UNet

**Kiến trúc:** U-Net nhẹ (~3M tham số), `feature_scale=4`, bộ lọc `[16, 32, 64, 128, 256]`

**Hai thành phần chính:**
- **Prompt Spatial Gate (PSG):** Tại mỗi tầng mã hóa, bản đồ nhiệt câu nhắc được giảm mẫu và nhân có trọng số (`1 + alpha * gate(prompt)`, `alpha` khởi tạo 0.1, học được) vào feature map để tăng cường đặc trưng vùng ROI mà không triệt tiêu phần còn lại.
- **Conditioned Attention Decoder (CAD):** Tại mỗi tầng giải mã, tín hiệu gating của Attention Gate (kế thừa từ Attention U-Net) được điều kiện hóa bằng đặc trưng câu nhắc, với trọng số giảm dần theo tầng `[1.0, 0.7, 0.4, 0.2]`.

**Biểu diễn câu nhắc:** Plateau Heatmap — vùng trong bounding box (mở rộng 5px mỗi cạnh) gán giá trị 1, làm mịn biên bằng Gaussian kernel `31×31`.

**Prompt augmentation (trong `forward()` của model, chỉ khi `training=True`):** 15% prompt bị xóa trắng (mô phỏng không có câu nhắc), 15% prompt bị nhiễu Gaussian (σ=0.1), 70% giữ nguyên.

**Cài đặt huấn luyện (`train.py`):**

| Tham số | Giá trị |
|---|---|
| Epochs | 100 (early stop patience=15, theo Dice zoom-out trên tập val) |
| Batch size | 4 |
| Image size | 512×512 |
| Optimizer | AdamW (lr=1e-4, weight_decay=1e-4) |
| Scheduler | ReduceLROnPlateau (mode=max, factor=0.5, patience=5) |
| Loss | BCEWithLogitsLoss + Dice Loss (tổng, trọng số bằng nhau) |
| Gradient clipping | max_norm=1.0 |
| Image augmentation | HFlip 50%, Rotate ±15° (50%), áp dụng đồng bộ ảnh/mask/prompt |

---

## Gatekeeper — EfficientNet_B3

Phân lớp nhị phân (bình thường / bệnh lý) đặt trước PGA-UNet trong pipeline, sàng lọc ảnh trước khi đưa vào phân đoạn.
Tinh chỉnh hai giai đoạn: (1) đóng băng backbone, chỉ huấn luyện head (25 epoch, lr=1e-4); (2) mở toàn bộ, CosineAnnealingLR (tối đa 100 epoch, dừng sớm patience=15, lr=1e-5).

Kết quả trên tập kiểm thử (N=375: 187 bệnh lý + 188 bình thường):

| Metric | Giá trị |
|---|---|
| Accuracy | 88.00% |
| Precision | 87.37% |
| Recall (Sensitivity) | 88.77% |
| Specificity | 87.23% |
| NPV | 88.65% |
| F1-Score | 88.06% |
| AUC-ROC | 0.9405 |

---

## Pipeline End-to-End

`File_Test/test-pipeline-evaluation.ipynb` đánh giá toàn bộ luồng trên tập `dataset_online` hỗn hợp (375 ảnh: 187 bệnh lý + 188 bình thường):
- Ảnh bình thường → Gatekeeper chặn (TN) hoặc lọt (FP, PGA-UNet chạy nhưng không có GT → Dice=0)
- Ảnh bệnh lý → Gatekeeper thông (TP, PGA-UNet phân đoạn với bounding box prompt) hoặc bị bỏ sót (FN, không tính)
- Kết quả: TP=166, FP=24, FN=21, TN=164 → **Pipeline Dice = 0.7544**, **Pipeline IoU = 0.6693** (mẫu số 190 = 166 ảnh TP + 24 ảnh FP)

---

## So sánh với baseline (U-Net) và SAM-Med2D

Trên tập kiểm thử BTXRD (PGA-UNet/U-Net: N=187 ảnh, image-level; SAM-Med2D: N=232 mẫu per-polygon — xem lý do khác đơn vị đánh giá tại `Report/Chapter4/chapter4.tex`, mục "Phương pháp đánh giá image-level"); PGA-UNet ở kịch bản Zoom-out:

| Mô hình | Độ phân giải | Dice↑ | IoU↑ | Precision↑ | Recall↑ | HD95*↓ (chuẩn hóa) | CBL↑ |
|---|---|---|---|---|---|---|---|
| U-Net (baseline, không prompt) | 512 | 0.4790 | 0.3815 | 0.6245 | 0.5184 | 0.285 | 0.5906 |
| **PGA-UNet (Zoom-out, đề xuất)** | **512** | **0.8584** | **0.7617** | **0.8526** | **0.8817** | **0.029** | **0.9500** |
| SAM-Med2D fine-tuned | 256 | 0.7350 | 0.6130 | 0.7513 | 0.7478 | 0.196 | 0.8907 |

> HD95* chuẩn hóa theo kích thước ảnh (px ÷ độ phân giải tương ứng) vì U-Net/PGA-UNet chạy ở 512×512 còn SAM-Med2D bắt buộc 256×256 (giới hạn position embedding ViT-B) — so sánh HD95 thô giữa hai độ phân giải khác nhau không có ý nghĩa.

Chi tiết đầy đủ (3 kịch bản prompt, ablation, cross-validation, sub-category, fine-tuned vs zero-shot, và thực nghiệm tổng quát hóa trên FracAtlas) xem `Report/Chapter4/chapter4.tex`.

---

## Yêu cầu môi trường

Các notebook được thiết kế chạy trên **Google Colab / Kaggle** (GPU T4/A100/P100).

```
torch >= 2.0
torchvision
numpy
opencv-python
scikit-learn
matplotlib
scipy
tqdm
gdown
```

Package PGA-UNet được clone trực tiếp từ GitHub trong mỗi notebook (branch `TN_B_ON`) và thêm vào `sys.path`, ví dụ:
```python
!git clone -b TN_B_ON https://github.com/ThongLuc2k3/Prompt-Guided-XRay-Segmentation.git
sys.path.insert(0, '/content/Prompt-Guided-XRay-Segmentation')
```
