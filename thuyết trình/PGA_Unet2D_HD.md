# PGA-UNet — Kiến trúc và Nguyên lý Hoạt động

---

## 1. Vấn đề: tại sao U-Net thường không đủ?

Trên ảnh X-quang xương, khối u và vết nhiễu (artifact kim loại, vôi hóa) thường có cùng
mức độ sáng. U-Net thông thường chỉ nhận ảnh đầu vào và tự suy luận toàn bộ — nó không
nhận bất kỳ thông tin nào về *vùng nào trên ảnh cần phân đoạn*. Kết quả là mô hình dễ
nhầm nhiễu với tổn thương, đặc biệt trên các ca khó.

**PGA-UNet** giải quyết điều này bằng cách tiếp nhận thêm một **câu nhắc trực quan**
(bounding box do bác sĩ vẽ) và đưa tín hiệu định hướng đó vào hai điểm then chốt trong
kiến trúc mạng.

---

## 2. Tổng quan: U-Net vs. PGA-UNet

![Tổng quan U-Net vs PGA-UNet](fig2_unet_vs_pga.png)

| | U-Net thường | PGA-UNet |
|---|---|---|
| Đầu vào | Ảnh X-quang | Ảnh X-quang + Prompt heatmap |
| Encoder | Rút trích đặc trưng thuần | Rút trích đặc trưng **+ PSG** |
| Decoder | Tái tạo mặt nạ thuần | Tái tạo mặt nạ **+ CAD** |
| Biết vùng cần phân đoạn? | Không | Có — qua 2 thành phần mới |

PSG và CAD là hai đóng góp kiến trúc độc lập so với U-Net gốc:
- **PSG** (Prompt Spatial Gate) — tác động tại **encoder**: khuếch đại đặc trưng tại vùng câu nhắc, giữ nguyên vùng ngoài
- **CAD** (Conditioned Attention Decoder) — tác động tại **decoder**: cổng chú ý nhận thêm heatmap để định hướng lọc

---

## 3. Nền tảng: Cấu trúc encoder–decoder của U-Net

![Cấu trúc U-Net cơ bản](fig1_unet_structure.png)

U-Net có hình dạng chữ **U**:

- **Encoder** (đi xuống — nửa trái): ảnh được thu nhỏ dần qua các lớp conv + pooling.
  Mỗi bước xuống, kích thước spatial giảm một nửa, số kênh tăng — đặc trưng ngày càng
  trừu tượng hơn (từ cạnh/màu → hình dạng → ngữ nghĩa).
- **Bottleneck** (đáy chữ U — điểm thắt): ảnh đã bị thu nhỏ đến mức nhỏ nhất (7×7 pixel
  trong mạng này). Tại đây mạng không còn thấy chi tiết vị trí nữa, chỉ thấy "bức tranh
  toàn cục" — vùng nào sáng, cấu trúc xương tổng thể trông ra sao. Đây là điểm mà mạng
  "hiểu ngữ nghĩa" nhiều nhất trước khi bắt đầu tái tạo mặt nạ.
- **Decoder** (đi lên — nửa phải): phóng to dần qua các lớp upsample + conv, tái tạo
  mặt nạ phân đoạn về kích thước gốc.
- **Skip connection**: chuyển đặc trưng chi tiết (cạnh, vị trí) từ tầng encoder sang
  tầng decoder cùng mức độ phân giải, bù lại thông tin vị trí bị mất khi đi qua bottleneck.

---

## 4. Mã hóa câu nhắc: Gaussian Plateau Heatmap

**Đầu vào:** Bounding box bác sĩ vẽ — một hình chữ nhật bao quanh vùng nghi ngờ tổn thương.

**Quy trình — 3 bước:**

**Bước 1 — Tạo mặt nạ trắng/đen cứng:**
Vẽ một ảnh toàn đen cùng kích thước với ảnh X-quang. Tô trắng hoàn toàn (giá trị 1.0)
toàn bộ vùng bên trong hộp, phần còn lại giữ nguyên đen (giá trị 0).

![Từ mặt nạ nhị phân sang heatmap](fig7_binary_to_heatmap.png)

---

**Bước 2 — Làm mờ viền (Gaussian blur):**

Kernel (cửa sổ tính toán) trượt qua từng pixel của ảnh. Tại mỗi vị trí, kernel đặt
chồng lên ảnh và tính một giá trị mới cho pixel đang xét bằng cách nhân từng ô trong
cửa sổ với trọng số tương ứng của kernel, rồi cộng tất cả lại và chia cho tổng trọng số.

![Kernel trượt trên ảnh](fig8_kernel_slide.png)

Với kernel 5×5 Gaussian (giữa nặng, mép nhẹ), xét một pixel nằm ngay trên cạnh hộp —
nửa cửa sổ thấy ô 1 (trong hộp), nửa còn lại thấy ô 0 (ngoài hộp):

![Cách tính nhân kernel với ảnh](fig9_kernel_multiply.png)

Kết quả: pixel đó ra giá trị 0.70 — không còn là 0 hay 1 cứng nữa mà là giá trị trung
gian phản ánh mức độ "gần cạnh hộp".

> **Gaussian vs average thường khác nhau chỗ nào?**
>
> Average thường: mỗi ô trong cửa sổ đóng góp bằng nhau (1/25 với cửa sổ 5×5).
>
> Gaussian: ô giữa đóng góp nhiều nhất (trọng số 41), ô góc đóng góp rất ít (trọng số 1):
> ```
>  1   4   7   4   1
>  4  16  26  16   4
>  7  26  41  26   7
>  4  16  26  16   4
>  1   4   7   4   1
> ```
> Kết quả thực tế ít khác nhau — cả hai đều tạo dải mờ. Gaussian cho đường chuyển
> tiếp mượt hơn một chút, không bị bậc thang ở rìa cửa sổ. Đây là chi tiết kỹ thuật
> nhỏ, **không phải đóng góp chính**.

---

**Bước 3 — Giữ vùng trong hộp = 1.0 (Plateau):**
Sau blur, vùng sâu bên trong hộp cũng bị giảm nhẹ. Bước này lấy giá trị lớn hơn giữa
mặt nạ gốc và kết quả blur — vùng trong hộp được phục hồi về đúng 1.0, chỉ viền mới
bị mờ. Kết quả là hình dạng "mâm phẳng" (plateau): phẳng ở 1.0 bên trong, dốc dần ở
viền, phẳng ở 0 bên ngoài.

Ma trận heatmap thực tế sau khi kernel trượt hết toàn bộ ảnh:

![Ma trận heatmap kết quả](fig10_heatmap_matrix.png)

Và nhìn theo mặt cắt ngang qua tâm hộp:

![Đồ thị mặt cắt heatmap](fig11_heatmap_profile.png)

**Đóng góp thực sự ở đây là gì?**

Không phải ở chỗ dùng Gaussian hay average. Đóng góp nằm ở **hình thức biểu diễn**:
bounding box được chuyển thành một **ảnh 2D cùng kích thước với ảnh X-quang**, thay vì
dùng dưới dạng 4 con số tọa độ rời rạc.

- SAM/SAM-Med2D đưa bounding box vào dưới dạng 4 tọa độ số → mạng phải tự học cách
  ánh xạ 4 con số đó sang không gian ảnh → cần kiến trúc đặc biệt (Transformer, prompt
  encoder riêng), tham số lớn
- PGA-UNet đưa heatmap vào như một kênh ảnh → mạng CNN có thể dùng heatmap trực tiếp
  tại từng vị trí pixel, không cần cơ chế ánh xạ phức tạp, không tăng tham số đáng kể

Nói gọn: **đóng góp là cách biểu diễn 2D này cho phép một mạng CNN nhỏ (~3M tham số)
tiếp nhận được câu nhắc không gian mà không cần kiến trúc phức tạp.**

---

**Tại sao không dùng bước 1 đơn thuần (mặt nạ cứng)?**

Nếu chỉ dùng mặt nạ trắng/đen: cạnh hộp là đường sắc hoàn toàn. Khi bác sĩ vẽ lệch
5 pixel, cạnh đó rơi vào sai vị trí — pixel ngay cạnh đó nhảy từ 1.0 xuống 0.0 đột
ngột, tạo ra tín hiệu nhiễu mạnh ngay tại biên. Mạng sẽ học được rằng "cạnh hộp = quan
trọng" thay vì "vùng trong hộp = quan trọng", gây ra lỗi khi hộp không hoàn hảo.

Dải mờ 15 pixel đóng vai trò **vùng đệm**: kể cả khi bác sĩ vẽ lệch 10 pixel, tổn
thương thực vẫn nằm trong vùng có giá trị cao, và mạng không bị tín hiệu nhảy đột ngột.

**Kết quả:** Một ảnh đơn kênh (giống ảnh grayscale) cùng kích thước với ảnh X-quang —
đây là **heatmap**. Nó được đưa vào mạng song song với ảnh X-quang, và tự động thu nhỏ
hoặc phóng to về cùng kích thước với từng tầng khi PSG và CAD cần dùng.

---

## 5. PSG (Prompt Spatial Gate — Cổng không gian câu nhắc) — Tích hợp câu nhắc tại Encoder

> **PSG = Prompt Spatial Gate**: "Spatial" vì nó hoạt động trên từng vị trí không gian
> của bản đồ đặc trưng; "Gate" vì nó là một cổng kiểm soát mức độ khuếch đại tại mỗi vị trí.

![Chi tiết PSG — sơ đồ luồng](fig4_psg_detail.png)

**Đầu vào:** Hai thứ đến cùng lúc tại mỗi tầng encoder:
- Bản đồ đặc trưng vừa được tính từ lớp tích chập tại tầng đó — chứa thông tin về cạnh,
  kết cấu, hình dạng trong toàn bộ ảnh, chưa phân biệt vùng nào quan trọng hơn
- Heatmap câu nhắc đã được thu nhỏ về cùng kích thước với bản đồ đặc trưng tầng đó

---

### 5a. Quy trình PSG theo từng bước — minh họa ma trận

**Bước ① — Đầu vào: ảnh đặc trưng x và prompt heatmap**

Hai ma trận cùng kích thước vào cùng lúc. Ảnh đặc trưng x chứa cả tín hiệu tổn thương
(giá trị cao ≈ 0.60–0.80) lẫn nhiễu kim loại (giá trị cao tương tự) — không phân biệt
được. Heatmap prompt biết vùng nào bác sĩ chỉ định (giá trị 1.00 bên trong, 0.00 bên ngoài).

![Bước ① — Ma trận đầu vào: ảnh x và prompt heatmap](fig4b_psg_step01_input.png)

---

**Bước ② — Chuyển heatmap thành bản đồ cổng (gate)**

Lớp Conv 1×1 + Sigmoid đọc heatmap và tạo ra bản đồ cổng: mỗi ô mang giá trị 0–1 thể
hiện mức độ "trong vùng câu nhắc". Trong vùng bbox: cổng ≈ 0.88; ngoài bbox: cổng ≈ 0.12.

![Bước ② — x sau Conv và heatmap sau Conv+Sigmoid thành cổng](fig4c_psg_step02_conv.png)

---

**Bước ③④ — Khuếch đại có chọn lọc và kết quả**

Từng ô của đặc trưng được nhân theo công thức:

$$\tilde{x}[i,j] = x[i,j] \times (1 + \text{cổng}[i,j])$$

- Ô **tổn thương** trong bbox: `0.80 × (1 + 0.88) = 0.80 × 1.88 = 1.50` — nổi bật rõ
- Ô **nhiễu** ngoài bbox: `0.70 × (1 + 0.08) = 0.70 × 1.08 = 0.78` — gần giữ nguyên
- Ô **nền**: `0.10 × (1 + 0.12) = 0.10 × 1.12 = 0.11` — gần giữ nguyên

![Bước ③④ — Nhân cổng và kết quả x̃](fig4d_psg_step34_gate.png)

Mạng không bị mù với vùng ngoài — cấu trúc xương xung quanh vẫn được nhìn thấy, chỉ
là ít được ưu tiên hơn so với vùng bác sĩ chỉ định.

---

**Kết quả:** Bản đồ đặc trưng đã điều chỉnh x̃ — cùng kích thước với đầu vào, nhưng tín
hiệu tổn thương trong vùng câu nhắc được nổi bật đáng kể so với nhiễu bên ngoài. Bản đồ
này tiếp tục đi xuống tầng encoder tiếp theo theo đúng luồng U-Net thông thường (đồng thời
được lưu lại làm skip connection cho decoder tầng tương ứng).

PSG được áp dụng tại **hai tầng encoder trung gian** (56×56 và 28×28). Tầng đầu (112×112)
bị bỏ qua vì đặc trưng ở đó còn quá thô (chủ yếu là cạnh và màu), chưa mang ý nghĩa
phân đoạn.

---

## 6. CAD (Conditioned Attention Decoder — Bộ giải mã chú ý có điều kiện) — Mở rộng Attention Gate tại Decoder

> **CAD = Conditioned Attention Decoder**: "Conditioned" vì cổng chú ý được điều kiện hóa
> bởi câu nhắc (heatmap) — không còn chỉ dựa vào ảnh như Attention U-Net gốc.

### 6a. Cổng chú ý hoạt động ra sao — và prompt thay đổi điều gì?

![Hiệu ứng cổng chú ý](fig6_attention_effect.png)

**Bối cảnh — skip connection mang cả nhiễu lẫn tín hiệu:**

Khi encoder đi xuống, mỗi tầng lưu lại một bản sao đặc trưng gọi là **skip connection**
và chuyển ngang sang decoder tầng tương ứng. Mục đích là bổ sung chi tiết vị trí cho
decoder — vì đặc trưng qua bottleneck đã mất thông tin không gian.

Vấn đề: bản sao đó chứa tất cả, cả vùng tổn thương lẫn vùng nhiễu đều có giá trị kích
hoạt cao tương đương nhau. Decoder nhận vào sẽ không biết cái nào nên tin.

---

**Đầu vào của cổng chú ý — ba nguồn:**

- **Đặc trưng skip** (từ encoder tầng này): chi tiết vị trí cao, nhưng chưa lọc — chứa
  cả u lẫn nhiễu
- **Tín hiệu định hướng** (từ decoder tầng sâu hơn, một bước bên dưới): tầng đó đã xử
  lý từ bottleneck lên, nên đã "hiểu" được cấu trúc tổng thể — biết tổn thương nhìn tổng
  quát trông như thế nào, nằm ở vùng nào của ảnh
- *(Chỉ có ở CAD)* **Heatmap câu nhắc**: biết chính xác vùng bác sĩ chỉ định

**Quy trình:**

Cổng so sánh từng vị trí trên đặc trưng skip với tín hiệu định hướng — vị trí nào "khớp"
với những gì tín hiệu định hướng mô tả thì được giữ lại nhiều, vị trí nào không khớp thì
bị giảm trọng số. Kết quả là một **bản đồ trọng số** (giá trị 0–1 tại mỗi ô), rồi nhân
bản đồ đó vào đặc trưng skip.

**Khi không có prompt (Attention U-Net):** cổng chỉ dựa vào đặc trưng ảnh từ decoder sâu
hơn. Nếu một vùng nhiễu trông tương tự tổn thương về mặt đặc trưng ảnh, cổng vẫn có thể
giữ nhầm vì nó không có thêm thông tin vị trí.

**Khi có thêm prompt (CAD):** heatmap được cộng vào tín hiệu định hướng trước khi cổng
tính bản đồ trọng số. Cổng lúc này biết thêm "bác sĩ chỉ vùng này" — nên ngay cả khi
nhiễu trông giống u, cổng vẫn ưu tiên vùng câu nhắc và giảm mạnh vùng nằm ngoài.

**Kết quả trả ra:** Đặc trưng skip đã được lọc — vùng tổn thương trong vùng câu nhắc
được giữ gần nguyên, vùng nhiễu bị giảm đáng kể. Đặc trưng đã lọc này được ghép với
đặc trưng decoder (từ tầng dưới phóng to lên) để tiếp tục tái tạo mặt nạ.

### 6b. Ba thế hệ: U-Net → Attention U-Net → CAD

![Tiến hóa CAD](fig5_cad_evolution.png)

**① U-Net**: skip connection nối thẳng vào decoder, không qua lọc nào. Mọi đặc trưng
(u lẫn nhiễu) đều đi vào decoder với trọng số như nhau.

**② Attention U-Net**: thêm cổng lọc trên skip. Cổng dùng tín hiệu từ decoder sâu hơn
để tự suy luận vùng nào quan trọng — nhưng vì chỉ nhìn vào ảnh, nếu nhiễu trông giống
tổn thương thì cổng vẫn có thể giữ nhầm.

**③ CAD (PGA-UNet)**: cổng lọc nhận thêm heatmap câu nhắc bên cạnh tín hiệu từ decoder.
Hai nguồn kết hợp: ảnh nói "cái này trông như tổn thương", heatmap nói "đây là vùng bác
sĩ chỉ định" — cổng ra quyết định dựa trên cả hai, cho phép lọc chính xác hơn ngay cả
khi nhiễu có hình dạng tương tự tổn thương.

CAD kế thừa toàn bộ cơ chế lọc của Attention U-Net, chỉ bổ sung thêm heatmap làm đầu
vào cho tín hiệu định hướng — phần còn lại giữ nguyên.

---

## 7. Bản đồ tầng đầy đủ

![Bản đồ tầng PGA-UNet](fig3_layer_map.png)

```
ENCODER (đi xuống)                    DECODER (đi lên)

112×112  ────────────────────────────────────────→  112×112 (mặt nạ ra)
          ↓ conv + pool                              ↑ conv + upsample
56×56   ★ PSG  ──────────────────────────────────→  56×56
          ↓ conv + pool                              ↑ conv + upsample  ◆ CAD
28×28   ★ PSG  ──────────────────────────────────→  28×28
          ↓ conv + pool                              ↑ conv + upsample  ◆ CAD
14×14   ────────────────────────────────────────→  14×14              ◆ CAD
                    ↓
                  7×7 (bottleneck)
                    ↑
```

| Vị trí | Kích thước | Thành phần |
|--------|-----------|------------|
| Encoder tầng 2 | 56×56 | ★ PSG — khuếch đại đặc trưng theo heatmap |
| Encoder tầng 3 | 28×28 | ★ PSG — khuếch đại đặc trưng theo heatmap |
| Bottleneck | 7×7 | — |
| Decoder skip 1 | 14×14 | ◆ CAD — lọc skip theo gating + heatmap |
| Decoder skip 2 | 28×28 | ◆ CAD — lọc skip theo gating + heatmap |
| Decoder skip 3 | 56×56 | ◆ CAD — lọc skip theo gating + heatmap |
| Đầu ra | 112×112 | Mặt nạ phân đoạn |

---

## 8. Tóm tắt đóng góp

| Thành phần | Vị trí | Cơ chế | So với U-Net gốc |
|---|---|---|---|
| **Gaussian Plateau Heatmap** | Đầu vào | Mã hóa bbox thành kênh 2D liên tục | Mới hoàn toàn |
| **PSG** | Encoder | Khuếch đại có chọn lọc đặc trưng theo bản đồ heatmap | Mới hoàn toàn |
| **CAD** | Decoder (skip) | Cộng heatmap vào tín hiệu định hướng của cổng chú ý | Kế thừa Attention U-Net, mở rộng thêm prompt |

Cả ba thành phần cùng dùng chung một heatmap được tính một lần từ bounding box — không
có tham số phụ trợ nào đáng kể, tổng mô hình vẫn ở mức ~3 triệu tham số.
