#!/usr/bin/env python3
"""
Kaggle 快速開始腳本
一鍵設定並執行 PromptDresser
"""

import os
import sys
import subprocess
import zipfile
from pathlib import Path

def print_step(step_num, description):
    """打印步驟資訊"""
    print(f"\n{'='*60}")
    print(f"步驟 {step_num}: {description}")
    print(f"{'='*60}")

def run_command(cmd, description):
    """執行命令並處理錯誤"""
    print(f"執行: {description}")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} 成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失敗")
        print(f"錯誤: {e.stderr}")
        return False

def check_environment():
    """檢查環境"""
    print_step(1, "檢查環境")
    
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
        else:
            print("❌ GPU 不可用")
    except FileNotFoundError:
        print("❌ nvidia-smi 不可用")

def setup_environment():
    """設定環境"""
    print_step(2, "設定環境")
    
    if not run_command(['python', 'kaggle_setup.py'], "環境設定"):
        return False
    
    return True

def setup_token():
    """設定 Token"""
    print_step(3, "設定 Hugging Face Token")
    
    # 檢查是否已設定 HF_TOKEN
    hf_token = os.getenv('HF_TOKEN')
    if not hf_token:
        print("⚠️  未設定 HF_TOKEN 環境變數")
        print("請在執行此腳本前設定：")
        print("import os")
        print("os.environ['HF_TOKEN'] = 'your_token_here'")
        return False
    
    print("✅ HF_TOKEN 已設定")
    return True

def download_models():
    """下載模型"""
    print_step(4, "下載預訓練模型")
    
    if not run_command(['python', 'scripts/download_models.py'], "下載模型"):
        return False
    
    return True

def patch_config():
    """修補配置"""
    print_step(5, "修補配置檔案")
    
    if not run_command(['python', 'scripts/patch_config.py'], "修補配置"):
        return False
    
    return True

def prepare_dataset():
    """準備資料集"""
    print_step(6, "準備資料集")
    
    # 檢查是否有資料集檔案
    kaggle_input = Path('/kaggle/input')
    if kaggle_input.exists():
        datasets = list(kaggle_input.glob('*'))
        if datasets:
            print(f"找到資料集: {datasets}")
            
            # 尋找 zip 檔案
            for dataset in datasets:
                zip_files = list(dataset.glob('*.zip'))
                if zip_files:
                    zip_file = zip_files[0]
                    print(f"解壓資料集: {zip_file}")
                    
                    try:
                        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                            zip_ref.extractall('data/zalando-hd-resized/')
                        print("✅ 資料集解壓成功")
                        return True
                    except Exception as e:
                        print(f"❌ 資料集解壓失敗: {e}")
    
    print("⚠️  未找到資料集，請手動上傳 VITON-HD 測試集")
    print("或使用以下命令解壓：")
    print("with zipfile.ZipFile('/kaggle/input/your-dataset/viton_hd_test.zip', 'r') as zip_ref:")
    print("    zip_ref.extractall('data/zalando-hd-resized/')")
    
    return False

def check_dataset():
    """檢查資料集"""
    print_step(7, "檢查資料集")
    
    if not run_command(['python', 'tools/check_dataset.py', 'data/zalando-hd-resized'], "檢查資料集"):
        return False
    
    return True

def run_inference():
    """執行推論"""
    print_step(8, "執行推論")
    
    if not run_command(['python', 'kaggle_inference.py'], "執行推論"):
        return False
    
    return True

def show_results():
    """顯示結果"""
    print_step(9, "顯示結果")
    
    result_dir = Path('outputs/kaggle-demo/paired')
    if result_dir.exists():
        images = list(result_dir.glob('*.png')) + list(result_dir.glob('*.jpg'))
        if images:
            print(f"✅ 找到 {len(images)} 張生成的圖片")
            print("圖片位置:")
            for img in images[:5]:  # 只顯示前5張
                print(f"  - {img}")
            
            print("\n要查看圖片，請執行：")
            print("import matplotlib.pyplot as plt")
            print("import matplotlib.image as mpimg")
            print(f"img = mpimg.imread('{images[0]}')")
            print("plt.imshow(img)")
            print("plt.axis('off')")
            print("plt.show()")
        else:
            print("❌ 未找到生成的圖片")
    else:
        print("❌ 結果目錄不存在")

def main():
    """主函數"""
    print("🚀 PromptDresser Kaggle 快速開始")
    print("此腳本將自動完成所有設定步驟")
    
    # 檢查環境
    check_environment()
    
    # 設定環境
    if not setup_environment():
        print("❌ 環境設定失敗")
        return
    
    # 設定 Token
    if not setup_token():
        print("❌ Token 設定失敗")
        return
    
    # 下載模型
    if not download_models():
        print("❌ 模型下載失敗")
        return
    
    # 修補配置
    if not patch_config():
        print("❌ 配置修補失敗")
        return
    
    # 準備資料集
    prepare_dataset()
    
    # 檢查資料集
    if not check_dataset():
        print("❌ 資料集檢查失敗")
        return
    
    # 執行推論
    if not run_inference():
        print("❌ 推論執行失敗")
        return
    
    # 顯示結果
    show_results()
    
    print("\n🎉 所有步驟完成！")
    print("如果遇到問題，請檢查上述錯誤訊息")

if __name__ == "__main__":
    main()
