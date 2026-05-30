# So Sánh Toàn Diện: PGA-UNet vs SAM-Med2D

> Dataset đánh giá: **BTXRD** (X-quang xương, Nature Scientific Data 2024)
> Task: Phân đoạn khối u xương với prompt do bác sĩ cung cấp

---

## 1. Tổng Quan

| | PGA-UNet (Ours) | SAM-Med2D |
|---|---|---|
| **Loại mô hình** | Lightweight CNN U-Net tùy chỉnh | Foundation model thích nghi y tế |
| **Xuất phát** | Thiết kế từ đầu cho bài toán này | Fine-tune từ SAM (Meta AI) |
| **Pretrained** | Không (train từ scratch) | Có (4M+ ảnh y tế) |
| **Mục tiêu thiết kế** | Prompt-guided segmentation nhẹ, nhanh | Interactive segmentation đa mục đích |

---

## 2. Kiến Trúc Mô Hình

### PGA-UNet

```
Input (512×512×1) + Prompt (512×512×1)
        │
 PromptSpatialGate ← encoder level 1 (16 ch)
        │                     ↓ MaxPool
 PromptSpatialGate ← encoder level 2 (32 ch)
        │                     ↓ MaxPool
 PromptSpatialGate ← encoder level 3 (64 ch)
        │                     ↓ MaxPool
 PromptSpatialGate ← encoder level 4 (128 ch)
        │                     ↓ MaxPool
                     center bottleneck (256 ch)
                              │
        PromptAttention → decoder level 4 + GridAttention
        PromptAttention → decoder level 3 + GridAttention
        PromptAttention → decoder level 2 + GridAttention
        PromptAttention → decoder level 1 + GridAttention
                              │
                     Output (512×512×1) sigmoid
```

- **Encoder**: 4 tầng `unetConv2` (2× Conv2d 3×3 + BatchNorm + ReLU mỗi tầng)
- **Bottleneck**: `unetConv2` tại chiều sâu nhất — dùng để hook GradCAM
- **Decoder**: 4 tầng `unetUp_PromptAttention` = ConvTranspose2d + Skip + GridAttentionBlock2D
- **PromptSpatialGate** (encoder, tùy chọn): `feat × (1 + α × gate(prompt))`, α learnable khởi tạo 0.1
- **GridAttentionBlock2D** (decoder): tính attention map từ gating signal (prompt-encoded) × skip features
- **Prompt encoding**: 2× Conv2d + InstanceNorm + ReLU → confidence map qua AdaptiveAvgPool2d
- **Final fusion**: `output += β × prompt_encoded`, β = 0.05

### SAM-Med2D

```
Input (256×256×3)
        │
  Image Encoder (ViT-B, frozen)
  ├─ 12 Transformer blocks
  ├─ Adapter module tại mỗi block (trainable)
  └─ Global attention tại layers [2, 5, 8, 11]
        │
  Image Embedding (16×16×256)
        │              ↑
  Prompt Encoder   Box/Point prompt
  ├─ Box → 2 corner embeddings
  ├─ Point → positional encoding + label embed
  └─ Dense prompt (prev mask) → conv
        │
  Mask Decoder (2-way Transformer, trainable)
  ├─ 2 layers cross-attention (tokens ↔ image)
  ├─ 3 mask output tokens (multimask)
  └─ IoU prediction head
        │
  Output: 3 masks (256×256) + IoU scores
  → chọn mask có IoU cao nhất
```

- **Adapter**: Linear down-proj (768→64) + GELU + Linear up-proj (64→768), thêm vào residual sau FFN
- **Prompt Encoder**: sinusoidal positional encoding cho tọa độ
- **Mask Decoder**: 2-way attention (image tokens attend to prompt tokens và ngược lại)

---

## 3. Số Lượng Tham Số

| | PGA-UNet | SAM-Med2D |
|---|---|---|
| **Tổng parameters** | ~4M | ~100M |
| **Trainable** | ~4M (100%) | ~12–17M (~13%) |
| **Frozen** | 0 | ~83M (ViT-B backbone) |
| **Trainable/MB** | ~15 MB | ~50–65 MB |
| **Pre-trained weight** | Không có | `sam_med2d.pth` (4M+ ảnh y tế) |

> PGA-UNet **nhỏ hơn 25×** về tổng số tham số, nhưng trainable gần nhau (~4M vs ~15M).

---

## 4. Input / Output

| | PGA-UNet | SAM-Med2D |
|---|---|---|
| **Image size** | 512×512 | 256×256 |
| **Image channels** | 1 (grayscale) | 3 (RGB, replicate gray) |
| **Prompt input** | Heatmap 512×512×1 | Box [x1,y1,x2,y2] hoặc Points [(x,y,label)] |
| **Output** | Binary mask 512×512 (sigmoid) | 3 masks 256×256 (logits) |
| **Post-processing** | sigmoid > 0.5 + LCC extraction | chọn mask max IoU + threshold > 0 |

---

## 5. Cơ Chế Prompt

### PGA-UNet — Plateau Heatmap
```
GT BBox → noisy BBox (zoom_out/shift) → Gaussian blur (kernel 31, σ≈10)
       → heatmap [0,1] cùng resolution với image (512×512)
       → đưa vào model cùng image (2-channel input)
```
- Prompt được xử lý **trong kiến trúc** tại cả encoder và decoder
- Thể hiện vùng quan tâm bằng giá trị xác suất liên tục
- Không phân biệt foreground/background

### SAM-Med2D — Box + Point Prompts
```
GT BBox → noisy BBox → 4 tọa độ [x1,y1,x2,y2]
       → Prompt Encoder → sparse embeddings
       → kết hợp với dense embeddings trong Mask Decoder
```
- Prompt được xử lý **tách biệt** trong Prompt Encoder
- Box prompt: 2 corner points (x_min,y_min), (x_max,y_max) + special token
- Point prompt (refinement): tọa độ + nhãn (1=fg, 0=bg)
- Có thể kết hợp box + point trong cùng một inference

---

## 6. Augmentation & Data Pipeline

### PGA-UNet
| Augmentation | Xác suất | Ghi chú |
|---|---|---|
| Horizontal Flip | 50% | Đồng bộ image + mask + prompt |
| Rotation ±15° | 50% | Đồng bộ image + mask + prompt |
| Zero prompt | 15% | Thay toàn bộ prompt = 0 (robustness) |
| Noisy prompt | 15% | Prompt += Gaussian noise × 0.1 |
| Noisy BBox | 100% | zoom_out [0.15–0.45] bất đối xứng |

### SAM-Med2D
| Augmentation | Ghi chú |
|---|---|
| Resize 256×256 | PadIfNeeded nếu nhỏ hơn, Resize nếu lớn hơn |
| Normalize | pixel_mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375] |
| Noisy BBox | zoom_ratio=[0.15,0.45] + shift_ratio=0.30 (thêm vào để fairness) |
| mask_num=5 | Mỗi ảnh lấy 5 mask ngẫu nhiên (với replacement) |

> Không có random flip/rotation trong `train_transforms` của SAM-Med2D gốc.

---

## 7. Loss Function

| | PGA-UNet | SAM-Med2D |
|---|---|---|
| **Loss** | BCE + Dice Loss | FocalDiceloss_IoULoss |
| **BCE** | Binary Cross-Entropy (pixel-wise) | Không dùng trực tiếp |
| **Dice** | Dice Loss (overlap-based) | Focal Dice (trọng số class imbalance) |
| **IoU** | Không có | IoU regression loss (decoder IoU head) |
| **Focal** | Không có | Áp dụng vào Dice để down-weight easy examples |
| **Mục tiêu** | Pixel accuracy + overlap | Overlap + localization quality |

---

## 8. Optimizer & Learning Rate

| | PGA-UNet | SAM-Med2D |
|---|---|---|
| **Optimizer** | AdamW | Adam |
| **Weight decay** | 1e-4 | Không rõ |
| **Learning rate** | 1e-4 | 1e-4 |
| **Scheduler** | ReduceLROnPlateau (factor=0.5, patience=5) | MultiStepLR (milestones=[5,10], γ=0.5) — optional |
| **Grad clip** | max_norm=1.0 | Không có |
| **Early stop** | patience=15 | patience=10 |
| **Max epochs** | 100 | 50 |
| **Batch size** | 4 | 2 |

---

## 9. Training Strategy

### PGA-UNet — End-to-End
```
Epoch 1..100:
  for batch in train_loader:
    output = model(image, prompt)      ← một forward pass
    loss = BCE(output, mask) + Dice(output, mask)
    loss.backward()
    optimizer.step()
  
  val_loss = evaluate(val_loader)
  if val_loss < best → save checkpoint
  scheduler.step(val_loss)
```
- Toàn bộ model train từ đầu, không freeze gì
- Val checkpoint dựa trên **validation loss** (hoặc val Dice)

### SAM-Med2D — Two-Stage per Batch
```
Epoch 1..50:
  for batch in train_loader:
    # Stage 1: Box/Point initial pass
    freeze(image_encoder.non_adapter)    ← chỉ adapter train
    pred_0 = model(image, box_or_point_prompt)
    loss_0.backward(); optimizer.step()
    
    # Stage 2: Iterative point refinement (iter_point=3)
    freeze(image_encoder)                ← encoder hoàn toàn frozen
    for iter in range(3):
      if iter == init_mask_num or last: clear_prompts()  ← mask-only pass
      pred_i = model(image, point_prompt_i)
      loss_i.backward(); optimizer.step()
      point_prompt_{i+1} = generate_point(pred_i, gt)
  
  val_dice = val_one_epoch(val_loader)   ← single-pass bbox inference
  if val_dice > best → save checkpoint
```
- Checkpoint dựa trên **validation Dice** (single-pass, không refinement)
- Training metrics (log ra) là từ **iteration cuối** (mask-only) → cao hơn thực tế

---

## 10. Inference & Refinement

### PGA-UNet — IPR (Iterative Prompt Refinement)
```
Inference:
  pred_0 = model(image, initial_prompt)     ← single pass
  
  IPR k=3:
    centroid_1 = centroid(pred_0)
    pred_1 = model(image, updated_prompt(centroid_1))
    centroid_2 = centroid(pred_1)
    pred_2 = model(image, updated_prompt(centroid_2))
    centroid_3 = centroid(pred_2)
    pred_3 = model(image, updated_prompt(centroid_3))   ← final
  
  GradCAM Rescue (dark background):
    if is_dark_bg AND pred<50px AND confidence<0.25:
      sal = GradCAM(model, zero_prompt)
      initial_prompt = rescue_box(sal.argmax())
      → chạy IPR từ vị trí GradCAM tìm được
```
- IPR cập nhật **tâm của prediction** làm điểm mới
- Model weight **không thay đổi** trong IPR — chỉ update prompt
- Thời gian inference: 1 + k = 4 forward passes

### SAM-Med2D — Single-Pass (tại test time)
```
Inference (test):
  pred = model(image, noisy_bbox)           ← single pass
  → chọn mask có IoU cao nhất (multimask)
  → threshold > 0 (sigmoid 0.5)
```
- Không dùng point refinement khi test (chỉ dùng trong training)
- 1 forward pass duy nhất
- Nhanh hơn PGA-UNet IPR (~4× forward passes)

---

## 11. Điều Kiện Đánh Giá (Fairness)

Để so sánh **công bằng** (chỉ khác biệt kiến trúc, không phải training strategy):

| Điều kiện | PGA-UNet | SAM-Med2D |
|---|---|---|
| **Dataset** | BTXRD (cùng) | BTXRD (cùng) |
| **Train prompt** | Noisy bbox zoom_out/shift | Noisy bbox zoom_out/shift (**đã thêm**) |
| **Test prompt** | zoom_out / shift / mixed_7_3 | zoom_out / shift / mixed_7_3 (cùng) |
| **Test protocol** | Single-pass | Single-pass |
| **Metrics** | Dice, IoU, Prec, Rec, HD95, CBL | Dice, IoU, Prec, Rec, HD95, CBL |
| **Image size** | 512×512 | 256×256 (khác nhau — inherent) |

> SAM-Med2D ban đầu fine-tune với **tight bbox** (gốc tác giả). Đã cập nhật sang **noisy bbox** để fair.

---

## 12. Bảng Tóm Tắt Tổng Hợp

| Khía cạnh | PGA-UNet | SAM-Med2D |
|---|---|---|
| **Kiến trúc** | CNN U-Net + Attention | ViT-B + Adapter |
| **Tham số tổng** | ~4M | ~100M |
| **Tham số train** | ~4M (100%) | ~15M (15%) |
| **Pretrained** | Không | Có (4M+ ảnh y tế) |
| **Image size** | 512×512 | 256×256 |
| **Prompt type** | Heatmap 2D liên tục | Box 4-coord + Point discrete |
| **Prompt tích hợp** | Trong kiến trúc (encoder+decoder) | Tách biệt (Prompt Encoder) |
| **Loss** | BCE + Dice | Focal Dice + IoU regression |
| **Optimizer** | AdamW + ReduceLROnPlateau | Adam + MultiStepLR |
| **Epochs** | 100 | 50 |
| **Augmentation** | HFlip + Rotation + prompt noise | Resize/Normalize only |
| **Training passes/sample** | 1 | 4 (1 init + 3 refinement) |
| **Checkpoint selection** | Val Dice | Val Dice (single-pass) |
| **Inference** | IPR k=3 (4 passes) | Single-pass |
| **GradCAM Rescue** | Có (dark background) | Không |
| **Speed (inference)** | ~4× SAM | 1× (baseline) |
| **Điểm mạnh** | Nhẹ, nhanh, IPR tự động | Pretrained mạnh, interactive |
| **Điểm yếu** | Train từ scratch, nhỏ | Nặng, input 256 (thông tin thấp hơn) |

---

*File tạo tự động từ phân tích source code — cập nhật lần cuối: 2026-05-30*
