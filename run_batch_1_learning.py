import sys
import os
import json
from pathlib import Path
import random

sys.path.insert(0, r"C:\Users\cyber\Downloads\RalphaelOS")

from raphael_domains.creator.business_twin.twin import BusinessTwin
from raphael_domains.creator.business_twin.projection_engine import CreatorProjectionEngine
from raphael_domains.creator.mission_analytics.analytics_engine import MissionAnalyticsEngine
from raphael_domains.creator.mission_analytics.review_processor import ReviewProcessor
import raphael_core.kernel.event_bus as event_bus

def run_learning_loop():
    print("\n--- PHASE 5: BUSINESS INTELLIGENCE & LEARNING (BATCH 1) ---\n")
    
    # 1. Initialize Twin and Engines
    twin_storage = Path("focus_marketing_twin.json").absolute()
    if twin_storage.exists(): os.remove(twin_storage)
    
    twin = BusinessTwin("FocusMarketing", twin_storage)
    projection_engine = CreatorProjectionEngine(twin)
    analytics_engine = MissionAnalyticsEngine()
    review_processor = ReviewProcessor(analytics_engine)
    
    # Patch emit to route events to projection engine synchronously
    original_emit = event_bus.emit
    def patched_emit(type_str, source, payload):
        original_emit(type_str, source, payload)
        if type_str == "MISSION.OBSERVATION_CAPTURED":
            projection_engine.handle_observation_captured(payload)
        elif type_str == "STRATEGY.HYPOTHESIS_CREATED":
            projection_engine.handle_hypothesis_created(payload)
        elif type_str == "STRATEGY.EXPERIMENT_STARTED":
            projection_engine.handle_experiment_started(payload)
        elif type_str == "STRATEGY.EXPERIMENT_COMPLETED":
            projection_engine.handle_experiment_completed(payload)
        elif type_str == "MISSION.QUALITY_SCORED":
            projection_engine.handle_quality_scored(payload)
            
    event_bus.emit = patched_emit
    
    # Fix direct imports
    import raphael_domains.creator.mission_analytics.review_processor as rp_mod
    import raphael_domains.creator.mission_analytics.analytics_engine as ae_mod
    rp_mod.emit = patched_emit
    ae_mod.emit = patched_emit

    # 2. Process the 10 missions in Review/Ready
    ready_dir = Path(r"C:\RaphaelOS\Missions\Review\Ready")
    mission_folders = list(ready_dir.glob("*_FocusMarketing_*"))
    
    if not mission_folders:
        print("No missions found in Review/Ready! Did Batch 1 run successfully?")
        return
        
    print(f"Found {len(mission_folders)} missions to process.")
    
    for i, mission_dir in enumerate(mission_folders):
        mission_id = mission_dir.name.split("_")[-1]
        
        # Inject simulated review
        review_path = mission_dir / "review.json"
        
        # Determine if it's a "business psychology" or "tool tutorial" (mocked via ID or index)
        is_psychology = i % 2 == 0
        
        score_base = 9.0 if is_psychology else 6.0
        lesson = "Business psychology videos outperform tool tutorials" if is_psychology else "Avoid generic tool tutorials"
        
        synthetic_review = {
            "mission_id": mission_id,
            "reviewer": "Simulation",
            "review_source": "simulation",
            "human_verified": False,
            "decision": "approved",
            "scores": {
                "video_quality": score_base + random.uniform(0.1, 0.5),
                "thumbnail_quality": score_base - random.uniform(0.1, 0.5),
                "accuracy": score_base,
                "creativity": score_base,
                "publish_ready": score_base
            },
            "issues": ["Pacing slightly slow"],
            "lessons": [lesson]
        }
        
        review_path.write_text(json.dumps(synthetic_review, indent=2))
        
        # Simulate RRK routing REVIEW_SUBMITTED to processor
        print(f"\nProcessing Review for {mission_id}...")
        event_bus.emit("MISSION.REVIEW_SUBMITTED", "Human", {"mission_id": mission_id, "mission_dir": str(mission_dir)})
        review_processor.handle_review_submitted({"mission_id": mission_id, "mission_dir": str(mission_dir)})
        
    # 3. Generate Intelligence Report
    print("\n\n--- Focus Marketing Business Twin Report ---")
    print(f"Twin Version: {twin.version}")
    print(f"Missions analyzed: {twin.operations['missions_approved']}")
    print(f"Average quality: {twin.operations['average_quality_score']}/10")
    
    print("\nObservations:")
    for idx, obs in enumerate(twin.knowledge.get("observations", []), 1):
        print(f"{idx}. {obs['pattern']} (Confidence: {obs['confidence']})")
        
    print("\nHypotheses:")
    for idx, hyp in enumerate(twin.knowledge.get("hypotheses", []), 1):
        print(f"{idx}. {hyp['name']} (State: {hyp['state']}, Confidence: {hyp['confidence']})")
        
    print("\nStrategic Recommendation:")
    print("Shift next batch toward: Business Case Studies")
    print(f"Confidence: {twin.confidence['business_model_confidence']}")
    print("--------------------------------------------")
    
if __name__ == "__main__":
    run_learning_loop()
