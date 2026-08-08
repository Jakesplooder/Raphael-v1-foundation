import sys
import json
import asyncio
from pathlib import Path

sys.path.insert(0, '.')
from raphael_core import legacy
from raphael_core.kernel.event_bus import global_event_bus, Event
from raphael_core.kernel.interfaces import EventType
from raphael_core.kernel.managers.world_manager import WorldManager
from raphael_core.kernel.repositories.world_repository import WorldRepository

# Monkeypatch emit to actually publish to the event bus
import raphael_domains.career.market_intelligence as mi
import raphael_domains.career.career_twin as ct

def sync_emit(type_str: str, source: str, payload: dict):
    # Construct event and put it on the queue synchronously for the loop to pick up
    event = Event(source=source, type=EventType(type_str), payload=payload)
    global_event_bus._volatile_queue.put_nowait(event)

mi.emit = sync_emit
ct.emit = sync_emit

from raphael_domains.career.career_api import CareerAPI

async def main():
    config = legacy.load_config(Path('Ralphael/config/settings.json'))
    
    # 1. Initialize Kernel Services
    await global_event_bus.initialize()
    await global_event_bus.start()
    
    world_manager = WorldManager(global_event_bus, config)
    await world_manager.initialize()
    await world_manager.start()
    
    api = CareerAPI(config)
    repo = world_manager.repository
    
    # Small helper to let async queue process
    async def wait_for_events():
        await asyncio.sleep(0.5)

    print("Generating Executive Brief for PERSON-AARON-TEST...")
    
    try:
        # Pre-count
        initial_nodes = len(repo.get_nodes())
        initial_rels = len(repo.get_relationships())
        print(f"[PRE-RUN] World Model state: {initial_nodes} nodes, {initial_rels} relationships")
        
        # Call 1
        payload = api.executive_brief(
            request_id="REQ-TEST-IDEMP",
            person_id="PERSON-AARON-TEST"
        )
        
        # Wait for events to propagate
        await wait_for_events()
        
        post_run_1_nodes = len(repo.get_nodes())
        post_run_1_rels = len(repo.get_relationships())
        
        print("\n=== Career Executive Brief ===")
        print(json.dumps(payload, indent=2))
        
        print(f"\n[POST-RUN 1] World Model state: {post_run_1_nodes} nodes, {post_run_1_rels} relationships")
        print(f"Diff: +{post_run_1_nodes - initial_nodes} nodes, +{post_run_1_rels - initial_rels} relationships")
        
        # Call 2 (Idempotency)
        print("\n--- Idempotency Test (Calling again with same request_id) ---")
        payload2 = api.executive_brief(
            request_id="REQ-TEST-IDEMP",
            person_id="PERSON-AARON-TEST"
        )
        
        await wait_for_events()
        
        post_run_2_nodes = len(repo.get_nodes())
        post_run_2_rels = len(repo.get_relationships())
        
        print(f"Idempotency cache hit returned: {len(payload2['top_opportunities'])} opportunities")
        print(f"[POST-RUN 2] World Model state: {post_run_2_nodes} nodes, {post_run_2_rels} relationships")
        print(f"Diff: +{post_run_2_nodes - post_run_1_nodes} nodes, +{post_run_2_rels - post_run_1_rels} relationships")
        
    except Exception as e:
        print(f"Error during execution: {e}")
    finally:
        await world_manager.shutdown()
        await global_event_bus.stop()
        await global_event_bus.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
