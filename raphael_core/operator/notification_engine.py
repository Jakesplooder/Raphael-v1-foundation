from typing import List
import time
from .executive_analysis import ExecutiveRecommendation

class NotificationEngine:
    """
    Filters and deduplicates executive recommendations so that the same 
    recommendations are not constantly blasted to the UI or downstream 
    notification systems (like Discord/Voice) on every tick.
    """
    def __init__(self):
        # Maps a semantic signature of a recommendation to the timestamp it was last emitted.
        self._emitted_cache = {}
        self._dedupe_ttl_seconds = 3600  # 1 hour default
        
    def filter(self, recommendations: List[ExecutiveRecommendation]) -> List[ExecutiveRecommendation]:
        now = time.time()
        filtered_recs = []
        
        for rec in recommendations:
            # Create a semantic signature to deduplicate
            # e.g., "Review System Health:system_health"
            sig = f"{rec.action}:{rec.target}"
            
            last_emitted = self._emitted_cache.get(sig, 0)
            if now - last_emitted > self._dedupe_ttl_seconds:
                filtered_recs.append(rec)
                self._emitted_cache[sig] = now
            else:
                # Suppressed because it was emitted recently
                pass
                
        return filtered_recs
        
    def reset(self):
        self._emitted_cache.clear()

# Global singleton
notification_engine = NotificationEngine()
