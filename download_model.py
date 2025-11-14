"""
Wan2.2-I2V-A14B 모델 다운로드 스크립트
"""
from huggingface_hub import snapshot_download
import os

# 모델 저장 경로
model_path = "models/checkpoints/wan22"

# Hugging Face에서 모델 다운로드
print("Downloading Wan2.2-I2V-A14B model...")
print("This may take 10-30 minutes depending on your internet speed...")

snapshot_download(
    repo_id="Wan-AI/Wan2.2-I2V-A14B",
    local_dir=model_path,
    token=os.environ.get("HUGGING_FACE_HUB_TOKEN"),  # 환경 변수에서 토큰 읽기
    resume_download=True,  # 중단된 다운로드 재개
)

print(f"Model downloaded to: {model_path}")
print("You can now use this model in ComfyUI!")
