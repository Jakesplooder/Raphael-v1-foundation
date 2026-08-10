import os
import json
import hashlib
import time
from pathlib import Path
from typing import Optional, Any
from .providers.base_provider import ReasoningResult

CACHE_DIR = Path(os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"R:\RaphaelOS"), r"\memory\llm_cache"))
CACHE_DIR.mkdir(parents=True, exist_ok=True)

class CacheManager:
    TTL_MAP = {
        "prediction": 24 * 3600,
        "executive": 3600,
        "research": 7 * 24 * 3600,
        "creative": float('inf')
    }

    @staticmethod
    def _generate_hash(model: str, system_prompt: str, context: str, task: str) -> str:
        data = f"{model}:{system_prompt}:{context}:{task}"
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    @staticmethod
    def get(model: str, system_prompt: str, context: str, task: str, category: str) -> Optional[ReasoningResult]:
        cache_hash = CacheManager._generate_hash(model, system_prompt, context, task)
        cache_file = CACHE_DIR / f"{cache_hash}.json"
        
        if not cache_file.exists():
            return None
            
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Check expiration
            ttl = CacheManager.TTL_MAP.get(category, 0)
            if ttl < float('inf'):
                age = time.time() - data.get("timestamp", 0)
                if age > ttl:
                    return None
                    
            return ReasoningResult(
                provider_name=data["provider_name"],
                model_name=data["model_name"],
                response=data["response"],
                latency_sec=data["latency_sec"],
                token_count=data["token_count"],
                raw_output=data["raw_output"]
            )
        except Exception:
            return None

    @staticmethod
    def set(model: str, system_prompt: str, context: str, task: str, result: ReasoningResult):
        cache_hash = CacheManager._generate_hash(model, system_prompt, context, task)
        cache_file = CACHE_DIR / f"{cache_hash}.json"
        
        data = {
            "hash": cache_hash,
            "timestamp": time.time(),
            "provider_name": result.provider_name,
            "model_name": result.model_name,
            "response": result.response,
            "latency_sec": result.latency_sec,
            "token_count": result.token_count,
            "raw_output": result.raw_output
        }
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass
