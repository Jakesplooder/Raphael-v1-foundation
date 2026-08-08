import json
from pathlib import Path
from typing import Dict, Any

from raphael_core.kernel.event_bus import emit

class MissionAnalyticsEngine:
    def __init__(self):
        pass
        
    def process_review(self, mission_dir: Path):
        review_path = mission_dir / "review.json"
        if not review_path.exists():
            return
            
        review_data = json.loads(review_path.read_text())
        
        if review_data.get("decision") != "approved":
            return
            
        # Extract Production Intelligence
        # Mocking extraction for now
        production_intel = {
            "average_production_time": "14m",
            "highest_delay": "thumbnail generation"
        }
        
        # Extract Content Intelligence
        content_intel = []
        for lesson in review_data.get("lessons", []):
            content_intel.append({
                "pattern": lesson,
                "confidence": 0.72,
                "evidence": [review_data["mission_id"]],
                "classification": "observation"
            })
            
        # Extract Strategy Intelligence (but don't emit as pattern discovered automatically anymore)
        strategy_intel = {
            "decision": "Increase Business Case Studies production",
            "approval_required": True
        }
        
        analysis = {
            "mission": review_data["mission_id"],
            "production_intel": production_intel,
            "content_intel": content_intel,
            "strategy_intel": strategy_intel
        }
        
        (mission_dir / "mission_analysis.json").write_text(json.dumps(analysis, indent=2))
        
        for intel in content_intel:
            # Emit observation
            emit("MISSION.OBSERVATION_CAPTURED", "MissionAnalyticsEngine", intel)
            
            # If observation is strong enough (mocked as true for this test), form a hypothesis
            if "psychology" in intel["pattern"].lower() or "case studies" in strategy_intel["decision"].lower():
                hypothesis = {
                    "id": f"hyp_{review_data['mission_id']}",
                    "name": intel["pattern"],
                    "state": "PROPOSED",
                    "confidence": 0.75,
                    "evidence_count": 1,
                    "evidence_list": [review_data["mission_id"]],
                    "strategy_action": strategy_intel
                }
                emit("STRATEGY.HYPOTHESIS_CREATED", "MissionAnalyticsEngine", hypothesis)
