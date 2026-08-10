import sys
from pathlib import Path
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')

sys.path.insert(0, r"R:\RalphaelOS_Repo")

from raphael_core.kernel.repositories.idempotency_store import IdempotencyStore
from raphael_domains.creator.video_engine import VideoPipelineFSM, BrandContext

def run_test():
    store_path = Path("test_generation_idempotency.json").absolute()
    if store_path.exists():
        store_path.unlink()
        
    store = IdempotencyStore(store_path)
    engine = VideoPipelineFSM(store)
    
    brand = BrandContext(
        brand_id="test_brand",
        youtube_credentials_ref="mock",
        voice_profile="test",
        visual_style={},
        content_categories=[]
    )
    
    import uuid
    # Use a unique request ID for this test to ensure we don't hit old caches
    request_id = f"test_idemp_{uuid.uuid4().hex[:8]}"
    
    print(f"\n=== PASS 1: Real Generation ===")
    print(f"Request ID: {request_id}")
    
    # We force a crash right AFTER generation (during export) to ensure it doesn't finish publish.
    # Actually, we can just run it to completion and then run it again! 
    # Because if we run it again, it should skip everything (including generation) and just hit "PUBLISHED".
    
    context = {
        "video_concept": {
            "subject_description": "A bottle with a beautiful rainbow galaxy inside it on top of a wooden table",
            "scene_direction": "The bottle glows softly on the wooden table, tiny stars twinkling inside the galaxy. A subtle camera push-in highlights the cosmic swirl inside."
        },
        "mock_youtube_db": []
    }
    
    result1 = engine.run_pipeline(request_id, context, brand=brand)
    print(f"Pass 1 Final State: {result1['final_state']}")
    
    print(f"\n=== PASS 2: Idempotent Skip ===")
    print(f"Running exact same request_id {request_id} again...")
    
    context2 = {
        "video_concept": {
            "subject_description": "A bottle with a beautiful rainbow galaxy inside it on top of a wooden table",
            "scene_direction": "The bottle glows softly on the wooden table, tiny stars twinkling inside the galaxy. A subtle camera push-in highlights the cosmic swirl inside."
        },
        "mock_youtube_db": context["mock_youtube_db"]
    }
    
    result2 = engine.run_pipeline(request_id, context2, brand=brand)
    print(f"Pass 2 Final State: {result2['final_state']}")

if __name__ == "__main__":
    run_test()
