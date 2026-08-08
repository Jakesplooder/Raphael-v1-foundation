import sys
from pathlib import Path
import subprocess

sys.path.insert(0, r"C:\Users\cyber\Downloads\RalphaelOS")

from raphael_core.kernel.repositories.idempotency_store import IdempotencyStore
from raphael_domains.creator.video_engine import VideoPipelineFSM, BrandContext
from raphael_domains.creator.video_qa import verify_video_qa, VideoQAError

def create_test_videos():
    output_dir = Path("test_videos")
    output_dir.mkdir(exist_ok=True)
    
    pass_vid_path = output_dir / "pass_qa.mp4"
    fail_vid_path = output_dir / "fail_qa.mp4"
    
    # Create pass video (a 2-second valid video using ffmpeg)
    # Generate a simple black 2-second video
    if not pass_vid_path.exists():
        ffmpeg_path = r"C:\Users\cyber\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.2-full_build\bin\ffmpeg.exe"
        cmd = [
            ffmpeg_path, "-y", "-f", "lavfi", "-i", "color=c=black:s=640x480:d=2", 
            "-vcodec", "libx264", str(pass_vid_path)
        ]
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        except Exception as e:
            print(f"Failed to generate test video. Is ffmpeg in PATH? {e}")
            sys.exit(1)
            
    # Create fail video (just a text file masquerading as a video)
    with open(fail_vid_path, "w") as f:
        f.write("This is not a video. It is a corrupt text file.")
        
    return pass_vid_path, fail_vid_path

def test_video_qa(pass_vid_path, fail_vid_path):
    print("=== VIDEO QA GATE OUTPUT ===")
    
    # Pass Case
    print("\n[TEST: PASS CASE]")
    try:
        verify_video_qa(pass_vid_path, expected_min_duration=1.0, expected_max_duration=10.0)
        print("RESULT: QA Passed successfully.")
    except Exception as e:
        print(f"RESULT: Failed unexpectedly: {type(e).__name__}: {e}")
        
    # Fail Case
    print("\n[TEST: FAIL CASE (Corrupt File)]")
    try:
        verify_video_qa(fail_vid_path)
        print("RESULT: QA Passed unexpectedly!")
    except VideoQAError as e:
        print(f"RESULT: Properly rejected by QA Gate: {type(e).__name__}: {e}")

def test_idempotency_2_layer():
    print("\n=== TWO-LAYER IDEMPOTENCY TEST ===")
    import os
    store_path = Path("test_video_idempotency.json").absolute()
    if store_path.exists():
        os.remove(store_path)
        
    store = IdempotencyStore(store_path)
    engine = VideoPipelineFSM(store)
    
    brand = BrandContext(
        brand_id="focus_marketing",
        youtube_credentials_ref="secret/focus_yt",
        voice_profile="professional_male",
        visual_style={"font": "inter"},
        content_categories=["marketing_psychology"]
    )
    request_id = "test_vid_req_001"
    
    # LAYER 2: Test Data-Layer Duplicate Rejection directly
    print("\n[LAYER 2: Testing Underlying Data-Layer Rejection]")
    context = {"mock_youtube_db": []}
    
    print("  -> First publish call (raw): ", end="")
    engine._mock_publish_target(request_id, context)
    print("Success.")
    
    print("  -> Second publish call (raw duplicate): ", end="")
    try:
        engine._mock_publish_target(request_id, context)
        print("Failed to reject duplicate!")
    except ValueError as e:
        print(f"Properly rejected: {e}")
        
    # Use a different file for Layer 1 test to avoid Windows file locks
    store_path_2 = Path("test_video_idempotency_2.json").absolute()
    if store_path_2.exists():
        os.remove(store_path_2)
    store = IdempotencyStore(store_path_2)
    engine = VideoPipelineFSM(store)
    
    context = {
        "mock_youtube_db": [],
        "force_crash_during_publish": True,
        "video_template": "image_to_video"  # Triggers the conditional branch
    }
    
    print("\n[LAYER 1: Triggering FSM Pipeline with Forced Crash]")
    try:
        engine.run_pipeline(request_id, context, brand)
    except SystemExit as e:
        print(f"Process crashed as expected: {e}")
        
    print("\n[LAYER 1: Restarting FSM Pipeline (Recovery)]")
    context["force_crash_during_publish"] = False
    result = engine.run_pipeline(request_id, context, brand)
    print(f"Final State: {result['final_state']}")
    print(f"[VERIFICATION] Videos found on mock publish target: {len(context['mock_youtube_db'])}")

if __name__ == "__main__":
    pass_vid, fail_vid = create_test_videos()
    test_video_qa(pass_vid, fail_vid)
    test_idempotency_2_layer()
