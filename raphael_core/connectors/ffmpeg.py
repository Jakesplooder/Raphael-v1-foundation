import os
import subprocess
import logging
from typing import Dict, Any, List
from raphael_core.connectors.base_connector import BaseConnector

logger = logging.getLogger(__name__)

class FFmpegConnector(BaseConnector):
    """
    Handles video manipulation, specifically the multi-shot STITCH_AND_SYNC stage.
    """
    
    def metadata(self) -> Dict[str, Any]:
        return {
            "name": "FFmpegConnector",
            "version": "1.0",
            "requires_auth": False,
            "supports_async": True
        }

    def capabilities(self) -> List[Dict[str, Any]]:
        return [{"action": "stitch_and_sync", "description": "Concatenates video shots and syncs master audio"}]

    async def validate(self, action: str, params: Dict[str, Any]) -> bool:
        if action == "stitch_and_sync":
            if not params.get("video_shots") or not params.get("audio_master"):
                raise ValueError("stitch_and_sync requires 'video_shots' array and 'audio_master' path.")
            return True
        return False

    async def health(self) -> bool:
        try:
            subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True
        except Exception:
            return False

    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        await self.validate(action, params)
        
        if action == "stitch_and_sync":
            return await self._stitch_and_sync(params)
            
        raise ValueError(f"Unsupported action: {action}")

    async def _stitch_and_sync(self, params: Dict[str, Any]) -> Dict[str, Any]:
        videos = params["video_shots"]
        audio_master = params["audio_master"]
        output_path = params.get("output_path", os.path.join(os.getcwd(), "final_render.mp4"))
        concat_file = os.path.join(os.getcwd(), "videos.txt")

        # Step 1: Build the concat demuxer file
        with open(concat_file, "w") as f:
            for video in videos:
                # Absolute paths required for safety
                f.write(f"file '{os.path.abspath(video)}'\n")

        # Step 2: Execute the FFmpeg STITCH
        # -map 0:v explicitly drops native LTX audio
        # -map 1:a overlays the XTTS master track
        # -shortest automatically trims excess video frames to match audio duration
        cmd = [
            "ffmpeg",
            "-y",  # Overwrite output if exists
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file,
            "-i", audio_master,
            "-map", "0:v",
            "-map", "1:a",
            "-c:v", "copy",
            "-c:a", "aac", 
            "-shortest",
            output_path
        ]

        logger.info(f"Executing STITCH_AND_SYNC: {' '.join(cmd)}")
        
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if process.returncode == 0:
            logger.info(f"STITCH_AND_SYNC complete. Final render at {output_path}")
            if os.path.exists(concat_file):
                os.remove(concat_file)
                
            return {
                "status": "success",
                "data": {"final_render_path": output_path}
            }
        else:
            logger.error(f"FFmpeg failed: {process.stderr}")
            return {
                "status": "failed",
                "data": {"error": process.stderr}
            }
