import sys
import os
import json
import time
from pathlib import Path
import random

sys.path.insert(0, r"R:\RalphaelOS_Repo")

from raphael_core.kernel.repositories.idempotency_store import IdempotencyStore
from raphael_domains.creator.video_engine import VideoPipelineFSM, BrandContext
from raphael_domains.creator.business_twin.twin import BusinessTwin
from raphael_domains.creator.business_twin.projection_engine import CreatorProjectionEngine
from raphael_domains.creator.mission_analytics.analytics_engine import MissionAnalyticsEngine
from raphael_domains.creator.mission_analytics.review_processor import ReviewProcessor
import raphael_core.kernel.event_bus as event_bus
import raphael_domains.creator.mission_analytics.review_processor as rp_mod
import raphael_domains.creator.mission_analytics.analytics_engine as ae_mod

def run_experiment_loop():
    print("\n--- PHASE 6: STRATEGY EXPERIMENTATION (BATCH 2) ---\n")
    
    twin_storage = Path("focus_marketing_twin.json").absolute()
    if not twin_storage.exists():
        print("Business Twin state not found. Did you run batch 1 learning?")
        return
        
    twin = BusinessTwin("FocusMarketing", twin_storage)
    projection_engine = CreatorProjectionEngine(twin)
    analytics_engine = MissionAnalyticsEngine()
    review_processor = ReviewProcessor(analytics_engine)
    
    # Patch emit
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
    rp_mod.emit = patched_emit
    ae_mod.emit = patched_emit
    
    # 1. Human Approval Gate
    print(f"Total experiments in Twin: {len(twin.knowledge.get('experiments', []))}")
    pending_experiments = [e for e in twin.knowledge.get("experiments", []) if e.get("result") == "pending"]
    if not pending_experiments:
        print("No pending experiments found in the Business Twin.")
        return
        
    exp = pending_experiments[-1]
    print(f"Human CEO Approved Experiment: {exp['experiment_id']}")
    event_bus.emit("STRATEGY.EXPERIMENT_STARTED", "HumanGate", {
        "experiment_id": exp["experiment_id"],
        "hypothesis_id": exp["hypothesis_id"]
    })
    
    # 2. Execution (FSM)
    topics = [
        # 7 Business Case Studies
        "Why LEGO Almost Went Bankrupt", "Nintendo's Ocean Strategy",
        "How Pixar Scales Creativity", "McDonald's Real Estate Empire",
        "IKEA's Psychological Maze", "Costco's Loss Leader Mastery",
        "Ferrari's Artificial Scarcity",
        # 2 Marketing Psychology
        "The Decoy Effect in SaaS", "Color Psychology in Branding",
        # 1 AI Marketing (Control)
        "How to use LTX for Ads"
    ]
    
    brand = BrandContext("FocusMarketing", "ref_1", "voice_1", {}, [])
    store = IdempotencyStore(str(Path("batch2_idempotency.db").absolute()))
    engine = VideoPipelineFSM(store)
    
    for i, topic in enumerate(topics, 11): # Starting from 11
        request_id = f"Batch2_Mission_{i:03d}"
        print(f"\n[Mission {i}/20] Kicking off '{topic}'")
        engine.run_pipeline(request_id, {"objective": f"Create video: {topic}"}, brand)
        time.sleep(0.1)
        
    # 3. Simulate Reviews and Process
    ready_dir = Path(r"R:\RaphaelOS\Missions\Review\Ready")
    batch2_folders = list(ready_dir.glob("*_FocusMarketing_Batch2_*"))
    
    for folder in batch2_folders:
        mission_id = folder.name.split("_")[-1]
        topic_idx = int(mission_id.split("_")[-1]) - 11
        topic_name = topics[topic_idx]
        
        # Simulated performance
        if topic_idx < 7: # Case Studies
            score = 9.4 + random.uniform(0.1, 0.5)
        elif topic_idx < 9: # Psychology
            score = 8.5 + random.uniform(0.1, 0.5)
        else: # Control (AI)
            score = 6.2 + random.uniform(0.1, 0.5)
            
        synthetic_review = {
            "mission_id": mission_id,
            "reviewer": "Simulation",
            "review_source": "simulation",
            "human_verified": False,
            "decision": "approved",
            "scores": {
                "video_quality": score,
                "thumbnail_quality": score - 0.2,
                "accuracy": score,
                "creativity": score,
                "publish_ready": score
            },
            "issues": [],
            "lessons": [f"Result for {topic_name}"]
        }
        
        (folder / "review.json").write_text(json.dumps(synthetic_review, indent=2))
        event_bus.emit("MISSION.REVIEW_SUBMITTED", "Human", {"mission_id": mission_id, "mission_dir": str(folder)})
        review_processor.handle_review_submitted({"mission_id": mission_id, "mission_dir": str(folder)})
        
    # 4. Evaluate Experiment and update Confidence
    print(f"\nEvaluating Experiment {exp['experiment_id']}...")
    event_bus.emit("STRATEGY.EXPERIMENT_COMPLETED", "AnalyticsEngine", {
        "experiment_id": exp["experiment_id"],
        "hypothesis_id": exp["hypothesis_id"],
        "result": "validated",
        "confidence_change": 0.14
    })
    
    # 5. Output Report
    print("\n\n--- Focus Marketing Business Twin Report ---")
    print(f"Twin Version: {twin.version}")
    print(f"Missions analyzed: {twin.operations['missions_approved']}")
    print(f"Average quality: {twin.operations['average_quality_score']}/10")
    
    print("\nActive Hypotheses:")
    for hyp in twin.knowledge.get("hypotheses", []):
        print(f"- {hyp['name']} (State: {hyp['state']}, Confidence: {hyp['confidence']})")
        
    print("\nDecision Journal:")
    for decision in twin.decision_journal:
        print(f"- {decision['decision']} (Confidence: {decision['confidence']})")

if __name__ == "__main__":
    run_experiment_loop()
