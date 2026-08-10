## Bước 1 – Chuẩn bị môi trường
- pip install torch torchvision opencv-python scipy matplotlib tqdm

## Tiền xử lý đầu vào
- Ảnh, mask và prompt map đều dùng quy trình `resize + padding`, không kéo giãn trực tiếp về khung vuông.
- Cạnh dài được co về `img_size`, sau đó đệm nền để tạo ảnh vuông `img_size x img_size`.
- `image` dùng `cv2.INTER_LINEAR`, `mask` dùng `cv2.INTER_NEAREST`, `prompt_map` dùng `cv2.INTER_LINEAR`.
- Prompt chỉ còn 2 chế độ: `zoom_out` và `shift`.
- `zoom_out` khi train được lấy ngẫu nhiên trong khoảng `0.15-0.45`; khi test dùng một mức cố định là `0.30`.
- `shift` dùng độ lệch tương đối `0.30`.
- Tham số prompt phụ thuộc độ phân giải:
  - `img_size=256` → khoảng ngữ cảnh tối thiểu quanh GT là `5 px`, Gaussian kernel `31`
  - `img_size=512` → khoảng ngữ cảnh tối thiểu quanh GT là `10 px`, Gaussian kernel `61`

## Cấu trúc thư mục cần có:
# dataset_<DATASET_NAME>/
  - train/images/  train/annotations/
  - val/images/    val/annotations/
  - test/images/   test/annotations/
# models/
  - layers/grid_attention_layer.py
  - networks/prompt_unet_2D.py     ← file vừa viết
  - networks_other.py
# dataset.py
# train.py
# test_exp.py

## Bước 2 – Huấn luyện với prompt bao trọn
# Trong train.py: TRAIN_PROMPT_MODE='zoom_out', USE_ENCODER_PROMPT=False
- đặt `PROMPT_DATASET_ROOT=dataset_<DATASET_NAME>`
- python train.py
# → checkpoints/pga_unet_zoom_out_256_best.pth hoặc _512_best.pth
- python test_exp.py
# → in bảng 6 metrics, show các ảnh test (cần show ảnh nào thì ghi tên ảnh đó ở int main)

## Bước 3 – Huấn luyện với prompt bao trọn + Encoder Prompt
# Trong train.py: TRAIN_PROMPT_MODE='zoom_out', USE_ENCODER_PROMPT=True
- python train.py
- python test_exp.py
# → so sánh Dice/CBL với bước 2

## Bước 4 – Huấn luyện với prompt lệch tâm
# Trong train.py: TRAIN_PROMPT_MODE='shift', USE_ENCODER_PROMPT=True
- python train.py
# → checkpoints/pga_unet_shift_256_best.pth hoặc _512_best.pth
- python test_exp.py
# → bảng 2 kịch bản `zoom_out` và `shift`, show các ảnh test (cần show ảnh nào thì ghi tên ảnh đó ở int main)
