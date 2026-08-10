import urllib.request
import urllib.error
import json
import time

workflow = {
    "5": {"class_type": "EmptyLatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
    "6": {"class_type": "CLIPTextEncode", "inputs": {"text": "A test prompt", "clip": ["11", 0]}},
    "11": {"class_type": "DualCLIPLoader", "inputs": {"clip_name1": "t5xxl_fp16.safetensors", "clip_name2": "clip_l.safetensors", "type": "flux"}},
    "12": {"class_type": "UNETLoader", "inputs": {"unet_name": "flux1-schnell-fp8.safetensors", "weight_dtype": "fp8_e4m3fn"}},
    "13": {"class_type": "VAELoader", "inputs": {"vae_name": "ae.safetensors"}},
    "3": {"class_type": "KSampler", "inputs": {"seed": 123, "steps": 4, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0, "model": ["12", 0], "positive": ["6", 0], "negative": ["6", 0], "latent_image": ["5", 0]}},
    "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["13", 0]}},
    "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "test_req", "images": ["8", 0]}}
}

url = "http://127.0.0.1:8188/prompt"
data = json.dumps({"prompt": workflow}).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

try:
    response = urllib.request.urlopen(req, timeout=10)
    print(json.loads(response.read()))
except urllib.error.HTTPError as e:
    print(f"HTTPError {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(e)
