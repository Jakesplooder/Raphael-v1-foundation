import sys
import os
from pathlib import Path
import json
import time
import asyncio
from deepdiff import DeepDiff

# Add api_gateway to sys.path
sys.path.insert(0, r"C:\Users\cyber\Downloads\RalphaelOS")
sys.path.insert(0, r"C:\Users\cyber\Downloads\RalphaelOS\api_gateway")

from api_gateway.gateway import get_overview as api_overview
from api_gateway.gateway import client as gateway_client

REGISTRY_PATH = Path(r"C:\Users\cyber\Downloads\RalphaelOS\api_gateway\feature_registry.json")

def set_feature_backend(feature: str, backend: str):
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)
    registry[feature] = backend
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=4)
    print(f"[Toggle] Set {feature} -> {backend}")

def clean_paths(items):
    return [{k: v for k, v in item.items() if k != "path"} for item in items]

async def main():
    print("Testing Tasks Rollback & Feature Toggle")
    
    # Must start the gateway httpx client manually because we're running outside fastapi lifecycle
    await gateway_client.__aenter__()
    
    try:
        # 1. Legacy
        print("\n--- Testing tasks=legacy ---")
        set_feature_backend("tasks", "legacy")
        start = time.time()
        legacy_data = await api_overview()
        legacy_dur = time.time() - start
        print(f"Legacy payload retrieved in {legacy_dur*1000:.2f}ms")
        
        if "tasks" not in legacy_data:
            print("FAIL: 'tasks' missing from legacy payload")
            sys.exit(1)
            
        legacy_tasks = clean_paths(legacy_data["tasks"])
        legacy_council = clean_paths(legacy_data.get("council_tasks", []))
        print(f"Legacy tasks count: {len(legacy_tasks)}")
        print(f"Legacy council_tasks count: {len(legacy_council)}")
        
        # 2. RRK
        print("\n--- Testing tasks=rrk ---")
        set_feature_backend("tasks", "rrk")
        start = time.time()
        rrk_data = await api_overview()
        rrk_dur = time.time() - start
        print(f"RRK payload retrieved in {rrk_dur*1000:.2f}ms")
        
        if "tasks" not in rrk_data:
            print("FAIL: 'tasks' missing from RRK payload")
            sys.exit(1)
            
        rrk_tasks = clean_paths(rrk_data["tasks"])
        rrk_council = clean_paths(rrk_data.get("council_tasks", []))
        print(f"RRK tasks count: {len(rrk_tasks)}")
        print(f"RRK council_tasks count: {len(rrk_council)}")
        
        # Verify Parity
        print("\n--- Verifying Payload Parity ---")
        diff_tasks = DeepDiff(legacy_tasks, rrk_tasks, ignore_order=True)
        diff_council = DeepDiff(legacy_council, rrk_council, ignore_order=True)
        
        if diff_tasks:
            print("FAIL: Tasks drift detected!")
            print(diff_tasks)
            sys.exit(1)
            
        if diff_council:
            print("FAIL: Council Tasks drift detected!")
            print(diff_council)
            sys.exit(1)
            
        print("Tasks Parity: PASS")
        print("Feature Toggle Verified: PASS")
        print("Rollback Tested: PASS")
        
    finally:
        set_feature_backend("tasks", "rrk")
        await gateway_client.__aexit__()

if __name__ == "__main__":
    asyncio.run(main())
