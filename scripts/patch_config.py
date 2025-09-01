#!/usr/bin/env python3
"""
修補配置檔案腳本
將 dataset.text_file_postfix 設為 None
"""

import os
import sys
import yaml
from ruamel.yaml import YAML

def main():
    # 設定檔案路徑（支援 Kaggle 環境）
    input_config = 'PromptDresser/configs/VITONHD.yaml'
    output_config = 'PromptDresser/configs/VITONHD_noprompt.yaml'
    
    # 檢查輸入檔案是否存在
    if not os.path.exists(input_config):
        print(f"錯誤：找不到配置檔案 {input_config}")
        sys.exit(1)
    
    # 讀取原始配置
    yaml_loader = YAML()
    yaml_loader.preserve_quotes = True
    
    try:
        with open(input_config, 'r', encoding='utf-8') as f:
            config = yaml_loader.load(f)
    except Exception as e:
        print(f"錯誤：無法讀取配置檔案 {input_config}: {e}")
        sys.exit(1)
    
    # 檢查並修改 dataset.text_file_postfix
    if 'dataset' in config:
        current_value = config['dataset'].get('text_file_postfix')
        print(f"原始 text_file_postfix 值：{current_value}")
        
        if current_value is None:
            print("text_file_postfix 已經是 None，直接複製檔案")
            # 直接複製檔案
            with open(input_config, 'r', encoding='utf-8') as src:
                content = src.read()
            with open(output_config, 'w', encoding='utf-8') as dst:
                dst.write(content)
        else:
            print("將 text_file_postfix 設為 None")
            config['dataset']['text_file_postfix'] = None
            
            # 寫入新配置檔案
            with open(output_config, 'w', encoding='utf-8') as f:
                yaml_loader.dump(config, f)
    else:
        print("警告：配置檔案中沒有 dataset 區段")
        # 直接複製檔案
        with open(input_config, 'r', encoding='utf-8') as src:
            content = src.read()
        with open(output_config, 'w', encoding='utf-8') as dst:
            dst.write(content)
    
    print(f"✓ 配置檔案已生成：{output_config}")

if __name__ == "__main__":
    main()
