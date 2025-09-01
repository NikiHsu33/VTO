# 部署指南：GitHub + Kaggle

## 🚀 快速部署到 GitHub

### 1. 初始化 Git 倉庫

```bash
# 執行初始化腳本
python init_github.py
```

這個腳本會：
- 初始化 Git 倉庫
- 添加所有檔案
- 提交初始版本
- 提示您輸入 GitHub 倉庫 URL
- 推送到 GitHub

### 2. 手動部署（如果自動腳本失敗）

```bash
# 初始化 Git
git init

# 添加檔案
git add .

# 提交
git commit -m "Initial commit: PromptDresser VTO Project"

# 在 GitHub 上建立新倉庫後，添加遠端
git remote add origin https://github.com/your-username/promptdresser-vto.git

# 推送
git push -u origin main
```

## 🎯 在 Kaggle 中使用

### 方法 1: 一鍵執行（推薦）

```python
# Cell 1: 克隆專案
!git clone https://github.com/your-username/promptdresser-vto.git
%cd promptdresser-vto

# Cell 2: 設定 Token
import os
os.environ['HF_TOKEN'] = 'hf_your_token_here'

# Cell 3: 一鍵執行所有步驟
!python kaggle_quickstart.py
```

### 方法 2: 分步驟執行

```python
# Cell 1: 克隆專案
!git clone https://github.com/your-username/promptdresser-vto.git
%cd promptdresser-vto

# Cell 2: 設定 Token
import os
os.environ['HF_TOKEN'] = 'hf_your_token_here'

# Cell 3: 設定環境
!python kaggle_setup.py

# Cell 4: 下載模型
!python scripts/download_models.py

# Cell 5: 修補配置
!python scripts/patch_config.py

# Cell 6: 準備資料集（上傳您的 VITON-HD 資料集）
import zipfile
with zipfile.ZipFile('/kaggle/input/viton-hd-test/viton_hd_test.zip', 'r') as zip_ref:
    zip_ref.extractall('data/zalando-hd-resized/')

# Cell 7: 檢查資料集
!python tools/check_dataset.py data/zalando-hd-resized

# Cell 8: 執行推論
!python kaggle_inference.py
```

## 📁 檔案說明

### 核心檔案
- `kaggle_setup.py` - Kaggle 環境設定
- `kaggle_inference.py` - Kaggle 推論執行
- `kaggle_quickstart.py` - 一鍵執行腳本
- `test_kaggle.py` - 環境測試

### 腳本目錄
- `scripts/download_models.py` - 下載預訓練模型
- `scripts/patch_config.py` - 修補配置檔案
- `tools/check_dataset.py` - 檢查資料集
- `tools/eval.py` - 評估工具

### 配置檔案
- `requirements_kaggle.txt` - Python 套件清單
- `env.example` - 環境變數範例
- `.gitignore` - Git 忽略檔案

### 文檔
- `README.md` - 主要說明文件
- `KAGGLE_GUIDE.md` - Kaggle 詳細指南
- `SETUP_GUIDE.md` - 本地設定指南
- `DEPLOYMENT_GUIDE.md` - 部署指南

## 🔧 自定義設定

### 修改倉庫名稱

如果您想使用不同的倉庫名稱：

1. 在 GitHub 上建立新倉庫
2. 修改 `init_github.py` 中的預設 URL
3. 更新 README.md 中的克隆命令

### 添加更多功能

1. 在 `scripts/` 目錄添加新腳本
2. 在 `tools/` 目錄添加新工具
3. 更新 `kaggle_quickstart.py` 整合新功能
4. 更新文檔說明

## 🛠️ 故障排除

### GitHub 相關問題

1. **權限問題**
   ```bash
   # 設定 Git 用戶資訊
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

2. **推送失敗**
   ```bash
   # 檢查遠端倉庫
   git remote -v
   
   # 重新設定遠端
   git remote set-url origin https://github.com/your-username/promptdresser-vto.git
   ```

### Kaggle 相關問題

1. **克隆失敗**
   ```python
   # 檢查網路連線
   !ping -c 3 github.com
   
   # 重新克隆
   !rm -rf promptdresser-vto
   !git clone https://github.com/your-username/promptdresser-vto.git
   ```

2. **權限問題**
   ```python
   # 檢查檔案權限
   !ls -la
   
   # 修改權限
   !chmod +x *.py
   !chmod +x scripts/*.py
   !chmod +x tools/*.py
   ```

## 📊 版本管理

### 更新專案

```bash
# 本地修改後
git add .
git commit -m "Update: 描述您的修改"
git push origin main
```

### 在 Kaggle 中更新

```python
# 拉取最新版本
!cd promptdresser-vto && git pull origin main
```

## 🎯 最佳實踐

1. **版本控制**
   - 定期提交和推送
   - 使用有意義的提交訊息
   - 保持主分支穩定

2. **文檔維護**
   - 更新 README.md
   - 記錄重要變更
   - 提供使用範例

3. **測試**
   - 在推送前測試功能
   - 使用 GitHub Actions 自動測試
   - 在 Kaggle 中驗證

4. **安全性**
   - 不要提交敏感資訊
   - 使用環境變數
   - 定期更新依賴

## 📝 注意事項

- 確保 `.env` 檔案在 `.gitignore` 中
- 大型檔案（模型、資料集）不會上傳到 GitHub
- Kaggle 環境有執行時間限制
- 定期備份重要結果

## 🎉 完成！

現在您的 PromptDresser VTO 專案已經準備好在 GitHub 和 Kaggle 中使用了！

- **GitHub**: 用於版本控制和分享
- **Kaggle**: 用於 GPU 加速執行
- **本地**: 用於開發和測試
