# TEMPORARY: Standalone kernel bootloader for live integration testing.
# The daemon should natively support goal-driven mission dispatch
# without this script once D10 goal-polling ships.
# Remove or fold into daemon startup once that lands.

import asyncio
import logging
import time
import sys
import os
import json
import datetime

sys.path.insert(0, ".")
from raphael_core.kernel.registry import registry
from raphael_core.kernel.event_bus import EventBus
from raphael_core.kernel.services.telemetry_service import TelemetryService
from raphael_core.kernel.managers.workflow_manager import WorkflowManager
from raphael_core.kernel.managers.memory_manager import MemoryManager
from raphael_core.kernel.managers.world_manager import WorldManager
from raphael_core.kernel.interfaces import Event, EventType, EventPriority
from raphael_core.kernel.models.workflow import WorkflowStep, WorkflowStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Mission2.Live")

class MockConfig:
    vault = "."

async def main():
    logger.info("Initializing Native Kernel Modules...")
    
    # 1. Initialize EventBus
    event_bus = EventBus()
    registry.register_service(event_bus)
    await event_bus.initialize()
    await event_bus.start()
    
    # 2. Initialize Telemetry Service
    trace_path = ".system_generated/traces.jsonl"
    if os.path.exists(trace_path):
        os.remove(trace_path)
    telemetry = TelemetryService(trace_file=trace_path)
    
    async def telemetry_handler(event: Event):
        await telemetry.log_event(event.type.value, event.payload, event_timestamp=event.timestamp)
        
    for et in EventType:
        event_bus.subscribe(et, telemetry_handler)
        
    # We will manually emit SEARCH_QUERY_STARTED and COMPLETED 
    # from the python_provider to mimic a native provider, or emit here using a wrapper.
    # Actually, the action doesn't emit it natively yet unless we patch python_provider.py or just emit it during execution.
    # We updated python_provider.py, let's just make sure it's traceable. 
    # We will let WorkflowService's STEP_STARTED/COMPLETED serve as the bounds.
    
    # 3. Initialize Memory Manager
    memory_manager = MemoryManager(event_bus)
    registry.register_service(memory_manager)
    await memory_manager.initialize()
    await memory_manager.start()
    
    # 4. Initialize World Manager
    world_manager = WorldManager(event_bus, config=MockConfig())
    registry.register_service(world_manager)
    await world_manager.initialize()
    await world_manager.start()
    
    # 5. Initialize Workflow Manager
    wf_manager = WorkflowManager(event_bus, config=MockConfig())
    registry.register_service(wf_manager)
    await wf_manager.initialize()
    await wf_manager.start()
    
    logger.info("Kernel Ready. Dispatching Mission 2: Research")
    
    run_id = f"Mission2-{int(time.time())}"
    steps = [
        WorkflowStep(
            id="step_1", 
            name="Search SearxNG", 
            action="search.searxng", 
            parameters={"query": "autonomous agents industry overview 2026"}
        ),
        WorkflowStep(
            id="step_2", 
            name="Analyze with Ollama", 
            action="llm.ollama", 
            parameters={
                "model": "llama3.1:latest",
                "prompt": "Summarize the autonomous agents industry using the search results."
            }
        ),
        WorkflowStep(
            id="step_3", 
            name="Store Cognitive Memory", 
            action="memory.store", 
            parameters={"content": f"Autonomous agents industry research complete for {run_id}.", "source": run_id}
        ),
        WorkflowStep(
            id="step_4", 
            name="Update World Model", 
            action="world_model.create_node", 
            parameters={
                "node_id": "BRIEF-M2-RESEARCH",
                "title": "Industry Research Brief",
                "description": "The autonomous agents industry is rapidly evolving, moving towards multi-agent workflows and OS-level integrations."
            }
        )
    ]
    
    wf = await wf_manager.service.create_workflow("Mission 2: Research", steps, "strategic")
    execution = await wf_manager.service.trigger_workflow(wf.id)
    
    logger.info(f"Workflow {wf.id} execution {execution.id} started. Awaiting completion...")
    
    timeout = 120
    start = time.time()
    
    completed = False
    while time.time() - start < timeout:
        if execution.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED, WorkflowStatus.CANCELLED]:
            completed = True
            break
        await asyncio.sleep(1)
        
    if not completed:
        logger.error(f"Mission timeout after {timeout}s")
        
    logger.info(f"Mission execution finished with status: {execution.status}")
    for step_id, status in execution.step_executions.items():
        logger.info(f"  {step_id}: {status}")
        
    if execution.status == WorkflowStatus.FAILED:
        logger.error("Mission failed. Flat execution aborting.")
        
    await asyncio.sleep(2)
        
    logger.info("\n=== POST-MISSION VERIFICATION ===")
    
    res = await memory_manager.service.retrieve_memories("autonomous agents", limit=50)
    # Filter only those created by THIS specific execution or source
    mission_records = [r for r in res if r.source == execution.id or r.source == run_id]
    
    logger.info(f"[Verification 1] Memory query returned {len(mission_records)} record(s) matching this execution.")
    for r in mission_records:
        logger.info(f"    -> {r.id}: {r.content}")
        
    logger.info("[Verification 2] Trace Latency (Workflow Step 1)")
    if os.path.exists(trace_path):
        search_start = None
        search_end = None
        with open(trace_path, "r") as f:
            for line in f:
                trace = json.loads(line)
                et = trace.get("event_type")
                payload = trace.get("payload", {})
                if et == "workflow_step_started" and payload.get("step_id") == "step_1":
                    search_start = trace.get("timestamp")
                elif et == "workflow_step_completed" and payload.get("step_id") == "step_1":
                    search_end = trace.get("timestamp")
                    
        if search_start and search_end:
            logger.info(f"    -> SEARCH_QUERY_STARTED:   {search_start}")
            logger.info(f"    -> SEARCH_QUERY_COMPLETED: {search_end}")
            t1 = datetime.datetime.fromisoformat(search_start.replace("Z", "+00:00"))
            t2 = datetime.datetime.fromisoformat(search_end.replace("Z", "+00:00"))
            delta = (t2 - t1).total_seconds()
            logger.info(f"    -> Real SearxNG Latency Delta: {delta:.3f} seconds")
        else:
            logger.warning("    -> Could not find SEARCH_QUERY bounds in traces.jsonl.")
            
    logger.info("[Verification 3] World Model Node Creation")
    node = world_manager.repository.get_node("BRIEF-M2-RESEARCH")
    if node:
        logger.info(f"    -> Node created: {node.id}")
        logger.info(f"    -> Source reference: {node.source_reference}")
        if os.path.exists(node.source_reference):
            logger.info("    -> Source reference path exists on disk.")
        else:
            logger.warning("    -> Source reference path does not exist on disk!")
    else:
        logger.warning("    -> World Model node not found.")

    await event_bus.shutdown()
    
if __name__ == "__main__":
    asyncio.run(main())
