import json
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any

def run_health_check(url: str, output_dir: Path) -> int:
    print("Running ComfyUI Health Check...\n")
    start_time = time.time()
    
    # 1. API Connectivity
    try:
        req = urllib.request.Request(f"{url}/system_stats")
        with urllib.request.urlopen(req, timeout=5) as response:
            stats = json.loads(response.read())
            print("API ............... PASS")
            # GPU check
            devices = stats.get("devices", [])
            if devices and any(d.get("type") == "cuda" for d in devices):
                print("GPU ............... PASS")
            else:
                print("GPU ............... WARN (No CUDA device found in stats)")
    except Exception as e:
        print(f"API ............... FAIL ({e})")
        return 1

    # 2. Workflow Submission
    workflow = {
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "cfg": 7,
                "denoise": 1,
                "latent_image": ["5", 0],
                "model": ["4", 0],
                "negative": ["7", 0],
                "positive": ["6", 0],
                "sampler_name": "euler",
                "scheduler": "normal",
                "seed": int(time.time()),
                "steps": 4
            }
        },
        "4": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": "sd_xl_base_1.0.safetensors"
            }
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "batch_size": 1,
                "height": 512,
                "width": 512
            }
        },
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": ["4", 1],
                "text": "A simple green square, simple"
            }
        },
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": ["4", 1],
                "text": "blurry, complex"
            }
        },
        "8": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["3", 0],
                "vae": ["4", 2]
            }
        },
        "9": {
            "class_type": "SaveImage",
            "inputs": {
                "filename_prefix": "ComfyUI_HealthCheck",
                "images": ["8", 0]
            }
        }
    }
    
    prompt_id = None
    try:
        data = json.dumps({"prompt": workflow}).encode("utf-8")
        req = urllib.request.Request(f"{url}/prompt", data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as response:
            res = json.loads(response.read())
            prompt_id = res.get("prompt_id")
            if prompt_id:
                print("Workflow .......... PASS")
            else:
                print("Workflow .......... FAIL (No prompt_id returned)")
                return 1
    except Exception as e:
        print(f"Workflow .......... FAIL ({e})")
        return 1

    # 3. Execution & Generation
    print("Image Generation .. Waiting...")
    history = {}
    attempts = 0
    while attempts < 30: # up to 60 seconds
        time.sleep(2)
        attempts += 1
        try:
            req = urllib.request.Request(f"{url}/history/{prompt_id}")
            with urllib.request.urlopen(req, timeout=5) as response:
                history = json.loads(response.read())
                if prompt_id in history:
                    break
        except Exception:
            pass
            
    if prompt_id not in history:
        print("Image Generation .. FAIL (Timeout or error waiting for completion)")
        return 1
        
    print("Image Generation .. PASS")

    # 4. Filesystem validation
    outputs = history[prompt_id].get("outputs", {})
    image_found = False
    for node_id, node_output in outputs.items():
        if "images" in node_output:
            for img in node_output["images"]:
                filename = img.get("filename")
                if filename:
                    # check if file exists on disk (assuming mounted to C:/ComfyUI/output)
                    filepath = output_dir / filename
                    if filepath.exists():
                        image_found = True
                        # clean it up
                        try:
                            filepath.unlink()
                        except:
                            pass
    
    if image_found:
        print("Filesystem ........ PASS")
    else:
        print("Filesystem ........ FAIL (Output file not found in C:/ComfyUI/output)")
        return 1

    total_time = time.time() - start_time
    print(f"\nTotal Time: {total_time:.1f}s")
    return 0
