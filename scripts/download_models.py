#!/usr/bin/env python3
"""
下載預訓練模型腳本
"""

import os
import sys
from huggingface_hub import snapshot_download
from dotenv import load_dotenv

def main():
    # 載入環境變數
    load_dotenv()
    
    # 取得 HF_TOKEN（支援 Kaggle 環境變數）
    hf_token = os.getenv('HF_TOKEN')
    if not hf_token:
        print("錯誤：未設定 HF_TOKEN 環境變數")
        print("在 Kaggle 中，請使用：os.environ['HF_TOKEN'] = 'your_token'")
        sys.exit(1)
    
    # 建立 pretrained_models 目錄
    os.makedirs('pretrained_models', exist_ok=True)
    
    # 要下載的模型列表
    models = [
        {
            'repo_id': 'stabilityai/stable-diffusion-xl-base-1.0',
            'local_dir': 'pretrained_models/stable-diffusion-xl-base-1.0'
        },
        {
            'repo_id': 'diffusers/stable-diffusion-xl-1.0-inpainting-0.1',
            'local_dir': 'pretrained_models/stable-diffusion-xl-1.0-inpainting-0.1'
        },
        {
            'repo_id': 'madebyollin/sdxl-vae-fp16-fix',
            'local_dir': 'pretrained_models/sdxl-vae-fp16-fix'
        }
    ]
    
    # 下載每個模型
    for model in models:
        print(f"正在下載 {model['repo_id']}...")
        try:
            snapshot_download(
                repo_id=model['repo_id'],
                local_dir=model['local_dir'],
                token=hf_token,
                local_dir_use_symlinks=False
            )
            print(f"✓ 成功下載 {model['repo_id']}")
        except Exception as e:
            print(f"✗ 下載 {model['repo_id']} 失敗：{e}")
            sys.exit(1)
    
    print("所有模型下載完成！")

if __name__ == "__main__":
    main()
