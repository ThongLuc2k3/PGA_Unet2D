## Bước 1 – Chuẩn bị môi trường
- pip install torch torchvision opencv-python scipy matplotlib tqdm

## Tiền xử lý đầu vào
- Ảnh, mask và prompt map đều dùng quy trình `resize + padding`, không kéo giãn trực tiếp về khung vuông.
- Cạnh dài được co về `img_size`, sau đó đệm nền để tạo ảnh vuông `img_size x img_size`.
- `image` dùng `cv2.INTER_LINEAR`, `mask` dùng `cv2.INTER_NEAREST`, `prompt_map` dùng `cv2.INTER_LINEAR`.

## Cấu trúc thư mục cần có:
# dataset_BTXRD/
  - train/images/  train/annotations/
  - val/images/    val/annotations/
  - test/images/   test/annotations/
# models/
  - layers/grid_attention_layer.py
  - networks/prompt_unet_2D.py     ← file vừa viết
  - networks_other.py
# dataset.py
# train.py
# test_expA.py
# test_expB.py

## Bước 2 – Thí nghiệm A (baseline sạch, zoom-out only)
# Trong train.py: EXPERIMENT='A', USE_ENCODER_PROMPT=False
- python train.py
# → checkpoints/pga_unet_expA_best.pth
- python test_expA.py
# → in bảng 6 metrics, show các ảnh test (cần show ảnh nào thì ghi tên ảnh đó ở int main)

## Bước 3 – Thí nghiệm A + Encoder Prompt (so sánh với bước 2)
# Trong train.py: EXPERIMENT='A', USE_ENCODER_PROMPT=True
- python train.py
- python test_expA.py
# → so sánh Dice/CBL với bước 2

## Bước 4 – Thí nghiệm B (zoom-out + shift)
# Trong train.py: EXPERIMENT='B', USE_ENCODER_PROMPT=True
- python train.py
# → checkpoints/pga_unet_expB_best.pth
- python test_expB.py
# → bảng 3 kịch bản, how các ảnh test (cần show ảnh nào thì ghi tên ảnh đó ở int main)
# → ảnh result_inference_check_*.png (cải tiến inference)
