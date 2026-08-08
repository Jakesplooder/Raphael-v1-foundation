import json
import urllib.request
from pathlib import Path
import time
import urllib.error
import shutil
import subprocess

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

def main():
    workflow_path = r"C:\Users\cyber\Downloads\video_ltx2_3_i2v (1).json"
    with open(workflow_path, "r", encoding="utf-8") as f:
        workflow = json.load(f)

    # 1. Image
    # We'll copy ComfyUI_00001_.png to the input dir just to be safe
    src_image = r"C:\ComfyUI\output\ComfyUI_00001_.png"
    dst_image = r"C:\ComfyUI\input\test_audio_input.png"
    shutil.copy(src_image, dst_image)
    workflow["269"]["inputs"]["image"] = "test_audio_input.png"

    # 2. Prompt for speech
    speech_prompt = (
        "A woman stands in a plain white room, looking directly at the camera. "
        "She says clearly: 'Testing one two three, this is a voice test.' "
        "Her mouth moves in sync with the words. No music, no background noise, "
        "no other sound effects."
    )
    workflow["320:319"]["inputs"]["value"] = speech_prompt
    
    # Ensure I2V flag is false (so it acts as video-to-video? No, video_ltx2_3_i2v is image-to-video). 
    # Wait, the user said "320:302 = false for image-to-video". Let's verify that.
    workflow["320:302"]["inputs"]["value"] = False
    
    # 3. Queue Prompt
    print("Queuing prompt...")
    res = queue_prompt(workflow)
    if not res:
        return
        
    prompt_id = res['prompt_id']
    print(f"Prompt queued! ID: {prompt_id}")

    # 4. Wait for completion
    print("Waiting for generation to complete (approx 4-5 mins)...")
    while True:
        history = check_history(prompt_id)
        if history and prompt_id in history:
            print("Generation complete!")
            outputs = history[prompt_id].get("outputs", {})
            for node_id, node_output in outputs.items():
                if "gifs" in node_output:
                    for gif in node_output["gifs"]:
                        filename = gif["filename"]
                        print(f"Result video: {filename}")
                        # Extract Audio
                        video_path = Path(r"C:\ComfyUI\output") / filename
                        audio_path = Path(r"C:\Users\cyber\Downloads\RalphaelOS") / "test_audio.aac"
                        if audio_path.exists():
                            audio_path.unlink()
                            
                        print("Extracting audio...")
                        subprocess.run([
                            "ffmpeg", "-i", str(video_path), "-vn", "-acodec", "copy", str(audio_path)
                        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        print(f"Audio extracted to {audio_path}")
            break
        time.sleep(10)

if __name__ == "__main__":
    main()
