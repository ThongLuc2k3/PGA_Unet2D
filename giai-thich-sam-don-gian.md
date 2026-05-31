# SAM & SAM-Med2D — Cách hoạt động (dành cho sinh viên ML)

---

## 1. SAM là gì và vì sao nó khác U-Net?

U-Net học từ dữ liệu có nhãn → chỉ phân đoạn đúng lớp vật thể nó đã thấy lúc train.  
SAM (Segment Anything Model — Meta AI, 2023) là **foundation model**: được train trên 1 tỷ mask từ 11 triệu ảnh thực tế → có thể phân đoạn **bất kỳ vật thể nào** chỉ cần người dùng chỉ ra qua **prompt** (điểm, hộp, hoặc mask thô).

Điểm khác biệt cốt lõi: SAM không học "đây là khối u", nó học **"đây là một vật thể tách biệt với nền"**.

---

## 2. Kiến trúc SAM — 3 thành phần

```
Ảnh đầu vào (1024×1024)
        │
        ▼
┌──────────────────┐
│  Image Encoder   │  ←── ViT-H/L/B (Vision Transformer)
│  (nặng, chạy 1   │       Trích xuất feature map toàn cảnh ảnh
│   lần duy nhất)  │       Ra: feature map 64×64×256
└────────┬─────────┘
         │
         │              Prompt (box / point / mask)
         │                      │
         ▼                      ▼
┌──────────────────────────────────────┐
│           Mask Decoder               │  ←── 2-way Transformer
│  (nhẹ, chạy lại mỗi lần có prompt)  │       Tokens từ prompt ↔ feature map
└──────────────────────────────────────┘
         │
         ▼
  3 mask ứng viên + 3 điểm IoU dự đoán
         │
         ▼
  Chọn mask có IoU cao nhất → Output
```

### Image Encoder (ViT)

Dùng Vision Transformer thay vì CNN. Ảnh được chia thành các **patch** 16×16, mỗi patch được biến thành một vector → Transformer xử lý toàn bộ các patch đồng thời thay vì quét cục bộ như CNN.

Ưu điểm: nắm được **ngữ cảnh toàn cục** (quan hệ giữa vùng xa nhau trong ảnh).  
Nhược điểm: rất nặng (~300M params cho ViT-H), chỉ chạy 1 lần và cache lại feature.

### Prompt Encoder

Biến đổi prompt thành vector (embedding) cùng chiều với feature map:
- **Bounding box**: 2 điểm góc → positional encoding (sinusoidal) + token đặc biệt "top-left corner" / "bottom-right corner"
- **Point**: tọa độ (x, y) → positional encoding + token "foreground" hoặc "background"
- **Mask thô**: downscale rồi dùng CNN nhỏ → embedding

### Mask Decoder

Dùng **2-way Transformer**: token của prompt attend vào feature ảnh, đồng thời feature ảnh attend ngược lại vào token prompt.

→ Kết quả: feature ảnh được "cập nhật" theo ngữ cảnh prompt → upscale thành 3 mask ứng viên.

Lý do có 3 mask: cùng một prompt có thể khớp nhiều diện tích (ví dụ: click vào tay người → có thể khoanh ngón tay, cả bàn tay, hoặc cả cánh tay). SAM trả về cả 3, dùng điểm IoU dự đoán để chọn hoặc để người dùng chọn.

---

## 3. SAM-Med2D — Fine-tune SAM cho ảnh y tế

SAM gốc train trên ảnh tự nhiên → feature của Image Encoder không phù hợp với ảnh y tế (X-quang, CT, MRI có phân phối pixel khác hoàn toàn).

**SAM-Med2D** (2023) fine-tune SAM trên **4.6 triệu ảnh y tế** từ nhiều phương thức (X-quang, CT, MRI, nội soi).

### Kỹ thuật Adapter (Parameter-Efficient Fine-Tuning)

Thay vì fine-tune toàn bộ ViT-B (~86M params) — tốn tài nguyên và dễ quên kiến thức cũ — SAM-Med2D **đóng băng** backbone và chèn thêm các **Adapter module** nhỏ vào sau mỗi block Transformer:

```
[ViT Block (frozen)] → [Adapter (trainable, ~1-2% params)] → tiếp tục
```

Mỗi Adapter là một bottleneck nhỏ: Linear ↓ (giảm chiều) → ReLU → Linear ↑ (tăng chiều lại). Chỉ học thêm đặc trưng y tế mà không phá vỡ kiến thức đã có.

**Kết quả:** chỉ cần train ~15M/100M tham số mà vẫn thích nghi tốt với ảnh y tế.

### Quy trình train của SAM-Med2D trên BTXRD (trong đề tài này)

```
Ảnh X-quang (256×256)  +  Bounding box (có nhiễu: zoom-out / shift)
        │
        ▼
Image Encoder (ViT-B + Adapters)  ──►  Feature map 16×16×256
        │
Prompt Encoder (box → 2 token góc)
        │
        ▼
Mask Decoder (2-way Transformer, trainable)
        │
        ▼
3 masks + 3 IoU scores → chọn mask tốt nhất → LCC extraction
        │
        ▼
Loss = FocalDice + IoU regression
```

**Lúc train**: dùng thêm **iterative point refinement** (`iter_point=3`) — sau mỗi bước dự đoán, lấy điểm sai (FP/FN) làm prompt bổ sung để cải thiện mask tiếp theo.

**Lúc test**: chỉ dùng bounding box một lần (không có iterative refinement).

---

## 4. Hạn chế của SAM-Med2D trên bài toán này

| Hạn chế | Nguyên nhân |
|---------|-------------|
| Ảnh đầu vào bắt buộc 256×256 | Position embedding của ViT-B được train ở 256, tăng lên 512 phải interpolate → mất thông tin chi tiết |
| Nặng (~100M params tổng) | ViT-B encoder rất lớn so với CNN tương đương |
| HD95 cao (52 px) | Độ phân giải 256 không đủ để bắt được đường biên nhỏ trên X-quang xương |
| Hội tụ nhanh nhưng ở mức thấp | Dừng ở epoch 12/50 với val Dice 0.773 — pretrained mạnh giúp hội tụ nhanh nhưng không đủ domain-specific |

---

## 5. So sánh với PGA-UNet (đề tài)

| | SAM-Med2D | PGA-UNet |
|---|---|---|
| Kiến trúc | ViT-B + Adapter (Transformer) | CNN U-Net + custom attention gate |
| Tham số | ~100M tổng, ~15M trainable | ~4M, 100% trainable |
| Ảnh đầu vào | 256×256 | 512×512 |
| Cách nhận prompt | Prompt Encoder riêng biệt (discrete coordinates) | Gaussian heatmap hòa vào encoder (continuous) |
| Tự tinh chỉnh lúc test | Không | Có (IPR 3 vòng) |
| Dice (zoom-out) | 0.762 | **0.866** |
| HD95 (zoom-out) | 52 px | **12 px** |

**Tại sao PGA vượt dù nhỏ hơn 25 lần?**  
SAM-Med2D là foundation model đa mục đích → tốt ở nhiều loại ảnh y tế nhưng không được tối ưu cho X-quang xương.  
PGA-UNet được thiết kế từ đầu cho bài toán này: prompt tích hợp sâu vào kiến trúc, ảnh độ phân giải cao hơn, và có IPR tự tinh chỉnh lúc inference.

---

## Tóm tắt luồng hoạt động SAM-Med2D (1 câu)

> **ViT-B đóng băng** trích xuất đặc trưng toàn cục → **Adapter** thêm kiến thức y tế → **Prompt Encoder** biến bounding box thành token → **2-way Transformer Decoder** kết hợp feature + prompt → xuất mask có IoU cao nhất.
