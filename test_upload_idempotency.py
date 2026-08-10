import sys
import logging
import uuid
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
sys.path.insert(0, r"R:\RalphaelOS_Repo")

from raphael_core.kernel.repositories.idempotency_store import IdempotencyStore
from raphael_domains.creator.video_engine import VideoPipelineFSM, BrandContext
from raphael_core.kernel.services.mission_artifact_pipeline import MissionArtifactPipeline
from verify_youtube_upload import create_dummy_video

def main():
    store = IdempotencyStore(Path(r"R:\RaphaelOS\System\idempotency"))
    engine = VideoPipelineFSM(store)
    
    brand = BrandContext(
        brand_id="test_brand",
        youtube_credentials_ref="mock",
        voice_profile="test",
        visual_style={},
        content_categories=[]
    )
    req_id = f"crash_test_{uuid.uuid4().hex[:8]}"
    
    video_path = create_dummy_video()
    
    # Pre-warm the cache so we skip the 4-minute generation and QA
    store.set(f"{req_id}:shot_0", {"video_path": str(Path(video_path).absolute())})
    store.set(f"{req_id}_QA", {"passed": True})
    
    logging.info(f"=== PASS 1: Initiating Crash-Mid-Upload Test for {req_id} ===")
    
    context = {
        "brand": brand,
        "video_template": "text_to_video",
        "force_crash_during_publish_after_api": True
    }
    
    # Pass 1: Should physically upload the video to YouTube, then crash before local cache save.
    try:
        engine.run_pipeline(req_id, context, brand=brand)
    except SystemExit as e:
        logging.info(f"Pass 1 successfully crashed as expected: {e}")
        
    logging.info("Waiting 20 seconds for YouTube Search Index to propagate...")
    time.sleep(20)
    
    logging.info(f"\n=== PASS 2: Idempotent Recovery Test for {req_id} ===")
    
    context2 = {
        "brand": brand,
        "video_template": "text_to_video"
    }
    
    # Pass 2: Should search YouTube, find the video uploaded in Pass 1, and skip the upload.
    result = engine.run_pipeline(req_id, context2, brand=brand)
    
    logging.info(f"Pass 2 Final State: {result['final_state']}")
    
if __name__ == "__main__":
    main()
