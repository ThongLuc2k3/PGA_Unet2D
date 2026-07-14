# PGA-UNet2D — Khóa Luận Tốt Nghiệp

**Đề tài:** Phát triển hệ thống phân đoạn tổn thương xương trên ảnh X-quang dựa trên câu nhắc trực quan  
**Dataset:** BTXRD (Nature Scientific Data 2024) — bone tumor X-ray, 248 test samples  
**Kết quả chính:** PGA-UNet Dice=0.8606 > SAM-Med2D Dice=0.7554 (+13.3%), ~4M params (25× nhỏ hơn SAM)

---

## Cấu trúc thư mục

```
PGA_Unet2D/
├── Report/              # Báo cáo LaTeX
├── Source/              # Notebook thực nghiệm + code gốc
│   └── Ablation/        # 5 notebook ablation study
├── Result/              # Notebook đã chạy xong (có output)
├── diagrams/            # File DrawIO nguồn của các sơ đồ
└── Bao_cao_tien_do.md   # Theo dõi tiến độ khóa luận
```

---

## Report/

Báo cáo LaTeX — compile bằng `latexmk -pdf main.tex` tại thư mục `Report/`.

| File/Folder | Nội dung |
|---|---|
| `main.tex` | Entry point — import tất cả chapter |
| `main.pdf` | PDF đã compile |
| `Chapter1/chapter1.tex` | Giới thiệu, mục tiêu, phạm vi đề tài |
| `Chapter4/chapter4.tex` | Thực nghiệm & đánh giá: tất cả bảng số liệu |
| `Chapter5/chapter5.tex` | Kết luận, hạn chế, hướng phát triển |
| `Appendix/` | Phụ lục: tóm tắt, cảm ơn, đề cương, cam kết |
| `References/references.bib` | Danh sách tài liệu tham khảo (BibTeX) |
| `images/` | Toàn bộ hình ảnh được nhúng vào báo cáo |

### Report/images/ — các file quan trọng

| File | Dùng ở đâu |
|---|---|
| `system_architecture.png` | Chapter 3 — kiến trúc tổng thể pipeline |
| `preprocessing_pipeline.png` | Chapter 3 — quy trình tiền xử lý |
| `classification_pipeline.png` | Chapter 3 — pipeline phân lớp MobileNetV4 |
| `classification_evaluation.png` | Chapter 4 — ROC curve + confusion matrix MobileNetV4 |
| `diagram_pga.png` | Chapter 3 — kiến trúc PGA-UNet chi tiết |
| `diagram_unet.png` / `diagram_attunet.png` / `diagram_sammed2d.png` | Chapter 2/3 — so sánh kiến trúc |
| `vis_pga_*.png` / `vis_unet_*.png` / `vis_attunet_*.png` / `vis_sam_*.png` | Chapter 4 — ảnh visualization định tính |

---

## Source/

Notebook thực nghiệm — tất cả chạy trên **Google Colab** (T4 GPU). Clone repo tự động trong Cell 1.

### Huấn luyện mô hình

| Notebook | Mô hình | Kết quả |
|---|---|---|
| `PGA_Unet2D.ipynb` | PGA-UNet (Exp B, PSG+CAD) | Dice=0.8606 (zoom_out), 0.8558 (mixed) |
| `Unet2D.ipynb` | U-Net 2D baseline | Dice=0.5090 |
| `Attention_Unet2D.ipynb` | Attention U-Net 2D baseline | Dice=0.4110 |
| `Finetune_SAMMed2D_test_robust.ipynb` | SAM-Med2D fine-tune trên BTXRD | Dice=0.7554 |

### Đánh giá & phân tích

| Notebook | Nội dung |
|---|---|
| `SAMMed2D_ZeroShot.ipynb` | SAM-Med2D zero-shot (không fine-tune) → Dice=0.5289 |
| `Defense_Comparison_SAM_vs_PGA.ipynb` | So sánh cơ chế phòng vệ SAM vs PGA |
| `PGA_Extended_Test.ipynb` | Kiểm tra robustness: zoom/shift/mixed prompt |
| `SubCat_PGA_vs_Baseline.ipynb` | PGA vs U-Net/AttUNet trên nhóm Dễ/Khó (Easy/Hard split) |
| `SubCat_PGA_vs_SAM.ipynb` | PGA vs SAM trên 3 nhóm: Tổn thương nhỏ / Biên giới mờ / Tổn thương rõ nét |
| `Test_app.ipynb` | Test Gradio app (`app.py`) |

### Source/project/ — Code Python gốc

```
project/
├── models/
│   ├── networks/
│   │   ├── prompt_unet_2D.py      # PGA-UNet: PSG + CAD (model chính)
│   │   ├── attention_unet_2D.py   # Attention U-Net baseline
│   │   ├── unet_2D.py             # U-Net baseline
│   │   └── utils.py               # Helper functions
│   └── layers/
│       ├── grid_attention_layer.py  # GridAttentionBlock2D (dùng trong CAD)
│       └── loss.py                  # BCE + Dice loss
├── train_pga.py      # Training script cho PGA-UNet
├── train_unet.py     # Training script cho U-Net
├── train_attunet.py  # Training script cho Attention U-Net
├── dataset_pga.py    # Dataset với plateau heatmap prompt
└── dataset_simple.py # Dataset đơn giản (không có prompt)
```

> Code được host trên GitHub: `ThongLuc2k3/Prompt-Guided-XRay-Segmentation` (branch `TN_B_ON`). Các notebook tự động clone khi chạy.

### Source/Ablation/ — Ablation study kiến trúc

5 notebook train lại từ đầu để tách đóng góp từng thành phần:

| Notebook | Cấu hình | Mục đích |
|---|---|---|
| `V1_NoPSG_NoCAD_Concat.ipynb` | Không PSG, không CAD — heatmap nối kênh | Baseline concat đơn giản |
| `V2_PSG_Only.ipynb` | Chỉ PSG ở encoder, decoder thường | Đóng góp riêng của PSG |
| `V3_CAD_Only.ipynb` | Chỉ CAD ở decoder (`use_encoder_prompt=False`) | Đóng góp riêng của CAD |
| `V4_Full_BinaryPrompt.ipynb` | PSG + CAD, train với prompt nhị phân | Heatmap vs binary prompt |
| `V5_Full_HeatmapPrompt.ipynb` | PSG + CAD, train với heatmap (chuẩn) | Reference — phải ~Dice 0.86 |

---

## Result/

Bản sao các notebook Source đã chạy xong, **có output đầy đủ**. Dùng để tra cứu số liệu mà không cần chạy lại.

| Notebook | Số liệu chính |
|---|---|
| `pga-unet2d-kq.ipynb` | PGA: Dice=0.8606/0.8380/0.8558 (3 kịch bản prompt) |
| `unet2d-btxrd.ipynb` | U-Net: Dice=0.5090, HD95=125.12px |
| `attention-unet2d-btxrd.ipynb` | Att-UNet: Dice=0.4110, HD95=141.23px |
| `finetune-sammed2d-kq.ipynb` | SAM fine-tuned: Dice=0.7554, HD95=51.84px |
| `sam-med2d-zero-shot.ipynb` | SAM zero-shot: Dice=0.5289, HD95=114.31px |
| `defense-comparison-sam-vs-pga.ipynb` | CBL(PGA)=0.2975 vs CBL(SAM)=0.4973 |
| `pga-extended-test.ipynb` | Robustness test nhiều kịch bản zoom/shift |
| `SubCat_PGA_vs_Baseline.ipynb` | Easy: PGA=0.8632 / Hard: PGA=0.8521 vs UNet=0.2379 |
| `SubCat_PGA_vs_SAM.ipynb` | Nhỏ: PGA=0.82 vs SAM=0.25 / Mờ: 0.82 vs 0.46 / Rõ: 0.89 vs 0.85 |
| `MobileNetV4_BTXRD_dataset.ipynb` | MobileNetV4: Acc=85.77%, AUC-ROC=0.9514 |

---

## diagrams/

File nguồn DrawIO cho tất cả sơ đồ trong báo cáo. Export PNG → `Report/images/`.

| File | Xuất thành |
|---|---|
| `system_architecture.drawio` | `Report/images/system_architecture.png` |
| `preprocessing_pipeline.drawio` | `Report/images/preprocessing_pipeline.png` |
| `classification_pipeline.drawio` | `Report/images/classification_pipeline.png` |
| `arch_pga_unet2d.drawio` | (tham khảo, không nhúng trực tiếp) |
| `arch_unet2d.drawio` / `arch_attention_unet2d.drawio` / `arch_sammed2d.drawio` | Sơ đồ kiến trúc các mô hình |
| `pipeline_pga_app_inference.drawio` | Luồng inference của app |

---

## Nhiệm vụ còn lại (deadline 12/06/2026)

| # | Nhiệm vụ | File | Ưu tiên |
|---|---|---|---|
| 1 | Chạy 5 ablation notebooks trên Colab | `Source/Ablation/V1–V5` | 🔴 Cao |
| 2 | Cập nhật `tab:ablation_prompt` trong chapter4.tex với số thật từ ablation | `Report/Chapter4/chapter4.tex` | 🔴 Cao |
| 3 | Thêm ảnh visualization sub-category vào chapter4.tex | `Report/images/` + chapter4.tex | 🟡 Trung bình |
| 4 | Compile và kiểm tra `main.pdf` lần cuối | `Report/main.tex` | 🟡 Trung bình |
