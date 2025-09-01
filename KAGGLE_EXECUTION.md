# Kaggle 執行指南

## 🚨 重要提醒

**請勿直接複製貼上程式碼！** 這會導致不可見字符錯誤。

## 📋 正確的執行方式

### Cell 1: 克隆專案
```python
!git clone https://github.com/NikiHsu33/VTO.git
%cd VTO
```

### Cell 2: 設定 Token
```python
import os
os.environ['HF_TOKEN'] = 'hf_your_token_here'
```

### Cell 3: 安裝套件
```python
!pip install huggingface_hub python-dotenv
```

### Cell 4: 設定環境
```python
!python kaggle_setup.py
```

### Cell 5: 下載模型
```python
!python scripts/download_models.py
```

### Cell 6: 修補配置
```python
!python scripts/patch_config.py
```

### Cell 7: 準備資料集
```python
import zipfile
with zipfile.ZipFile('/kaggle/input/viton-hd-test/viton_hd_test.zip', 'r') as zip_ref:
    zip_ref.extractall('data/zalando-hd-resized/')
```

### Cell 8: 檢查資料集
```python
!python tools/check_dataset.py data/zalando-hd-resized
```

### Cell 9: 執行推論
```python
!python kaggle_inference.py
```

## 🔧 替代方案：一鍵執行

如果上述方法仍有問題，可以使用一鍵執行腳本：

```python
# 克隆專案
!git clone https://github.com/NikiHsu33/VTO.git
%cd VTO

# 設定 Token
import os
os.environ['HF_TOKEN'] = 'hf_your_token_here'

# 一鍵執行
!python kaggle_quickstart.py
```

## 🛠️ 故障排除

### 1. 字符錯誤
- **症狀**: `SyntaxError: invalid non-printable character U+00A0`
- **解決**: 手動輸入程式碼，不要複製貼上

### 2. 權限錯誤
```python
!chmod +x *.py
!chmod +x scripts/*.py
!chmod +x tools/*.py
```

### 3. 路徑錯誤
```python
import os
print("當前目錄:", os.getcwd())
print("檔案列表:", os.listdir())
```

### 4. 套件安裝失敗
```python
!pip install --upgrade pip
!pip install huggingface_hub python-dotenv --force-reinstall
```

## 📝 最佳實踐

1. **逐個 Cell 執行**，不要一次執行多個
2. **手動輸入關鍵程式碼**，避免複製貼上
3. **檢查每個步驟的輸出**，確保成功
4. **定期清理記憶體**：
   ```python
   import gc
   import torch
   gc.collect()
   torch.cuda.empty_cache()
   ```

## 🎯 預期結果

成功執行後，您應該看到：
- ✅ 專案克隆成功
- ✅ 模型下載完成
- ✅ 配置修補成功
- ✅ 推論執行完成
- 📁 結果在 `outputs/kaggle-demo/` 目錄

## 📞 如果仍有問題

1. 檢查 Kaggle 環境是否正常
2. 確認網路連線
3. 檢查 HF_TOKEN 是否正確
4. 查看錯誤訊息的具體內容
