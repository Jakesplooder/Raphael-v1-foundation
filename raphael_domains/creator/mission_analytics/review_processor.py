import json
from pathlib import Path
from typing import Dict, Any

from raphael_core.kernel.event_bus import emit
from raphael_domains.creator.mission_analytics.analytics_engine import MissionAnalyticsEngine

class ReviewProcessor:
    def __init__(self, analytics_engine: MissionAnalyticsEngine):
        self.analytics_engine = analytics_engine
        
    def handle_review_submitted(self, event_payload: Dict[str, Any]):
        """
        Event payload expects:
        {
            "mission_id": str,
            "mission_dir": str
        }
        """
        mission_id = event_payload.get("mission_id")
        mission_dir = Path(event_payload.get("mission_dir"))
        
        # Validates review.json
        review_path = mission_dir / "review.json"
        if not review_path.exists():
            return
            
        review = json.loads(review_path.read_text())
        
        # We only process if it's approved
        if review.get("decision") == "approved":
            emit("MISSION.QUALITY_SCORED", "ReviewProcessor", {
                "mission_id": mission_id,
                "scores": review.get("scores", {})
            })
            
            # Trigger analytics
            self.analytics_engine.process_review(mission_dir)
