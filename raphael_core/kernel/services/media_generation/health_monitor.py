import time
import logging
from typing import Optional, Dict

logger = logging.getLogger("kernel.media_generation.health_monitor")

class ComfyUIHealthMonitor:
    def __init__(self, client):
        self.client = client
        self.last_stats: Optional[Dict] = None
        self.last_check_time = 0
        self.is_healthy = False
        
        # Incident thresholds
        self.consecutive_failures = 0
        
    def check_health(self) -> bool:
        """
        Pings /system_stats to assess health.
        Returns True if server is reachable and healthy, False otherwise.
        """
        try:
            stats = self.client.get_system_stats()
            self.is_healthy = True
            self.consecutive_failures = 0
            
            # TODO: Inspect stats for GPU memory or PID changes if supported by API.
            # Example: check if stats['uptime'] reset or stats['pid'] changed
            # Currently /system_stats mostly returns os, ram, devices
            
            self.last_stats = stats
            self.last_check_time = time.time()
            return True
            
        except Exception as e:
            self.consecutive_failures += 1
            self.is_healthy = False
            logger.warning(f"Health check failed ({self.consecutive_failures} consecutive): {e}")
            
            if self.consecutive_failures > 5:
                logger.error("Incident: ComfyUI is completely unreachable. Manual intervention required.")
            return False

    def wait_for_recovery(self, timeout=300) -> bool:
        """
        Blocks until health check passes, or timeout occurs.
        """
        logger.info("Waiting for ComfyUI to recover...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.check_health():
                logger.info("ComfyUI recovered. Continuing mission.")
                return True
            time.sleep(5)
            
        logger.error("ComfyUI did not recover within timeout.")
        return False
