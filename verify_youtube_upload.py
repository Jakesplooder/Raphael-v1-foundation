import sys
import logging
from pathlib import Path
import time
import uuid

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')

sys.path.insert(0, r"C:\Users\cyber\Downloads\RalphaelOS")

from raphael_core.kernel.services.youtube_client import YouTubeClient

def create_dummy_video():
    import subprocess
    output = "dummy_video.mp4"
    if not Path(output).exists():
        logging.info("Creating dummy 2-second video...")
        subprocess.run([
            "ffmpeg", "-f", "lavfi", "-i", "color=c=blue:s=1280x720:d=2", 
            "-c:v", "libx264", "-y", output
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output

if __name__ == "__main__":
    client = YouTubeClient()
    video_path = create_dummy_video()
    req_id = f"dummy_{uuid.uuid4().hex[:8]}"
    
    logging.info(f"Starting dummy upload with request ID: {req_id}")
    video_id = client.upload_video(
        video_path=video_path,
        title=f"Test Upload {req_id}",
        description=f"Automated test upload. request_id: {req_id}",
        privacy_status="private"
    )
    
    if video_id:
        logging.info(f"Successfully uploaded dummy video. URL: https://youtu.be/{video_id}")
        
        logging.info("Testing search-before-create idempotency...")
        found_id = client.search_video(req_id)
        if found_id == video_id:
            logging.info(f"Search successfully found the video: {found_id}")
        else:
            logging.error(f"Search failed to find video! Expected {video_id}, got {found_id}")
    else:
        logging.error("Failed to upload dummy video.")
