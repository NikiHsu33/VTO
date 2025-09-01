#!/usr/bin/env python3
"""
評估腳本
提供 FID/KID 和 Masked LPIPS 評估
"""

import os
import sys
import argparse
import numpy as np
import torch
import torch.nn.functional as F
from pathlib import Path
from PIL import Image
import lpips
from torch_fidelity import calculate_metrics
import cv2

class MaskedLPIPS:
    """Masked LPIPS 評估器"""
    
    def __init__(self, device='cuda'):
        self.device = device
        self.lpips_fn = lpips.LPIPS(net='alex').to(device)
    
    def calculate_masked_lpips(self, gen_dir, real_dir, mask_dir):
        """計算 Masked LPIPS"""
        gen_path = Path(gen_dir)
        real_path = Path(real_dir)
        mask_path = Path(mask_dir)
        
        if not all(p.exists() for p in [gen_path, real_path, mask_path]):
            raise ValueError("一個或多個目錄不存在")
        
        # 取得所有圖片檔案
        gen_files = sorted(list(gen_path.glob('*.png')) + list(gen_path.glob('*.jpg')))
        real_files = sorted(list(real_path.glob('*.png')) + list(real_path.glob('*.jpg')))
        mask_files = sorted(list(mask_path.glob('*.png')) + list(mask_path.glob('*.jpg')))
        
        if len(gen_files) != len(real_files) or len(gen_files) != len(mask_files):
            raise ValueError("圖片數量不匹配")
        
        total_lpips = 0.0
        valid_count = 0
        
        for gen_file, real_file, mask_file in zip(gen_files, real_files, mask_files):
            try:
                # 載入圖片
                gen_img = self.load_image(gen_file)
                real_img = self.load_image(real_file)
                mask = self.load_mask(mask_file)
                
                # 應用遮罩
                gen_masked = gen_img * mask
                real_masked = real_img * mask
                
                # 計算 LPIPS
                with torch.no_grad():
                    lpips_score = self.lpips_fn(gen_masked, real_masked).item()
                
                total_lpips += lpips_score
                valid_count += 1
                
            except Exception as e:
                print(f"處理檔案時出錯 {gen_file.name}: {e}")
                continue
        
        if valid_count == 0:
            raise ValueError("沒有有效的圖片對")
        
        return total_lpips / valid_count
    
    def load_image(self, file_path):
        """載入並預處理圖片"""
        img = Image.open(file_path).convert('RGB')
        img = img.resize((256, 256))  # 調整大小
        img = torch.from_numpy(np.array(img)).float() / 255.0
        img = img.permute(2, 0, 1).unsqueeze(0).to(self.device)
        return img
    
    def load_mask(self, file_path):
        """載入並預處理遮罩"""
        mask = cv2.imread(str(file_path), cv2.IMREAD_GRAYSCALE)
        mask = cv2.resize(mask, (256, 256))
        mask = torch.from_numpy(mask).float() / 255.0
        mask = mask.unsqueeze(0).unsqueeze(0).to(self.device)
        return mask

def calculate_fid_kid(gen_dir, real_dir):
    """計算 FID 和 KID 分數"""
    print(f"計算 FID/KID 分數...")
    print(f"生成圖片目錄：{gen_dir}")
    print(f"真實圖片目錄：{real_dir}")
    
    try:
        metrics = calculate_metrics(
            input1=gen_dir,
            input2=real_dir,
            fid=True,
            kid=True,
            verbose=True
        )
        
        return {
            'fid': metrics['frechet_inception_distance'],
            'kid': metrics['kernel_inception_distance_mean']
        }
    except Exception as e:
        print(f"計算 FID/KID 時出錯：{e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='評估腳本')
    parser.add_argument('--mode', choices=['fid_kid', 'masked_lpips'], required=True,
                       help='評估模式')
    parser.add_argument('--gen_dir', required=True, help='生成圖片目錄')
    parser.add_argument('--real_dir', required=True, help='真實圖片目錄')
    parser.add_argument('--mask_dir', help='遮罩目錄（僅用於 masked_lpips 模式）')
    parser.add_argument('--device', default='cuda', help='計算裝置')
    
    args = parser.parse_args()
    
    if args.mode == 'fid_kid':
        print("=" * 50)
        print("FID/KID 評估")
        print("=" * 50)
        
        results = calculate_fid_kid(args.gen_dir, args.real_dir)
        if results:
            print(f"\n結果：")
            print(f"FID: {results['fid']:.4f}")
            print(f"KID: {results['kid']:.4f}")
        else:
            print("評估失敗")
            sys.exit(1)
    
    elif args.mode == 'masked_lpips':
        if not args.mask_dir:
            print("錯誤：masked_lpips 模式需要 --mask_dir 參數")
            sys.exit(1)
        
        print("=" * 50)
        print("Masked LPIPS 評估")
        print("=" * 50)
        
        try:
            evaluator = MaskedLPIPS(device=args.device)
            lpips_score = evaluator.calculate_masked_lpips(
                args.gen_dir, args.real_dir, args.mask_dir
            )
            print(f"\nMasked LPIPS: {lpips_score:.4f}")
        except Exception as e:
            print(f"評估失敗：{e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
