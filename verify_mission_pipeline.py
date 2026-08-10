import sys
import os
import glob
from pathlib import Path

sys.path.insert(0, r"R:\RalphaelOS_Repo")

from raphael_core.kernel.repositories.idempotency_store import IdempotencyStore
from raphael_domains.creator.video_engine import VideoPipelineFSM, BrandContext

def run_tests():
    print("\n--- RUNNING PHASE 3 TESTS (Mission Artifact Pipeline) ---\n")
    
    store_path = Path("test_mission_idempotency.json").absolute()
    if store_path.exists(): os.remove(store_path)
    
    import shutil
    ready_dir = Path(r"R:\RaphaelOS\Missions\Review\Ready")
    if ready_dir.exists():
        for d in ready_dir.glob("*_FocusMarketing_001"):
            shutil.rmtree(d)
            
    active_dir = Path(r"R:\RaphaelOS\Missions\Active")
    if active_dir.exists():
        for d in active_dir.glob("*_FocusMarketing_001"):
            shutil.rmtree(d)
    
    store = IdempotencyStore(store_path)
    engine = VideoPipelineFSM(store)
    
    brand = BrandContext("FocusMarketing", "ref_1", "voice_1", {}, [])
    
    request_id = "001"
    
    print("Executing Video Engine Pipeline (should produce a full Mission Folder)")
    result = engine.run_pipeline(request_id, {"objective": "Create AI marketing tutorial"}, brand)
    print(f"Final State: {result['final_state']}")
    
    # Now verify the outputs
    ready_dir = Path(r"R:\RaphaelOS\Missions\Review\Ready")
    folders = list(ready_dir.glob("*_FocusMarketing_001"))
    
    assert len(folders) > 0, "No mission folder found in Review/Ready!"
    mission_dir = folders[-1]
    print(f"\nMission Folder Generated: {mission_dir}")
    
    expected_files = [
        "mission.json",
        "objective.md",
        "reasoning_trace.json",
        "mission_report.txt",
        "review.json",
        "artifact_manifest.json",
        "content/video.mp4",
        "content/thumbnail.png",
        "qa/qa_report.json",
        "publishing/publish_payload.json"
    ]
    
    for rel in expected_files:
        f_path = mission_dir / rel
        assert f_path.exists(), f"Missing expected artifact: {rel}"
        print(f"  [x] Found: {rel}")
        
    print("\nReading Mission Report:")
    print("---------------------------------")
    print((mission_dir / "mission_report.txt").read_text())
    print("---------------------------------")
    
    print("\nReading Reasoning Trace:")
    print("---------------------------------")
    print((mission_dir / "reasoning_trace.json").read_text())
    print("---------------------------------")
    
    print("\nALL PHASE 3 TESTS PASSED.")

if __name__ == "__main__":
    run_tests()
