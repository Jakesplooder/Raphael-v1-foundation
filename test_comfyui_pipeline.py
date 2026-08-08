import urllib.request
import urllib.parse
import urllib.error
import json
import time
import os
import shutil
import hashlib
from pathlib import Path
from pprint import pprint
import subprocess

COMFY_URL = "http://127.0.0.1:8188"
COMFY_INPUT_DIR = Path(r"C:\ComfyUI\input")
COMFY_OUTPUT_DIR = Path(r"C:\ComfyUI\output")

def queue_prompt(prompt_json):
    p = {"prompt": prompt_json}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"{COMFY_URL}/prompt", data=data, headers={'Content-Type': 'application/json'})
    try:
        response = urllib.request.urlopen(req)
        return json.loads(response.read())
    except urllib.error.URLError as e:
        print(f"Error connecting to ComfyUI. Is it running? {e}")
        return None

def get_history(prompt_id):
    req = urllib.request.Request(f"{COMFY_URL}/history/{prompt_id}")
    try:
        response = urllib.request.urlopen(req)
        return json.loads(response.read())
    except Exception as e:
        print(f"Transient error polling history: {e}")
        return None

def wait_for_completion(prompt_id, timeout=300):
    start_time = time.time()
    while True:
        history = get_history(prompt_id)
        if history and prompt_id in history:
            return history[prompt_id]
        
        if time.time() - start_time > timeout:
            print("Timeout waiting for completion.")
            return None
            
        time.sleep(2)

def generate_flux_image(request_id: str, prompt_text: str) -> str:
    seed = int(hashlib.sha256(request_id.encode()).hexdigest(), 16) % (2**53 - 1)
    
    with open(r"C:\Users\cyber\Downloads\RalphaelOS\flux_schnell_api.json", "r", encoding="utf-8") as f:
        flux_workflow = json.load(f)
        
    flux_workflow["31"]["inputs"]["seed"] = seed
    flux_workflow["6"]["inputs"]["text"] = prompt_text
    flux_workflow["9"]["inputs"]["filename_prefix"] = f"flux_{request_id}"
    
    print(f"[FLUX] Queuing generation for request {request_id}...")
    result = queue_prompt(flux_workflow)
    if not result:
        return None
        
    prompt_id = result['prompt_id']
    print(f"[FLUX] Wait for completion of prompt {prompt_id}...")
    history = wait_for_completion(prompt_id)
    if not history:
        return None
        
    outputs = history.get('outputs', {})
    for node_id, node_output in outputs.items():
        if 'images' in node_output:
            for img in node_output['images']:
                filename = img['filename']
                src_path = COMFY_OUTPUT_DIR / filename
                dst_path = COMFY_INPUT_DIR / filename
                print(f"[FLUX] Saving to input folder: {filename}")
                shutil.copy(src_path, dst_path)
                return filename
                
    return None

def generate_ltx_video(request_id: str, scene_direction: str, input_image_filename: str = None) -> str:
    seed = int(hashlib.sha256(request_id.encode()).hexdigest(), 16) % (2**53 - 1)
    
    # Load LTX workflow
    with open(r"C:\Users\cyber\Downloads\video_ltx2_3_i2v (1).json", "r", encoding="utf-8") as f:
        ltx_workflow = json.load(f)
        
    # Apply substitutions
    # 1. 320:277 seed
    ltx_workflow["320:277"]["inputs"]["noise_seed"] = seed
    
    # 1b. 320:325 LLM seed (to make prompt enhancement deterministic)
    ltx_workflow["320:325"]["inputs"]["sampling_mode.seed"] = seed
    
    # 2. 320:319 prompt
    ltx_workflow["320:319"]["inputs"]["value"] = scene_direction
    
    # 3. 269 Image / 320:302 Switch mode
    if input_image_filename:
        print(f"[LTX] Using input image: {input_image_filename} (Image-to-Video Mode)")
        ltx_workflow["269"]["inputs"]["image"] = input_image_filename
        ltx_workflow["320:302"]["inputs"]["value"] = False
    else:
        print(f"[LTX] No input image provided (Text-to-Video Mode)")
        ltx_workflow["320:302"]["inputs"]["value"] = True
        
    # Leave 320:328 True (enhance)
    ltx_workflow["320:328"]["inputs"]["value"] = True
    
    # Optional output naming
    if "75" in ltx_workflow:
        ltx_workflow["75"]["inputs"]["filename_prefix"] = f"video/LTX_2.3_{request_id}"
        
    print(f"[LTX] Queuing generation for request {request_id}...")
    result = queue_prompt(ltx_workflow)
    if not result:
        return None
        
    prompt_id = result['prompt_id']
    print(f"[LTX] Wait for completion of prompt {prompt_id}... (this may take a few minutes)")
    # Longer timeout for video generation
    history = wait_for_completion(prompt_id, timeout=900)
    if not history:
        return None
        
    outputs = history.get('outputs', {})
    for node_id, node_output in outputs.items():
        # Look for video/image output from the save node
        # In ComfyUI Video nodes it might be 'gifs' or 'images' or 'videos'
        # Let's check all arrays
        for k, items in node_output.items():
            if isinstance(items, list) and len(items) > 0 and isinstance(items[0], dict) and 'filename' in items[0]:
                for item in items:
                    filename = item['filename']
                    # Some nodes put videos in a subfolder
                    subfolder = item.get('subfolder', '')
                    file_path = COMFY_OUTPUT_DIR / subfolder / filename
                    print(f"[LTX] Generated video: {file_path}")
                    return str(file_path)
                
    return None

def test_pipeline():
    import uuid
    request_id = f"test_run_{uuid.uuid4().hex[:8]}"
    
    print("--- 1. Generating Image with Flux ---")
    subject = "A bottle with a beautiful rainbow galaxy inside it on top of a wooden table"
    image_filename = generate_flux_image(request_id, subject)
    
    if not image_filename:
        print("Failed to generate image.")
        return
        
    print(f"Flux Image generated successfully: {image_filename}")
    
    print("\n--- 2. Generating Video with LTX-2.3 ---")
    scene_direction = "The bottle glows softly on the wooden table, tiny stars twinkling inside the galaxy. A subtle camera push-in highlights the cosmic swirl inside."
    
    video_path = generate_ltx_video(request_id, scene_direction, image_filename)
    
    if not video_path:
        print("Failed to generate video.")
        return
        
    print(f"LTX Video generated successfully: {video_path}")
    
    print("\n--- 3. Verifying with ffprobe ---")
    cmd = [
        "ffprobe", 
        "-v", "error", 
        "-show_entries", "format=duration:stream=width,height,bit_rate,codec_name", 
        "-of", "json",
        str(video_path)
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        probe_data = json.loads(result.stdout)
        pprint(probe_data)
    except subprocess.CalledProcessError as e:
        print(f"ffprobe failed: {e.stderr.strip()}")

if __name__ == "__main__":
    test_pipeline()
