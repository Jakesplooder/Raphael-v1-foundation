import os
import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class XTTSClient:
    def __init__(self, base_url="http://localhost:8020"):
        self.base_url = base_url

    def generate_speech(self, text: str, voice: str = "persona_1.wav", output_path: str = "output.wav") -> str:
        url = f"{self.base_url}/tts_to_audio/"
        
        payload = {
            "text": text,
            "speaker_wav": voice,
            "language": "en"
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        logger.info(f"Generating TTS for: {text[:50]}... using voice: {voice}")
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            logger.info(f"TTS generated and saved to {output_path}")
            return output_path
        else:
            logger.error(f"TTS generation failed: {response.status_code} - {response.text}")
            raise Exception(f"TTS Generation failed: {response.text}")
