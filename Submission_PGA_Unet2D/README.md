# Khóa Luận Tốt Nghiệp — PGA-UNet

**Đề tài:** Phát triển hệ thống phân đoạn ảnh X-quang xương dựa vào câu nhắc trực quan (Visual Prompt)

**Tác giả:** Lục Tố Thông  
**Giảng viên hướng dẫn:** [Tên thầy/cô]  
**Trường:** Đại học Khoa học Tự nhiên — ĐHQG TP.HCM  
**Năm:** 2026

---

## Đóng góp khoa học chính

1. **Kiến trúc PGA-UNet**: Tích hợp Prompt Spatial Gate và Conditioned Attention vào U-Net để phân đoạn có dẫn hướng từ bounding box của bác sĩ
2. **Mã hóa Gaussian Heatmap**: Chuyển đổi bounding box thành plateau heatmap (Gaussian blur kernel 31×31) — khác với SAM dùng sparse positional embedding
3. **IPR (Iterative Prompt Refinement)**: Tự động tinh chỉnh prompt qua 3 vòng lặp, hội tụ tại k=2, tổng ≤180ms
4. **GradCAM Rescue**: Cơ chế phòng vệ end-to-end: phát hiện prompt xấu → GradCAM gợi ý vùng tổn thương → IPR phục hồi. Tỷ lệ phát hiện 100% (174/174)
5. **MobileNetV4 Gatekeeper**: Phân loại có/không bệnh (AUC-ROC=0.9514, Recall=89.64%) trước khi phân đoạn

---

## Kết quả chính

| Mô hình | Dice↑ | IoU↑ | HD95↓ | CBL↑ |
|---------|-------|------|-------|------|
| U-Net (baseline) | 0.5090 | 0.4125 | 125.12px | 0.6457 |
| Attention U-Net | 0.4110 | 0.3212 | 141.23px | 0.5917 |
| SAM-Med2D zero-shot | 0.5298 | 0.3867 | 111.27px | 0.8199 |
| SAM-Med2D fine-tuned | 0.7624 | 0.6424 | 52.08px | 0.9003 |
| **PGA-UNet (ours)** | **0.8558** | **0.7552** | **12.79px** | **0.9532** |

*Kịch bản Mixed 70/30 (thực tế nhất), N=248 test samples*

---

## Cấu trúc thư mục

```
01_Bao_Cao/              Báo cáo PDF + Slide thuyết trình
02_Ma_Nguon/             Source code đầy đủ
  ├── models/            Kiến trúc PGA-UNet, U-Net, Attention U-Net
  ├── dataset_pga.py     Dataset loader với 3 prompt modes
  ├── dataset_simple.py  Dataset loader cho baseline models
  ├── train_pga.py       Training script PGA-UNet
  ├── train_unet.py      Training script U-Net
  ├── train_attunet.py   Training script Attention U-Net
  ├── app.py             Demo Gradio UI
  └── requirements.txt   Thư viện cần thiết
03_Ket_Qua_Thuc_Nghiem/ Số liệu + ảnh kết quả
  ├── Metrics_Detail.csv Bảng số liệu đầy đủ tất cả mô hình
  └── images/            Ảnh visualization kết quả phân đoạn
04_So_Do_Kien_Truc/      Sơ đồ kiến trúc (.drawio + .png)
```

---

## Dataset & Checkpoints (Google Drive)

| Nội dung | Link |
|----------|------|
| Dataset BTXRD (train/val/test) | https://drive.google.com/file/d/1fU7KPln7joaa3EZZtGn-VKeg9i4AmPG3 |
| PGA-UNet checkpoint | https://drive.google.com/file/d/1Mv-rUPI7KGmYemd27hmKbJQRHc4ZKB9z |
| SAM-Med2D fine-tuned | https://drive.google.com/file/d/1fTEhbgpEzzEqdB8CEW8wH8KnX1YlJJM4 |
| MobileNetV4 Gatekeeper | [Điền link Drive] |
| Result notebooks (Kaggle) | [Điền link Drive] |

---

## Hướng dẫn chạy Demo

```bash
git clone https://github.com/ThongLuc2k3/Prompt-Guided-XRay-Segmentation.git
cd Prompt-Guided-XRay-Segmentation
pip install -r requirements.txt
python app.py
```

Mở trình duyệt tại `http://localhost:7860`

---

## Notebooks thực nghiệm (chạy trên Kaggle/Colab)

| Notebook | Mục đích |
|----------|----------|
| `Source/PGA_Unet2D.ipynb` | Train + test PGA-UNet |
| `Source/Unet2D.ipynb` | Train + test U-Net baseline |
| `Source/Attention_Unet2D.ipynb` | Train + test Attention U-Net |
| `Source/Finetune_SAMMed2D_test_robust.ipynb` | Fine-tune + test SAM-Med2D |
| `Source/SAMMed2D_ZeroShot.ipynb` | Test SAM-Med2D zero-shot |
| `Source/PGA_GradCAM_IPR.ipynb` | Thực nghiệm GradCAM + IPR phòng vệ |
| `Source/PGA_Extended_Test.ipynb` | Extended test 3 prompt modes |
| `Source/Defense_Comparison_SAM_vs_PGA.ipynb` | So sánh phòng hộ SAM vs PGA |
