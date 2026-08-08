import sys
import logging
from pathlib import Path
from pprint import pprint

sys.path.insert(0, r"C:\Users\cyber\Downloads\RalphaelOS")

from raphael_core.kernel.repositories.idempotency_store import IdempotencyStore
from raphael_domains.creator.video_engine import VideoPipelineFSM, BrandContext

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

# Clean up any existing state
test_db_path = Path("C:/RaphaelOS/stage1_idempotency.db")
if test_db_path.exists():
    test_db_path.unlink()

test_video = Path("C:/RaphaelOS/Ventures/FocusMarketing/video_stage1_test_001.mp4")
if test_video.exists():
    test_video.unlink()

store = IdempotencyStore("C:/RaphaelOS/stage1_idempotency.db")
fsm = VideoPipelineFSM(idempotency_store=store)

brand = BrandContext(
    brand_id="FocusMarketing",
    youtube_credentials_ref="secret_123",
    voice_profile="professional_male",
    visual_style={"primary_color": "blue"},
    content_categories=["marketing"],
    publish_default="unlisted"
)

# A mock external database for the Layer 2 uniqueness check
external_db = []

def run_pass(pass_name: str):
    print(f"\n{'='*50}")
    print(f"RUNNING {pass_name}")
    print(f"{'='*50}")
    
    context = {
        "objective": "Test real ffmpeg FSM",
        "mock_youtube_db": external_db
    }
    
    result = fsm.run_pipeline("stage1_test_001", context, brand)
    print(f"\nFinal State: {result['final_state']}")
    print(f"External DB Count: {len(external_db)}")
    
    if test_video.exists():
        print(f"File exists: {test_video}")
        print(f"File size: {test_video.stat().st_size} bytes")
    
    return result

# PASS 1: First full generation
run_pass("PASS 1: INITIAL GENERATION")

# PASS 2: Idempotency (Should skip QA and hit API cache)
run_pass("PASS 2: LOCAL IDEMPOTENCY CHECK")

# MOCK SPLIT-BRAIN: Clear local cache, force it to hit the external DB
print("\n[Simulating Local Cache Loss...]")
if hasattr(store, 'db'):
    store.db.close()
if Path("C:/RaphaelOS/stage1_idempotency.db").exists():
    Path("C:/RaphaelOS/stage1_idempotency.db").unlink()
store = IdempotencyStore("C:/RaphaelOS/stage1_idempotency.db")
fsm.idempotency_store = store
store.save()

# PASS 3: External Idempotency (Should detect video already published in external_db)
run_pass("PASS 3: EXTERNAL SEARCH-BEFORE-CREATE")
