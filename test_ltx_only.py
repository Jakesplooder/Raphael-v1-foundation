import urllib.request
import urllib.parse
import urllib.error
import json
import time

COMFY_URL = "http://127.0.0.1:8188"

def queue_prompt(prompt_json):
    p = {"prompt": prompt_json}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"{COMFY_URL}/prompt", data=data, headers={'Content-Type': 'application/json'})
    response = urllib.request.urlopen(req)
    return json.loads(response.read())

def get_history(prompt_id):
    req = urllib.request.Request(f"{COMFY_URL}/history/{prompt_id}")
    try:
        response = urllib.request.urlopen(req)
        return json.loads(response.read())
    except Exception as e:
        print(f"Transient error polling history: {e}")
        return None

def wait_for_completion(prompt_id, timeout=900):
    start_time = time.time()
    while True:
        history = get_history(prompt_id)
        if history and prompt_id in history:
            return history[prompt_id]
        
        if time.time() - start_time > timeout:
            print("Timeout waiting for completion.")
            return None
            
        time.sleep(5)

def test_ltx():
    # Load LTX workflow
    with open(r"C:\Users\cyber\Downloads\video_ltx2_3_i2v (1).json", "r", encoding="utf-8") as f:
        ltx_workflow = json.load(f)
        
    # We will just run it as-is, which uses egyptian_queen.png and prompt enhancement.
    # Just override seed for uniqueness
    request_id = "ltx_test_001"
    seed = 123456789
    ltx_workflow["320:277"]["inputs"]["noise_seed"] = seed
    ltx_workflow["320:325"]["inputs"]["sampling_mode.seed"] = seed
    ltx_workflow["75"]["inputs"]["filename_prefix"] = f"video/LTX_2.3_{request_id}"
    
    # Bypass broken TextGenerateLTX2Prompt node (due to PyTorch version mismatch)
    ltx_workflow["320:328"]["inputs"]["value"] = False
        
    print(f"[LTX] Queuing generation for request {request_id}...")
    try:
        result = queue_prompt(ltx_workflow)
    except Exception as e:
        print(f"Failed to queue: {e}")
        return
        
    prompt_id = result['prompt_id']
    print(f"[LTX] Wait for completion of prompt {prompt_id}...")
    
    history = wait_for_completion(prompt_id, timeout=900)
    if not history:
        print("[LTX] Failed to get history (timeout or continuous crash)")
        return
        
    outputs = history.get('outputs', {})
    print("Generation complete! Outputs:")
    print(json.dumps(outputs, indent=2))

if __name__ == "__main__":
    test_ltx()
