# Giải thích PGA-UNet (bản thuyết trình)

Dùng đúng thuật ngữ chuyên ngành của đề tài (không mượn ví dụ từ ngành khác), viết theo mạch nói chuyện — người nghe không chuyên vẫn theo được, nhưng đầy đủ công thức và lý do đặt từng công thức ở đúng vị trí đó trong kiến trúc.

---

## 1. Vấn đề cần giải quyết

Muốn phân đoạn (khoanh chính xác từng pixel) vùng tổn thương xương trên ảnh X-quang. Có hai hướng cũ:

- **U-Net tự động**: đưa thẳng ảnh vào, mô hình tự tìm vùng bệnh — nhưng không có ai chỉ hướng nên dễ nhầm lẫn, đặc biệt ảnh X-quang tương phản thấp.
- **SAM-Med2D**: một mô hình nền tảng lớn, nhận thêm bounding box (khung chữ nhật bác sĩ vẽ quanh vùng nghi ngờ) làm gợi ý — chính xác hơn nhưng rất nặng (~91 triệu tham số) và bị giới hạn cứng ở độ phân giải nhỏ (256×256).

PGA-UNet ra đời để lấy ưu điểm của cả hai: nhẹ như U-Net nhưng vẫn nhận được gợi ý bounding box như SAM-Med2D.

---

## 2. Ý tưởng cốt lõi: biến bounding box thành "bản đồ nhiệt" (heatmap)

Thay vì đưa bounding box vào dưới dạng một khối 0/1 cứng (trong hộp là 1, ngoài hộp là 0), PGA-UNet chuyển nó thành một bản đồ nhiệt: giá trị cao đều bên trong hộp, mờ dần ra viền, mượt liên tục thay vì đứt gãy đột ngột ở biên hộp.

**Lý do làm vậy:** bounding box bác sĩ vẽ tay không bao giờ hoàn hảo — có thể lệch tâm một chút, to hơn hoặc nhỏ hơn vùng bệnh thật. Nếu mô hình tin tuyệt đối vào đúng viền hộp (dạng 0/1 cứng), chỉ cần hộp lệch một chút là mô hình dễ sai theo. Bản đồ nhiệt mềm giúp mô hình hiểu "vùng nghi ngờ nằm khoảng đây, tin tưởng giảm dần ra ngoài", nên chịu được sai số của bác sĩ tốt hơn.

### 2.1. Công thức: Plateau Heatmap với Gaussian Blur, $k = 31$

Bác sĩ vẽ một hộp giới hạn $\mathbf{B} = (x_1, y_1, x_2, y_2)$. Quy trình biến hộp này thành bản đồ nhiệt liên tục $\mathbf{H}_{prompt}$ gồm 2 bước:

**Bước 1 — Tạo mặt nạ nhị phân có đệm:** Từ hộp $\mathbf{B}$, tạo một mặt nạ nhị phân $\mathbf{B}_{mask}$ (bên trong hộp = 1, bên ngoài = 0), nhưng hộp được nới rộng thêm 5 pixel mỗi cạnh trước khi gán giá trị 1, để không cắt sát ngay biên tổn thương thực tế.

**Bước 2 — Làm mềm biên bằng bộ lọc Gaussian:**

$$\mathbf{H}_{prompt} = \text{GaussianBlur}\left(\mathbf{B}_{mask},\ k=31\right)$$

Ở đây $k$ là **kích thước cửa sổ lọc** (kernel size) — tức là khi làm mềm một điểm ảnh, bộ lọc sẽ nhìn vào một vùng vuông $31 \times 31$ pixel xung quanh điểm đó, tính trung bình có trọng số (trọng số giảm dần theo khoảng cách tới tâm, đúng theo phân phối Gaussian) để quyết định giá trị mới. Kết quả: bên trong hộp vẫn giữ nguyên giá trị cao gần bằng 1 (vì toàn bộ vùng lân cận cũng là 1, trung bình ra vẫn xấp xỉ 1), còn tại **đường biên hộp**, giá trị giảm dần mượt mà từ 1 xuống 0 trong một vùng chuyển tiếp, thay vì nhảy đột ngột từ 1 xuống 0 như mặt nạ nhị phân gốc.

**Tại sao chọn đúng $k = 31$:** Nhóm đã thử nghiệm với $k \in \{15, 21, 31, 51\}$ trên tập xác thực:

- $k < 21$: vùng chuyển tiếp quá hẹp, gần như vẫn là mặt nạ nhị phân cứng, không giải quyết được vấn đề ban đầu.
- $k > 51$: vùng chuyển tiếp quá rộng, tín hiệu câu nhắc "tràn" ra ngoài, lấn sang các cấu trúc xương lân cận không liên quan.
- $k = 31$ tạo vùng chuyển tiếp mượt khoảng 15 pixel mỗi bên (đủ phủ vùng biên tổn thương điển hình trên ảnh $512\times512$), cho Dice tốt nhất trên tập xác thực. Số 31 là số lẻ vì bộ lọc cần có đúng một pixel tâm để đối xứng đều hai bên.

**Vì sao không dùng mặt nạ nhị phân cứng luôn:** Khi một mặt nạ có cạnh sắc nét đi qua một lớp tích chập, đường biên đột ngột đó tạo ra gradient giả tạo — mạng dễ học theo hình dạng cạnh của hộp thay vì học đặc trưng thật của tổn thương. Bản đồ nhiệt mượt tránh được hiện tượng này, đồng thời phù hợp tự nhiên với cách các mạng nơ-ron vốn tạo ra vùng kích hoạt dạng phân phối liên tục (mạnh ở trung tâm, giảm dần ra biên).

**So với cách SAM/SAM-Med2D mã hóa prompt:** SAM mã hóa hộp giới hạn thành các vector nhúng vị trí rời rạc (positional embedding), phù hợp với kiến trúc Transformer vốn xử lý tập token rời rạc. PGA-UNet dùng kiến trúc U-Net với feature map 2D liên tục, nên chọn biểu diễn bản đồ nhiệt 2D cùng không gian $H \times W$ với feature map — cho phép nhân trực tiếp theo từng điểm ảnh (sẽ thấy ở công thức PSG bên dưới), đơn giản, hiệu quả và không mất thông tin vị trí như khi phải chiếu một vector rời rạc vào không gian 2D.

---

## 3. Đưa bản đồ nhiệt vào đúng hai chỗ trong kiến trúc U-Net

PGA-UNet vẫn giữ khung U-Net gốc (một nhánh mã hóa nén ảnh xuống, một nhánh giải mã dựng lại mặt nạ), nhưng thêm hai thành phần mới đưa bản đồ nhiệt vào:

- **Cổng không gian (Prompt Spatial Gate – PSG)**, đặt ở nhánh mã hóa: tăng cường đặc trưng đúng vùng được khoanh ngay từ giai đoạn trích đặc trưng.
- **Cơ chế chú ý có điều kiện (Conditioned Attention Decoder – CAD)**, đặt ở nhánh giải mã: mở rộng Attention Gate sẵn có, đưa thêm câu nhắc vào tín hiệu quyết định "nên chú ý vào đâu" khi dựng lại mặt nạ.

Tóm gọn vai trò: PSG lo phần "tập trung sớm" ở đầu vào, CAD lo phần "bám đúng vùng" ở đầu ra. Cả hai cùng dùng chung một bản đồ nhiệt $\mathbf{H}_{prompt}$ làm tín hiệu dẫn đường xuyên suốt mạng.

### 3.1. Cổng không gian tại Encoder (PSG) — công thức và lý do

Encoder của PGA-UNet vẫn là encoder U-Net chuẩn: ảnh đi qua nhiều tầng, mỗi tầng gồm các lớp tích chập trích đặc trưng rồi giảm kích thước không gian (downsample) để chuyển sang tầng sau — tầng càng sâu thì kích thước ảnh càng nhỏ nhưng số kênh đặc trưng càng nhiều.

PSG được chèn thêm vào **ngay sau bước trích đặc trưng của mỗi tầng, trước khi đặc trưng đó được downsample chuyển xuống tầng kế tiếp**. Tại tầng thứ $l$, gọi đặc trưng vừa trích được là $\mathbf{x}^l$:

**Bước 1:** Bản đồ nhiệt gốc $\mathbf{H}_{prompt}$ được resize (giảm mẫu) về đúng kích thước không gian của $\mathbf{x}^l$ tại tầng đó, gọi là $\mathbf{H}^l$. Lý do bắt buộc phải resize: $\mathbf{x}^l$ càng sâu thì kích thước càng nhỏ, nên heatmap phải thu nhỏ theo để nhân được với nhau theo từng điểm ảnh tương ứng.

**Bước 2 — Công thức cổng:**

$$\tilde{\mathbf{x}}^l = \mathbf{x}^l \odot \Big(1 + \alpha \cdot \sigma(\mathbf{W}_{gate} * \mathbf{H}^l)\Big)$$

Giải thích từng ký hiệu:

- $\mathbf{W}_{gate} * \mathbf{H}^l$: phép tích chập $1\times1$ (chỉ đổi số kênh, không đổi kích thước không gian), biến heatmap từ 1 kênh thành đúng số kênh $C^l$ của $\mathbf{x}^l$ tại tầng đó, để hai bên khớp nhau khi nhân.
- $\sigma$: hàm sigmoid, ép giá trị về khoảng $(0,1)$.
- $\alpha \in [0,1]$: một tham số học được, khởi tạo nhỏ ở $0.1$ để không làm xáo trộn huấn luyện ban đầu.
- $\odot$: nhân theo từng phần tử (element-wise), tức mỗi điểm ảnh, mỗi kênh nhân riêng.

**Vì sao công thức có dạng $(1 + \alpha \cdot \sigma(\cdot))$ chứ không phải chỉ $\alpha \cdot \sigma(\cdot)$:** Đây là điểm mấu chốt. Vì luôn cộng thêm 1, hệ số nhân luôn $\geq 1$ — nghĩa là đặc trưng **chỉ có thể được khuếch đại lên, không bao giờ bị nhân với số nhỏ hơn 1 để triệt tiêu**. Ở vùng trong hộp (nơi $\mathbf{H}^l$ gần 1), hệ số nhân sẽ lớn hơn 1, đặc trưng được tăng cường. Ở vùng ngoài hộp ($\mathbf{H}^l \approx 0$), hệ số nhân gần bằng 1, đặc trưng giữ nguyên như cũ, không bị mất đi. Đây gọi là "tăng cường có chọn lọc" (selective enhancement) — encoder không bỏ sót thông tin toàn cục, chỉ ưu tiên truyền mạnh hơn phần đặc trưng nằm trong vùng bác sĩ chỉ định xuống các tầng sâu hơn.

**Tại sao đặt PSG ở encoder mà không phải chỗ khác:** Vì encoder là nơi quyết định đặc trưng nào được giữ lại và truyền tiếp xuống các tầng sau. Nếu không định hướng ngay từ đây, mạng phải tự học lọc nhiễu nền trên toàn ảnh — lãng phí và dễ sai. Đặt PSG ngay sau mỗi tầng trích đặc trưng nghĩa là mọi tầng sâu hơn phía sau đều được thừa hưởng phần đặc trưng đã được "nhắc" ngay từ đầu vào của chúng. Đây cũng là thành phần **không tồn tại trong U-Net hay Attention U-Net gốc** — hoàn toàn mới được thêm vào cho PGA-UNet.

### 3.2. Cơ chế chú ý có điều kiện tại Decoder (CAD) — công thức và lý do

Decoder chuẩn của Attention U-Net hoạt động thế này: ở mỗi tầng giải mã, đặc trưng từ tầng sâu hơn (đã qua upsample) được dùng làm **tín hiệu gating** $\mathbf{g}$, tín hiệu này quyết định nên "chú ý" vào phần nào của đặc trưng skip-connection $\mathbf{x}^l$ (lấy từ encoder cùng tầng, đã qua PSG ở trên) khi ghép nối lại. Vấn đề của thiết kế gốc: $\mathbf{g}$ được tính hoàn toàn từ đặc trưng ảnh, không hề biết bác sĩ đã chỉ vùng nào.

CAD sửa đúng bước tính $\mathbf{g}$ này, chèn thêm câu nhắc vào **trước khi** $\mathbf{g}$ được đưa vào cổng chú ý chuẩn. Cụ thể gồm 4 bước:

**Bước 1 — Mã hóa câu nhắc riêng cho tầng này:**

$$\mathbf{p}_{enc} = f_{enc}(\mathbf{H}_{prompt})$$

$f_{enc}$ là hai lớp tích chập $3\times3$ liên tiếp (kèm InstanceNorm và ReLU), nhận heatmap (đã resize về đúng kích thước của $\mathbf{g}$ tại tầng này) làm đầu vào, biến nó thành một đặc trưng $\mathbf{p}_{enc}$ có cùng số kênh với $\mathbf{g}$.

**Bước 2 — Tính điểm tin cậy vô hướng:**

$$c = \sigma(\text{GAP}(\mathbf{p}_{enc}))$$

GAP (Global Average Pooling) lấy trung bình toàn bộ không gian của $\mathbf{p}_{enc}$, gộp thành một con số duy nhất cho mỗi kênh, rồi qua sigmoid ra một điểm tin cậy $c \in (0,1)$. Con số này đại diện cho việc "câu nhắc ở tầng này rõ ràng/mạnh đến mức nào" trên toàn ảnh.

**Bước 3 — Cộng có trọng số vào tín hiệu gating:**

$$\mathbf{g}' = \mathbf{g} + c \cdot \alpha \cdot w_l \cdot \mathbf{p}_{enc}$$

Trong đó $\alpha = \sigma(\alpha_{raw})$ là một tham số học được khác (trọng số hòa trộn), còn $w_l$ là hệ số cố định theo từng tầng giải mã, đi từ tầng sâu nhất ra tầng nông nhất: $\{1.0,\ 0.7,\ 0.4,\ 0.2\}$.

**Tại sao $w_l$ giảm dần từ tầng sâu ra tầng nông:** Tầng giải mã sâu nhất (kích thước ảnh nhỏ nhất) là nơi quyết định vị trí tổng thể của tổn thương — câu nhắc cần ảnh hưởng mạnh nhất ở đây ($w_l = 1.0$). Càng ra các tầng nông hơn (kích thước ảnh lớn dần, gần với đầu ra cuối), nhiệm vụ chính chuyển sang tinh chỉnh đường biên chi tiết dựa trên đặc trưng ảnh thật (gradient xương, độ tương phản) — nếu vẫn ép câu nhắc ảnh hưởng mạnh như ban đầu sẽ khiến mô hình "cứng nhắc" bám theo đúng hình chữ nhật của hộp thay vì bám theo hình dạng tổn thương thật. Giảm dần $w_l$ giúp câu nhắc "buông tay" dần, nhường chỗ cho đặc trưng ảnh quyết định đường biên cuối cùng.

**Bước 4 — Đưa vào cổng chú ý chuẩn:** $\mathbf{g}'$ (đã được điều kiện hóa) được đưa vào khối GridAttentionBlock2D — chính là cơ chế Attention Gate gốc không đổi — để tính hệ số chú ý $\boldsymbol{\alpha}_{cond}$, dùng để điều chỉnh đặc trưng skip-connection $\mathbf{x}^l$ trước khi ghép với đặc trưng decoder. Ngoài ra, tại đầu ra khối decoder tầng này còn cộng thêm một thành phần dư nhỏ $+\beta \cdot \mathbf{H}_{prompt}$ ($\beta$ học được) để đảm bảo tín hiệu câu nhắc gốc vẫn còn dấu vết trực tiếp, không bị pha loãng hoàn toàn qua nhiều phép biến đổi.

**Vì sao CAD chỉ sửa $\mathbf{g}$ mà không sửa thẳng $\mathbf{x}^l$ (khác cách PSG làm ở encoder):** Vì vai trò của $\mathbf{g}$ trong Attention Gate vốn dĩ là "người ra quyết định nên chú ý vào đâu" — sửa đúng chỗ ra quyết định là hiệu quả nhất, còn cơ chế chú ý chuẩn (GridAttentionBlock2D) phía sau vẫn được giữ nguyên để tận dụng cách nó đã được chứng minh hoạt động tốt trong Attention U-Net gốc. Đây là điểm khác biệt cốt lõi so với Attention Gate gốc: CAD là phần **mở rộng** một kỹ thuật đã có (không phải làm mới hoàn toàn như PSG), bằng cách bổ sung câu nhắc trực tiếp vào tín hiệu gating.

---

## 4. Hàm mất mát — không đổi

$$\mathcal{L}_{seg} = \mathcal{L}_{Dice} + \mathcal{L}_{BCE}$$

Câu nhắc **không** làm thay đổi công thức hàm mất mát này — nó vẫn tính trên mặt nạ dự đoán cuối cùng so với nhãn thật, y hệt U-Net thường. Ảnh hưởng của câu nhắc chỉ đi vào qua kiến trúc (PSG, CAD), lan truyền tới hàm mất mát gián tiếp qua gradient trong quá trình lan truyền ngược. Điểm này đáng nói khi thuyết trình vì nó cho thấy PGA-UNet không "gian lận" bằng cách thêm số hạng phạt đặc biệt nào cho phần câu nhắc — toàn bộ cải thiện đến từ cách kiến trúc dùng câu nhắc, không phải từ hàm mất mát.

---

## 5. Vì sao thiết kế này hiệu quả (tổng kết)

- **Nhẹ:** chỉ khoảng 3 triệu tham số, học từ đầu hoàn toàn trên dữ liệu X-quang xương, không cần mượn trọng số khổng lồ có sẵn như SAM-Med2D (~91 triệu tham số).
- **Chính xác hơn U-Net tự động:** vẫn tận dụng được gợi ý của bác sĩ nhờ hai cơ chế PSG (tập trung sớm ở encoder) và CAD (bám đúng vùng ở decoder).
- **Bền bỉ trước sai số bác sĩ:** nhờ dùng bản đồ nhiệt mềm (Gaussian, $k=31$) thay vì hộp cứng, mô hình chịu được sai lệch khi bác sĩ vẽ hộp không hoàn toàn chuẩn — thử nghiệm cho thấy khi hộp bị lệch tâm, độ chính xác gần như không đổi.
- **Minh bạch về mặt thiết kế:** toàn bộ cải thiện đến từ kiến trúc (PSG + CAD), không phải từ việc thay đổi hàm mất mát hay "mẹo" huấn luyện nào khác.
