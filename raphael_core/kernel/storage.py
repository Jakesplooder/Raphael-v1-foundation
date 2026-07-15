import os
import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger("rrk.kernel.storage")

class KernelStorage:
    """
    Unified storage interface for RRK Kernel.
    Phase 1/2: Writes go to native 'raphael_storage', reads fallback to legacy if not found.
    """
    def __init__(self, base_dir: str = "raphael_storage"):
        self.base_dir = base_dir
        self.legacy_dirs = {
            "vision": "vision_memory",
            "workforce": "workforce_memory",
            "world": "world_memory",
            "business": "business_factory_memory",
            "self_improvement": "self_improvement_memory"
        }
        os.makedirs(self.base_dir, exist_ok=True)
        
    def _get_native_path(self, domain: str, filename: str) -> str:
        domain_dir = os.path.join(self.base_dir, "memory", domain)
        os.makedirs(domain_dir, exist_ok=True)
        return os.path.join(domain_dir, filename)
        
    def _get_legacy_path(self, domain: str, filename: str) -> str:
        legacy_dir = self.legacy_dirs.get(domain)
        if legacy_dir:
            return os.path.join(legacy_dir, filename)
        return None

    def save(self, domain: str, filename: str, data: Any) -> bool:
        path = self._get_native_path(domain, filename)
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Saved to native storage: {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save {path}: {e}")
            return False

    def load(self, domain: str, filename: str) -> Any:
        # 1. Try native
        native_path = self._get_native_path(domain, filename)
        if os.path.exists(native_path):
            with open(native_path, "r", encoding="utf-8") as f:
                return json.load(f)
                
        # 2. Fallback to legacy
        legacy_path = self._get_legacy_path(domain, filename)
        if legacy_path and os.path.exists(legacy_path):
            logger.info(f"Legacy fallback read: {legacy_path}")
            with open(legacy_path, "r", encoding="utf-8") as f:
                return json.load(f)
                
        return None

    def query(self, domain: str) -> List[str]:
        # Return combined list of files from native and legacy
        results = set()
        native_dir = os.path.join(self.base_dir, "memory", domain)
        if os.path.exists(native_dir):
            results.update(os.listdir(native_dir))
            
        legacy_dir = self.legacy_dirs.get(domain)
        if legacy_dir and os.path.exists(legacy_dir):
            results.update(os.listdir(legacy_dir))
            
        return list(results)

    def archive(self, domain: str, filename: str):
        # Move file to an archive folder within native storage
        native_path = self._get_native_path(domain, filename)
        if os.path.exists(native_path):
            archive_dir = os.path.join(self.base_dir, "archive", domain)
            os.makedirs(archive_dir, exist_ok=True)
            os.rename(native_path, os.path.join(archive_dir, filename))
            return True
        return False
