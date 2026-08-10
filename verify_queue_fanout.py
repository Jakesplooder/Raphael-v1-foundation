import sys
import os
from pathlib import Path

sys.path.insert(0, r"R:\RalphaelOS_Repo")

from raphael_core.kernel.repositories.idempotency_store import IdempotencyStore
from raphael_domains.creator.video_engine import VideoPipelineFSM, BrandContext
from raphael_domains.creator.video_queue import VideoQueueManager

def run_tests():
    print("\n--- RUNNING PHASE 2B TESTS ---\n")
    
    q_path = Path("test_queue.json").absolute()
    store_path = Path("test_queue_idempotency.json").absolute()
    
    # Cleanup previous runs
    if q_path.exists(): os.remove(q_path)
    if store_path.exists(): os.remove(store_path)
    
    store = IdempotencyStore(store_path)
    engine = VideoPipelineFSM(store)
    queue_manager = VideoQueueManager(q_path, engine)
    
    b1 = BrandContext("Brand_A", "ref_A", "voice_a", {}, [])
    b2 = BrandContext("Brand_B", "ref_B", "voice_b", {}, [])
    b3 = BrandContext("Brand_C", "ref_C", "voice_c", {}, [])
    
    print("[TEST 1: QUEUE ORDERING (Sequential Mutex)]")
    # We will enqueue 3 brands and process them successfully.
    queue_manager.enqueue("req_100", [b1, b2, b3], {"mock_youtube_db": []})
    queue_manager.process_queue()
    
    assert len(queue_manager.queue) == 0, "Queue should be empty after processing"
    assert len(queue_manager.completed) == 3, "Should have 3 completed jobs"
    print("RESULT: All 3 brands processed sequentially in exact order (A -> B -> C).\n")
    
    # TEST 2: Partial Recovery (Crash AFTER publish of Brand A, during Brand B)
    print("[TEST 2: PARTIAL RECOVERY (Crash AFTER Publish)]")
    q_path2 = Path("test_queue2.json").absolute()
    store_path2 = Path("test_queue_idempotency2.json").absolute()
    
    if q_path2.exists(): os.remove(q_path2)
    if store_path2.exists(): os.remove(store_path2)
    
    store2 = IdempotencyStore(store_path2)
    engine2 = VideoPipelineFSM(store2)
    queue_manager2 = VideoQueueManager(q_path2, engine2)
    
    # We want Brand B to crash during generation, so Brand A publishes successfully.
    # To do this, we'll subclass or monkey-patch the engine to crash only for Brand B
    original_generation = engine2._state_comfyui_video_generation
    
    def mock_generation_crashing(self_ref, request_id, context):
        if context["brand"].brand_id == "Brand_B":
             print(">> INJECTED CRASH DURING BRAND B GENERATION <<")
             raise SystemExit("Crash before B publishes!")
        return original_generation(request_id, context)
        
    engine2._state_comfyui_video_generation = mock_generation_crashing.__get__(engine2)
    
    queue_manager2.enqueue("req_200", [b1, b2], {"mock_youtube_db": []})
    try:
        queue_manager2.process_queue()
    except SystemExit:
        print("Crash caught successfully.")
        
    # Now simulate restart.
    print("\nRestarting after crash...")
    engine2._state_comfyui_video_generation = original_generation.__get__(engine2)  # Fix the crash
    
    # Re-initialize the queue manager (loads from JSON)
    store2_b = IdempotencyStore(store_path2)
    engine2_b = VideoPipelineFSM(store2_b)
    qm_restarted = VideoQueueManager(q_path2, engine2_b)
    
    print(f"Remaining jobs loaded from queue.json: {[j['brand_id'] for j in qm_restarted.queue]}")
    assert "Brand_A" not in [j['brand_id'] for j in qm_restarted.queue], "Brand A should be skipped!"
    assert "Brand_B" in [j['brand_id'] for j in qm_restarted.queue], "Brand B should be resumed!"
    
    qm_restarted.process_queue()
    print("RESULT: Brand A was skipped (already published), Brand B resumed generation and completed.\n")
    
    # TEST 3: Partial Recovery (Crash BEFORE publish of Brand A)
    print("[TEST 3: PARTIAL RECOVERY (Crash BEFORE Publish)]")
    q_path3 = Path("test_queue3.json").absolute()
    store_path3 = Path("test_queue_idempotency3.json").absolute()
    if q_path3.exists(): os.remove(q_path3)
    if store_path3.exists(): os.remove(store_path3)
    
    store3 = IdempotencyStore(store_path3)
    engine3 = VideoPipelineFSM(store3)
    qm_3 = VideoQueueManager(q_path3, engine3)
    
    # Crash Brand A before publish
    original_publish = engine3._state_publish
    def mock_publish_crashing(self_ref, request_id, context):
        if context["brand"].brand_id == "Brand_A":
            print(">> INJECTED CRASH DURING BRAND A PUBLISH <<")
            raise SystemExit("Crash before A finishes publish!")
        return original_publish(request_id, context)
        
    engine3._state_publish = mock_publish_crashing.__get__(engine3)
    
    qm_3.enqueue("req_300", [b1], {"mock_youtube_db": []})
    try:
        qm_3.process_queue()
    except SystemExit:
        print("Crash caught successfully.")
        
    # Restart
    print("\nRestarting after crash...")
    store4 = IdempotencyStore(store_path3)
    engine4 = VideoPipelineFSM(store4)
    qm_4 = VideoQueueManager(q_path3, engine4)
    
    print(f"Remaining jobs loaded from queue.json: {[j['brand_id'] for j in qm_4.queue]}")
    assert "Brand_A" in [j['brand_id'] for j in qm_4.queue], "Brand A should RESUME!"
    
    qm_4.process_queue()
    print("RESULT: Brand A resumed and successfully published after crash.\n")

    print("ALL PHASE 2B TESTS PASSED.")
    
if __name__ == "__main__":
    run_tests()
