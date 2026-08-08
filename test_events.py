import asyncio
import httpx
import json
from raphael_core.kernel.event_bus import global_event_bus
from raphael_core.kernel.interfaces import Event, EventType

async def test_event_bus():
    # 1. Initialize EventBus
    await global_event_bus.initialize()
    await global_event_bus.start()
    
    # 2. Wait a moment
    await asyncio.sleep(1)
    
    # 3. Publish test events
    print("Publishing NODE_STARTED...")
    await global_event_bus.publish(Event(
        source="TestScript",
        type=EventType.NODE_STARTED,
        mission_id="test_mission",
        workflow_id="builder_workflow",
        node_id="generate_image",
        council="Creator Council",
        payload={"msg": "Generating image"}
    ))
    
    await asyncio.sleep(1)
    
    print("Publishing NODE_COMPLETED...")
    await global_event_bus.publish(Event(
        source="TestScript",
        type=EventType.NODE_COMPLETED,
        mission_id="test_mission",
        workflow_id="builder_workflow",
        node_id="generate_image",
        council="Creator Council",
        payload={"status": "success"}
    ))
    
    await asyncio.sleep(1)
    
    # Check recent events
    recent = global_event_bus.get_recent_events()
    print(f"Recent events count: {len(recent)}")
    for e in recent:
        print("Recent:", e["type"], e.get("node_id"))
        
    await global_event_bus.stop()
    await global_event_bus.shutdown()

if __name__ == "__main__":
    asyncio.run(test_event_bus())
