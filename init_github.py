#!/usr/bin/env python3
"""
GitHub 倉庫初始化腳本
"""

import os
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """執行命令"""
    print(f"執行: {description}")
    print(f"命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} 成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失敗: {e}")
        return False

def init_git():
    """初始化 Git 倉庫"""
    print("🔧 初始化 Git 倉庫...")
    
    # 檢查是否已經是 Git 倉庫
    if Path('.git').exists():
        print("✅ Git 倉庫已存在")
        return True
    
    # 初始化 Git 倉庫
    if not run_command(['git', 'init'], "初始化 Git 倉庫"):
        return False
    
    return True

def add_files():
    """添加檔案到 Git"""
    print("📁 添加檔案到 Git...")
    
    # 添加所有檔案
    if not run_command(['git', 'add', '.'], "添加檔案"):
        return False
    
    return True

def commit_files():
    """提交檔案"""
    print("💾 提交檔案...")
    
    commit_message = """Initial commit: PromptDresser VTO Project

- Add Docker support for local environment
- Add Kaggle GPU environment support
- Add model download scripts
- Add dataset preparation tools
- Add evaluation tools
- Add comprehensive documentation"""
    
    if not run_command(['git', 'commit', '-m', commit_message], "提交檔案"):
        return False
    
    return True

def create_remote():
    """建立遠端倉庫"""
    print("🌐 建立遠端倉庫...")
    
    # 提示用戶輸入倉庫 URL
    print("\n請在 GitHub 上建立一個新的倉庫，然後輸入倉庫 URL")
    print("例如: https://github.com/your-username/promptdresser-vto.git")
    
    repo_url = input("請輸入 GitHub 倉庫 URL: ").strip()
    
    if not repo_url:
        print("❌ 未輸入倉庫 URL")
        return False
    
    # 添加遠端倉庫
    if not run_command(['git', 'remote', 'add', 'origin', repo_url], "添加遠端倉庫"):
        return False
    
    # 推送到 GitHub
    if not run_command(['git', 'push', '-u', 'origin', 'main'], "推送到 GitHub"):
        return False
    
    return True

def show_next_steps():
    """顯示後續步驟"""
    print("\n🎉 GitHub 倉庫建立完成！")
    print("\n📋 後續步驟：")
    print("1. 在 Kaggle Notebook 中克隆您的倉庫：")
    print("   !git clone https://github.com/your-username/promptdresser-vto.git")
    print("   %cd promptdresser-vto")
    print("\n2. 設定環境變數：")
    print("   import os")
    print("   os.environ['HF_TOKEN'] = 'your_token_here'")
    print("\n3. 執行快速開始腳本：")
    print("   !python kaggle_quickstart.py")
    print("\n4. 或者分步驟執行：")
    print("   !python kaggle_setup.py")
    print("   !python scripts/download_models.py")
    print("   !python scripts/patch_config.py")
    print("   !python kaggle_inference.py")

def main():
    """主函數"""
    print("🚀 GitHub 倉庫初始化")
    print("此腳本將幫您建立並推送到 GitHub")
    
    # 初始化 Git
    if not init_git():
        print("❌ Git 初始化失敗")
        return
    
    # 添加檔案
    if not add_files():
        print("❌ 添加檔案失敗")
        return
    
    # 提交檔案
    if not commit_files():
        print("❌ 提交檔案失敗")
        return
    
    # 建立遠端倉庫
    if not create_remote():
        print("❌ 建立遠端倉庫失敗")
        return
    
    # 顯示後續步驟
    show_next_steps()

if __name__ == "__main__":
    main()
