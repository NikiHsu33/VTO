# PromptDresser Docker 專案 Makefile

.PHONY: build up models patch infer check help

# 預設目標
help:
	@echo "可用的目標："
	@echo "  build   - 建立 Docker 映像檔"
	@echo "  up      - 啟動容器（含 GPU 支援）"
	@echo "  models  - 在容器內下載預訓練模型"
	@echo "  patch   - 在容器內修補配置檔案"
	@echo "  infer   - 在容器內執行推論"
	@echo "  check   - 在容器內檢查資料集"
	@echo "  help    - 顯示此說明"

# 建立 Docker 映像檔
build:
	@echo "建立 Docker 映像檔..."
	docker-compose -f docker/docker-compose.yaml build

# 啟動容器（含 GPU 支援）
up:
	@echo "啟動容器..."
	docker-compose -f docker/docker-compose.yaml up -d

# 在容器內下載預訓練模型
models:
	@echo "下載預訓練模型..."
	docker exec -it promptdresser python scripts/download_models.py

# 在容器內修補配置檔案
patch:
	@echo "修補配置檔案..."
	docker exec -it promptdresser python scripts/patch_config.py

# 在容器內執行推論
infer:
	@echo "執行推論..."
	docker exec -it promptdresser python inference.py \
		--config_p ./configs/VITONHD_noprompt.yaml \
		--save_name local-demo \
		--num_inference_steps 28 \
		--s_idx 0 \
		--e_idx 3

# 在容器內檢查資料集
check:
	@echo "檢查資料集..."
	docker exec -it promptdresser python tools/check_dataset.py DATA/zalando-hd-resized

# 進入容器
shell:
	@echo "進入容器..."
	docker exec -it promptdresser /bin/bash

# 停止容器
down:
	@echo "停止容器..."
	docker-compose -f docker/docker-compose.yaml down

# 清理
clean:
	@echo "清理容器和映像檔..."
	docker-compose -f docker/docker-compose.yaml down --rmi all --volumes --remove-orphans
