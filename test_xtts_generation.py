import sys
import logging
import time
from pathlib import Path
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
sys.path.insert(0, r"C:\Users\cyber\Downloads\RalphaelOS")

from raphael_core.kernel.services.media_generation.xtts_client import XTTSClient

def wait_for_server(url="http://localhost:8020", timeout=600):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            res = requests.get(f"{url}/docs")
            if res.status_code == 200:
                logging.info("XTTS Server is up!")
                return True
        except requests.ConnectionError:
            pass
        logging.info("Waiting for XTTS server to start...")
        time.sleep(5)
    return False

def main():
    if not wait_for_server():
        logging.error("XTTS server failed to start.")
        return
        
    client = XTTSClient(base_url="http://localhost:8020")
    
    script = (
        "This is the first sentence of the continuous narration. "
        "And here is the second sentence, which will be spoken by the same voice in the same continuous breath."
    )
    
    out_path = str(Path(r"C:\Users\cyber\Downloads\RalphaelOS\xtts_master_audio.wav").absolute())
    
    try:
        # Use persona_1.wav that we mapped to the container
        # Note: Depending on daswer123's implementation, the voice might just be the filename
        # like "persona_1.wav" or just "persona_1"
        result_path = client.generate_speech(text=script, voice="persona_1.wav", output_path=out_path)
        logging.info(f"Success! Master audio generated at: {result_path}")
    except Exception as e:
        logging.error(f"Generation failed: {e}")

if __name__ == "__main__":
    main()
