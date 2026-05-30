# Kế hoạch: Dọn 3 Folder Code + Align Notebooks + Cập nhật .md So Sánh

## Context

3 folder source code đúng (clone từ GitHub) được cung cấp. Cần:
1. Xóa file thừa không dùng đến trong mỗi folder
2. Đảm bảo notebook dùng đúng code từ 3 folder này
3. Cập nhật file `.md` so sánh PGA vs SAM-Med2D dựa trên code thực tế

**Folder → Notebook mapping:**

| Folder | Notebook |
|---|---|
| `Prompt-Guided-XRay-Segmentation-TN_B_ON/` | `PGA_Unet2D.ipynb` |
| `Prompt-Guided-XRay-Segmentation-Unet2D/` | `Unet2D.ipynb` |
| `Prompt-Guided-XRay-Segmentation-attention-unet2D/` | `Attention_Unet2D.ipynb` |

---

## Bước 1 — Làm sạch 3 folder ✅ HOÀN THÀNH

### Kết quả verify trước khi xóa

| File | Kế hoạch ban đầu | Thực tế sau verify | Kết quả |
|---|---|---|---|
| `TN_B_ON/models/networks_other.py` | Xóa | **GIỮ** — được import bởi `utils.py`, `grid_attention_layer.py`, `unet_2D.py` | Giữ |
| `TN_B_ON/models/layers/grid_attention_layer.py` | Không đề cập | **GIỮ** — import bởi `prompt_unet_2D.py` | Giữ |
| `Unet2D/models/networks_other.py` | Xóa | **GIỮ** — import bởi `unet_2D.py`, `utils.py` | Giữ |
| `Unet2D/models/layers/grid_attention_layer.py` | Xóa | Xác nhận xóa — `unet_2D.py` không import; `layers/__init__.py` import nó nhưng `train.py` không gọi `models.layers` | Đã xóa |
| `attention-unet2D/models/networks_other.py` | Xóa | **GIỮ** — import bởi `attention_unet_2D.py`, `utils.py`, `grid_attention_layer.py` | Giữ |
| `attention-unet2D/models/networks/unet_2D.py` | Xóa | **GIỮ** — `models/networks/__init__.py` làm `from .unet_2D import *` | Giữ |
| `attention-unet2D/models/layers/grid_attention_layer.py` | Xóa (sau verify) | **GIỮ** — import bởi `attention_unet_2D.py` | Giữ |

### Files đã xóa thực tế

**TN_B_ON:**
- [x] `app.py` — Gradio app, không dùng trong `PGA_Unet2D.ipynb`
- [x] `test_GradCAM.txt` — file text thử nghiệm
- [x] `test_show_zoom_shiff_mix.txt` — file text thử nghiệm

**Unet2D:**
- [x] `clean_data.py` — script tiền xử lý standalone, không gọi trong notebook
- [x] `models/layers/grid_attention_layer.py` — không ai import trong pipeline của folder này
- [x] `Train_Attention_Unet_data_Orig.ipynb` — notebook cũ, không phải notebook chính
- [x] `.gradio/` (thư mục) — artifact runtime, đã trong `.gitignore`

**attention-unet2D:**
- [x] `Train_Attention_Unet_data_Orig.ipynb` — notebook cũ, không phải notebook chính
- [x] `.gradio/` (thư mục) — artifact runtime, đã trong `.gitignore`

### Cấu trúc sạch sau bước 1

```
TN_B_ON/
├── dataset.py
├── train.py
├── models/
│   ├── networks_other.py       ← init_weights (dùng bởi utils, grid_attention, unet_2D)
│   ├── layers/
│   │   ├── grid_attention_layer.py  ← dùng bởi prompt_unet_2D
│   │   └── loss.py
│   └── networks/
│       ├── prompt_unet_2D.py   ← model chính PGA
│       ├── unet_2D.py
│       └── utils.py

Unet2D/
├── dataset.py
├── train.py
├── models/
│   ├── networks_other.py       ← init_weights
│   ├── layers/
│   │   └── loss.py
│   └── networks/
│       ├── unet_2D.py          ← model chính
│       └── utils.py

attention-unet2D/
├── dataset.py
├── train.py
├── models/
│   ├── networks_other.py       ← init_weights
│   ├── layers/
│   │   ├── grid_attention_layer.py  ← dùng bởi attention_unet_2D
│   │   └── loss.py
│   └── networks/
│       ├── attention_unet_2D.py ← model chính
│       ├── unet_2D.py           ← giữ vì __init__.py import nó
│       └── utils.py
```

---

## Bước 2 — Align 3 folder với notebook ✅ HOÀN THÀNH

### PGA_Unet2D.ipynb ↔ TN_B_ON — ✅ ALIGNED

- Clone `-b TN_B_ON` → `%cd Prompt-Guided-XRay-Segmentation` → `!python train.py`
- Dùng thẳng `train.py` từ repo, không có `%%writefile`
- Import `from dataset import BTXRD_Dataset`, `from models.networks.prompt_unet_2D import PGA_UNet` — khớp với files trong folder

---

### Unet2D.ipynb ↔ Unet2D — ⚠️ 3 BẤT NHẤT

**#1 — CRITICAL: `dataset_simple.py` không tồn tại**

Notebook Cell 2 (`%%writefile train_unet.py`) import:
```python
from dataset_simple import BTXRD_Dataset
```
Folder chỉ có `dataset.py` → **notebook sẽ crash `ModuleNotFoundError` khi chạy `!python train_unet.py` trên Colab**.

Cell 6 (test phase inline) dùng `from dataset import BTXRD_Dataset` — nhất quán với folder, nhưng khác với Cell 2.

> **Quyết định cần user:** Tạo `dataset_simple.py` trong repo Unet2D (bản copy/đơn giản hóa của `dataset.py`)?

**#2 — MAJOR: `train.py` trong folder là phiên bản cũ, không được dùng**

Notebook viết `train_unet.py` riêng qua `%%writefile`. Folder's `train.py` là version cũ với config khác hẳn:

| | Notebook (`%%writefile`) | Folder `train.py` |
|---|---|---|
| `BATCH_SIZE` | 4 | 8 |
| `EPOCHS` | 100 | 50 |
| `IMG_SIZE` | 512 | 256 |
| `WEIGHT_DECAY` | 1e-4 | không có |
| `Scheduler` | ReduceLROnPlateau(mode='max') | không có |
| `Gradient clip` | max_norm=1.0 | không có |
| `Early stopping` | patience=15 | không có |
| Checkpoint tên | `unet_best.pth` | `att_unet_last.pth` (SAI tên) |

> **Quyết định cần user:** Cập nhật `train.py` trong folder Unet2D bằng nội dung `%%writefile` từ notebook?

**#3 — MINOR: Augmentation trong `dataset.py` khác notebook cũ**

`Unet2D/dataset.py` có augmentation mạnh (HFlip + Rotation + Affine + Brightness). `attention-unet2D/dataset.py` chỉ có HFlip đơn giản. Cả hai đều thiếu `dataset_simple.py`.

---

### Attention_Unet2D.ipynb ↔ attention-unet2D — ⚠️ 2 BẤT NHẤT

**#1 — CRITICAL: `dataset_simple.py` không tồn tại** (giống Unet2D)

Cell 2 (`%%writefile train_attunet.py`) và Cell 7 (test phase) đều dùng `from dataset_simple import BTXRD_Dataset` → **crash trên Colab**.

> **Quyết định cần user:** Tạo `dataset_simple.py` trong repo attention-unet2D?

**#2 — MAJOR: `train.py` trong folder là phiên bản cũ** (giống Unet2D — cùng file cũ)

Cùng diff pattern: Batch=8/Epochs=50/IMG_SIZE=256, không có scheduler/early stopping, checkpoint lưu sai tên `att_unet_last.pth`.

> **Quyết định cần user:** Cập nhật `train.py` trong folder attention-unet2D bằng nội dung `%%writefile`?

---

### Hành động đã thực hiện

| # | Vấn đề phát hiện | Action |
|---|---|---|
| 1 | `dataset_simple.py` thiếu trong Unet2D + attention-unet2D | ✅ Copy từ `Source/project/dataset_simple.py` vào cả 2 folder |
| 2 | `train.py` trong 2 folder là phiên bản cũ (Batch=8, Epochs=50, IMG_SIZE=256, không có scheduler) | ✅ Ghi đè bằng nội dung `%%writefile` từ notebook (Batch=4, Epochs=100, IMG_SIZE=512, có ReduceLROnPlateau + grad clip + early stopping) |

> ✅ Đã sửa thêm: Cell 6 test phase trong `Source/Unet2D.ipynb` đổi `from dataset import` → `from dataset_simple import` cho nhất quán với train cell.

---

## Bước 3 — Cập nhật `docs/comparison_PGA_vs_SAMMed2D.md` ✅ HOÀN THÀNH

Re-verify từ `TN_B_ON/train.py`, `dataset.py`, `models/networks/prompt_unet_2D.py`:

- [x] Loss: `BCEWithLogitsLoss + DiceLoss` ✅ khớp
- [x] Optimizer: AdamW, weight_decay=1e-4 ✅ khớp
- [x] Scheduler: `ReduceLROnPlateau(mode='max', factor=0.5, patience=5)` ✅ khớp
- [x] Grad clip: max_norm=1.0 ✅ khớp
- [x] Early stop: patience=15 ✅ khớp
- [x] Augmentation: HFlip 50% + Rotation ±15° 50% + Zero prompt 15% + Noisy prompt 15% ✅ khớp
- [x] Architecture: filters [16,32,64,128,256], PromptSpatialGate encoder, GridAttentionBlock2D decoder, β=0.05 ✅ khớp
- [x] **Sửa lỗi**: `σ≈10` → `σ≈5` trong Section 5 (GaussianBlur kernel=31 → σ = 0.3×14 + 0.8 = 5.0)

---

## Verification Checklist

- [x] Mỗi folder chỉ còn files được dùng bởi notebook tương ứng
- [x] `!python train.py` trong mỗi notebook chạy được với code trong folder
- [x] Import statements trong notebook khớp hoàn toàn với files trong folder
- [x] `.md` comparison chính xác với code trong `TN_B_ON/`
