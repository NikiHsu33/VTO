#!/usr/bin/env python3
"""
Kaggle Notebook 執行範例
請逐個 cell 執行，避免複製貼上問題
"""

# Cell 1: 克隆專案
# 在 Kaggle Notebook 中執行：
# !git clone https://github.com/NikiHsu33/VTO.git
# %cd VTO

# Cell 2: 設定環境變數
# 在 Kaggle Notebook 中執行：
# import os
# os.environ['HF_TOKEN'] = 'hf_your_token_here'

# Cell 3: 安裝必要套件
# 在 Kaggle Notebook 中執行：
# !pip install huggingface_hub python-dotenv

# Cell 4: 執行環境設定
# 在 Kaggle Notebook 中執行：
# !python kaggle_setup.py

# Cell 5: 下載模型
# 在 Kaggle Notebook 中執行：
# !python scripts/download_models.py

# Cell 6: 修補配置
# 在 Kaggle Notebook 中執行：
# !python scripts/patch_config.py

# Cell 7: 準備資料集
# 在 Kaggle Notebook 中執行：
# import zipfile
# with zipfile.ZipFile('/kaggle/input/viton-hd-test/viton_hd_test.zip', 'r') as zip_ref:
#     zip_ref.extractall('data/zalando-hd-resized/')

# Cell 8: 檢查資料集
# 在 Kaggle Notebook 中執行：
# !python tools/check_dataset.py data/zalando-hd-resized

# Cell 9: 執行推論
# 在 Kaggle Notebook 中執行：
# !python kaggle_inference.py
