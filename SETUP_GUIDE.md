# PromptDresser 設定指南

## 🚀 快速開始

### 1. 環境準備

#### 1.1 啟動 Docker Desktop
在 macOS 上，請啟動 Docker Desktop 應用程式。

#### 1.2 設定 Hugging Face Token
編輯 `.env` 檔案，加入您的 HF_TOKEN：

```bash
# 編輯 .env 檔案
HF_TOKEN=hf_your_token_here
```

### 2. 建立並啟動容器

```bash
# 建立 Docker 映像檔
make build

# 啟動容器（含 GPU 支援）
make up
```

### 3. 下載預訓練模型

```bash
# 下載 SDXL / Inpainting / VAE 模型
make models
```

這會下載以下模型到 `./pretrained_models/`：
- `stabilityai/stable-diffusion-xl-base-1.0`
- `diffusers/stable-diffusion-xl-1.0-inpainting-0.1`
- `madebyollin/sdxl-vae-fp16-fix`

## 📁 資料集準備

### 方法 1：手動準備

將 VITON-HD 測試集放入 `./data/zalando-hd-resized/` 目錄，確保包含：

```
data/zalando-hd-resized/
├── test_fine/
│   ├── image/
│   ├── image-densepose/
│   ├── agnostic-mask/
│   └── cloth/
├── test_coarse/
│   ├── image/
│   ├── image-densepose/
│   ├── agnostic-mask/
│   └── cloth/
├── test_pairs.txt
└── test_unpairs.txt
```

### 方法 2：自動準備

如果只有 `test/` 目錄，可以自動複製為 `test_fine/` 和 `test_coarse/`：

```bash
# 先將資料放入 data/zalando-hd-resized/test/
python prepare_dataset.py copy
```

## 🔍 檢查與修補

### 檢查資料集完整性

```bash
# 檢查資料夾結構是否完整
make check
```

### 修補配置檔案

```bash
# 生成無提示詞的配置檔案
make patch
```

這會生成 `configs/VITONHD_noprompt.yaml`，將 `dataset.text_file_postfix` 設為 `None`。

## 🎯 執行推論

### 最小推論測試（3-4 張圖片）

```bash
# 執行推論
make infer
```

輸出結果會在：
- `./outputs/local-demo/paired/`
- `./outputs/local-demo/unpaired/`

## 📊 評估（可選）

### 準備參考資料

建立真實穿搭的參考資料夾：

```bash
mkdir -p real_ref
# 將真實穿搭圖片放入 real_ref/
```

### 執行評估

```bash
# FID/KID 評估
docker compose -f docker/docker-compose.yaml exec promptdresser \
  python tools/eval.py --mode fid_kid \
  --gen_dir ./sampled_images/local-demo/paired \
  --real_dir ./real_ref

# Masked LPIPS 評估
docker compose -f docker/docker-compose.yaml exec promptdresser \
  python tools/eval.py --mode masked_lpips \
  --gen_dir ./sampled_images/local-demo/paired \
  --real_dir ./DATA/zalando-hd-resized/test_fine/cloth \
  --mask_dir ./DATA/zalando-hd-resized/test_fine/agnostic-mask
```

## 🛠️ 常用命令

```bash
# 進入容器
make shell

# 停止容器
make down

# 清理所有資源
make clean

# 檢查環境設定
python test_setup.py
```

## ❗ 故障排除

### Docker 相關問題

1. **Docker daemon 未運行**
   ```bash
   # 啟動 Docker Desktop
   # 或檢查 Docker 狀態
   docker ps
   ```

2. **GPU 不可用**
   ```bash
   # 檢查 GPU 是否可用
   docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu20.04 nvidia-smi
   ```

### 模型下載問題

1. **HF_TOKEN 未設定**
   - 檢查 `.env` 檔案中的 `HF_TOKEN` 是否正確

2. **網路連線問題**
   - 確保網路連線正常
   - 檢查防火牆設定

### 記憶體不足

如果遇到 CUDA 記憶體不足：
1. 減少 `--num_inference_steps` 參數
2. 減少批次大小
3. 關閉其他 GPU 應用程式

## 📝 注意事項

- `.env` 檔案包含敏感資訊，不會被 commit 到 Git
- 資料集和模型檔案較大，請確保有足夠的磁碟空間
- 首次建立映像檔可能需要較長時間
- 建議使用至少 16GB GPU 記憶體（推薦 24GB+）
