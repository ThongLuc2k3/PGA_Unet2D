# Danh sách việc cần sửa báo cáo KLTN

> Review toàn bộ 87 trang PDF. Ưu tiên từ cao xuống thấp.

---

## 🔴 KHẨN CẤP — Bắt buộc sửa trước khi nộp

### 1. Thêm Lời cam đoan *(bắt buộc theo quy định ĐHKHTN)*
- **Vấn đề:** `main.tex` dòng 152–153 đang comment out:
  ```latex
  %\addcontentsline{toc}{chapter}{Lời cam đoan}
  %\include{Appendix/reassurances}
  ```
- **Sửa:** Bỏ comment 2 dòng trên. File `Appendix/reassurances.tex` đã có sẵn.

---

### 2. Xóa viền đỏ hyperlink trong mục lục / danh sách hình / bảng
- **Vấn đề:** Toàn bộ mục lục, danh sách hình, danh sách bảng có viền đỏ bao quanh từng mục — do hyperlink chưa ẩn màu. Trông rất mất thẩm mỹ khi in và nộp.
- **Sửa:** Thêm vào `main.tex` (sau phần khai báo `\usepackage[unicode]{hyperref}`):
  ```latex
  \hypersetup{hidelinks}
  ```

---

### 3. Fix trang 27 gần như trắng hoàn toàn
- **Vấn đề:** Câu `"sáng của ký tự R/L là tổn thương xương."` nằm đơn độc ở đầu trang 27, phần còn lại trắng. Nguyên nhân: có `\clearpage` hoặc `\FloatBarrier` thừa trong `Chapter3/chapter3.tex` sau đoạn mô tả Lưu ý R/L.
- **Sửa:** Tìm và xóa `\clearpage` / `\newpage` / `\FloatBarrier` thừa trong section 3.2.2 của `Chapter3/chapter3.tex`.

---

### 4. Thống nhất tháng trên trang bìa và lời cảm ơn
- **Vấn đề:**
  - Trang bìa: `tháng 07/2026`
  - Lời cảm ơn (`Appendix/thanks.tex`): `tháng 6 năm 2026`
- **Sửa:** Chọn một tháng thống nhất (tháng 6 hoặc 7) rồi sửa cả hai nơi.

---

### 5. *(Đã sửa)* Đề cương — Bỏ so sánh với Attention U-Net
- **Trạng thái:** ✅ Đã sửa trong `Appendix/decuong.tex` dòng 74 và 85.
- **Lý do:** Attention U-Net được kế thừa kiến trúc (CAD mở rộng từ Attention Gate), không phải là mô hình đối sánh trong thực nghiệm.

---

## 🟠 QUAN TRỌNG — Ảnh hưởng đến điểm đánh giá học thuật

### 6. Tài liệu tham khảo quá ít (chỉ 8 tài liệu)
- **Vấn đề:** KLTN chuẩn cần 20–30+ tài liệu. Hiện tại:
  - `[1]` là website bệnh viện (không phải công trình khoa học)
  - `[2]` SAM-Med2D là arXiv preprint, chưa peer-reviewed
  - `[3]`, `[4]` là website tool (Roboflow, YOLO)
- **Cần bổ sung (gợi ý):**
  - SAM gốc (Kirillov et al., 2023, ICCV)
  - MedSAM (Ma et al., 2024)
  - nnU-Net (Isensee et al., 2021, Nature Methods)
  - TransUNet (Chen et al., 2021)
  - SwinUNet (Cao et al., 2022)
  - Survey về medical image segmentation
  - Survey về interactive segmentation
  - Các bài báo về bone tumor detection/segmentation
  - PACS system references
  - Các bài báo về prompt-based learning in computer vision

---

### 7. Thiếu kiểm định thống kê (Statistical Significance Test)
- **Vấn đề:** Mục 4.3.2 tự nhắc "kiểm định Wilcoxon signed-rank là bước được khuyến nghị" nhưng **không thực hiện và không báo cáo p-value** nào. Không có p-value thì kết luận "vượt trội" không có cơ sở thống kê.
- **Sửa:** Chạy Wilcoxon signed-rank test (phi tham số) trên 232 giá trị Dice per-polygon cho các cặp so sánh chính:
  - PGA-UNet (V5) vs V4 (Binary prompt)
  - PGA-UNet vs U-Net
  - PGA-UNet vs SAM-Med2D FT
  - Báo cáo p-value trong Bảng 4.7 hoặc text phân tích.

---

### 8. Thiếu đường cong huấn luyện (Training Curves)
- **Vấn đề:** Không có biểu đồ Loss/Dice theo epoch. Đây là hình cơ bản trong mọi báo cáo deep learning — xác nhận mô hình hội tụ ổn định, không overfit.
- **Sửa:** Thêm vào Section 4.1.2 hoặc 4.2 một figure gồm:
  - Train Loss vs Val Loss theo epoch (PGA-UNet)
  - Train Dice vs Val Dice theo epoch (PGA-UNet)
  - Có thể thêm U-Net để so sánh tốc độ hội tụ.

---

### 9. Section 4.4 Qualitative Results quá nghèo
- **Vấn đề:** Chỉ có **1 hình duy nhất** (Hình 4.1, 8 ảnh nhỏ khó đọc). Một hội đồng sẽ yêu cầu nhiều ví dụ hơn.
- **Sửa:** Thêm ít nhất 2 hình nữa:
  - Hình 4.2: So sánh trực quan PGA-UNet vs U-Net trên nhóm **Khó** (tổn thương nhỏ / biên giới mờ)
  - Hình 4.3: Failure cases — 3–4 trường hợp PGA-UNet dự đoán kém, kèm chú thích lý do

---

### 10. Thêm Abstract tiếng Anh
- **Vấn đề:** Trang đề cương đã có tiêu đề tiếng Anh nhưng `Appendix/tomtat.tex` chỉ có tiếng Việt. Báo cáo khoa học chuẩn cần cả 2 ngôn ngữ.
- **Sửa:** Thêm phần "Abstract" tiếng Anh vào `Appendix/tomtat.tex`, ngay sau phần tiếng Việt, có cùng cấu trúc: Problem / Solution / Results / Keywords.

---

## 🟡 NÊN SỬA — Cải thiện chất lượng tổng thể

### 11. Phần 2.1 Related Work quá ngắn
- **Vấn đề:** Chỉ đề cập 2 mô hình (U-Net, Attention U-Net) + SAM-Med2D trong 1.5 trang. Hội đồng thường hỏi về bức tranh tổng quan.
- **Sửa:** Mở rộng Section 2.1 thêm ít nhất:
  - nnU-Net (self-configuring, SOTA trên nhiều benchmark y tế)
  - TransUNet / SwinUNet (hybrid CNN-Transformer)
  - MedSAM, SEEM (các foundation model interactive khác)
  - Kết thúc bằng bảng tóm tắt so sánh các công trình liên quan.

---

### 12. Thiếu hình minh họa tiền xử lý (Section 3.2)
- **Vấn đề:** Mô tả quy trình xóa nhiễu R/L rất chi tiết nhưng không có ảnh ví dụ before/after. Khó thuyết phục hội đồng về hiệu quả tiền xử lý.
- **Sửa:** Thêm Hình 3.2b (hoặc thay thế Hình 3.2 hiện tại bằng một figure kết hợp flowchart + ví dụ ảnh) gồm:
  - 2 ảnh gốc chứa ký tự R/L
  - 2 ảnh tương ứng sau khi xóa nhiễu

---

### 13. Các trang trắng không cần thiết
- **Vấn đề:** Trang 8, 21, 39, 63, 69 — nội dung kết thúc rất sớm, phần còn lại của trang hoàn toàn trắng. Không nghiêm trọng nhưng trông thiếu chuyên nghiệp.
- **Sửa:** Kiểm tra và xóa `\clearpage` / `\newpage` thừa ở cuối các section tương ứng trong:
  - `Chapter1/chapter1.tex` (trang 8)
  - `Chapter2/chapter2.tex` (trang 21)
  - `Chapter3/chapter3.tex` (trang 39)
  - `Chapter4/chapter4.tex` (trang 63)
  - `Chapter5/chapter5.tex` (trang 69)

---

### 14. Thêm Phụ lục (Appendix)
- **Vấn đề:** `main.tex` dòng 197–198 có appendix bị comment out hoàn toàn. Không có phụ lục nào trong báo cáo.
- **Sửa (tối thiểu):** Thêm vào `Appendix/appendix1.tex`:
  - Bảng hyperparameters đầy đủ của tất cả mô hình (PGA-UNet, U-Net, EfficientNet_B3)
  - Thêm visualization kết quả bổ sung (10–15 ảnh) nếu còn chỗ

---

### 15. Hình ablation study thiếu trực quan hóa
- **Vấn đề:** Bảng 4.7 (Ablation) chỉ có số, không có hình so sánh trực quan V1 vs V5. Kết quả sẽ thuyết phục hơn nhiều nếu có hình side-by-side.
- **Sửa:** Thêm 1 figure trong Section 4.3.1 so sánh mask phân đoạn của V1 (concat heatmap đơn giản) vs V5 (PSG+CAD+Gaussian) trên cùng 1 ca ảnh, đặc biệt kịch bản Shift.

---

## Ghi chú từ review GVHD trước (giữ lại)

Phải tự kiểm tra báo cáo ít nhất 10 lần
1. Đóng góp
Xác định đóng góp: đóng góp gì (final solution)? Phần nào là kế thừa, phần nào là tự phát triển (sử dụng visual prompt ko phải là đóng góp).
Xác định đối tượng end user: bác sĩ đọc ảnh (đã xác định)
2 module phân đoạn Image Encoder, Mask Decoder thì có kế thừa/cải tiến cải lùi gì
Làm rõ kiến trúc khối mã hóa và hòa trộn: Giải thích sâu về kỹ thuật trong cách thức hoạt động của Image Encoder, Prompt Encoder, kỹ thuật xử lý để huyện prompt và encoder/decoder với nhau. Attention ở đây là trên ảnh hay prompt hay gì?
Nhấn mạnh kỹ thuật mã hóa visual prompt (kế thừa hay cải tiến từ đâu): giải thích từng kiểu prompt (heatmap vs binary(token)), giải thích lý do chọn heatmap, so sánh bản chất của 2 kỹ thuật này. Nói rõ đóng góp này trong chương 3 và khi nói là đóng góp thì sẽ bị soi xuống phần thực nghiệm để minh chứng
Giải thích hàm loss có thay đổi gì không khi có thêm visual prompt trong giai đoạn học không
Thực nghiệm phải luôn có minh chứng cho phần đóng góp

2. Về ảnh đầu vào
Về vấn đề resize ảnh thì có 2 hướng:
Hướng 1 (không resize): Thử nghiệm dùng kiến trúc Swin Transformer để chia ảnh thành các patch nhỏ
Hướng 2: Nếu phải resize, cần chứng minh rằng dù ảnh bị scale nhỏ nhưng khi có visual prompt hỗ trợ thì hiệu suất phân đoạn được kéo lại đáng kể

3. Quy trình pipeline
Nâng chỉ số Gatekeeper
Cần bổ sung phần thảo luận và chuẩn bị câu trả lời phản biện cho hai tình huống thực tế sau:
Bác sĩ không vẽ, không đưa bất kỳ gợi ý nào (prompt rỗng) thì hệ thống xử lý ra sao?
Bác sĩ nhận thức sai, vẽ bbox lệch tâm hoặc sai hoàn toàn vị trí thì hệ thống vận hành ra sao?
⇒ Phải đưa ra thêm các lý luận để giải thích thỏa đáng 

4. Sửa đổi thực nghiệm và đánh giá so sánh
Mọi tuyên bố cải tiến kỹ thuật (như việc thay đổi cách mã hóa từ binary sang heatmap) đều phải có số liệu thực nghiệm đối chứng trực tiếp để chứng minh tính hiệu quả
Đảm bảo tính công bằng:
Với unet và att unet thì đừng dùng từ so sánh hay lý luận như thế nào đó
Nói rõ về mẫu theo ảnh và mẫu theo GT
Kết quả tốt là do prompt hay do kiến trúc
Att unet chưa tối ưu
So sánh với sam-med2d cần cùng kích thước 256x256

5. Tiền xử lý dữ liệu
Cần nói rõ là việc xóa chữ R/L, văn bản thông tin bệnh nhân trên ảnh x quang là chỉ nằm trong phạm vi cho mô hình học đặc trưng. Trên giao diện làm việc thực tế thì vẫn hiển thị những thông tin đó.

---

# CODE REVIEW TOÀN BỘ — PGA_Unet2D

> Review thực hiện ngày 2026-06-23. Phủ toàn bộ source code Python trong dự án.

---

## 1. Kiến trúc tổng thể

```
Source/Prompt-Guided-XRay-Segmentation/
├── dataset.py                          ← BTXRD_Dataset
├── train.py                            ← training loop
├── models/
│   ├── __init__.py                     ← EMPTY (1 dòng trắng)
│   ├── networks_other.py               ← legacy GAN utilities (KHÔNG DÙNG)
│   ├── networks/
│   │   ├── __init__.py                 ← legacy factory + import unet_2D (BUG)
│   │   └── prompt_unet_2D.py           ← CORE: PGA-UNet, PSG, CAD
│   └── layers/
│       ├── __init__.py                 ← re-export grid_attention_layer
│       └── grid_attention_layer.py     ← GridAttentionBlock2D (có bugs)
thuyết trình/
├── manim_01_prompt_encoding.py         ← animation Gaussian Plateau
├── manim_02_psg_encoder.py             ← animation PSG
└── manim_03_cad_decoder.py             ← animation CAD
```

---

## 2. `prompt_unet_2D.py` — Core Architecture

**Đánh giá: TỐT. Thiết kế sạch, tư duy rõ ràng.**

### 2.1 `PromptSpatialGate` (PSG)

```python
# Công thức: features * (1 + clamp(alpha, 0, 1) * sigmoid(conv1x1(prompt)))
gate_conv = Conv2d(1 → C, k=1) + Sigmoid
alpha     = Parameter(0.1)  # learnable, clamp [0,1]
forward:  features * (1.0 + clamp(alpha, 0, 1) * gate_conv(prompt))
```

**Tốt:**
- Dùng `(1 + alpha * gate)` thay vì chỉ `gate` → đảm bảo `output >= input`, chỉ khuếch đại không tắt tín hiệu
- `clamp(alpha, 0, 1)` ngăn alpha âm (gây triệt tín hiệu)
- Khởi tạo alpha=0.1 nhỏ → gating yếu ban đầu, gradient dần hội tụ

**Vấn đề nhỏ:**
- Không có `register_buffer` hay note về việc prompt được resize ra sao trước khi vào PSG → phụ thuộc F.interpolate trong forward của PGA_UNet (cần kiểm tra)

---

### 2.2 `unetUp_PromptAttention` (CAD — Conditioned Attention Decoder)

```python
alpha_raw  = Parameter(-0.84)   # sigmoid(-0.84) ≈ 0.30
beta       = Parameter(0.05)    # output residual
w          = prompt_weight      # float, varies per level: 1.0 / 0.7 / 0.4 / 0.2
skip_att + 0.3 * skip           # residual hardcode 0.3 — không học được!
```

**Tốt:**
- `confidence = AdaptiveAvgPool + Conv1x1 + Sigmoid` → global context từ prompt
- Prompt encoder: 2×(Conv3x3 + InstanceNorm + ReLU) → biến đổi phi tuyến trước khi hòa trộn
- `g_fused = gating + conf * sigmoid(alpha_raw) * w * p_encoded` → điều chỉnh gating bằng confidence
- `beta=0.05` residual nhỏ tránh over-correction

**Vấn đề:**
- **Line ~92: `skip_att + 0.3 * skip` — hardcode 0.3**. Đây là skip residual cố định, không học được. Có thể cần tune nếu muốn kiến trúc linh hoạt hơn. Không gây bug nhưng là design choice cứng.
- `prompt_weights=(1.0, 0.7, 0.4, 0.2)` theo thứ tự decoder từ sâu lên nông — hợp lý (tầng sâu cần prompt nhiều hơn), nhưng các giá trị này là hyperparameter cứng, không học.

---

### 2.3 `PGA_UNet`

```python
filters = [16, 32, 64, 128, 256]  # với feature_scale=4
pg1..pg4  = PromptSpatialGate      # 4 PSG tại encoder
up1..up4  = unetUp_PromptAttention # 4 CAD tại decoder
```

**Tốt:**
- `use_encoder_prompt=True` flag cho phép tắt PSG để thử nghiệm ablation → sạch
- Training augmentation trong `forward()`:
  ```python
  if r < 0.15: prompt = zeros(...)     # 15% prompt rỗng (zero-prompt robustness)
  elif r < 0.30: prompt += noise(...)  # 15% prompt nhiễu (noise robustness)
  ```
  → Đây là kỹ thuật quan trọng, tương tự dropout nhưng trên prompt
- Resize heatmap về từng resolution encoder trong forward: `F.interpolate(prompt, size=...)` tại mỗi tầng

**Vấn đề nhỏ:**
- Training augmentation (zero/noisy prompt) chỉ chạy khi `self.training` — nhưng không dùng `if self.training:` explicit, dùng `if self.training` ẩn trong điều kiện random → cần xác nhận không leak sang eval mode
- Không có comment giải thích tại sao chọn threshold 0.15 / 0.30 → magic numbers

---

## 3. `grid_attention_layer.py` — GridAttentionBlock2D

**Đánh giá: CÓ BUGS. File legacy, cần chú ý.**

### 3.1 Bugs xác nhận

| # | Vị trí | Vấn đề | Mức độ |
|---|--------|---------|--------|
| B1 | `_GridAttentionBlockND.__init__` | `raise NotImplemented` → phải là `raise NotImplementedError()` | **CRITICAL** (sẽ raise TypeError nếu gọi) |
| B2 | `_GridAttentionBlockND.forward` | `F.sigmoid(...)` → deprecated, dùng `torch.sigmoid(...)` | WARNING |
| B3 | `_GridAttentionBlockND_TORR.__init__` | `nn.init.constant(...)` → deprecated, dùng `nn.init.constant_(...)` | WARNING |
| B4 | `_GridAttentionBlockND_TORR.forward` | `parallel = False` dead code block không bao giờ chạy | DEAD CODE |
| B5 | Bottom of file | `if __name__ == '__main__':` test code | MINOR (không hại) |

**B1 chi tiết:** `raise NotImplemented` → Python sẽ raise `TypeError: exceptions must derive from BaseException` vì `NotImplemented` là built-in hằng số (dùng trong `__eq__` etc.), không phải exception. Nếu class này bị gọi trực tiếp, sẽ crash theo cách khó debug.

### 3.2 Thiết kế

- `GridAttentionBlock2D` dùng `concatenation` mode: `θ(x) + φ(g) → ReLU → ψ → Sigmoid`
- Đây là Attention Gate chuẩn từ paper Attention U-Net (Oktay et al., 2018)
- PGA-UNet kế thừa pattern này cho CAD (Conditioned Attention Decoder)

---

## 4. `networks_other.py` — Legacy GAN Utilities

**Đánh giá: FILE LEGACY, KHÔNG DÙNG. Nhiều deprecated APIs.**

### 4.1 Deprecated APIs (toàn bộ file)

```python
# Tất cả cần thêm dấu _ (underscore):
init.normal(...)          → init.normal_(...)
init.xavier_normal(...)   → init.xavier_normal_(...)
init.orthogonal(...)      → init.orthogonal_(...)
init.constant(...)        → init.constant_(...)
```

### 4.2 Bug nghiêm trọng

```python
# Dòng 137:
return NotImplementedError('learning rate policy [%s] is not implemented', opt.lr_policy)
# Bug: trả về Error object thay vì raise! Caller nhận về một Exception object
# nhưng không biết đó là lỗi → silent failure
```

### 4.3 Deprecated patterns

```python
from torch.autograd import Variable   # Không cần từ PyTorch >= 0.4
nn.parallel.data_parallel(...)         # Deprecated, dùng nn.DataParallel
```

### 4.4 Classes không dùng

- `GANLoss`, `ResnetGenerator`, `ResnetBlock`, `UnetGenerator`, `UnetSkipConnectionBlock`, `NLayerDiscriminator` → toàn bộ là GAN infrastructure từ pix2pix, không tham chiếu trong bất kỳ notebook hay train script nào của project.
- File này là legacy code, nên giữ riêng hoặc xóa để tránh nhầm lẫn.

---

## 5. `models/networks/__init__.py` — Legacy Factory

**Đánh giá: CÓ BUG IMPORT, DEAD CODE.**

```python
# Dòng 1: BUG NGHIÊM TRỌNG
from .unet_2D import *
# File unet_2D.py KHÔNG TỒN TẠI trong codebase hiện tại
# → Nếu ai import models.networks sẽ nhận ImportError ngay lập tức
```

```python
# Dòng 44: Bug logic
raise 'Model {} not available'.format(name)
# Raise một string thay vì Exception → TypeError
# Chuẩn: raise ValueError('Model {} not available'.format(name))
```

- Toàn bộ factory `get_network()` và `_get_model_instance()` không được gọi bởi `train.py` hay bất kỳ notebook nào → dead code cho project hiện tại

---

## 6. `dataset.py` — BTXRD_Dataset

**Đánh giá: XUẤT SẮC. Code sạch, đúng, tư duy kỹ.**

### 6.1 Điểm mạnh

- **Synchronized augmentation:** `hflip` và `rotate` áp dụng đồng bộ lên `image`, `mask`, `prompt` → đúng tuyệt đối
- **INTER_NEAREST** cho mask resize → bảo toàn giá trị nhị phân ✓
- **Plateau heatmap:** fill 1.0 trong bbox + GaussianBlur(31,31) → gradient mềm tại viền, tâm ≈1.0 tự nhiên khi bbox đủ lớn ✓
- **Test-time determinism:** `_shift_bbox` dùng `random.Random(seed_idx)` → reproducible ✓
- **Mixed_7_3 test:** `idx % 10 >= 7` → 30% shift, 70% zoom_out, deterministic ✓
- **Normalization:** `(/ 255 - 0.5) / 0.5` → range [-1, 1] ✓

### 6.2 Điểm cần lưu ý

- **`_shift_bbox` test-time** (line 81-82):
  ```python
  dx = rng.uniform(gt_w * 0.4, gt_w * 0.7) * self.shift_ratio
  dy = rng.uniform(gt_h * 0.1, gt_h * 0.3) * self.shift_ratio
  ```
  Shift test-time luôn dương (dx > 0, dy > 0) → bbox luôn lệch về phía dưới-phải. Train-time ngẫu nhiên cả chiều âm lẫn dương. Đây là intentional (để deterministic) nhưng tạo asymmetry có thể ảnh hưởng tính đại diện.

- **Không có error handling** nếu `image` là `None` (cv2.imread thất bại) → sẽ crash với `AttributeError: 'NoneType' object` tại `image.shape`. Trong thực tế không ảnh hưởng nếu dataset clean.

- **JSON re-open mỗi sample**: `__getitem__` mở JSON 2 lần (lần đầu trong `__init__` chỉ đếm polygon, lần 2 trong `__getitem__` để đọc points). Tối ưu hơn nếu cache toàn bộ JSON data trong `__init__`, nhưng không ảnh hưởng correctness.

---

## 7. `train.py` — Training Loop

**Đánh giá: TỐT. Training loop đúng và đủ.**

### 7.1 Điểm mạnh

- **Loss = BCEWithLogitsLoss + DiceLoss:** kết hợp chuẩn cho segmentation ✓
- **Gradient clipping max_norm=1.0:** ổn định training ✓
- **AdamW + weight_decay=1e-4:** phòng overfitting ✓
- **ReduceLROnPlateau (mode='max', factor=0.5, patience=5):** giảm LR khi Dice plateau ✓
- **Early stopping patience=15:** hợp lý ✓
- **Save best + last checkpoint:** đúng ✓
- **Validation trên 3 loaders** (Exp B): đánh giá robustness Zoom/Shift/Mixed đồng thời ✓

### 7.2 CBL Metric (Center-Based Localization)

```python
cbl = clamp(1 - dist(centroid_pred, centroid_gt) / diag_gt, min=0)
```

- Metric custom đo vị trí trung tâm predicted mask so với GT
- Scale-invariant (chuẩn hóa theo đường chéo bbox GT)
- **Tốt:** `if gt_area < smooth: continue` bỏ qua mẫu GT rỗng ✓
- **Vấn đề nhỏ:** CBL chỉ measure centroid localization, không capture shape. Không được báo cáo trong paper cuối — chỉ dùng monitor training. OK.

### 7.3 `batch_metrics_sum`

```python
return dice.sum(), iou.sum(), precision.sum(), recall.sum()  # trả SUM qua batch
# Chia cho n_total bên ngoài → macro-average per-sample ✓
```

Đúng. Không dùng reduce='mean' trong hàm để có thể tích lũy đúng qua nhiều batch.

### 7.4 Vấn đề nhỏ

- **`EXPERIMENT = 'B'`** (mixed_7_3) là config mặc định — không có validation rằng 'B' vs 'A' mapping đúng với checkpoint names. Comment giải thích 'A' → 'B' là đủ.
- **`num_workers=2`** cố định — có thể bottleneck trên máy nhiều CPU. Không critical.
- **Emoji 🥇 trong logger** có thể gây UnicodeEncodeError trên Windows với encoding CP1252. Trên Linux/WSL OK.

---

## 8. Manim Scripts (Presentation Animations)

**Đánh giá: CHẤT LƯỢNG CAO. Tư duy sư phạm tốt.**

### 8.1 `manim_01_prompt_encoding.py`

- Chính xác mô tả pipeline: BBox → Binary → GaussianBlur → Plateau Heatmap
- **Quan trọng:** có comment inline `# Code thực KHÔNG có bước max(blur,binary)` → phân biệt rõ "minh họa 6x6" vs "code thực 31x31 tự nhiên plateau"
- Dữ liệu minh họa (6x6 grid) nhất quán với code thực
- Pipeline text: `BBox → Binary Mask → Gaussian Blur → Plateau → Heatmap` — chính xác

### 8.2 `manim_02_psg_encoder.py`

- Công thức hiển thị: `x̃ = x × (1 + α × gate)` → khớp code
- Chú thích rõ `VÍ DỤ — code dùng 31×31, σ≈5px`; `α = 1.0 (VÍ DỤ sau huấn luyện)` → tránh mislead
- Minh họa tổn thương vs nhiễu: tổn thương trong bbox được khuếch đại, nhiễu ngoài bbox giữ nguyên — đúng tinh thần PSG

### 8.3 `manim_03_cad_decoder.py`

- So sánh `ATTN_NO_HM` vs `ATTN_CAD`: nhiễu (3,3) giảm từ 0.63 → 0.18 khi có heatmap
- Dữ liệu minh họa nhất quán với logic CAD

**Vấn đề nhỏ:** Tất cả 3 file dùng `from manim import *` → namespace pollution, nhưng đây là convention của Manim.

---

## 9. Tổng kết: Bug cần sửa (nếu triển khai production)

| # | File | Vấn đề | Priority |
|---|------|---------|----------|
| 1 | `grid_attention_layer.py` | `raise NotImplemented` → `raise NotImplementedError()` | HIGH |
| 2 | `models/networks/__init__.py` | `from .unet_2D import *` — file không tồn tại | HIGH (ImportError) |
| 3 | `models/networks/__init__.py` | `raise 'Model...'` → `raise ValueError('Model...')` | MEDIUM |
| 4 | `networks_other.py` | `return NotImplementedError(...)` → `raise NotImplementedError(...)` line 137 | MEDIUM |
| 5 | `grid_attention_layer.py` | `F.sigmoid` → `torch.sigmoid` | LOW |
| 6 | `grid_attention_layer.py` | `nn.init.constant` → `nn.init.constant_` | LOW |
| 7 | `networks_other.py` | `init.normal`, `init.xavier_normal`, etc. → thêm `_` | LOW |
| 8 | `networks_other.py` | `torch.autograd.Variable` → xóa, không cần | LOW |

**Không ảnh hưởng đến kết quả thực nghiệm:** Bugs 1-8 đều nằm trong code đường không được gọi bởi `train.py` và các notebook chính (grid_attention_layer được kế thừa pattern nhưng PGA-UNet không import GridAttentionBlock2D trực tiếp).

---

## 10. Đánh giá tổng thể chất lượng code

| Thành phần | Chất lượng | Ghi chú |
|-----------|-----------|---------|
| `prompt_unet_2D.py` | ⭐⭐⭐⭐⭐ | Core đóng góp, thiết kế rõ, tư duy kỹ |
| `dataset.py` | ⭐⭐⭐⭐⭐ | Clean, đúng, synchronized aug |
| `train.py` | ⭐⭐⭐⭐ | Loop tốt, CBL metric thú vị |
| `manim_*.py` | ⭐⭐⭐⭐⭐ | Minh họa chính xác, sư phạm tốt |
| `grid_attention_layer.py` | ⭐⭐⭐ | Legacy bugs, nhưng không ảnh hưởng chạy |
| `networks_other.py` | ⭐⭐ | Toàn bộ deprecated + 1 silent bug |
| `models/networks/__init__.py` | ⭐ | ImportError ngay dòng đầu |

**Kết luận:** Phần code thực sự chạy (prompt_unet_2D.py, dataset.py, train.py) có chất lượng **tốt đến xuất sắc** — tư duy kỹ thuật rõ ràng, không có lỗi logic trong luồng chính. Các bug tập trung ở legacy code không được sử dụng.
