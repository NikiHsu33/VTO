# Kaggle GPU 環境使用指南

## 🚀 快速開始

### 1. 在 Kaggle Notebook 中設定環境

```python
# 第一個 cell：執行環境設定
!python kaggle_setup.py
```

### 2. 設定 Hugging Face Token

```python
# 第二個 cell：設定環境變數
import os
os.environ['HF_TOKEN'] = 'hf_your_token_here'
```

### 3. 下載預訓練模型

```python
# 第三個 cell：下載模型
!python scripts/download_models.py
```

### 4. 修補配置檔案

```python
# 第四個 cell：修補配置
!python scripts/patch_config.py
```

### 5. 準備資料集

#### 方法 1：上傳資料集到 Kaggle
1. 將 VITON-HD 測試集打包成 zip 檔案
2. 在 Kaggle 中上傳資料集
3. 解壓到正確位置

```python
# 第五個 cell：解壓資料集
import zipfile
import os

# 假設資料集檔案名為 viton_hd_test.zip
with zipfile.ZipFile('/kaggle/input/viton-hd-test/viton_hd_test.zip', 'r') as zip_ref:
    zip_ref.extractall('data/zalando-hd-resized/')
```

#### 方法 2：使用現有資料集
```python
# 如果資料集已經在 /kaggle/input/ 中
import shutil
shutil.copytree('/kaggle/input/viton-hd-test/', 'data/zalando-hd-resized/')
```

### 6. 檢查資料集

```python
# 第六個 cell：檢查資料集
!python tools/check_dataset.py data/zalando-hd-resized
```

### 7. 執行推論

```python
# 第七個 cell：執行推論
!python kaggle_inference.py
```

## 📋 完整的 Kaggle Notebook 範例

```python
# Cell 1: 環境設定
!python kaggle_setup.py

# Cell 2: 設定 Token
import os
os.environ['HF_TOKEN'] = 'hf_your_token_here'

# Cell 3: 下載模型
!python scripts/download_models.py

# Cell 4: 修補配置
!python scripts/patch_config.py

# Cell 5: 準備資料集
import zipfile
with zipfile.ZipFile('/kaggle/input/viton-hd-test/viton_hd_test.zip', 'r') as zip_ref:
    zip_ref.extractall('data/zalando-hd-resized/')

# Cell 6: 檢查資料集
!python tools/check_dataset.py data/zalando-hd-resized

# Cell 7: 執行推論
!python kaggle_inference.py

# Cell 8: 查看結果
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

# 顯示生成的圖片
result_dir = 'outputs/kaggle-demo/paired'
if os.path.exists(result_dir):
    images = [f for f in os.listdir(result_dir) if f.endswith(('.png', '.jpg'))]
    if images:
        img = mpimg.imread(os.path.join(result_dir, images[0]))
        plt.imshow(img)
        plt.axis('off')
        plt.show()
```

## 🔧 Kaggle 環境特點

### 優勢
- ✅ 免費 GPU 資源（P100 或 T4）
- ✅ 預裝 Python 和常用套件
- ✅ 無需本地設定
- ✅ 可以直接分享結果

### 限制
- ⚠️ 執行時間限制（9小時）
- ⚠️ 記憶體限制（16GB RAM）
- ⚠️ 磁碟空間限制（20GB）
- ⚠️ 網路連線限制

## 📊 記憶體優化建議

### 1. 減少批次大小
```python
# 在推論時使用較小的批次
cmd = [
    'python', 'PromptDresser/inference.py',
    '--config_p', 'PromptDresser/configs/VITONHD_noprompt.yaml',
    '--save_name', 'kaggle-demo',
    '--num_inference_steps', '20',  # 減少步數
    '--s_idx', '0',
    '--e_idx', '2'  # 減少圖片數量
]
```

### 2. 使用較小的模型
```python
# 如果記憶體不足，可以考慮使用較小的模型
# 但需要修改 PromptDresser 的配置
```

### 3. 清理記憶體
```python
# 在執行推論前清理記憶體
import gc
import torch

gc.collect()
torch.cuda.empty_cache()
```

## 🛠️ 故障排除

### 1. 記憶體不足
```python
# 檢查 GPU 記憶體
!nvidia-smi

# 清理記憶體
import gc
import torch
gc.collect()
torch.cuda.empty_cache()
```

### 2. 模型下載失敗
```python
# 檢查網路連線
!ping -c 3 huggingface.co

# 重新下載模型
!python scripts/download_models.py
```

### 3. 資料集路徑問題
```python
# 檢查資料集結構
!find data/ -type f | head -10

# 重新準備資料集
!python prepare_dataset.py
```

## 📁 檔案結構

```
/working/
├── kaggle_setup.py          # Kaggle 環境設定
├── kaggle_inference.py      # Kaggle 推論腳本
├── scripts/
│   ├── download_models.py   # 下載模型
│   └── patch_config.py      # 修補配置
├── tools/
│   ├── check_dataset.py     # 檢查資料集
│   └── eval.py              # 評估腳本
├── data/
│   └── zalando-hd-resized/  # 資料集
├── outputs/                 # 輸出結果
├── pretrained_models/       # 預訓練模型
└── PromptDresser/           # 主專案
```

## 🎯 最佳實踐

1. **分階段執行**: 將設定和推論分成不同的 cell
2. **定期儲存**: 使用 Kaggle 的儲存功能保存重要結果
3. **監控資源**: 定期檢查 GPU 和記憶體使用情況
4. **錯誤處理**: 在每個步驟後檢查是否成功
5. **結果備份**: 將重要結果下載到本地

## 📝 注意事項

- Kaggle 環境會在 9 小時後自動停止
- 建議在執行長時間任務前先測試小規模推論
- 記得在 `.env` 檔案中設定正確的 HF_TOKEN
- 資料集檔案較大，上傳時需要耐心等待
