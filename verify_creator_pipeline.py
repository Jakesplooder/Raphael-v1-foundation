import sys
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, r"R:\RalphaelOS_Repo")

from raphael_core.kernel.repositories.idempotency_store import IdempotencyStore
from raphael_domains.creator.pod_engine import PodPipelineFSM
from raphael_domains.creator.visual_qa import verify_visual_qa, QAError

def create_test_images():
    output_dir = Path("test_images")
    output_dir.mkdir(exist_ok=True)
    
    pass_img_path = output_dir / "pass_qa.png"
    fail_img_path = output_dir / "fail_qa.png"
    
    # Create pass image (1000x1000 white background, large black text in the center)
    img_pass = np.ones((1000, 1000, 3), dtype=np.uint8) * 255
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img_pass, "POD DESIGN", (200, 500), font, 3, (0, 0, 0), 10, cv2.LINE_AA)
    cv2.imwrite(str(pass_img_path), img_pass)
    
    # Create fail image (borderline out of bounds at x=30, high contrast, readable)
    img_fail = np.ones((1000, 1000, 3), dtype=np.uint8) * 255
    cv2.putText(img_fail, "BORDERLINE DESIGN", (30, 500), font, 3, (0, 0, 0), 10, cv2.LINE_AA)
    cv2.imwrite(str(fail_img_path), img_fail)
    
    return pass_img_path, fail_img_path

def test_visual_qa(pass_img_path, fail_img_path):
    print("=== VISUAL QA GATE OUTPUT ===")
    
    # Pass Case
    print("\n[TEST: PASS CASE]")
    try:
        verify_visual_qa(pass_img_path, expected_text="POD DESIGN")
        print("RESULT: QA Passed successfully.")
    except Exception as e:
        print(f"RESULT: Failed unexpectedly: {type(e).__name__}: {e}")
        
    # Fail Case
    print("\n[TEST: FAIL CASE (Borderline Out-of-Bounds)]")
    try:
        verify_visual_qa(fail_img_path, expected_text="BORDERLINE DESIGN")
        print("RESULT: QA Passed unexpectedly!")
    except QAError as e:
        print(f"RESULT: Properly rejected by QA Gate: {type(e).__name__}: {e}")

def test_forced_crash():
    print("\n=== FORCED CRASH MID-PUBLISH TEST ===")
    import os
    store_path = Path("test_idempotency.json").absolute()
    if store_path.exists():
        os.remove(store_path)
        
    store = IdempotencyStore(store_path)
    engine = PodPipelineFSM(store)
    
    request_id = "test_req_001"
    context = {
        "force_crash_during_publish": True,
        "mock_db": []
    }
    
    print("\n[RUN 1: Triggering Pipeline with Forced Crash]")
    try:
        engine.run_pipeline(request_id, context)
    except SystemExit as e:
        print(f"Process crashed as expected: {e}")
        
    print("\n[RUN 2: Restarting Pipeline (Recovery)]")
    context["force_crash_during_publish"] = False
    result = engine.run_pipeline(request_id, context)
    print(f"Final State: {result['final_state']}")
    print(f"[VERIFICATION] Listings found on mock publish target: {len(context['mock_db'])}")

if __name__ == "__main__":
    pass_img, fail_img = create_test_images()
    test_visual_qa(pass_img, fail_img)
    test_forced_crash()
