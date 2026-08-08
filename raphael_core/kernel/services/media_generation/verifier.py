import subprocess
import json
import logging
import os
from typing import Dict, Any

logger = logging.getLogger("kernel.media_generation.verifier")

class ArtifactVerifier:
    def verify(self, video_path: str) -> bool:
        """
        Runs ffprobe to ensure the downloaded video is actually a valid media file,
        has size > 0, and has a duration.
        """
        if not os.path.exists(video_path):
            logger.error(f"Video file not found at {video_path}")
            return False
            
        if os.path.getsize(video_path) == 0:
            logger.error(f"Video file at {video_path} is 0 bytes.")
            return False
            
        cmd = [
            "ffprobe", 
            "-v", "quiet", 
            "-print_format", "json", 
            "-show_format", 
            "-show_streams", 
            video_path
        ]
        
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            probe_data = json.loads(result.stdout)
            
            # Check for at least one video stream
            streams = probe_data.get("streams", [])
            has_video = any(s.get("codec_type") == "video" for s in streams)
            
            if not has_video:
                logger.error(f"Artifact {video_path} has no video streams.")
                return False
                
            # Check duration
            format_data = probe_data.get("format", {})
            duration = float(format_data.get("duration", 0.0))
            if duration <= 0:
                logger.error(f"Artifact {video_path} has invalid duration: {duration}")
                return False
                
            logger.info(f"Verified artifact {video_path} (duration: {duration}s)")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"FFProbe failed on artifact {video_path}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error during artifact verification: {e}")
            return False
