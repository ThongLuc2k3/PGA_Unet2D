# Kế Hoạch & Đánh Giá Thực Nghiệm — PGA-UNet2D Luận Văn

> Cập nhật: 2026-05-28

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

## 5. Diagram 4 — Inference Pipeline PGA-UNet (App)

**File:** `diagrams/diagram_4_full_pipeline.drawio`

### Flow đầy đủ (đã bổ sung khối PGA-UNet Inference₀):

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

## 6. Kết Quả Mong Đợi (Bảng Luận Văn)

| Model | Prompt Mode | Dice↑ | IoU↑ | Pre↑ | Rec↑ | HD95↓ | CBL↑ | N |
|-------|-------------|-------|------|------|------|-------|------|---|
| U-Net 2D | N/A | — | — | — | — | — | — | 187 |
| Att U-Net 2D | N/A | — | — | — | — | — | — | 187 |
| PGA-UNet Exp B | zoom_out | — | — | — | — | — | — | 248 |
| PGA-UNet Exp B | shift | — | — | — | — | — | — | 248 |
| PGA-UNet Exp B | mixed_7_3 | — | — | — | — | — | — | 248 |
| SAM-Med2D | zoom_out | — | — | — | — | — | — | 248 |
| SAM-Med2D | shift | — | — | — | — | — | — | 248 |
| SAM-Med2D | mixed_7_3 | — | — | — | — | — | — | 248 |

> **Lưu ý khi đọc HD95**: U-Net/ATT/PGA tính trên 512px; SAM-Med2D tính trên 256px.  
> HD95 normalize = `hd95_raw / img_size` để so sánh tương đối.

---

## 7. App Pipeline (`app.py`)

**File:** `Source/project/app.py` (17.4 KB) — **Hoàn chỉnh v1**

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

### Giai đoạn 1 — Lấy số liệu thực nghiệm ⚡ (ưu tiên cao nhất)

Chạy tuần tự 4 notebook trên Colab T4/A100. Mỗi notebook cho ra 1 file CSV kết quả.

#### 1.1 U-Net 2D
- [ ] Mở `Source/Unet2D.ipynb` trên Colab
- [ ] Chạy Cell 1 (setup) → Cell 2 (writefile) → Cell 3 (train) — ~3–5h
- [ ] Chạy Cell test → lấy `results/unet2d_results.csv`
- [ ] Điền vào bảng Section 6: hàng U-Net 2D (N=187)

#### 1.2 Attention U-Net 2D
- [ ] Mở `Source/Attention_Unet2D.ipynb` trên Colab
- [ ] Chạy Cell setup → writefile → train — ~4–6h
- [ ] Chạy Cell test → lấy `results/attunet2d_results.csv`
- [ ] Điền vào bảng Section 6: hàng ATT-UNet 2D (N=187)

#### 1.3 PGA-UNet 2D
- [ ] Mở `Source/PGA_Unet2D.ipynb` trên Colab
- [ ] Chạy Cell 1 (setup + dataset) → Cell 2 (train) — ~6–10h
- [ ] Tải checkpoint lên Drive (Cell 15)
- [ ] Chạy Cell 9 (test 3 modes: zoom_out / shift / mixed_7_3)
- [ ] Lấy `results/pga_unet_expB_results.csv`
- [ ] Điền vào bảng Section 6: 3 hàng PGA (N=248)
- [ ] **Giữ lại 3 ảnh visualization** (IMG001768, IMG001538, IMG001100) để dùng trong báo cáo

#### 1.4 SAM-Med2D
- [ ] Mở `Source/Finetune_SAMMed2D_test_robust.ipynb` trên Colab
- [ ] **Phần 1 — Fine-tune:**
  - [ ] Cell 2–5: setup + download dataset `1fU7...`
  - [ ] **Cell 6: JSON → per-polygon masks** (bắt buộc chạy trước Cell 7)
  - [ ] Kiểm tra `dataset_BTXRD/train/masks/` có dạng `IMG_1.png` ✓
  - [ ] Cell 7: create_mapping_json (train=1859, val=211)
  - [ ] Cell 8–9: writefile train.py + build_sam.py
  - [ ] Cell 10: training ≤50 epochs (~4–7h)
  - [ ] Cell 11: lưu checkpoint lên Drive
- [ ] **Phần 2 — Test:**
  - [ ] Cell 14: create_evaluation_json (test=248) + load CHECKPOINT
  - [ ] Cell 15–16: writefile DataLoader.py + test.py
  - [ ] Cell 18: test zoom_out → `workdir/test_results/csv/sammed2d_zoom_out.csv`
  - [ ] Cell 20: test shift → `workdir/test_results/csv/sammed2d_shift.csv`
  - [ ] Cell 22: test mixed_7_3 → `workdir/test_results/csv/sammed2d_mixed_7_3.csv`
  - [ ] Cell 24: visualization 3 ảnh PGA → lưu `visualization_sammed_*.png`
- [ ] Điền vào bảng Section 6: 3 hàng SAMmed2D (N=248)

---

### Giai đoạn 2 — Hoàn thiện báo cáo Chapter 4

**File chính:** `Report/Chapter4/chapter4.tex`

- [ ] Điền số liệu thực vào `tab:baseline_comparison` (U-Net, ATT-UNet vs PGA zoom_out)
- [ ] Thêm bảng so sánh robust prompt: PGA vs SAMmed2D × 3 modes
- [ ] Thêm caption ghi chú: *"N=248 (PGA, SAMmed2D) vs N=187 (U-Net, ATT-UNet) — xem phân tích Section 2.4"*
- [ ] Normalize HD95 trong bảng: ghi cả `raw` và `/ img_size` cho SAMmed2D
- [ ] Chèn ảnh visualization (3 ảnh × 4 model) vào section qualitative
- [ ] Viết phân tích: **mixed_7_3 là giá trị chính** khi kết luận về hiệu năng thực tế PGA
- [ ] Viết đoạn so sánh PGA vs SAMmed2D: cùng paradigm, cùng 248 samples, lightweight vs heavy

**Lưu ý viết báo cáo:**
- Tránh so sánh trực tiếp Dice PGA vs Dice U-Net mà không ghi chú paradigm khác nhau
- Kết quả zoom_out = ceiling lý thuyết; mixed_7_3 = thực tế; shift = worst-case
- HD95 SAMmed2D ~2× nhỏ hơn do scale 256 vs 512 — cần normalize khi so sánh

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
- [ ] Kiểm tra Chapter 5 (kết luận) đồng bộ với kết quả thực
- [ ] Build PDF từ `Report/main.tex` → kiểm tra format
- [ ] Backup toàn bộ checkpoints lên Drive

---

### Tóm tắt thứ tự ưu tiên

```
[Ngay bây giờ]  Giai đoạn 1.3 PGA  →  1.4 SAMmed2D  →  1.1 UNet  →  1.2 AttUNet
[Sau khi có số] Giai đoạn 2 (Chapter 4)
[Nếu còn thời] Giai đoạn 3 (MedSAM zero-shot)
[Cuối cùng]    Giai đoạn 4 (chốt & nộp)
```

> **Bottleneck chính:** Thời gian training trên Colab T4 (~18–28h tổng cho 4 model).  
> Nên chạy song song nếu có 2 tài khoản Colab Pro, hoặc xếp hàng chạy qua đêm.
