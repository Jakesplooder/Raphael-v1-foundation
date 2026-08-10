import sys
import os
import time
from pathlib import Path

sys.path.insert(0, r"R:\RalphaelOS_Repo")

from raphael_core.kernel.repositories.idempotency_store import IdempotencyStore
from raphael_domains.creator.video_engine import VideoPipelineFSM, BrandContext

def run_batch():
    print("\n--- RUNNING BATCH 1: CALIBRATION (10 Missions) ---\n")
    
    brand = BrandContext("FocusMarketing", "ref_1", "voice_1", {}, [])
    
    # We use a fresh idempotency store for each run or one global one to simulate a long running system
    store_path = Path("batch1_idempotency.db").absolute()
    store = IdempotencyStore(str(store_path))
    engine = VideoPipelineFSM(store)
    
    topics = [
        "Why Costco Makes Billions",
        "The Secret of IKEA's Maze",
        "How Supreme Created Scarcity",
        "Apple's Supply Chain Masterclass",
        "The Psychology of Starbucks Prices",
        "Amazon's Loss Leader Strategy",
        "Ferrari's Brand Exclusivity",
        "How Trader Joe's Hacks Choice",
        "The Subscription Model Trap",
        "Rolex's Artificial Demand"
    ]
    
    for i, topic in enumerate(topics, 1):
        request_id = f"Batch1_Mission_{i:03d}"
        print(f"\n[Mission {i}/10] Kicking off '{topic}' (Request ID: {request_id})")
        
        context = {"objective": f"Create AI marketing tutorial: {topic}"}
        result = engine.run_pipeline(request_id, context, brand)
        
        print(f"Mission {i} Final State: {result['final_state']}")
        time.sleep(1) # Small delay to ensure timestamp separation if needed
        
    print("\n--- BATCH 1 COMPLETE ---")
    print(f"Check C:\\RaphaelOS\\Missions\\Review\\Ready for the {len(topics)} generated mission folders.")

if __name__ == "__main__":
    run_batch()
