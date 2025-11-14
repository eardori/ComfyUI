"""
Improved RunPod Serverless Handler for ComfyUI with Wan2.2
"""
import runpod
import requests
import json
import time
import subprocess
import os
import sys
from pathlib import Path


# ComfyUI 프로세스를 백그라운드에서 시작
comfyui_process = None

def start_comfyui():
    """ComfyUI 서버 시작"""
    global comfyui_process

    if comfyui_process is None:
        print("Starting ComfyUI server...")
        comfyui_process = subprocess.Popen(
            [sys.executable, "main.py", "--listen", "0.0.0.0", "--port", "8188"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd="/workspace"
        )

        # ComfyUI가 준비될 때까지 대기
        max_retries = 30
        for i in range(max_retries):
            try:
                response = requests.get("http://127.0.0.1:8188/")
                if response.status_code == 200:
                    print("ComfyUI server is ready!")
                    return True
            except:
                pass
            time.sleep(2)
            print(f"Waiting for ComfyUI... ({i+1}/{max_retries})")

        print("Failed to start ComfyUI")
        return False
    return True


def handler(event):
    """
    Handler function for RunPod Serverless

    Expected input:
    {
        "input": {
            "workflow": {
                "prompt": "A cat walking",
                "image_url": "https://...",
                "width": 1280,
                "height": 704,
                "frames": 49
            }
        }
    }
    """
    try:
        # ComfyUI 서버 시작 확인
        if not start_comfyui():
            return {
                "error": "Failed to start ComfyUI server",
                "status": "failed"
            }

        input_data = event.get("input", {})
        workflow = input_data.get("workflow", {})

        # ComfyUI API endpoint
        comfyui_url = "http://127.0.0.1:8188"

        # 실제 ComfyUI workflow JSON 구성
        # (이 부분은 ComfyUI에서 저장한 워크플로우를 사용해야 함)
        comfy_workflow = {
            "1": {
                "inputs": {
                    "image": workflow.get("image_url", ""),
                    "width": workflow.get("width", 1280),
                    "height": workflow.get("height", 704),
                    "frames": workflow.get("frames", 49)
                },
                "class_type": "WanImageToVideo"
            }
        }

        # ComfyUI에 워크플로우 제출
        response = requests.post(
            f"{comfyui_url}/prompt",
            json={"prompt": comfy_workflow}
        )

        if response.status_code != 200:
            return {
                "error": f"ComfyUI API error: {response.text}",
                "status_code": response.status_code
            }

        result = response.json()
        prompt_id = result.get("prompt_id")

        # 작업 완료 대기 (polling)
        max_wait = 600  # 10분
        start_time = time.time()

        while time.time() - start_time < max_wait:
            history_response = requests.get(f"{comfyui_url}/history/{prompt_id}")
            if history_response.status_code == 200:
                history = history_response.json()
                if prompt_id in history:
                    # 완료됨
                    outputs = history[prompt_id].get("outputs", {})
                    return {
                        "status": "success",
                        "prompt_id": prompt_id,
                        "outputs": outputs
                    }

            time.sleep(5)

        return {
            "error": "Timeout waiting for video generation",
            "status": "timeout"
        }

    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }


# Start the handler
if __name__ == "__main__":
    print("Initializing RunPod Serverless Handler...")
    runpod.serverless.start({"handler": handler})
