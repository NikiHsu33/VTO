#!/usr/bin/env python3
"""
Kaggle 環境推論腳本
適用於 Kaggle Notebooks 的 GPU 環境
"""

import os
import sys
import subprocess
from pathlib import Path

def run_inference():
    """執行推論"""
    print("🎯 開始執行推論...")
    
    # 檢查 PromptDresser 是否存在
    if not os.path.exists('PromptDresser'):
        print("❌ PromptDresser 專案不存在，請先執行 python kaggle_setup.py")
        return False
    
    # 檢查配置檔案
    config_file = 'PromptDresser/configs/VITONHD_noprompt.yaml'
    if not os.path.exists(config_file):
        print("❌ 配置檔案不存在，請先執行 python scripts/patch_config.py")
        return False
    
    # 檢查資料集
    data_dir = 'data/zalando-hd-resized'
    if not os.path.exists(data_dir):
        print("❌ 資料集目錄不存在")
        return False
    
    # 執行推論
    cmd = [
        'python', 'PromptDresser/inference.py',
        '--config_p', config_file,
        '--save_name', 'kaggle-demo',
        '--num_inference_steps', '28',
        '--s_idx', '0',
        '--e_idx', '3'
    ]
    
    print(f"執行命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 推論執行成功！")
        print("輸出結果在: outputs/kaggle-demo/")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 推論執行失敗: {e}")
        print(f"錯誤輸出: {e.stderr}")
        return False

def check_models():
    """檢查模型是否已下載"""
    print("🔍 檢查預訓練模型...")
    
    required_models = [
        'pretrained_models/stable-diffusion-xl-base-1.0',
        'pretrained_models/stable-diffusion-xl-1.0-inpainting-0.1',
        'pretrained_models/sdxl-vae-fp16-fix'
    ]
    
    missing_models = []
    for model in required_models:
        if not os.path.exists(model):
            missing_models.append(model)
        else:
            print(f"✅ {model} 存在")
    
    if missing_models:
        print(f"❌ 缺少模型: {missing_models}")
        print("請先執行: python scripts/download_models.py")
        return False
    
    return True

def main():
    print("🚀 Kaggle 推論腳本")
    print("=" * 50)
    
    # 檢查模型
    if not check_models():
        return
    
    # 執行推論
    if run_inference():
        print("\n🎉 推論完成！")
        print("📁 結果位置: outputs/kaggle-demo/")
    else:
        print("\n❌ 推論失敗")

if __name__ == "__main__":
    main()
