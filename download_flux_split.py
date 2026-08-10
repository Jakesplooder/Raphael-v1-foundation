import os
import sys
import time
from huggingface_hub import hf_hub_download

os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

models_to_download = [
    {
        "repo_id": "Kijai/flux-fp8",
        "filename": "flux1-schnell-fp8-e4m3fn.safetensors",
        "local_dir": r"R:\ComfyUI\models\unet"
    },
    {
        "repo_id": "comfyanonymous/flux_text_encoders",
        "filename": "t5xxl_fp8_e4m3fn.safetensors",
        "local_dir": r"R:\ComfyUI\models\clip"
    },
    {
        "repo_id": "comfyanonymous/flux_text_encoders",
        "filename": "clip_l.safetensors",
        "local_dir": r"R:\ComfyUI\models\clip"
    },
    {
        "repo_id": "black-forest-labs/FLUX.1-schnell",
        "filename": "ae.safetensors",
        "local_dir": r"R:\ComfyUI\models\vae"
    }
]

import threading
def monitor_downloads():
    while True:
        total_size = 0
        for m in models_to_download:
            dest = os.path.join(m["local_dir"], m["filename"])
            if os.path.exists(dest):
                total_size += os.path.getsize(dest)
            
            cache_dir = os.path.join(m["local_dir"], ".cache")
            if os.path.exists(cache_dir):
                for root, _, files in os.walk(cache_dir):
                    for f in files:
                        if f.endswith(".incomplete"):
                            total_size += os.path.getsize(os.path.join(root, f))
                            
        print(f"Total downloaded: {total_size / (1024*1024):.2f} MB", flush=True)
        time.sleep(5)

t = threading.Thread(target=monitor_downloads, daemon=True)
t.start()

for m in models_to_download:
    print(f"Downloading {m['filename']} from {m['repo_id']}...")
    try:
        path = hf_hub_download(
            repo_id=m["repo_id"], 
            filename=m["filename"], 
            local_dir=m["local_dir"]
        )
        print(f"Successfully downloaded: {path}")
    except Exception as e:
        print(f"Failed to download {m['filename']}: {e}")
        sys.exit(1)

print("All downloads completed and verified successfully.")
sys.stdout.flush()
