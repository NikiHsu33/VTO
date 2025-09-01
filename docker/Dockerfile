FROM nvidia/cuda:12.1.0-runtime-ubuntu20.04

# 設定環境變數
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 建立工作目錄
WORKDIR /workspace

# 安裝 PyTorch 2.1 with CUDA 12.1
RUN pip3 install torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cu121

# 安裝其他 Python 套件
RUN pip3 install \
    diffusers==0.25.0 \
    accelerate==0.31.0 \
    transformers==4.43.3 \
    onnxruntime-gpu==1.19.2 \
    ruamel.yaml \
    lpips \
    torch-fidelity \
    opencv-python \
    scikit-image \
    peft \
    huggingface_hub

# 克隆 PromptDresser 專案
RUN git clone https://github.com/rlawjdghek/PromptDresser /workspace/PromptDresser

# 設定工作目錄為 PromptDresser
WORKDIR /workspace/PromptDresser

# 設定預設命令
CMD ["/bin/bash"]
