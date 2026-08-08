import sys
import asyncio
from pathlib import Path

sys.path.insert(0, '.')
from raphael_core import legacy
from raphael_core.kernel.event_bus import global_event_bus, Event
from raphael_core.kernel.interfaces import EventType
from raphael_core.kernel.managers.world_manager import WorldManager

import raphael_domains.career.career_twin as ct

def sync_emit(type_str: str, source: str, payload: dict):
    event = Event(source=source, type=EventType(type_str), payload=payload)
    global_event_bus._volatile_queue.put_nowait(event)

ct.emit = sync_emit

async def main():
    config = legacy.load_config(Path('Ralphael/config/settings.json'))
    
    await global_event_bus.initialize()
    await global_event_bus.start()
    
    world_manager = WorldManager(global_event_bus, config)
    await world_manager.initialize()
    await world_manager.start()
    
    repo = world_manager.repository
    
    async def wait_for_events():
        await asyncio.sleep(0.5)

    print("Testing record_skill_acquisition() write-path idempotency...")
    
    try:
        initial_nodes = len(repo.get_nodes())
        initial_rels = len(repo.get_relationships())
        print(f"[PRE-RUN] World Model state: {initial_nodes} nodes, {initial_rels} relationships")
        
        print("\n--- Call 1: Recording new skill 'AWS' ---")
        ct.record_skill_acquisition("PERSON-AARON-TEST", "AWS", 0.9, "test_script")
        await wait_for_events()
        
        post_run_1_nodes = len(repo.get_nodes())
        post_run_1_rels = len(repo.get_relationships())
        print(f"[POST-RUN 1] World Model state: {post_run_1_nodes} nodes, {post_run_1_rels} relationships")
        print(f"Diff: +{post_run_1_nodes - initial_nodes} nodes, +{post_run_1_rels - initial_rels} relationships")
        
        print("\n--- Call 2: Duplicate recording 'AWS' ---")
        ct.record_skill_acquisition("PERSON-AARON-TEST", "AWS", 0.9, "test_script")
        await wait_for_events()
        
        post_run_2_nodes = len(repo.get_nodes())
        post_run_2_rels = len(repo.get_relationships())
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
