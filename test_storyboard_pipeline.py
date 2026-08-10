import sys
import logging
import uuid
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
sys.path.insert(0, r"R:\RalphaelOS_Repo")

from raphael_core.kernel.repositories.idempotency_store import IdempotencyStore
from raphael_domains.creator.video_engine import VideoPipelineFSM, BrandContext
from verify_youtube_upload import create_dummy_video

def main():
    store = IdempotencyStore(Path(r"R:\RaphaelOS\System\idempotency"))
    engine = VideoPipelineFSM(store)
    
    brand = BrandContext(
        brand_id="test_brand",
        youtube_credentials_ref="mock",
        voice_profile="persona_1.wav",
        visual_style={},
        content_categories=[]
    )
    
    # We use a unique request ID to bypass old caches
    req_id = f"apple_decoy_{uuid.uuid4().hex[:8]}"
    
    logging.info(f"=== Initiating Phase 2 Storyboard Pipeline for {req_id} ===")
    
    # Wait for XTTS server to be up
    import urllib.request, json
    logging.info("Checking if XTTS server is up on port 8020...")
    while True:
        try:
            urllib.request.urlopen("http://localhost:8020/speakers", timeout=5)
            logging.info("XTTS server is responsive!")
            break
        except Exception:
            logging.info("Waiting for XTTS server to start...")
            time.sleep(5)
            
    # To save time during active development, we'll let it run end-to-end,
    # but we can force it to stop before YouTube publish by catching an exception or let it publish privately.
    # Since we want to verify the output video, letting it run to completion is ideal.
    
    context = {
        "brand": brand,
        "video_template": "text_to_video",
        "objective": "Why Apple Never Competes on Price"
    }
    
    result = engine.run_pipeline(req_id, context, brand=brand)
    logging.info(f"Pipeline finished with state: {result['final_state']}")
    if "video_path" in result["context"]:
        logging.info(f"Final STITCHED video available at: {result['context']['video_path']}")

if __name__ == "__main__":
    main()
