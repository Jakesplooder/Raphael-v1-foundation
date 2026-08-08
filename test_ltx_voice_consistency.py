import json
import urllib.request
from pathlib import Path
import time
import urllib.error
import shutil

def queue_prompt(prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request("http://127.0.0.1:8188/prompt", data=data)
    try:
        response = urllib.request.urlopen(req)
        return json.loads(response.read())
    except urllib.error.URLError as e:
        print(f"Failed to queue prompt: {e}")
        return None

def check_history(prompt_id):
    req = urllib.request.Request(f"http://127.0.0.1:8188/history/{prompt_id}")
    try:
        response = urllib.request.urlopen(req)
        return json.loads(response.read())
    except urllib.error.URLError:
        return None

def run_shot(workflow_path, image_name, prompt_text, run_id):
    with open(workflow_path, "r", encoding="utf-8") as f:
        workflow = json.load(f)

    # 1. Set Image
    workflow["269"]["inputs"]["image"] = image_name

    # 2. Set Prompt
    workflow["320:319"]["inputs"]["value"] = prompt_text
    workflow["320:302"]["inputs"]["value"] = False
    
    # Give a specific prefix
    if "75" in workflow:
        workflow["75"]["inputs"]["filename_prefix"] = f"video/LTX_consistency_{run_id}"

    # 3. Queue
    print(f"[{run_id}] Queuing prompt...")
    res = queue_prompt(workflow)
    if not res:
        return None
        
    prompt_id = res['prompt_id']
    print(f"[{run_id}] Prompt queued! ID: {prompt_id}")

    # 4. Wait
    while True:
        history = check_history(prompt_id)
        if history and prompt_id in history:
            print(f"[{run_id}] Generation complete!")
            outputs = history[prompt_id].get("outputs", {})
            for node_id, node_output in outputs.items():
                if "images" in node_output:
                    for img in node_output["images"]:
                        filename = img["filename"]
                        subfolder = img.get("subfolder", "")
                        return Path(r"C:\ComfyUI\output") / subfolder / filename
            return None
        time.sleep(5)

def main():
    workflow_path = r"C:\Users\cyber\Downloads\video_ltx2_3_i2v (1).json"

    src_image = r"C:\ComfyUI\output\ComfyUI_00001_.png"
    dst_image = r"C:\ComfyUI\input\test_consistency_input.png"
    shutil.copy(src_image, dst_image)
    
    prompt_1 = (
        "A woman stands in a plain white room, looking directly at the camera. "
        "She says clearly: 'This is the first sentence of the continuous narration.' "
        "Her mouth moves in sync with the words. No music, no background noise."
    )
    
    prompt_2 = (
        "A woman stands in a plain white room, looking directly at the camera. "
        "She says clearly: 'And here is the second sentence, split across a different shot.' "
        "Her mouth moves in sync with the words. No music, no background noise."
    )
    
    video1 = run_shot(workflow_path, "test_consistency_input.png", prompt_1, "shot_1")
    print(f"Shot 1 finished: {video1}")
    
    video2 = run_shot(workflow_path, "test_consistency_input.png", prompt_2, "shot_2")
    print(f"Shot 2 finished: {video2}")

if __name__ == "__main__":
    main()
