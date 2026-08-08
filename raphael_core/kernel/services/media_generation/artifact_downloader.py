import urllib.request
import urllib.parse
import os
import logging
from typing import Dict, Optional

logger = logging.getLogger("kernel.media_generation.artifact_downloader")

class ArtifactDownloader:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def download_video(self, history_output: Dict, target_path: str) -> bool:
        """
        Parses the /history output payload, finds the saved video filename,
        and downloads it via /view?filename=...
        """
        # Search for SaveVideo node output (which is node 75 in LTX)
        # However, the history structure for outputs usually looks like:
        # { "75": { "gifs": [ {"filename": "video/LTX_...", "subfolder": "", "type": "output"} ] } }
        
        target_filename = None
        subfolder = ""
        folder_type = "output"
        
        for node_id, output_data in history_output.items():
            if "gifs" in output_data:  # SaveVideo sometimes stores under 'gifs'
                vid_info = output_data["gifs"][0]
                target_filename = vid_info.get("filename")
                subfolder = vid_info.get("subfolder", "")
                folder_type = vid_info.get("type", "output")
                break
            elif "video" in output_data:
                vid_info = output_data["video"][0]
                target_filename = vid_info.get("filename")
                subfolder = vid_info.get("subfolder", "")
                folder_type = vid_info.get("type", "output")
                break
                
        if not target_filename:
            logger.error("No video artifact found in history output.")
            return False

        # Build download URL
        query = urllib.parse.urlencode({
            "filename": target_filename,
            "subfolder": subfolder,
            "type": folder_type
        })
        url = urllib.parse.urljoin(self.base_url, f"/view?{query}")
        
        try:
            logger.info(f"Downloading video from {url} to {target_path}")
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            urllib.request.urlretrieve(url, target_path)
            return True
        except Exception as e:
            logger.error(f"Failed to download video artifact: {e}")
            return False
