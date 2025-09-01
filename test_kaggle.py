#!/usr/bin/env python3
"""
Kaggle 環境測試腳本
"""

import os
import sys
import subprocess
from pathlib import Path

def test_kaggle_environment():
    """測試 Kaggle 環境"""
    print("🧪 測試 Kaggle 環境...")
    print("=" * 50)
    
    # 檢查是否在 Kaggle 環境中
    if os.path.exists('/kaggle/input'):
        print("✅ 檢測到 Kaggle 環境")
    else:
        print("⚠️  未檢測到 Kaggle 環境")
    
    # 檢查 GPU
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ GPU 可用")
            # 顯示 GPU 資訊
            lines = result.stdout.split('\n')
            for line in lines[:5]:  # 只顯示前5行
                if line.strip():
                    print(f"  {line}")
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
        print(f"✅ 可用記憶體: {memory.available // (1024**3)} GB")
    except ImportError:
        print("⚠️  無法檢查記憶體（需要 psutil）")
    
    # 檢查磁碟空間
    try:
        disk = psutil.disk_usage('/')
        print(f"✅ 磁碟總空間: {disk.total // (1024**3)} GB")
        print(f"✅ 可用空間: {disk.free // (1024**3)} GB")
    except:
        print("⚠️  無法檢查磁碟空間")

def test_packages():
    """測試必要套件"""
    print("\n📦 測試必要套件...")
    
    packages = [
        'torch',
        'torchvision',
        'diffusers',
        'transformers',
        'huggingface_hub',
        'opencv-python',
        'PIL'
    ]
    
    for package in packages:
        try:
            if package == 'PIL':
                import PIL
                print(f"✅ {package} 可用")
            else:
                __import__(package)
                print(f"✅ {package} 可用")
        except ImportError:
            print(f"❌ {package} 不可用")

def test_gpu_torch():
    """測試 PyTorch GPU 支援"""
    print("\n🔥 測試 PyTorch GPU 支援...")
    
    try:
        import torch
        print(f"✅ PyTorch 版本: {torch.__version__}")
        
        if torch.cuda.is_available():
            print(f"✅ CUDA 可用")
            print(f"✅ GPU 數量: {torch.cuda.device_count()}")
            print(f"✅ 當前 GPU: {torch.cuda.get_device_name()}")
            
            # 測試 GPU 記憶體
            gpu_memory = torch.cuda.get_device_properties(0).total_memory
            print(f"✅ GPU 記憶體: {gpu_memory // (1024**3)} GB")
            
            # 簡單的 GPU 測試
            x = torch.randn(1000, 1000).cuda()
            y = torch.mm(x, x.t())
            print("✅ GPU 計算測試成功")
            
        else:
            print("❌ CUDA 不可用")
    except Exception as e:
        print(f"❌ PyTorch GPU 測試失敗: {e}")

def main():
    print("🚀 Kaggle 環境測試開始...")
    
    test_kaggle_environment()
    test_packages()
    test_gpu_torch()
    
    print("\n🎉 測試完成！")
    print("\n📋 如果所有測試都通過，您可以開始使用 PromptDresser")

if __name__ == "__main__":
    main()
