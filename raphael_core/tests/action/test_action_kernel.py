import logging
import asyncio

from raphael_core.simulation.simulation_event_bus import SimulationEventBus
from raphael_core.action.action_kernel import ActionKernel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test.action_kernel")

async def run_action_benchmarks():
    logger.info("Starting D24: Autonomous Action Kernel Benchmarks...")
    event_bus = SimulationEventBus()
    kernel = ActionKernel(event_bus)
    
    # We will capture events to assert against them
    emitted_events = []
    
    # Monkey-patch the event bus emit to capture history for tests
    original_emit = event_bus.emit
    def test_emit(event_type: str, source: str, payload: dict = None):
        emitted_events.append({"type": event_type, "payload": payload})
        original_emit(event_type, source, payload)
    event_bus.emit = test_emit

    # ---------------------------------------------------------
    # Benchmark 1: Permission Boundary
    # ---------------------------------------------------------
    logger.info("\n--- Benchmark 1: Permission Boundary ---")
    emitted_events.clear()
    
    # Marketing Employee tries to launch ad campaign over budget
    res = await kernel.execute_intent(
        role="Marketing Employee",
        intent="launch_ad_campaign",
        payload={"cost": 1000}
    )
    assert res["status"] == "DENIED"
    assert "requires CEO approval" in res["reason"]
    logger.info("Permission Boundary perfectly blocked unauthorized spend.")

    # ---------------------------------------------------------
    # Benchmark 2: Action Routing
    # ---------------------------------------------------------
    logger.info("\n--- Benchmark 2: Action Routing ---")
    emitted_events.clear()
    
    res = await kernel.execute_intent(
        role="Marketing Employee",
        intent="create_social_post",
        payload={}
    )
    assert res["status"] == "SUCCESS"
    assert "n8n executed create_social_post" in res["details"]["message"]
    logger.info("Action perfectly routed to the correct execution provider (n8n).")

    # ---------------------------------------------------------
    # Benchmark 3: Simulation Gate
    # ---------------------------------------------------------
    logger.info("\n--- Benchmark 3: Simulation Gate ---")
    emitted_events.clear()
    
    # LOW risk action (no simulation)
    await kernel.execute_intent(role="CEO Agent", intent="create_social_post", payload={})
    sim_events = [e for e in emitted_events if e["type"] == "ACTION_SIMULATION_STARTED"]
    assert len(sim_events) == 0
    logger.info("LOW risk action skipped simulation correctly.")
    
    emitted_events.clear()
    
    # HIGH risk action (full D22 simulation)
    await kernel.execute_intent(role="CEO Agent", intent="spend_large_capital", payload={})
    sim_events = [e for e in emitted_events if e["type"] == "ACTION_SIMULATION_STARTED"]
    assert len(sim_events) == 1
    assert sim_events[0]["payload"]["type"] == "FULL_D22"
    logger.info("HIGH risk action correctly triggered a full D22 simulation.")

    # ---------------------------------------------------------
    # Benchmark 4: Execution Memory
    # ---------------------------------------------------------
    logger.info("\n--- Benchmark 4: Execution Memory ---")
    
    history = kernel.memory.get_history()
    # Check if 'create_social_post' was logged
    social_logs = [h for h in history if h["intent"] == "create_social_post" and h["status"] == "SUCCESS"]
    assert len(social_logs) > 0
    logger.info("Execution Memory correctly logged the external action for D19 intelligence.")

    # ---------------------------------------------------------
    # Benchmark 5: Failure Recovery
    # ---------------------------------------------------------
    logger.info("\n--- Benchmark 5: Failure Recovery ---")
    emitted_events.clear()
    
    # Trigger an unknown intent to force failure
    res = await kernel.execute_intent(role="CEO Agent", intent="unknown_action_123", payload={})
    assert res["status"] == "FAILED"
    failed_events = [e for e in emitted_events if e["type"] == "ACTION_FAILED"]
    assert len(failed_events) > 0
    logger.info("Failure safely caught and emitted ACTION_FAILED event.")

    # ---------------------------------------------------------
    # Benchmark 6: Full Entrepreneur Loop
    # ---------------------------------------------------------
    logger.info("\n--- Benchmark 6: Full Entrepreneur Loop ---")
    emitted_events.clear()
    
    # Simulating the ultimate chain:
    # Factory -> CEO Agent -> Simulation Gate -> n8n Execution -> Event Emitted
    
    res = await kernel.execute_intent(
        role="CEO Agent",
        intent="create_shopify_product",
        payload={"cost": 0}
    )
    
    assert res["status"] == "SUCCESS"
    assert "n8n executed" in res["details"]["message"]
    
    # Check if the right events fired
    event_types = [e["type"] for e in emitted_events]
    assert "ACTION_REQUESTED" in event_types
    assert "ACTION_AUTHORIZED" in event_types
    assert "ACTION_EXECUTED" in event_types
    assert "ACTION_LEARNED" in event_types
    
    logger.info("Full Entrepreneur Loop passed! Raphael can now decide and execute.")
    logger.info("\nALL D24 BENCHMARKS PASSED.")

if __name__ == "__main__":
    asyncio.run(run_action_benchmarks())
