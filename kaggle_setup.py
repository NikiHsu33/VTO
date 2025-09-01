#!/usr/bin/env python3
"""
Kaggle 環境設定腳本
適用於 Kaggle Notebooks 的 GPU 環境
"""

import os
import sys
import subprocess
from pathlib import Path

def check_kaggle_environment():
    """檢查 Kaggle 環境"""
    print("🔍 檢查 Kaggle 環境...")
    print("=" * 50)
    
    # 檢查是否在 Kaggle 環境中
    if os.path.exists('/kaggle/input'):
        print("✅ 檢測到 Kaggle 環境")
    else:
        print("⚠️  未檢測到 Kaggle 環境，但可以繼續執行")
    
    # 檢查 GPU
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ GPU 可用")
            print(result.stdout.split('\n')[0])  # 顯示 GPU 資訊
        else:
            print("❌ GPU 不可用")
    except FileNotFoundError:
        print("❌ nvidia-smi 不可用")
    
    # 檢查 Python 版本
    print(f"✅ Python 版本: {sys.version}")
    
    # 檢查可用記憶體
    try:
        import psutil
        memory = psutil.virtual_memory()
        print(f"✅ 系統記憶體: {memory.total // (1024**3)} GB")
    except ImportError:
        print("⚠️  無法檢查記憶體（需要 psutil）")

def install_requirements():
    """安裝必要的套件"""
    print("\n📦 安裝必要套件...")
    
    packages = [
        'torch==2.1.0',
        'torchvision==0.16.0',
        'diffusers==0.25.0',
        'accelerate==0.31.0',
        'transformers==4.43.3',
        'onnxruntime-gpu==1.19.2',
        'ruamel.yaml',
        'lpips',
        'torch-fidelity',
        'opencv-python',
        'scikit-image',
        'peft',
        'huggingface_hub',
        'python-dotenv',
        'psutil'
    ]
    
    for package in packages:
        print(f"安裝 {package}...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                         check=True, capture_output=True)
            print(f"✅ {package} 安裝成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ {package} 安裝失敗: {e}")

def setup_directories():
    """建立必要的目錄"""
    print("\n📁 建立目錄結構...")
    
    directories = [
        'data/zalando-hd-resized/test_fine/image',
        'data/zalando-hd-resized/test_fine/image-densepose',
        'data/zalando-hd-resized/test_fine/agnostic-mask',
        'data/zalando-hd-resized/test_fine/cloth',
        'data/zalando-hd-resized/test_coarse/image',
        'data/zalando-hd-resized/test_coarse/image-densepose',
        'data/zalando-hd-resized/test_coarse/agnostic-mask',
        'data/zalando-hd-resized/test_coarse/cloth',
        'outputs',
        'pretrained_models'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ 建立目錄: {directory}")

def clone_promptdresser():
    """克隆 PromptDresser 專案"""
    print("\n📥 克隆 PromptDresser 專案...")
    
    if not os.path.exists('PromptDresser'):
        try:
            subprocess.run(['git', 'clone', 'https://github.com/rlawjdghek/PromptDresser'], 
                         check=True, capture_output=True)
            print("✅ PromptDresser 克隆成功")
        except subprocess.CalledProcessError as e:
            print(f"❌ PromptDresser 克隆失敗: {e}")
    else:
        print("✅ PromptDresser 已存在")

def create_env_file():
    """建立環境變數檔案"""
    print("\n🔧 建立環境變數檔案...")
    
    env_content = """# Kaggle 環境變數
HF_TOKEN=hf_your_token_here
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env 檔案已建立")
    print("⚠️  請記得在 .env 檔案中設定您的 HF_TOKEN")

def main():
    print("🚀 Kaggle 環境設定開始...")
    
    check_kaggle_environment()
    install_requirements()
    setup_directories()
    clone_promptdresser()
    create_env_file()
    
    print("\n🎉 Kaggle 環境設定完成！")
    print("\n📋 下一步驟：")
    print("1. 在 .env 檔案中設定您的 HF_TOKEN")
    print("2. 執行 python scripts/download_models.py")
    print("3. 執行 python scripts/patch_config.py")
    print("4. 將 VITON-HD 資料集放入 data/zalando-hd-resized/")
    print("5. 執行推論：python PromptDresser/inference.py --config_p ./configs/VITONHD_noprompt.yaml")

if __name__ == "__main__":
    main()
