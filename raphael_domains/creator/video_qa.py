import subprocess
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class VideoQAError(Exception):
    pass

class VideoCorruptError(VideoQAError):
    pass

class VideoDurationError(VideoQAError):
    pass

def verify_video_qa(video_path: Path, expected_min_duration: float = 4.5, expected_max_duration: float = 5.5) -> dict:
    """
    Validates a generated video using ffprobe.
    1. Integrity: Ensures it decodes cleanly.
    2. Duration: Ensures duration falls within acceptable ranges.
    """
    if not video_path.exists():
        raise VideoCorruptError(f"Video file does not exist: {video_path}")
        
    cmd = [
        "ffprobe", 
        "-v", "error", 
        "-show_entries", "format=duration:stream=codec_name,codec_type", 
        "-of", "json",
        str(video_path)
    ]
    
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        probe_data = json.loads(result.stdout)
        
        format_info = probe_data.get("format", {})
        duration_str = format_info.get("duration")
        
        if not duration_str or duration_str == "N/A":
            raise VideoCorruptError("ffprobe returned empty or N/A duration, file may be corrupt or not a video.")
            
        duration = float(duration_str)
        
        if duration < expected_min_duration or duration > expected_max_duration:
            raise VideoDurationError(f"Video duration {duration:.2f}s is outside bounds [{expected_min_duration}s - {expected_max_duration}s].")
            
        streams = probe_data.get("streams", [])
        codecs = [s.get("codec_name") for s in streams]
        
        return {
            "passed": True,
            "duration": duration,
            "codecs": codecs
        }
        
    except subprocess.CalledProcessError as e:
        error_output = e.stderr.strip()
        raise VideoCorruptError(f"Video failed integrity check (corrupt file): {error_output}")
    except ValueError:
        raise VideoCorruptError(f"Could not parse duration from ffprobe output: {duration_str}")
