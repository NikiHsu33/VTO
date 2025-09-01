#!/usr/bin/env python3
"""
檢查 VITON-HD 資料集完整性腳本
"""

import os
import sys
from pathlib import Path

def check_directory_structure(data_root):
    """檢查目錄結構"""
    data_path = Path(data_root)
    
    if not data_path.exists():
        print(f"錯誤：資料集根目錄不存在 {data_root}")
        return False
    
    print(f"檢查資料集：{data_root}")
    print("=" * 50)
    
    # 檢查主要測試目錄
    test_dirs = ['test_fine', 'test_coarse']
    required_subdirs = ['image', 'image-densepose', 'agnostic-mask', 'cloth']
    
    missing_items = []
    existing_items = []
    
    for test_dir in test_dirs:
        test_path = data_path / test_dir
        if not test_path.exists():
            missing_items.append(f"目錄：{test_dir}/")
            continue
        
        existing_items.append(f"✓ 目錄：{test_dir}/")
        
        # 檢查子目錄
        for subdir in required_subdirs:
            subdir_path = test_path / subdir
            if not subdir_path.exists():
                missing_items.append(f"  - {test_dir}/{subdir}/")
            else:
                # 計算檔案數量
                file_count = len(list(subdir_path.glob('*')))
                existing_items.append(f"  ✓ {test_dir}/{subdir}/ ({file_count} 檔案)")
    
    # 檢查配對檔案
    pair_files = ['test_pairs.txt', 'test_unpairs.txt']
    for pair_file in pair_files:
        pair_path = data_path / pair_file
        if not pair_path.exists():
            missing_items.append(f"檔案：{pair_file}")
        else:
            # 計算行數
            try:
                with open(pair_path, 'r') as f:
                    line_count = sum(1 for _ in f)
                existing_items.append(f"✓ 檔案：{pair_file} ({line_count} 行)")
            except Exception as e:
                existing_items.append(f"✓ 檔案：{pair_file} (無法讀取行數)")
    
    # 輸出結果
    print("\n✅ 存在的項目：")
    for item in existing_items:
        print(f"  {item}")
    
    if missing_items:
        print("\n❌ 缺失的項目：")
        for item in missing_items:
            print(f"  {item}")
        return False
    else:
        print("\n🎉 資料集結構完整！")
        return True

def main():
    if len(sys.argv) != 2:
        print("使用方法：python check_dataset.py <DATA/zalando-hd-resized路徑>")
        print("範例：python check_dataset.py data/zalando-hd-resized")
        sys.exit(1)
    
    data_root = sys.argv[1]
    success = check_directory_structure(data_root)
    
    if not success:
        print("\n請確保資料集包含以下結構：")
        print("zalando-hd-resized/")
        print("├── test_fine/")
        print("│   ├── image/")
        print("│   ├── image-densepose/")
        print("│   ├── agnostic-mask/")
        print("│   └── cloth/")
        print("├── test_coarse/")
        print("│   ├── image/")
        print("│   ├── image-densepose/")
        print("│   ├── agnostic-mask/")
        print("│   └── cloth/")
        print("├── test_pairs.txt")
        print("└── test_unpairs.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()
