#!/usr/bin/env python3
"""
環境設定測試腳本
"""

import os
import sys
from pathlib import Path

def check_environment():
    """檢查環境設定"""
    print("🔍 檢查環境設定...")
    print("=" * 50)
    
    # 檢查 .env 檔案
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read().strip()
        if 'HF_TOKEN=' in content and len(content) > 10:
            print("✅ .env 檔案存在且包含 HF_TOKEN")
        else:
            print("⚠️  .env 檔案存在但 HF_TOKEN 可能未設定")
    else:
        print("❌ .env 檔案不存在")
    
    # 檢查目錄結構
    required_dirs = ['data', 'outputs', 'pretrained_models']
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✅ 目錄 {dir_name}/ 存在")
        else:
            print(f"❌ 目錄 {dir_name}/ 不存在")
    
    # 檢查 Docker 檔案
    docker_files = ['docker/Dockerfile', 'docker/docker-compose.yaml']
    for file_path in docker_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} 存在")
        else:
            print(f"❌ {file_path} 不存在")
    
    # 檢查腳本檔案
    script_files = [
        'scripts/download_models.py',
        'scripts/patch_config.py',
        'tools/check_dataset.py',
        'tools/eval.py'
    ]
    for file_path in script_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} 存在")
        else:
            print(f"❌ {file_path} 不存在")
    
    print("\n📋 下一步驟：")
    print("1. 啟動 Docker Desktop")
    print("2. 在 .env 檔案中設定您的 HF_TOKEN")
    print("3. 執行 make build")
    print("4. 執行 make up")
    print("5. 執行 make models")

if __name__ == "__main__":
    check_environment()
