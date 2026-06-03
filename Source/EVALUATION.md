# Kế Hoạch & Đánh Giá Thực Nghiệm — PGA-UNet2D Luận Văn

> Cập nhật: 2026-06-03 (tối) — fix references.bib tác giả đúng từ PDF, thêm YOLOv11/Roboflow, compile main.pdf OK (3.8MB), Submission tái cấu trúc 5 folder + .tex

---

## 0. Trạng Thái Tổng Quan (03/06/2026 — chiều)

### Đóng góp 1 — Nghiên cứu (PGA-UNet) — **~85% hoàn thành**

| Hạng mục | Trạng thái | Nguồn |
|---|---|---|
| Kiến trúc PGA-UNet (PSG, CAD, heatmap) — Chapter 3 | ✅ Viết xong | chapter3.tex |
| Lý thuyết heatmap encoding + so sánh SAM | ✅ Viết xong | chapter3.tex |
| Chiến lược huấn luyện từ đầu vs tinh chỉnh | ✅ Viết xong | chapter3.tex |
| Kết quả 4 mô hình (Dice/IoU/HD95/CBL × 3 modes) | ✅ Số thật | Result/ notebooks |
| SAM zero-shot comparison | ✅ Số thật | Result/sam-med2d-zero-shot.ipynb |
| GradCAM rescue + `tab:gradcam_rescue` (174/174=100%) | ✅ Số thật | Result/pga-gradcam-ipr.ipynb |
| IPR convergence `tab:ipr_convergence` k=0,1 | ⚠️ Một phần | k=2,3 chờ PGA_Ablation.ipynb |
| Ablation prompt type `tab:ablation_prompt` | ✅ Số thật | Result/PGA_Ablation.ipynb |
| **Ablation kiến trúc V1–V5** `tab:ablation_arch` | 🔴 Đang chạy Colab | Source/Ablation/ |
| Sub-category PGA vs Baseline (Dễ/Khó) | ✅ Số thật | Result/SubCat_PGA_vs_Baseline.ipynb |
| Sub-category PGA vs SAM (3 nhóm) | ✅ Số thật | Result/SubCat_PGA_vs_SAM.ipynb |
| Cross-validation `tab:cross_validation` | 🔴 **Đang chạy Colab** | Source/PGA_Unet2D.ipynb |

### Đóng góp 2 — Sản phẩm (Pipeline lâm sàng)

| Hạng mục | Trạng thái | Nguồn |
|---|---|---|
| MobileNetV4 gatekeeper (AUC-ROC=0.9514) | ✅ Số thật | Result/MobileNetV4_BTXRD_dataset.ipynb |
| GradCAM rescue 174/174=100%, 21.8% cứu hộ | ✅ Số thật | Result/pga-gradcam-ipr.ipynb |
| IPR k=2,3 convergence | 🔴 Chưa có | PGA_Ablation.ipynb |
| Defense comparison SAM vs PGA | ✅ Số thật | Result/defense-comparison-sam-vs-pga.ipynb |
| Cascading error lý thuyết ≈76.7% | ✅ Viết xong | chapter4.tex |
| Cascading error thực nghiệm | 🟠 Chưa làm | Tạo test_mixed/ |
| app.py Gradio UI | ✅ Có sẵn | Source/project/app.py |
| Chapter 3: Đóng góp IPR phân rõ thuộc Đóng góp 2 | ✅ Viết xong | chapter3.tex sec:ipr_pipeline |
| Chapter 4: sec:product_overview | ✅ Viết xong | chapter4.tex |
| Chapter 5: 5 hướng phát triển | ✅ Viết xong | chapter5.tex |

### Báo cáo — Chất lượng văn bản (hôm nay đã dọn)

| Hạng mục | Trạng thái |
|---|---|
| references.bib — **8 entry đúng** (tác giả lấy từ PDF) | ✅ |
| YOLOv11, Roboflow thêm link chính thức | ✅ |
| BTXRD tác giả đúng: Shunhan Yao et al., Sci.Data 12:88 (2025) | ✅ |
| SAM-Med2D tác giả đúng: Junlong Cheng et al. | ✅ |
| main.pdf compile không lỗi (3.8 MB) | ✅ |
| Anh-Việt lẫn lộn: paradigm, Warmup, subsection titles, header bảng | ✅ Đã sửa |
| Số liệu thời gian ms (chưa đo) đã xóa khỏi Ch.3, Ch.4 | ✅ |
| Phân rõ IPR thuộc Đóng góp 2 trong Ch.3 | ✅ |
| Float too large (system_architecture, preprocessing_pipeline) | ✅ Đã fix |
| Chapter 2 dọn sạch: bỏ UNet++, nnU-Net, TransUNet, SAM, SAM2, RITM, MedSAM | ✅ |

### Việc còn lại trước 12/06 (deadline 9 ngày)

| # | Việc | Ưu tiên |
|---|---|---|
| 1 | **Ablation V1–V5** → điền `tab:ablation_arch` | 🔴 Đang chạy Colab |
| 2 | **Cross-validation** → điền `tab:cross_validation` | 🔴 Đang chạy Colab |
| 3 | **main.pdf** compile không lỗi | ✅ Xong (3.8MB) |
| 4 | **IPR k=2,3** → chạy pga-gradcam-ipr sau khi có trọng số tốt nhất | 🟠 Đợi checkpoint |
| 5 | **Cascading error thực nghiệm** | 🟡 Nếu còn thời gian |
| 6 | **MobileNetV4 Drive link** | 🟡 Điền vào Submission README |
| 5 | IPR k=2,3 → điền `tab:ipr_convergence` | 🟠 |
| 6 | Cascading error thực nghiệm | 🟡 |

---

---

## 1. Tổng Quan Dự Án

Luận văn so sánh 4 mô hình phân đoạn sỏi tiết niệu trên ảnh X-quang 2D (dataset BTXRD):

| Vai trò | Model | Notebook |
|---------|-------|----------|
| Baseline không prompt | U-Net 2D | `Source/Unet2D.ipynb` |
| Baseline không prompt | Attention U-Net 2D | `Source/Attention_Unet2D.ipynb` |
| **Đề xuất** (có prompt) | PGA-UNet 2D Exp B | `Source/PGA_Unet2D.ipynb` |
| SOTA so sánh (có prompt) | SAM-Med2D fine-tuned | `Source/Finetune_SAMMed2D_test_robust.ipynb` |

---

## 2. Phân Tích Công Bằng Evaluation (Phát Hiện Quan Trọng)

### 2.1 Số samples test thực tế

Dataset BTXRD test: **187 ảnh**, trong đó **28 ảnh có 2 khối u** (→ 248 polygon tổng cộng).

| Model | Dataset class | Đọc từ | img_size | Test samples | Ghi chú |
|-------|--------------|--------|----------|-------------|---------|
| U-Net 2D | `dataset.py` (nhận `mask_dir`) | `masks/` PNG | 512 | **187** | Merged mask |
| ATT-UNet 2D | `dataset_simple.py` | `masks/` PNG | 512 | **187** | Merged mask |
| PGA-UNet | `dataset.py` (nhận `json_dir`) | `annotations/` JSON polygon | 512 | **248** | Per-polygon |
| SAM-Med2D | `DataLoader.py` + label2image | `masks/` PNG per-polygon | 256 | **248** ✅ | Đã fix |

### 2.2 Vì sao phải đồng nhất 248 samples cho SAM-Med2D?

PGA đọc từng polygon riêng trong JSON → 1 khối u = 1 sample với bbox riêng.  
SAM-Med2D cũng là prompt-based → phải cùng evaluation unit để so sánh công bằng.

**Fix đã thực hiện** (`Finetune_SAMMed2D_test_robust.ipynb` Cell 6):  
- Đọc JSON annotations → `cv2.fillPoly` từng polygon → lưu `IMG001768_1.png`, `IMG001768_2.png`...  
- Kết quả: train=**1859** / val=**211** / test=**248** samples — khớp chính xác PGA.

### 2.3 Vấn đề img_size (cần ghi chú trong báo cáo)

- U-Net, ATT-UNet, PGA: `512×512`
- SAM-Med2D: `256×256` (bắt buộc — position embedding SAM checkpoint train ở 256)

**Ảnh hưởng đến HD95**: HD95 tính theo pixel → SAMmed2D (~256px) nhỏ hơn ~2× so với các model 512px. Khi so sánh bảng cần normalize: `hd95_norm = hd95 / img_size`.

### 2.4 Vẫn còn bất đồng nhỏ (ghi chú trong chương 4)

U-Net và ATT-UNet test 187 samples (merged mask) trong khi PGA và SAM-Med2D test 248 samples (per-polygon). Với 28 ảnh multi-tumor:
- U-Net/ATT-UNet: Dice tính trên mask gộp 2 khối u
- PGA/SAMmed2D: Dice tính trên từng khối u riêng

Mức ảnh hưởng nhỏ (~15% test set). Ghi chú trong báo cáo là đủ.

---

## 3. Cài Đặt Chốt Cuối (Final Settings)

| Setting | UNet2D | AttUNet2D | PGA-UNet Exp B | SAM-Med2D |
|---------|--------|-----------|----------------|-----------|
| **IMG_SIZE** | 512 | 512 | 512 | **256** (cố định SAM) |
| **BATCH_SIZE** | 4 | 4 | 4 | 2 |
| **NUM_EPOCHS** | ≤100 | ≤100 | ≤100 | ≤50 |
| **Early Stop** | patience=15 | patience=15 | patience=15 | patience=10 |
| **LR** | 1e-4 | 1e-4 | 1e-4 | 1e-4 |
| **Optimizer** | AdamW + wd=1e-4 | AdamW + wd=1e-4 | AdamW + wd=1e-4 | AdamW |
| **Scheduler** | ReduceLROnPlateau | ReduceLROnPlateau | ReduceLROnPlateau | — |
| **Grad Clip** | max_norm=1.0 | max_norm=1.0 | max_norm=1.0 | — |
| **Loss** | BCE + Dice | BCE + Dice | BCE + Dice | FocalDice + IoU |
| **Test samples** | 187 | 187 | **248** | **248** |
| **Prompt modes** | N/A | N/A | zoom_out / shift / mixed_7_3 | zoom_out / shift / mixed_7_3 |
| **Post-process** | extract_lcc | extract_lcc | extract_lcc | extract_lcc ✅ |
| **Dataset ID** | `1fU7...` | `1fU7...` | `1fU7...` | `1fU7...` |

---

## 4. Trạng Thái Từng Notebook

### 4.1 `Unet2D.ipynb` ✅
| Hạng mục | Trạng thái |
|----------|-----------|
| IMG_SIZE = 512 | ✅ |
| BATCH_SIZE = 4 | ✅ |
| Scheduler ReduceLROnPlateau | ✅ |
| Early stopping patience=15 | ✅ |
| Grad clip max_norm=1.0 | ✅ |
| MODEL_PATH đúng (`unet_best.pth`) | ✅ đã fix |
| 6 metrics: Dice, IoU, Pre, Rec, HD95, CBL | ✅ |
| CSV save → `results/unet2d_results.csv` | ✅ |

### 4.2 `Attention_Unet2D.ipynb` ✅
| Hạng mục | Trạng thái |
|----------|-----------|
| IMG_SIZE = 512 | ✅ |
| BATCH_SIZE = 4 | ✅ |
| Scheduler + Early stopping | ✅ |
| `from dataset_simple import` (nhất quán) | ✅ đã fix |
| 6 metrics | ✅ |
| CSV save → `results/attunet2d_results.csv` | ✅ |

### 4.3 `PGA_Unet2D.ipynb` ✅
| Hạng mục | Trạng thái |
|----------|-----------|
| IMG_SIZE = 512, EXPERIMENT = B | ✅ |
| Dataset: JSON polygon, 248 test samples | ✅ |
| 3 prompt modes: zoom_out / shift / mixed_7_3 | ✅ |
| IPR 5 vòng + Dark background detection | ✅ |
| GradCAM visualization | ✅ |
| VIS_IMAGES: IMG001768, IMG001538, IMG001100 | ✅ |
| CSV save → `results/pga_unet_expB_results.csv` | ✅ |

### 4.4 `Finetune_SAMMed2D_test_robust.ipynb` ✅

### 4.5 `SAMMed2D_ZeroShot.ipynb` ✅ ĐÃ CHẠY (2026-06-02)
| Hạng mục | Trạng thái |
|----------|-----------|
| Dùng checkpoint pre-trained `sam_med2d.pth` | ✅ |
| Không có bước fine-tune | ✅ |
| 3 prompt modes: zoom_out / shift / mixed_7_3 | ✅ |
| Result: `Result/sam-med2d-zero-shot.ipynb` | ✅ |

### 4.6 `PGA_GradCAM_IPR.ipynb` ✅ (mới cập nhật)
| Hạng mục | Trạng thái |
|----------|-----------|
| Checkpoint ID: `1Mv-rUPI7KGmYemd27hmKbJQRHc4ZKB9z` (trọng số cũ tốt hơn) | ✅ |
| 3 cell gọn: Phòng hộ → Số liệu → Ảnh | ✅ |
| predict_with_check (5 điều kiện, giống file cũ) | ✅ |
| N tính trên tập bị phòng hộ (not 248) | ✅ |

### 4.4 (cũ) `Finetune_SAMMed2D_test_robust.ipynb` ✅
| Hạng mục | Trạng thái |
|----------|-----------|
| Cấu trúc: 24 cells, Phần 1 / Phần 2 rõ ràng | ✅ |
| Dataset ID `1fU7...` (cùng PGA) | ✅ |
| Cell 6: JSON → per-polygon masks (248 test samples) | ✅ MỚI |
| IMG_SIZE = 256 (SAM native) | ✅ |
| 3 prompt modes: zoom_out / shift / mixed_7_3 | ✅ |
| save_pred = True cả 3 mode | ✅ |
| extract_lcc trong test.py | ✅ |
| HD95 + CBL + CSV save | ✅ |
| VIS_IMAGES: IMG001768, IMG001538, IMG001100 | ✅ |
| Visualization: 3 hàng × 4 cột (bbox frame + GT + pred + diff) | ✅ |

---

## 5. Sơ Đồ Kiến Trúc & Pipeline

### Danh sách file diagrams (đã đổi tên 2026-05-30)

| File | Nội dung |
|---|---|
| `diagrams/arch_unet2d.drawio` | Kiến trúc U-Net 2D cơ bản |
| `diagrams/arch_attention_unet2d.drawio` | Kiến trúc Attention U-Net 2D |
| `diagrams/arch_pga_unet2d.drawio` | Kiến trúc PGA-UNet 2D (đề xuất) |
| `diagrams/arch_sammed2d.drawio` | Kiến trúc SAM-Med2D (ViT-B + Adapter + Mask Decoder) **[MỚI]** |
| `diagrams/pipeline_pga_app_inference.drawio` | Full inference pipeline PGA-UNet trong app.py |

### Pipeline PGA-UNet App — flow đầy đủ:

```
Ảnh X-quang
    ↓
MobileNetV4 (phân loại)
    ↓
Phát hiện tổn thương? → Không → [kết thúc]
    ↓ Có
Thông báo → Bác sĩ xác nhận? → Không → [kết thúc]
    ↓ Có
Bác sĩ vẽ Prompt (khoanh vùng) → Sinh Prompt₀ (BBox → Gaussian heatmap)
    ↓
[MỚI] PGA-UNet — Inference₀ (image, Prompt₀) → Prediction₀
    ↓                              ↘ Prediction₀ (dashed)
Prompt₀ ~70% đen?          GradCAM Mode
    ↓ Không                 (trích GradCAM từ Prediction₀ → Heatmap mới)
IPR k=3 (normal)                ↓
(prompt_{t+1} = pred_t > 0.5) IPR k=3 (GradCAM prompt)
    ↓                              ↓
    └──────── LCC Extraction ──────┘
                    ↓
    Output: Binary Mask + GradCAM Overlay (Gradio UI)
```

**Lý do thêm khối PGA-UNet Inference₀:**
- GradCAM cần 1 forward pass qua PGA-UNet để tính gradient
- IPR bắt đầu từ `pred₀` (prediction ban đầu), không phải từ prompt trực tiếp
- Nếu không có khối này, diagram không phản ánh đúng luồng xử lý thực tế

---

## 6. Kết Quả Thực Nghiệm ✅

> Chạy xong 4 notebook ngày 2026-05-30. Early stop: UNet=82ep, AttUNet=47ep, PGA=60ep, SAM=12ep.

### 6.1 Bảng kết quả đầy đủ

| Model | Mode | Dice↑ | IoU↑ | Pre↑ | Rec↑ | HD95↓(px) | HD95/size↓ | CBL↑ | N |
|-------|------|-------|------|------|------|-----------|------------|------|---|
| **U-Net 2D** | N/A | 0.5090 | 0.4125 | 0.6686 | 0.5235 | 125.12 | 0.2444 | 0.6457 | 187 |
| **Att U-Net 2D** | N/A | 0.4110 | 0.3212 | 0.6261 | 0.4035 | 141.23 | 0.2759 | 0.5917 | 187 |
| **PGA-UNet Exp B** | zoom_out | **0.8606** | **0.7619** | **0.8479** | **0.8897** | **12.16** | **0.0237** | **0.9558** | 248 |
| **PGA-UNet Exp B** | shift | 0.8380 | 0.7301 | 0.8331 | 0.8616 | 14.36 | 0.0280 | 0.9388 | 248 |
| **PGA-UNet Exp B** | mixed_7_3 | 0.8558 | 0.7552 | 0.8428 | 0.8862 | 12.79 | 0.0250 | 0.9532 | 248 |
| **SAM-Med2D (fine-tuned)** | zoom_out | 0.7624 | 0.6424 | 0.7597 | 0.7880 | 52.08 | 0.2035 | 0.9003 | 248 |
| **SAM-Med2D (fine-tuned)** | shift | 0.7273 | 0.5983 | 0.7318 | 0.7496 | 54.44 | 0.2126 | 0.8834 | 248 |
| **SAM-Med2D (fine-tuned)** | mixed_7_3 | 0.7554 | 0.6325 | 0.7558 | 0.7813 | 51.84 | 0.2025 | 0.8997 | 248 |
| **SAM-Med2D (zero-shot)** | zoom_out | 0.5298 | 0.3867 | 0.4703 | 0.6794 | 111.27 | 0.4346 | 0.8199 | 248 |
| **SAM-Med2D (zero-shot)** | shift | 0.5203 | 0.3763 | 0.4629 | 0.6665 | 115.55 | 0.4514 | 0.8001 | 248 |
| **SAM-Med2D (zero-shot)** | mixed_7_3 | 0.5289 | 0.3853 | 0.4687 | 0.6786 | 114.31 | 0.4465 | 0.8125 | 248 |

> **HD95/size** = `hd95_raw / img_size` (PGA: ÷512, SAM: ÷256, UNet/Att: ÷512) — dùng khi so sánh tương đối.  
> N=187 (UNet/AttUNet: merged mask) vs N=248 (PGA/SAM: per-polygon) — xem phân tích Sec 2.4.  
> **PGA numbers nguồn:** `Result/pga-extended-test.ipynb` (chạy 2026-06-02, dùng `create_plateau_heatmap` đúng). Số cũ trong `pga-unet2d-kq.ipynb` có thể khác nhẹ do checkpoint khác lần chạy.  
> **SAM zero-shot nguồn:** `Result/sam-med2d-zero-shot.ipynb` (chạy 2026-06-02).

### 6.2 Best Val Dice & Epochs

| Model | Best Val Dice | Epoch dừng | Ghi chú |
|-------|--------------|-----------|---------|
| U-Net 2D | 0.5345 | 82/100 | Early stop patience=15 |
| Att U-Net 2D | 0.4364 | 47/100 | Early stop patience=15 |
| PGA-UNet Exp B | 0.8652 | 60/100 | Early stop patience=15 |
| SAM-Med2D | 0.7731 | 12/50 | Early stop patience=10 — converge nhanh do pretrained ViT-B |

---

## 6.3 Phân Tích Kết Quả (cho Chapter 4 báo cáo)

### A. PGA-UNet vượt trội toàn diện

PGA-UNet (mixed_7_3 — kịch bản thực tế nhất) đạt **Dice=0.8552**, hơn SAM-Med2D 9.98% và hơn U-Net 34.6%, mặc dù nhỏ hơn SAM **25×** về tham số (4M vs 100M).

| So sánh | Dice gap | Ghi chú |
|---|---|---|
| PGA mixed vs SAM mixed | +0.0998 (+13.2%) | Cùng paradigm, cùng 248 samples |
| PGA mixed vs UNet | +0.3462 (+68%) | Khác paradigm: prompt vs blind |
| PGA zoom_out vs shift | −0.0378 (−4.4%) | Robustness khi prompt kém |
| SAM zoom_out vs shift | −0.0351 (−4.6%) | Tương đương PGA về robustness |

### B. HD95 — PGA vượt trội tuyệt đối (kể cả sau normalize)

| Model | HD95 raw | HD95/imgsize | Ý nghĩa |
|---|---|---|---|
| PGA zoom_out | 12.10px | **0.0236** | Rất sát biên GT |
| PGA mixed | 13.08px | **0.0255** | — |
| SAM zoom_out | 52.08px | 0.2035 | ~8.6× tệ hơn PGA (normalized) |
| U-Net | 125.12px | 0.2444 | ~10.4× tệ hơn PGA (normalized) |
| Att U-Net | 141.23px | 0.2759 | Tệ nhất |

### C. Phát hiện bất ngờ: Att U-Net tệ hơn U-Net

Attention U-Net (Dice=0.4110) < U-Net (0.5090) — ngược kỳ vọng. Nguyên nhân có thể:
- Converge sớm hơn (epoch 47 vs 82) — cơ chế attention cần thêm epoch để học
- Dataset đơn giản (chỉ HFlip) không đủ diversity cho attention gate học spatial prior
- `grid_attention_layer` thêm complexity khiến gradient flow khó hơn với dataset nhỏ

> **Khuyến nghị khi viết báo cáo:** Giải thích đây là kết quả thú vị — trên dataset nhỏ, cơ chế attention có thể **overfit** vào các spatial pattern đặc thù, dẫn đến tổng quát hóa kém hơn U-Net đơn giản. Đây là động lực thêm cho thiết kế *prompt-guided* thay vì *attention-only*.

### D. SAM early stop epoch 12 — bình thường với pretrained model

SAM-Med2D fine-tune từ ViT-B đã train trên 4M+ ảnh y tế → chỉ cần 12 epochs để adapt. Val Dice 0.7731 (epoch 2 best) và dừng ở epoch 12 không phải dấu hiệu underfitting, mà là model đã saturate.

### E. Kết luận định hướng Chapter 4

1. **Kết quả chính để báo cáo**: PGA mixed_7_3 Dice=**0.8552** vs SAM mixed_7_3 Dice=**0.7554**
2. **Highlight HD95**: PGA 13.08px ↔ SAM 51.84px (raw) — PGA chính xác hơn nhiều về biên
3. **CBL**: PGA (0.9525) > SAM (0.8997) — PGA định vị tâm tốt hơn
4. **Không so sánh Dice PGA với UNet/AttUNet trực tiếp** mà không giải thích paradigm khác
5. **Đề cập Att U-Net < U-Net** như một phát hiện phụ → củng cố luận điểm "prompt là cần thiết"

---

## 7. App Pipeline (`app.py`)

**File:** `Source/project/app.py` — **⚠️ CHƯA TỒN TẠI** (cần xây dựng)

```
Upload ảnh X-quang
    ↓ MobileNetV4 classify → CÓ/KHÔNG BỆNH
    ↓ (nếu có bệnh)
User vẽ bbox (2 click) → Gaussian heatmap Prompt₀
    ↓ PGA-UNet Inference₀ → Prediction₀   ← [khối quan trọng]
    ↓ Dark detection (>70% đen?)
    ├─ Không: IPR 3 vòng (normal)
    └─ Có:    GradCAM từ Prediction₀ → IPR 3 vòng (GradCAM prompt)
    ↓ LCC extraction
    ↓ Hiển thị mask + GradCAM overlay (Gradio UI tiếng Việt)
```

---

## 8. Checklist Colab Trước Khi Chạy

**Chung cho tất cả:**
- [ ] GPU T4/A100 được cấp phát
- [ ] Google Drive mount thành công
- [ ] Dataset `1fU7KPln7joaa3EZZtGn-VKeg9i4AmPG3` download → `dataset_BTXRD.zip`

**SAM-Med2D thêm:**
- [ ] Cell 6 (JSON → per-polygon) chạy xong trước Cell 7 (create_mapping_json)
- [ ] Sau Cell 6: kiểm tra `masks/train/*.png` có dạng `IMG_1.png` không

**Ước tính thời gian T4:**
| Notebook | Training | Test |
|----------|---------|------|
| UNet2D (512, ≤100ep) | 3–5h | ~5 phút |
| AttUNet2D (512, ≤100ep) | 4–6h | ~5 phút |
| PGA-UNet (512, ≤100ep) | 6–10h | ~10 phút |
| SAM-Med2D (256, ≤50ep) | 4–7h | ~15 phút |

---

## 9. So Sánh Với SOTA

> Mục tiêu: định vị PGA-UNet trong bức tranh lớn hơn — so với các SOTA no-prompt và SOTA prompt-based trên ảnh y khoa 2D.

### 9.1 SOTA Không Prompt (Blind Segmentation)

Các model phân đoạn tự động, không nhận bất kỳ tín hiệu vị trí nào từ người dùng:

| Model | Kiến trúc | Năm | Dataset tiêu biểu | Dice (BTXRD) | Ghi chú |
|-------|-----------|-----|-------------------|-------------|---------|
| **U-Net** | CNN encoder-decoder | 2015 | Medical general | — | Baseline của luận văn |
| **Attention U-Net** | U-Net + attention gate | 2018 | Medical general | — | Baseline cải tiến |
| UNet++ | Nested U-Net | 2018 | Multiple | N/A\* | Chưa test trên BTXRD |
| nnU-Net | Self-configuring U-Net | 2021 | 23 med. benchmarks | N/A\* | SOTA no-prompt tổng quát |
| TransUNet | CNN + ViT | 2021 | Synapse, ACDC | N/A\* | Cần GPU lớn |
| Swin-UNet | Pure Swin Transformer | 2022 | Synapse, ACDC | N/A\* | Full-transformer |
| MedT | Gated Axial Attention | 2021 | MoNuSeg, GlaS | N/A\* | Tốt dataset nhỏ |

> \* N/A: Chưa chạy trên BTXRD trong phạm vi luận văn này. Các giá trị trên benchmark khác không thể so sánh trực tiếp.

**Lý do không chạy thêm no-prompt SOTA:**
- Dataset BTXRD là dataset nội bộ, chưa có benchmark công bố từ các paper khác
- Mục tiêu luận văn là chứng minh **giá trị của prompt mechanism** (PGA vs no-prompt baseline), không phải so sánh toàn bộ kiến trúc encoder
- nnU-Net và TransUNet đã được đề cập trong Chapter 2 như context lý thuyết

### 9.2 SOTA Có Prompt (Interactive Segmentation)

Các model nhận bounding box hoặc point từ người dùng — **cùng paradigm với PGA-UNet**:

| Model | Prompt type | Backbone | Năm | Dataset | Dice (BTXRD) | Ghi chú |
|-------|-------------|----------|-----|---------|-------------|---------|
| **PGA-UNet (đề xuất)** | Gaussian heatmap bbox | U-Net gọn nhẹ | 2024 | BTXRD | — | 248 samples, zoom_out |
| **SAM-Med2D (fine-tuned)** | Hard bbox | ViT-B + Adapter | 2023 | BTXRD | — | 248 samples, zoom_out |
| SAM (zero-shot) | Hard bbox / point | ViT-H | 2023 | General | N/A\* | Không fine-tune, yếu trên X-ray |
| MedSAM | Hard bbox | ViT-B fine-tuned | 2024 | 1.5M med. images | N/A\* | Chưa test trên BTXRD |
| RITM | Click refinement | HRNet | 2022 | COCO, SBD | N/A\* | Interactive click, khác paradigm |

> **Đánh giá:** SAM-Med2D là SOTA prompt-based thực sự được chạy trong luận văn này, trên cùng dataset BTXRD, cùng 248 test samples — **đây là so sánh trực tiếp và công bằng nhất**.

---

## 10. Đánh Giá: Kết Quả PGA Có Bị "Ảo" Không?

### 10.1 Các nguồn tiềm năng gây "ảo"

#### A. Lợi thế prompt (KHÔNG phải ảo — by design)

PGA nhận Gaussian heatmap từ bounding box của bác sĩ → model biết **vị trí tổn thương trước khi phân đoạn**. U-Net/ATT-UNet không có thông tin này.

**Kết luận:** Đây là **lợi thế có chủ đích**, phản ánh đúng kịch bản thực tế (bác sĩ khoanh vùng nghi ngờ). Chapter 4 report đã ghi nhận rõ: *"sự chênh lệch hiệu năng phản ánh giá trị của việc tích hợp tri thức chuyên gia, chứ không đơn thuần là sự vượt trội của kiến trúc mạng."*

#### B. 248 vs 187 samples (ẢNH HƯỞNG NHỎ, đã xử lý)

- PGA test 248 samples (per-polygon), U-Net/ATT-UNet test 187 (merged mask)
- 28 ảnh multi-tumor: PGA phân đoạn từng khối u với bbox tight → có thể dễ hơn merged mask
- **Mức độ:** nhỏ (~15% test set bị ảnh hưởng)
- **Xử lý:** SAM-Med2D đã được đồng bộ lên 248 samples → so sánh PGA vs SAMmed2D là công bằng

#### C. Zoom_out là "oracle prompt" (THỰC SỰ CÓ RỦI RO)

Zoom_out r=0.30 tức là bbox mở rộng 30% đều từ **GT polygon chính xác** → đây là prompt gần lý tưởng nhất.

| Kịch bản | Prompt quality | Ý nghĩa |
|----------|---------------|---------|
| zoom_out | Gần lý tưởng (từ GT bbox) | Kết quả tốt nhất, nhưng không thực tế 100% |
| shift | Sai lệch vị trí ~30% | Mô phỏng bác sĩ vẽ không chính xác |
| mixed_7_3 | 70% zoom_out + 30% shift | **Thực tế nhất** |

**→ Kết quả zoom_out là "ceiling" (trần lý thuyết), mixed_7_3 mới là con số thực tế để so sánh.**

#### D. extract_lcc hậu xử lý (KHÔNG ảo — nhất quán)

Tất cả 4 model đều dùng extract_lcc (lấy vùng liên thông lớn nhất) → loại noise → công bằng.

### 10.2 Verdict tổng hợp

| Câu hỏi | Trả lời |
|---------|---------|
| PGA cao hơn U-Net/ATT-UNet có ảo không? | **Không ảo** — bởi vì PGA nhận thêm prompt (different paradigm). Ghi chú rõ trong báo cáo là đủ. |
| Số liệu zoom_out của PGA có đáng tin không? | **Có**, nhưng đây là ceiling. **mixed_7_3 là con số trung thực hơn** để báo cáo. |
| So sánh PGA vs SAMmed2D có công bằng không? | **Có** — cùng dataset `1f...`, cùng 248 test samples, cùng 3 prompt modes, cùng extract_lcc. |
| Cần thêm SOTA nào để tăng độ tin cậy? | MedSAM trên BTXRD là ideal. Nếu không chạy được: ghi trong "hướng phát triển tương lai". |

### 10.3 Khuyến nghị khi viết báo cáo

1. **Luôn báo cáo cả 3 modes** (zoom_out / shift / mixed_7_3) — không chỉ zoom_out
2. **Nhấn mạnh paradigm khác nhau** khi so sánh PGA vs U-Net: "tương tác vs tự động"
3. **Dùng mixed_7_3 làm giá trị chính** để kết luận về hiệu năng thực tế của PGA
4. **Ghi rõ N=248 (PGA, SAMmed2D) vs N=187 (U-Net, ATT-UNet)** trong caption bảng
5. **Normalize HD95** khi so sánh SAMmed2D (256px) với PGA (512px)

---

## 11. Kế Hoạch Từ Thời Điểm Hiện Tại

> Legend: `[ ]` chưa làm · `[~]` đang dở · `[x]` hoàn thành

---

### ✅ Giai đoạn 0 — Nộp Hồ Sơ Khẩn Cấp (Deadline: **15/6/2026**) — HOÀN THÀNH

> Đã nộp đầy đủ ngày 01/06/2026. Drive: https://drive.google.com/drive/folders/1OP8RgnqKwXyYOP_NQf8B_u7E3lpiGJ-m?usp=sharing

- [x] Báo cáo đúng format chuẩn trường (phần đóng góp = đóng góp của đề tài, không phải cá nhân)
- [x] Chốt danh mục **References** — trích dẫn chuẩn xác
- [x] Nộp toàn bộ **Source Code** kèm documentation
- [x] **Google Drive link** chứa: data gốc BTXRD, data đã xử lý chia train/val/test
- [x] Đã gửi giảng viên

---

### Giai đoạn 1 — Lấy số liệu thực nghiệm ✅ HOÀN THÀNH

#### 1.1 U-Net 2D ✅
- [x] Train → Early stop epoch 82 | Best Val Dice: **0.5345**
- [x] Test → Dice=0.5090 | IoU=0.4125 | HD95=125.12px | CBL=0.6457

#### 1.2 Attention U-Net 2D ✅
- [x] Train → Early stop epoch 47 | Best Val Dice: **0.4364**
- [x] Test → Dice=0.4110 | IoU=0.3212 | HD95=141.23px | CBL=0.5917

#### 1.3 PGA-UNet 2D ✅
- [x] Train → Early stop epoch 60 | Best Val Dice: **0.8652**
- [x] Test 3 modes → xem Section 6.1
- [x] CSV: `results/pga_unet_expB_results.csv`

#### 1.4 SAM-Med2D ✅
- [x] Fine-tune → Early stop epoch 12 | Best Val Dice: **0.7731**
- [x] Test 3 modes → xem Section 6.1
- [x] CSV: `workdir/test_results/csv/sammed2d_*.csv`

---

### Giai đoạn 2 — Hoàn thiện báo cáo Chapter 4 [~] HOÀN THÀNH 1/2

**File chính:** `Report/Chapter4/chapter4.tex`  
**Số liệu nguồn:** Section 6.1 & 6.3 của file này

#### Đã xong ✅
- [x] Điền số liệu thực vào `tab:baseline_comparison` (U-Net=0.5090, ATT=0.4110, PGA zoom_out=0.8658)
- [x] Thêm bảng `tab:sam_comparison`: PGA vs SAMmed2D × 3 modes + footnote HD95 chuẩn hóa
- [x] Cập nhật `tab:robustness_comparison` với số liệu thực (zoom=0.8658, shift=0.8280, mixed=0.8552)
- [x] Điền dataset stats `tab:dataset_stats` (train≈1495 ảnh/1859 samples, val≈159/211, test=187/248)
- [x] Chèn 5 ảnh visualization trích từ notebook → `Report/images/vis_*.png`:
  - `vis_pga_1.png` → `fig:qualitative_pga` (IMG001768, zoom+shift)
  - `vis_pga_2.png` → `fig:qualitative_ipr` (IMG001538, minh họa IPR)
  - `vis_sam_1.png` → `fig:qualitative_sam` (IMG001768, 3 modes SAM)
  - `vis_unet_1.png` → `fig:qualitative_unet`
  - `vis_attunet_1.png` → `fig:qualitative_attunet`
- [x] Cập nhật analysis text: số liệu Dice/HD95 đúng, phân tích AttUNet < UNet, PGA 4M > SAM 100M

#### Đã bổ sung thêm (2026-05-30) ✅
- [x] Thêm SAM-Med2D vào Chapter 2 (mô hình liên quan + diagram `diagram_sammed2d.png`)
- [x] Thêm `fig:attunet_architecture` (`diagram_attunet.png`) vào Chapter 2
- [x] Thêm `fig:pga_architecture` (`diagram_pga.png`) vào Chapter 3
- [x] Thay TikZ U-Net bằng `diagram_unet.png` (Chapter 2)
- [x] `fig:app_interface` — đã chèn `app_interface.png` vào Chapter 4
- [x] Fix Overfull hbox toàn bộ 4 bảng: `tab:robustness_comparison`, `tab:sam_comparison`, `tab:gradcam_rescue`, `tab:ipr_convergence`
- [x] Thêm ảnh vis thêm: `vis_unet_2`, `vis_attunet_2`, `vis_pga_3`, `vis_sam_2`

#### Còn thiếu — cần làm thủ công 🔲
- [x] `tab:gradcam_rescue` — đã có số thật (174/174=100%, 4 nhóm GradCAM; từ `Result/defense-comparison-sam-vs-pga.ipynb`)
- [x] `fig:confusion_matrix` + `AUC-ROC` — `images/classification_evaluation.png` đã tồn tại (untracked), AUC-ROC=0.9514 (từ `Result/MobileNetV4_BTXRD_dataset.ipynb`)
- [ ] `tab:ipr_convergence` (k=0..3) — hiện dùng số ước tính, cần chạy `Source/PGA_Ablation.ipynb` để có số thật
- [ ] Sơ đồ kiến trúc tổng thể hệ thống — TikZ đã xóa, cần vẽ và lưu `images/system_architecture.png`
- [ ] Sơ đồ quy trình tiền xử lý 6 bước — TikZ đã xóa, cần vẽ và lưu `images/preprocessing_pipeline.png`
- [ ] Sơ đồ pipeline phân lớp Gatekeeper (MobileNetV4) — TikZ đã xóa, cần vẽ và lưu `images/classification_pipeline.png`

**Lưu ý viết báo cáo:**
- Tránh so sánh trực tiếp Dice PGA vs Dice U-Net mà không ghi chú paradigm khác nhau
- Kết quả zoom_out = ceiling lý thuyết; mixed_7_3 = thực tế; shift = worst-case
- HD95 SAMmed2D ~2× nhỏ hơn do scale 256 vs 512 — cần normalize khi so sánh

---

### Giai đoạn 2B — Bổ Sung Lý Thuyết & Ablation (từ feedback giảng viên) 🔲

> Cần thiết để trả lời các câu hỏi phản biện trong buổi bảo vệ.

#### Lý thuyết Heatmap Encoding
- [x] Viết mục trong Chapter 3 (section 3.3.1): giải thích cơ sở khoa học chọn **Gaussian heatmap** thay vì hard binary mask
  - Lý do 1: binary mask tạo step edge → gradient giả tạo → mạng học cạnh hộp thay vì đặc trưng tổn thương
  - Lý do 2: Grad-CAM saliency map tự nhiên có dạng liên tục → Plateau Heatmap tương thích cơ chế học của mạng
  - So sánh SAM: dùng positional embedding rời rạc (2 vector 256d) → phù hợp Transformer token, không phù hợp U-Net feature map 2D
  - PGA dùng heatmap 2D → tương thích trực tiếp với phép nhân theo phần tử tại Spatial Gate (eq:spatial_gate)

#### Fine-tune Clarity
- [x] Ghi rõ trong Chapter 3 (subsection 3.3.4 mới) + Chapter 4: PGA-UNet huấn luyện **hoàn toàn từ đầu** (không đóng băng gì), SAM-Med2D fine-tune từ pretrained ViT-B
  - Bảng so sánh chiến lược: tab:training_strategy_compare đã thêm vào Chapter 3
  - Chapter 4 có thêm câu giải thích cross-reference về "train từ đầu vs fine-tune"

#### Ablation Study (ít nhất 2 kịch bản)
- [ ] Kịch bản A: **No-prompt baseline** — U-Net không có heatmap (đã có: Dice=0.5090)
- [ ] Kịch bản B: **Heatmap, không IPR** — chạy PGA chỉ 1 forward pass, không lặp IPR → so sánh với đầy đủ PGA
- [ ] Kịch bản C: **PGA đầy đủ** — zoom_out/shift/mixed (đã có)
- [ ] Bảng ablation trong Chapter 4: A vs B vs C → chứng minh mỗi thành phần đóng góp gì

#### Kịch bản So Sánh Công Bằng với SAM ✅ ĐÃ XONG
- [x] Thêm hàng **"SAM-Med2D zero-shot"** (không fine-tune) vào bảng so sánh
  - Dùng checkpoint gốc SAM-Med2D + box prompt trên BTXRD test 248 samples → ghi Dice/IoU
  - Điều này minh bạch hóa: SAM fine-tuned vs SAM zero-shot vs PGA (đã train)
- [ ] Ghi chú rõ trong caption bảng: "fine-tuned" vs "zero-shot" để tránh bị chỉ ra là so sánh khập khiễng

#### Phương Án Xử Lý Prompt Sai
- [ ] Mô tả trong Chapter 3/4: nếu bác sĩ vẽ bbox lệch vị trí, GradCAM rescue xử lý ra sao
- [ ] Xác định giới hạn: shift >50% thì model fail như thế nào (dùng shift prompt mode làm minh chứng)
- [ ] Đề xuất cải tiến: multi-round correction (bác sĩ điều chỉnh prompt sau khi thấy kết quả)

---

### Giai đoạn 2C — Loss Function Research (gợi ý giảng viên) 🔲

> Hướng thay thế bước MobileNetV4 classification bằng loss function thông minh hơn.

#### Nghiên cứu lý thuyết
- [ ] Tìm và trình bày công thức toán học của các loss function:
  - **Empty mask / no-disease**: Weighted BCE với `pos_weight` thấp khi mask rỗng; Tversky loss với penalty đặc biệt cho FP khi GT là 0
  - **Small lesions**: Focal Tversky Loss (`FTL = (1-Tversky)^γ` với γ>1)
  - **Fuzzy borders**: Boundary loss (Kervadec et al. 2019): `L_boundary = ∫ q(x) · s_θ(x) dx`
  - **Data imbalance**: Focal loss, Asymmetric loss

#### Thực nghiệm (nếu còn thời gian)
- [ ] Chạy PGA-UNet với Focal Tversky + Boundary loss kết hợp → xem Dice/HD95 thay đổi không
- [ ] Đặc biệt: xem model có tự nhận ra "ảnh không bệnh" (output mask rỗng) mà không cần MobileNetV4 không
- [ ] Ghi kết quả vào Chapter 4 (nếu có) hoặc Chapter 5 "hướng phát triển tương lai" (nếu không kịp chạy)

---

### Giai đoạn 2D — Đánh Giá Theo Sub-Category 🔲

> Giảng viên yêu cầu: không chỉ báo cáo overall Dice mà phải phân tích theo nhóm thách thức.

- [ ] Phân loại 248 test samples BTXRD thành 4 nhóm:
  - **Small lesions**: bbox diện tích < 32×32 px (tương đương ~4% diện tích ảnh 512×512)
  - **Fuzzy borders**: cần heuristic (e.g., mean gradient intensity thấp trong bbox)
  - **Large clear lesions**: bbox diện tích ≥ 64×64 px
  - **No-disease**: mask hoàn toàn rỗng (nếu có trong test set)
- [ ] Tính Dice/IoU/HD95 riêng cho từng nhóm → bảng trong Chapter 4
- [ ] So sánh PGA (mixed_7_3) vs SAM-Med2D (mixed_7_3) trên từng nhóm
- [ ] Dùng kết quả này để giải thích tại sao HD95 của PGA vượt trội (precision ở biên)

---

### Giai đoạn 3 — Tùy chọn (nếu còn thời gian)

- [ ] **MedSAM zero-shot trên BTXRD**: dùng `facebook/sam-vit-base` + box prompt, không fine-tune
  - Mục đích: thêm 1 điểm so sánh prompt-based SOTA không cần train
  - Ưu tiên: thấp (có thể thay bằng đề xuất trong "hướng phát triển")
- [ ] **nnU-Net** trên BTXRD: no-prompt SOTA tự cấu hình
  - Mục đích: upper bound cho no-prompt category
  - Ưu tiên: thấp (setup phức tạp, cần nhiều RAM)
- [ ] Cập nhật bảng SOTA Section 9 với số liệu thực sau khi chạy

---

### Giai đoạn 4 — Chốt & nộp

- [ ] Cập nhật Section 6 (bảng kết quả) với toàn bộ số liệu thực
- [ ] Review Chapter 4 lần cuối: số liệu, hình ảnh, phân tích
- [ ] Kiểm tra Chapter 3: có giải thích rõ heatmap encoding và lý thuyết cơ sở chưa (sau GD2B)
- [ ] Kiểm tra Chapter 5 (kết luận) đồng bộ với kết quả thực
- [ ] Bổ sung mục "Hạn chế và hướng phát triển" trong Chapter 5: đề cập loss function mới, semi-supervised PCPL, multi-dataset testing
- [ ] **Review toàn bộ báo cáo theo checklist giảng viên**: đóng góp rõ ràng, không đạo văn, số liệu nhất quán giữa các chapter
- [ ] Build PDF từ `Report/main.tex` → kiểm tra format, không có overfull hbox
- [ ] Backup toàn bộ checkpoints lên Drive

---

### Tóm tắt thứ tự ưu tiên (cập nhật 02/06/2026 — deadline 12/06/2026)

> **Khung đóng góp:** Đề tài có **2 đóng góp tách biệt** — (1) Nghiên cứu: PGA-UNet vượt SAM-Med2D trên BTXRD; (2) Sản phẩm: pipeline đầy đủ MobileNetV4 + IPR + GradCAM. Tách 2 đóng góp giải quyết lo ngại "cascading error" của GV: Dice=0.86 là số sạch của model, không bị pha lẫn với pipeline.

```
[✅ HOÀN THÀNH]
  GD0: Nộp hồ sơ đầy đủ ngày 01/06/2026
  GD1: Số liệu 4 mô hình (UNet, AttUNet, PGA, SAM fine-tuned + zero-shot)
  tab:gradcam_rescue: Số thật (174/174=100%, 4 nhóm GradCAM)
  classification_evaluation.png: File có sẵn, AUC-ROC=0.9514
  Lý thuyết heatmap (Chapter 3 sec 3.3.1): Cơ sở + so sánh SAM ✅
  Fine-tune clarity (Chapter 3 subsec 3.3.4): Bảng chiến lược + cross-ref Chapter 4 ✅

[NGAY BÂY GIỜ — trước 12/6, còn ~9 ngày]
  # Đóng góp 1 (Nghiên cứu)
  [x] GD2 diagrams: PNG đã export, đã referenced trong chapter3.tex ✅
  [x] GD2D: Sub-category evaluation ✅
        → SubCat_PGA_vs_Baseline: Easy Dice=0.8632 / Hard Dice=0.8521 vs UNet=0.2379 (+61%)
        → SubCat_PGA_vs_SAM: Nhỏ PGA=0.82/SAM=0.25 · Mờ PGA=0.82/SAM=0.46 · Rõ PGA=0.89/SAM=0.85
        → 2 bảng tab:subcat_baseline + tab:subcat_sam đã thêm vào chapter4.tex
  [ ] GD2B: Ablation kiến trúc V1–V5 → Source/Ablation/ (5 notebook, chạy Colab song song)
            Sau khi có số: cập nhật tab:ablation_prompt + xác nhận tab:ipr_convergence

[NẾU CÒN THỜI GIAN]
  GD2C: Loss function research (hướng thay thế MobileNetV4) → Chapter 5 hướng phát triển
  Cross-validation / resampling → Chapter 5 limitations
  Multi-dataset testing → Chapter 5 hướng phát triển
  app.py: Gradio UI demo sản phẩm

[CUỐI CÙNG]
  GD4: Review toàn bộ, build PDF kiểm tra format, backup checkpoints
```

> **Bottleneck (02/06/2026):** 10 ngày còn lại. Ưu tiên: 3 sơ đồ + ablation (`tab:ipr_convergence`) + sub-category evaluation.

---

## 12. Hướng Mở Rộng: Bán Giám Sát Với Prompt-Constrained Pseudo-Label (PCPL)

> Cập nhật: 2026-05-29

### 12.1 Cơ Sở Khả Thi

PGA-UNet có **cơ sở rõ ràng** để kết hợp học bán giám sát (semi-supervised learning) với điều kiện:
- Nhãn **prompt (bounding box) luôn có 100%** — cả labeled lẫn unlabeled
- Nhãn **mask polygon chỉ có ở subset labeled**

**Lý do PGA phù hợp hơn UNet thuần cho bán giám sát:**

| Yếu tố | UNet thuần | PGA-UNet |
|--------|-----------|----------|
| Pseudo-mask noise | Toàn ảnh, không có prior | Bị constrain vào vùng prompt bbox → ít noise |
| Spatial prior | Không có | PromptSpatialGate boost features đúng vùng tổn thương |
| Model robustness | Không có augmentation prompt | Forward() đã zero-out/noise prompt 30% training → robust |
| Pseudo-label quality | Thấp (dễ false positive ngoài ROI) | Cao hơn (prompt mask out vùng không liên quan) |

**Tính thực tế trong y tế:**
- Vẽ bounding box: ~5 giây/ảnh — rất rẻ
- Vẽ polygon mask: ~2–5 phút/ảnh — đắt gấp 20–60×
- → Semi-supervised với prompt 100% là kịch bản **hoàn toàn realistic**

### 12.2 Phương Pháp Đề Xuất: PCPL

**Prompt-Constrained Pseudo-Label** — 2 giai đoạn:

```
Phase 1 — Warm-up (supervised only, 30 epochs):
    Labeled data (L%): image + mask + prompt
    → train bình thường với L_sup = BCE + Dice
    → lưu model làm Teacher

Phase 2 — Semi-supervised (full training, ≤100 epochs):
    Labeled:   L_sup = BCE + Dice  (như cũ)
    Unlabeled: Teacher(image, prompt) → raw_pseudo
               pseudo = (sigmoid(raw_pseudo) > τ).float()
               pseudo *= (prompt_heatmap > 0.1).float()  ← clip vào vùng prompt
               L_pseudo = BCE(student(image, prompt), pseudo) + Dice(...)
    
    Tổng loss: L = L_sup + λ * L_pseudo
    Cập nhật Teacher: EMA của Student weights (α=0.999)
```

**Tham số cần tune:**
- `L%` ∈ {20%, 50%, 80%} — tỷ lệ dữ liệu có mask
- `τ = 0.5` — threshold tạo pseudo-mask
- `λ = 0.5` — trọng số unsupervised loss
- `α = 0.999` — EMA decay cho Teacher

### 12.3 Thiết Kế Thực Nghiệm

**Split dữ liệu train (tổng ~1859 samples):**

| Tên thực nghiệm | Labeled (có mask) | Unlabeled (chỉ prompt) |
|-----------------|-------------------|----------------------|
| PCPL-20 | 372 (~20%) | 1487 (~80%) |
| PCPL-50 | 930 (~50%) | 929 (~50%) |
| PCPL-80 | 1487 (~80%) | 372 (~20%) |
| Supervised-100 | 1859 (100%) | — (baseline) |

**Test:** giữ nguyên 248 samples, 3 prompt modes (zoom_out / shift / mixed_7_3).

**Bảng so sánh kết quả kỳ vọng:**

| Model | Labeled % | Dice↑ | IoU↑ | Pre↑ | Rec↑ | HD95↓ | CBL↑ |
|-------|-----------|-------|------|------|------|-------|------|
| PGA Supervised | 100% | — | — | — | — | — | — |
| PGA PCPL-80 | 80% | — | — | — | — | — | — |
| PGA PCPL-50 | 50% | — | — | — | — | — | — |
| PGA PCPL-20 | 20% | — | — | — | — | — | — |
| UNet Pseudo-50 | 50% | — | — | — | — | — | — |

> Kỳ vọng: **PCPL-80 ≈ Supervised-100** (prompt constraint giúp pseudo-label đủ sạch).  
> **PCPL-50 > UNet Pseudo-50** (lợi thế rõ nhờ spatial prior từ prompt).

### 12.4 Thay Đổi Code Cần Thiết

Không cần thay kiến trúc model. Chỉ cần bổ sung vào training pipeline:

**1. `dataset.py`** — thêm flag `has_mask=True/False` để split labeled/unlabeled:
```python
# Labeled sample: trả về (image, mask, prompt)
# Unlabeled sample: trả về (image, None, prompt)  ← mask = None
```

**2. `train_pga.py`** — thêm semi-supervised training loop:
```python
# Tách DataLoader thành labeled_loader + unlabeled_loader
# Phase 1: warm-up 30 epochs chỉ dùng labeled_loader
# Phase 2: mỗi batch = 1 labeled batch + 1 unlabeled batch
#   - Teacher.eval() → sinh pseudo_mask → clip prompt
#   - Student.train() → tính L_sup + λ * L_pseudo
#   - Cập nhật Teacher: EMA(Student)
```

**3. `PGA_Unet2D.ipynb`** — thêm cell mới sau cell Train:
- Cell markdown "**Bán Giám Sát (PCPL)**"
- Cell code chạy `train_pga_semi.py` với các tham số `--labeled_ratio 0.5 --lambda_unsup 0.5`

### 12.5 Điểm Mạnh Khi Báo Cáo

1. **Novelty rõ ràng**: Kết hợp prompt-guided attention với semi-supervised — chưa thấy trong các paper sỏi tiết niệu X-quang 2D.
2. **Practical contribution**: Chứng minh PGA cho phép giảm 50% công annotation mask mà vẫn giữ hiệu năng chấp nhận được.
3. **Phân tích so sánh**: PCPL-PGA vs Pseudo-UNet (cùng % labeled) → thấy rõ lợi thế của prompt constraint.
4. **Phù hợp hướng phát triển** (Chapter 5): "Bán giám sát với prompt cheaply annotated là hướng triển khai thực tế nhất trong bệnh viện."

### 12.6 Checklist Thực Hiện

> Chỉ thực hiện **sau khi có số liệu supervised đầy đủ** (Giai đoạn 1–2 hoàn thành).

- [ ] Có đủ số liệu supervised làm baseline (Section 6 điền xong)
- [ ] Viết `train_pga_semi.py` — thêm EMA teacher + pseudo-label loop
- [ ] Cập nhật `dataset.py` — thêm `labeled_ratio` split
- [ ] Thêm cell "Bán Giám Sát (PCPL)" vào `PGA_Unet2D.ipynb`
- [ ] Chạy PCPL-50 trước (thực nghiệm trọng tâm, ~8–12h trên T4)
- [ ] Chạy PCPL-20 và PCPL-80 nếu còn thời gian
- [ ] Điền bảng Section 12.3
- [ ] Viết đoạn phân tích trong Chapter 5 (hướng phát triển)
