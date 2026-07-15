import urllib.request
import json
import logging
from typing import Dict, Any

logger = logging.getLogger("rrk.models.health")

class ModelHealthChecker:
    """
    Interfaces with the Host Manager to determine hardware availability and model load status.
    """
    def __init__(self, host_manager_url: str = "http://127.0.0.1:8789"):
        self.host_url = host_manager_url

    def get_gpu_status(self) -> Dict[str, Any]:
        try:
            req = urllib.request.urlopen(f"{self.host_url}/gpu/status", timeout=2)
            data = json.loads(req.read().decode())
            if data.get("status") == "ok":
                return {"healthy": True, "gpus": data.get("gpus", [])}
            return {"healthy": False, "gpus": []}
        except Exception as e:
            logger.warning(f"GPU status check failed: {e}")
            return {"healthy": False, "gpus": []}

    def get_loaded_models(self) -> list:
        try:
            req = urllib.request.urlopen(f"{self.host_url}/models/status", timeout=2)
            data = json.loads(req.read().decode())
            if data.get("status") == "ok":
                # Extract names from ollama 'ps' response
                return [m.get("name") for m in data.get("loaded_models", [])]
            return []
        except Exception as e:
            logger.warning(f"Model status check failed: {e}")
            return []

    def can_load_model(self, model_name: str, required_vram_gb: int = 8) -> bool:
        """
        Check if we have enough VRAM to load the requested model.
        """
        status = self.get_gpu_status()
        if not status["healthy"] or not status["gpus"]:
            # If we can't check, assume we can try
            return True
            
        # Check first GPU
        gpu = status["gpus"][0]
        free_mb = gpu.get("memory_total_mb", 0) - gpu.get("memory_used_mb", 0)
        free_gb = free_mb / 1024.0
        
        return free_gb >= required_vram_gb
