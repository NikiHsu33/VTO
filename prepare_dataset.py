#!/usr/bin/env python3
"""
VITON-HD 資料集準備腳本
"""

import os
import sys
import shutil
from pathlib import Path

def create_test_structure():
    """建立測試資料結構"""
    print("📁 建立 VITON-HD 測試資料結構...")
    
    base_dir = Path('data/zalando-hd-resized')
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # 建立測試目錄結構
    test_dirs = ['test_fine', 'test_coarse']
    subdirs = ['image', 'image-densepose', 'agnostic-mask', 'cloth']
    
    for test_dir in test_dirs:
        test_path = base_dir / test_dir
        test_path.mkdir(exist_ok=True)
        
        for subdir in subdirs:
            subdir_path = test_path / subdir
            subdir_path.mkdir(exist_ok=True)
            print(f"✅ 建立目錄：{subdir_path}")
    
    # 建立空的配對檔案
    pair_files = ['test_pairs.txt', 'test_unpairs.txt']
    for pair_file in pair_files:
        pair_path = base_dir / pair_file
        if not pair_path.exists():
            pair_path.touch()
            print(f"✅ 建立檔案：{pair_path}")
        else:
            print(f"⚠️  檔案已存在：{pair_path}")
    
    print("\n📋 資料集結構已建立！")
    print("請將您的 VITON-HD 測試資料放入以下目錄：")
    print(f"  {base_dir}/")
    print("\n如果沒有 test_coarse/ 資料，可以複製 test/ 為 test_fine/ 和 test_coarse/")

def copy_test_to_fine_coarse():
    """將 test/ 複製為 test_fine/ 和 test_coarse/"""
    base_dir = Path('data/zalando-hd-resized')
    test_dir = base_dir / 'test'
    
    if not test_dir.exists():
        print("❌ 找不到 test/ 目錄")
        print("請先將 VITON-HD 測試資料放入 data/zalando-hd-resized/test/")
        return False
    
    print("🔄 複製 test/ 為 test_fine/ 和 test_coarse/...")
    
    # 複製為 test_fine
    fine_dir = base_dir / 'test_fine'
    if fine_dir.exists():
        shutil.rmtree(fine_dir)
    shutil.copytree(test_dir, fine_dir)
    print(f"✅ 複製到 {fine_dir}")
    
    # 複製為 test_coarse
    coarse_dir = base_dir / 'test_coarse'
    if coarse_dir.exists():
        shutil.rmtree(coarse_dir)
    shutil.copytree(test_dir, coarse_dir)
    print(f"✅ 複製到 {coarse_dir}")
    
    return True

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'copy':
        copy_test_to_fine_coarse()
    else:
        create_test_structure()
        print("\n💡 提示：如果已有 test/ 目錄，可以執行：")
        print("  python prepare_dataset.py copy")

if __name__ == "__main__":
    main()
