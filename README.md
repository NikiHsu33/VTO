# PromptDresser Docker 專案

這是一個基於 Docker 的 PromptDresser 專案，用於虛擬試衣（Virtual Try-On）任務。支援本地 Docker 環境和 Kaggle GPU 環境。

## 🚀 快速開始

### 方法 1: 本地 Docker 環境

#### 1. 設定環境變數

複製環境變數範例檔案並設定您的 Hugging Face Token：

```bash
cp env.example .env
# 編輯 .env 檔案，加入您的 HF_TOKEN
```

#### 2. 建立並啟動容器

```bash
# 建立 Docker 映像檔
make build

# 啟動容器（含 GPU 支援）
make up
```

#### 3. 下載預訓練模型

```bash
# 下載所需的預訓練模型
make models
```

#### 4. 修補配置檔案

```bash
# 生成無提示詞的配置檔案
make patch
```

#### 5. 執行推論

```bash
# 執行推論（預設參數）
make infer
```

### 方法 2: Kaggle GPU 環境

#### 1. 在 Kaggle Notebook 中克隆專案

```python
# 第一個 cell：克隆專案
!git clone https://github.com/your-username/promptdresser-vto.git
%cd promptdresser-vto
```

#### 2. 設定環境

```python
# 第二個 cell：設定環境
!python kaggle_setup.py
```

#### 3. 設定 Token 並下載模型

```python
# 第三個 cell：設定 Token 和下載模型
import os
os.environ['HF_TOKEN'] = 'hf_your_token_here'
!python scripts/download_models.py
```

#### 4. 修補配置並準備資料集

```python
# 第四個 cell：修補配置
!python scripts/patch_config.py

# 第五個 cell：準備資料集（上傳您的 VITON-HD 資料集）
import zipfile
with zipfile.ZipFile('/kaggle/input/viton-hd-test/viton_hd_test.zip', 'r') as zip_ref:
    zip_ref.extractall('data/zalando-hd-resized/')
```

#### 5. 執行推論

```python
# 第六個 cell：執行推論
!python kaggle_inference.py
```

## 📁 資料集設定

### VITON-HD 測試集

將 VITON-HD 測試集放置在 `./data/zalando-hd-resized/` 目錄下，確保包含以下結構：

```
data/
└── zalando-hd-resized/
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

### 檢查資料集完整性

```bash
# 檢查資料集結構是否完整
make check
```

## 評估

專案提供兩種評估方法：

### 1. FID/KID 評估

```bash
# 在容器內執行
docker exec -it promptdresser python tools/eval.py \
    --mode fid_kid \
    --gen_dir /workspace/PromptDresser/sampled_images/local-demo \
    --real_dir /workspace/PromptDresser/DATA/zalando-hd-resized/test_fine/image
```

### 2. Masked LPIPS 評估

```bash
# 在容器內執行
docker exec -it promptdresser python tools/eval.py \
    --mode masked_lpips \
    --gen_dir /workspace/PromptDresser/sampled_images/local-demo \
    --real_dir /workspace/PromptDresser/DATA/zalando-hd-resized/test_fine/cloth \
    --mask_dir /workspace/PromptDresser/DATA/zalando-hd-resized/test_fine/agnostic-mask
```

## 常用命令

### 本地 Docker 環境

```bash
# 進入容器
make shell

# 停止容器
make down

# 清理所有資源
make clean

# 顯示所有可用命令
make help
```

### Kaggle 環境

```python
# 測試環境
!python test_kaggle.py

# 檢查資料集
!python tools/check_dataset.py data/zalando-hd-resized

# 查看結果
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

result_dir = 'outputs/kaggle-demo/paired'
if os.path.exists(result_dir):
    images = [f for f in os.listdir(result_dir) if f.endswith(('.png', '.jpg'))]
    if images:
        img = mpimg.imread(os.path.join(result_dir, images[0]))
        plt.imshow(img)
        plt.axis('off')
        plt.show()
```

## 目錄結構

```
.
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yaml
├── scripts/
│   ├── download_models.py
│   └── patch_config.py
├── tools/
│   ├── check_dataset.py
│   └── eval.py
├── data/                    # 掛載到容器內的資料集
├── outputs/                 # 掛載到容器內的輸出目錄
├── pretrained_models/       # 掛載到容器內的預訓練模型
├── kaggle_setup.py          # Kaggle 環境設定
├── kaggle_inference.py      # Kaggle 推論腳本
├── test_kaggle.py           # Kaggle 環境測試
├── requirements_kaggle.txt  # Kaggle 套件清單
├── Makefile
├── env.example
├── README.md
├── SETUP_GUIDE.md
└── KAGGLE_GUIDE.md
```

## 故障排除

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

### Kaggle 相關問題

1. **記憶體不足**
   ```python
   # 清理記憶體
   import gc
   import torch
   gc.collect()
   torch.cuda.empty_cache()
   ```

2. **模型下載失敗**
   ```python
   # 檢查網路連線
   !ping -c 3 huggingface.co
   
   # 重新下載模型
   !python scripts/download_models.py
   ```

### 記憶體不足

如果遇到 CUDA 記憶體不足錯誤，可以：
1. 減少 `--num_inference_steps` 參數
2. 減少批次大小
3. 使用更小的模型

### 模型下載失敗

1. 檢查 HF_TOKEN 是否正確設定
2. 確保網路連線正常
3. 檢查磁碟空間是否足夠

## 注意事項

- `.env` 檔案包含敏感資訊，不會被 commit 到 Git
- 資料集和模型檔案較大，請確保有足夠的磁碟空間
- 首次建立映像檔可能需要較長時間
- 建議使用至少 16GB GPU 記憶體（推薦 24GB+）
- Kaggle 環境有執行時間限制（9小時）

## 授權

本專案基於 PromptDresser 原始碼，請參考原始專案的授權條款。
