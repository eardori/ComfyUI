FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.0-devel-ubuntu22.04

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Clone ComfyUI
RUN git clone https://github.com/eardori/ComfyUI .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install RunPod SDK
RUN pip install runpod

# Expose ComfyUI port
EXPOSE 8188

# Copy handler
COPY handler.py /workspace/handler.py

# Start command
CMD ["python", "handler.py"]
