import sys
import os
import json
import time
import random
from pathlib import Path

sys.path.insert(0, r"C:\Users\cyber\Downloads\RalphaelOS")

from raphael_domains.creator.business_twin.twin import BusinessTwin
from raphael_domains.creator.mission_analytics.analytics_engine import MissionAnalyticsEngine
from raphael_domains.creator.mission_analytics.review_processor import ReviewProcessor
from raphael_core.kernel.services.operations_engine.operations_engine import OperationsEngine
from raphael_core.kernel.services.notification_gateway.notification_service import notification_service
import raphael_core.kernel.event_bus as event_bus

def simulate_mission_execution(mission_id: str, strategy: str, should_fail: bool):
    print(f"\n[EXECUTING] Mission {mission_id} via strategy {strategy}...")
    
    cost_gpu = random.uniform(0.3, 0.6)
    cost_api = random.uniform(0.1, 0.2)
    cost_human = 0.5  # Fixed human time cost (simulated $)
    total_cost = cost_gpu + cost_api + cost_human
    
    if should_fail:
        print(f"!!! INJECTED FAILURE in {mission_id} !!!")
        # Generate failure incident artifact
        incidents_dir = Path(r"C:\RaphaelOS\Incidents")
        incidents_dir.mkdir(parents=True, exist_ok=True)
        incident_folder = incidents_dir / f"2026-07-17_Mission_{mission_id}_failure"
        incident_folder.mkdir(exist_ok=True)
        
        incident_json = {
            "mission_id": mission_id,
            "error": "Video generation failed: CUDA out of memory",
            "category": "Execution Failure",
            "cost_incurred": cost_gpu + cost_api,
            "status": "blocked"
        }
        (incident_folder / "incident.json").write_text(json.dumps(incident_json, indent=2))
        (incident_folder / "recovery_attempts.json").write_text(json.dumps([{"attempt": 1, "status": "failed fallback"}], indent=2))
        
        event_bus.emit("MISSION.FAILURE", "ExecutionEngine", {
            "mission_id": mission_id,
            "problem": "Video generation failed: CUDA out of memory",
            "recovery": "Attempted fallback model, failed. Escalating to human.",
            "priority": "critical"
        })
        return None
        
    return {
        "mission_id": mission_id,
        "strategy": strategy,
        "cost": total_cost,
        "quality": random.uniform(8.0, 9.5) if strategy == "Business Case Studies" else random.uniform(6.5, 8.5)
    }

def run_24_hour_sprint():
    print("\n--- PHASE 8: 24-HOUR SUPERVISED SPRINT ---\n")
    
    # Start notification gateway
    notification_service.start()
    
    twin_storage = Path("focus_marketing_twin.json").absolute()
    if not twin_storage.exists():
        print("Twin not found!")
        return
        
    twin = BusinessTwin("FocusMarketing", twin_storage)
    ops_engine = OperationsEngine(twin)
    
    print("\nStarting Daily Operating Cycle...")
    original_emit = event_bus.emit
    def patched_emit(type_str, source, payload):
        original_emit(type_str, source, payload)
        # Route to notification service
        if type_str in ["MISSION.REVIEW_REQUIRED", "MISSION.COMPLETED", "MISSION.FAILURE", "SYSTEM.DAILY_BRIEF"]:
            notification_service.handle_event(type_str, source, payload)
            
    event_bus.emit = patched_emit
    
    ops_engine.run_daily_cycle()
    
    # Execute a batch of 5 missions based on allocation
    active_strategies = [s for s in twin.knowledge.get("strategies", []) if s.get("state") == "ACTIVE"]
    if not active_strategies:
        active_strategies = [{"strategy": "Business Case Studies", "allocation_score": 1.0}]
        
    # Sort by allocation
    active_strategies.sort(key=lambda x: x.get("allocation_score", 0), reverse=True)
    top_strategy = active_strategies[0]["strategy"]
    
    missions_to_run = 5
    successful_results = []
    
    for i in range(missions_to_run):
        mission_id = f"SPRINT_00{i+1}"
        # Inject failure on mission 3
        should_fail = (i == 2)
        
        result = simulate_mission_execution(mission_id, top_strategy, should_fail)
        if result:
            event_bus.emit("MISSION.REVIEW_REQUIRED", "ExecutionEngine", {
                "mission_id": mission_id,
                "strategy": top_strategy,
                "quality_score": result["quality"] * 10,
                "confidence": active_strategies[0].get("confidence", 0.0),
                "priority": "high"
            })
            # Simulate human approval
            print(f"-> Human Approved {mission_id}")
            successful_results.append(result)
            
            event_bus.emit("MISSION.COMPLETED", "ExecutionEngine", {
                "mission_id": mission_id,
                "strategy": top_strategy,
                "quality_score": result["quality"] * 10,
                "status": "QA COMPLETE",
                "priority": "normal"
            })
            
            # Add cost to operations
            twin.operational_intelligence["production_cost"] = twin.operational_intelligence.get("production_cost", 0.0) + result["cost"]
            twin.operational_intelligence["missions_completed"] += 1

    twin.save()
    print(f"\nSprint completed. {len(successful_results)} missions succeeded. Twin updated.")

if __name__ == "__main__":
    run_24_hour_sprint()
