# PGA-UNet2D — Khóa Luận Tốt Nghiệp

**Đề tài:** Phát triển hệ thống phân đoạn tổn thương xương trên ảnh X-quang dựa trên câu nhắc trực quan  
**Bộ dữ liệu chính:** BTXRD và FracAtlas  
**Kết quả chính:** Trong thiết lập phân đoạn có hướng dẫn bằng hộp giới hạn, PGA-UNet đạt Dice `0.8607` trên BTXRD ở độ phân giải `512x512`, cao hơn U-Net và Attention U-Net; ở so sánh cùng điều kiện câu nhắc và độ phân giải `256x256`, PGA-UNet đạt Dice `0.8433`, cao hơn SAM-Med2D đã tinh chỉnh (`0.7541`). Mô hình trong report hiện được mô tả là có khoảng `3 triệu` tham số.

---

## Cấu trúc thư mục

```text
PGA_Unet2D/
├── Report/              # Báo cáo LaTeX
├── Source/              # Notebook thực nghiệm + mã nguồn
├── Result/              # Notebook đã chạy xong, có output
├── diagrams/            # File DrawIO nguồn của các sơ đồ
├── Xư_ly.md             # Ghi chú xử lý công việc hiện tại
├── Bao_cao_tien_do.md   # Ghi chú tiến độ hiện hành
└── Đánh giá.md          # Ghi chú phản biện và nhận xét học thuật
```

---

## Report/

Báo cáo LaTeX chính nằm trong `Report/`. Nếu môi trường có LaTeX đầy đủ, có thể biên dịch từ `Report/main.tex`.

| File/Folder | Nội dung |
|---|---|
| `main.tex` | File gốc để build toàn bộ báo cáo |
| `main.pdf` | Bản PDF đã biên dịch gần nhất |
| `Chapter1/` | Giới thiệu, bài toán, phạm vi, đóng góp |
| `Chapter2/` | Công trình liên quan và cơ sở lý thuyết |
| `Chapter3/` | Mô hình PGA-UNet và luồng xử lý |
| `Chapter4/` | Thực nghiệm và đánh giá |
| `Chapter5/` | Kết luận, hạn chế, hướng phát triển |
| `Appendix/` | Tóm tắt, phụ lục phân tích, biểu mẫu kèm theo |
| `References/references.bib` | Danh mục tài liệu tham khảo |
| `images/` | Hình dùng trong báo cáo |

### Một số hình quan trọng trong `Report/images/`

| File | Vai trò |
|---|---|
| `arch_pga_unet2d.png` | Kiến trúc PGA-UNet |
| `arch_unet2d.png` | Kiến trúc U-Net |
| `arch_attention_unet2d.png` | Kiến trúc Attention U-Net |
| `arch_sammed2d.png` | Kiến trúc SAM-Med2D |
| `pipeline_pga_app_inference.png` | Luồng xử lý có Gatekeeper và PGA-UNet |
| `chart_sam_comparison_256.png` | So sánh PGA-UNet và SAM-Med2D ở `256x256` |
| `chart_resolution_btxrd_fracatlas.png` | Ảnh hưởng của độ phân giải |
| `qual_robustness_zoom_shift.png` | Minh họa phản ứng với câu nhắc lệch tâm |

---

## Source/

Thư mục `Source/` chứa notebook huấn luyện, đánh giá và mã nguồn mô hình. Phần lớn notebook được thiết kế để chạy trên Colab hoặc Kaggle.

### Notebook huấn luyện chính

| Notebook | Nội dung |
|---|---|
| `Source/File_Train/PGA_Unet2D.ipynb` | Huấn luyện PGA-UNet |
| `Source/File_Train/Unet2D.ipynb` | Huấn luyện U-Net |
| `Source/File_Train/Attention_Unet2D.ipynb` | Huấn luyện Attention U-Net |
| `Source/File_Train/Finetune_SAMMed2D_test_robust.ipynb` | Tinh chỉnh SAM-Med2D |

### Notebook đánh giá và phân tích

| Notebook | Nội dung |
|---|---|
| `Source/File_Test/test-pga-samzs-samft-r256.ipynb` | So sánh PGA-UNet với SAM-Med2D |
| `Source/File_Test/pga-vs-unet2d-r512.ipynb` | So sánh PGA-UNet với U-Net ở `512x512` |
| `Source/File_Test/test-subcat-pga-vs-baseline.ipynb` | Phân tích theo nhóm ảnh với baseline |
| `Source/File_Test/test-subcat-pga-vs-sam-r256-r512.ipynb` | Phân tích theo nhóm ảnh với SAM-Med2D |
| `Source/File_Test/test-pipeline-evaluation.ipynb` | Đánh giá luồng hai giai đoạn |
| `PGA_Extended_Test.ipynb` | Kiểm tra thêm về các kịch bản câu nhắc |

### Mã nguồn mô hình

Mã nguồn chính nằm trong:

```text
Source/Prompt-Guided-XRay-Segmentation/
├── dataset.py
├── train.py
└── models/
    ├── networks/
    │   └── prompt_unet_2D.py
    └── layers/
        └── grid_attention_layer.py
```

Trong đó:
- `prompt_unet_2D.py` chứa triển khai PGA-UNet, gồm PSG và CAD.
- `grid_attention_layer.py` chứa cổng chú ý nền được tái sử dụng trong decoder.

---

## Result/

`Result/` chứa các notebook đã chạy xong, có sẵn output để tra cứu số liệu mà không cần chạy lại toàn bộ thí nghiệm.

| Thư mục/File | Nội dung |
|---|---|
| `Result/Result_BTXRD/` | Kết quả trên BTXRD |
| `Result/Result_FracAtlas/` | Kết quả trên FracAtlas |
| `Result/Result_BTXRD/Ablation/` | Kết quả ablation trên BTXRD |
| `Result/Result_FracAtlas/Ablation/` | Kết quả ablation trên FracAtlas |
| `Result/Result_BTXRD/pipeline/` | Kết quả luồng có Gatekeeper trên BTXRD |
| `Result/Result_FracAtlas/pipeline/` | Kết quả luồng có Gatekeeper trên FracAtlas |

---

## diagrams/

Chứa các sơ đồ nguồn DrawIO dùng để xuất hình cho report.

| File | Ghi chú |
|---|---|
| `arch_pga_unet2d.drawio` | Sơ đồ PGA-UNet |
| `arch_unet2d.drawio` | Sơ đồ U-Net |
| `arch_attention_unet2d.drawio` | Sơ đồ Attention U-Net |
| `arch_sammed2d.drawio` | Sơ đồ SAM-Med2D |
| `pipeline_pga_app_inference.drawio` | Luồng suy luận của hệ thống hỗ trợ |
| `classification_pipeline.drawio` | Sơ đồ phần sàng lọc hỗ trợ |

---

## Ghi chú về phạm vi kết quả

- Các kết quả tốt nhất của PGA-UNet trong report hiện được diễn giải trong phạm vi **phân đoạn có hướng dẫn bằng hộp giới hạn**.
- Với ảnh có nhiều tổn thương, phần đánh giá trong report sử dụng số lượng và vị trí hộp được suy ra từ nhãn gốc để đo chất lượng phân đoạn khi đã có thông tin định vị sơ bộ.
- Vì vậy, không nên đọc README này như mô tả một hệ thống phát hiện tổn thương hoàn toàn tự động.
