FROM runpod/pytorch:2.1.0-py3.10-cuda12.1.0-devel-ubuntu22.04

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy all files from current directory
COPY . /workspace/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install RunPod SDK
RUN pip install runpod

# Expose ComfyUI port
EXPOSE 8188

# Start command
CMD ["python", "-u", "handler.py"]
