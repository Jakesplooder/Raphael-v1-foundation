import sys
import asyncio
import json
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

    print("Testing record_skill_acquisition() confidence update path...")
    
    try:
        print("\n--- Call 1: Recording new skill 'Azure' with confidence=0.70 ---")
        ct.record_skill_acquisition("PERSON-AARON-TEST", "Azure", 0.70, "test_script_1")
        await wait_for_events()
        
        # Find the node and relationship to check initial confidence
        nodes_1 = [n for n in repo.get_nodes() if n.name == "Azure"]
        rels_1 = [r for r in repo.get_relationships() if r.relationship_type == "HAS_SKILL" and "Azure" in r.summary]
        
        if nodes_1 and rels_1:
            print(f"[POST-RUN 1] Azure Node Confidence: {nodes_1[0].confidence}")
            print(f"[POST-RUN 1] Azure Relationship Confidence: {rels_1[0].confidence}")
        
        print("\n--- Call 2: Updating skill 'Azure' with confidence=0.85 ---")
        ct.record_skill_acquisition("PERSON-AARON-TEST", "Azure", 0.85, "test_script_2")
        await wait_for_events()
        
        nodes_2 = [n for n in repo.get_nodes() if n.name == "Azure"]
        rels_2 = [r for r in repo.get_relationships() if r.relationship_type == "HAS_SKILL" and "Azure" in r.summary]
        
        if nodes_2 and rels_2:
            print(f"[POST-RUN 2] Azure Node Confidence: {nodes_2[0].confidence}")
            print(f"[POST-RUN 2] Azure Relationship Confidence: {rels_2[0].confidence}")
            
            if nodes_2[0].confidence == 0.85 and rels_2[0].confidence == 0.85:
                print("\nSUCCESS: Confidence correctly updated in-place (no silent drop).")
            else:
                print("\nFAILURE: Confidence was silently dropped or not updated.")
                
    except Exception as e:
        print(f"Error during execution: {e}")
    finally:
        await world_manager.shutdown()
        await global_event_bus.stop()
        await global_event_bus.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
