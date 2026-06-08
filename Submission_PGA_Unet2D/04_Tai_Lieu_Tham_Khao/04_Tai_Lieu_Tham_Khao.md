# Tài Liệu Tham Khảo

---

## Các Bài Báo Trực Tiếp Sử Dụng / Tham Chiếu Trong Đề Tài

| # | Tác giả | Tiêu đề | Nơi công bố | Năm |
|---|---|---|---|---|
| [1] | Ronneberger O., Fischer P., Brox T. | U-Net: Convolutional Networks for Biomedical Image Segmentation | MICCAI, Springer, pp. 234–241 | 2015 |
| [2] | Oktay O. et al. | Attention U-Net: Learning Where to Look for the Pancreas | Medical Imaging with Deep Learning (MIDL) | 2018 |
| [3] | Cheng J. et al. | SAM-Med2D | arXiv:2308.16184 | 2023 |
| [4] | Tan M., Le Q.V. | EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks | ICML | 2019 |
| [5] | Nguyen M.D. et al. | BTXRD: A Radiograph Dataset for the Classification, Localization, and Segmentation of Primary Bone Tumors | Nature Scientific Data | 2024 |
| [6] | Ultralytics | YOLO11 | GitHub: ultralytics/ultralytics | 2024 |

---

## Công Cụ và Nền Tảng

| Công cụ | Mục đích | Phiên bản / Nguồn |
|---|---|---|
| PyTorch | Framework học sâu chính | ≥ 2.0 |
| torchvision | EfficientNet_B3 pretrained | timm / torchvision |
| Roboflow | Gán nhãn bounding box nhiễu R/L | roboflow.com |
| YOLOv11s | Phát hiện và xóa nhiễu R/L trong tiền xử lý | ultralytics v8 |
| Google Colab | Môi trường huấn luyện (GPU T4/A100) | colab.research.google.com |
| OpenCV | Xử lý ảnh, tạo Plateau Heatmap, inpainting | cv2 ≥ 4.5 |
| Gradio | Giao diện demo ứng dụng app.py | gradio.app |

---

## Ghi Chú

- File BibTeX đầy đủ: `Report/References/references.bib`
- Tất cả bài báo có file PDF lưu tại `Report/References/`
- EfficientNet được sử dụng qua `torchvision.models.efficientnet_b3` với trọng số pretrained ImageNet
