"""
RunPod Serverless Handler for ComfyUI with Wan2.2
"""
import runpod
import requests
import json
import base64
import os
from io import BytesIO


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
        input_data = event.get("input", {})
        workflow = input_data.get("workflow", {})

        # ComfyUI API endpoint
        comfyui_url = "http://127.0.0.1:8188"

        # Construct ComfyUI workflow
        comfy_workflow = {
            "prompt": workflow.get("prompt", ""),
            "image": workflow.get("image_url", ""),
            "width": workflow.get("width", 1280),
            "height": workflow.get("height", 704),
            "frames": workflow.get("frames", 49),
            "model": "Wan2.2-I2V-A14B"
        }

        # Send to ComfyUI
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

        # Wait for completion and get result
        # (Simplified - in production, implement proper polling)

        return {
            "status": "success",
            "prompt_id": prompt_id,
            "result": result
        }

    except Exception as e:
        return {
            "error": str(e),
            "status": "failed"
        }


# Start the handler
runpod.serverless.start({"handler": handler})
