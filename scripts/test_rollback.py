import os
import sys
import json
import time
import requests
import subprocess
from pathlib import Path
from deepdiff import DeepDiff

sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

GATEWAY_URL = "http://localhost:8001/api/overview"
REGISTRY_PATH = Path(__file__).parent.parent / "api_gateway" / "feature_registry.json"

def set_feature_backend(feature: str, backend: str):
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)
    registry[feature] = backend
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=4)
    print(f"[Toggle] Set {feature} -> {backend}")

def run_rrk():
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).parent.parent.resolve())
    cmd = [sys.executable, "-c", "import asyncio; from raphael_core.cli import main; main(['start'])"]
    return subprocess.Popen(cmd, env=env, stdout=open("rrk_log.txt", "w"), stderr=subprocess.STDOUT)

def run_gateway():
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).parent.parent.resolve())
    cmd = [sys.executable, "-m", "uvicorn", "api_gateway.gateway:app", "--host", "0.0.0.0", "--port", "8001"]
    return subprocess.Popen(cmd, env=env, stdout=open("gateway_log.txt", "w"), stderr=subprocess.STDOUT)

def get_overview_metrics():
    start = time.time()
    resp = requests.get(GATEWAY_URL)
    duration = time.time() - start
    return resp.status_code, resp.json(), duration

def wait_for_gateway():
    for _ in range(30):
        try:
            requests.get(GATEWAY_URL)
            return True
        except:
            time.sleep(1)
    return False

def main():
    print("Setting initial state (Goals -> legacy)...")
    set_feature_backend("goals", "legacy")
    
    print("Starting processes...")
    gw_proc = run_gateway()
    rrk_proc = run_rrk()
    
    print("Waiting for gateway to be ready...")
    if not wait_for_gateway():
        print("Gateway failed to start.")
        gw_proc.terminate()
        rrk_proc.terminate()
        sys.exit(1)
    
    print("\n--- Legacy Mode ---")
    status_leg, payload_leg, time_leg = get_overview_metrics()
    print(f"Status: {status_leg}")
    print(f"Response Time: {time_leg*1000:.2f}ms")
    
    print("\n--- RRK Mode ---")
    set_feature_backend("goals", "rrk")
    time.sleep(1) # Let gateway read updated file
    status_rrk, payload_rrk, time_rrk = get_overview_metrics()
    print(f"Status: {status_rrk}")
    print(f"Response Time: {time_rrk*1000:.2f}ms")
    
    print("\n--- Rollback Mode (Legacy) ---")
    set_feature_backend("goals", "legacy")
    time.sleep(1)
    status_rb, payload_rb, time_rb = get_overview_metrics()
    print(f"Status: {status_rb}")
    print(f"Response Time: {time_rb*1000:.2f}ms")
    
    print("\n--- Validation ---")
    assert status_leg == status_rrk == status_rb == 200, "Status codes must be 200"
    diff_rrk = DeepDiff(payload_leg, payload_rrk, ignore_order=True)
    diff_rb = DeepDiff(payload_leg, payload_rb, ignore_order=True)
    
    if diff_rrk:
        print(f"❌ RRK payload differs from Legacy: {diff_rrk}")
    else:
        print("✅ RRK Payload matches Legacy exactly")
        
    if diff_rb:
        print(f"❌ Rollback payload differs from Legacy: {diff_rb}")
    else:
        print("✅ Rollback Payload matches Legacy exactly")

    print("\nCleaning up...")
    gw_proc.terminate()
    rrk_proc.terminate()
    
    if not diff_rrk and not diff_rb:
        print("✅ Rollback Test Passed")
        sys.exit(0)
    else:
        print("❌ Rollback Test Failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
