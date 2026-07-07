import asyncio
import time
from raphael_core.kernel.registry import registry
from raphael_core.kernel.event_bus import EventBus
from raphael_core.kernel.job_system import JobSystem
from raphael_core.kernel.calendar import ExecutiveCalendar
from raphael_core.kernel.health import HealthMonitor
from raphael_core.kernel.healing import SelfHealingRuntime
from raphael_core.kernel.dashboard import KernelDashboard
from raphael_core.kernel.core import Kernel
from raphael_core.kernel.interfaces import Event, EventType, Job

async def stress_test():
    print("=== RRK STRESS TEST ===")
    
    # 1. Register Core Services
    registry.register_service(EventBus())
    registry.register_service(JobSystem())
    registry.register_service(ExecutiveCalendar())
    registry.register_service(HealthMonitor())
    registry.register_service(SelfHealingRuntime())
    registry.register_service(KernelDashboard())

    kernel = Kernel(mode="development")
    
    # Run boot in background so we can inject stress events
    kernel_task = asyncio.create_task(kernel.boot())
    await asyncio.sleep(2) # Give it time to boot DAG
    
    eb = registry.get_service("EventBus")
    js = registry.get_service("JobSystem")
    
    print("\n--- Testing Volatile Event Throughput ---")
    start = time.time()
    for i in range(1000):
        # We only do 1000 for realistic simulation time in this test wrapper
        await eb.publish(Event(source="StressTest", type=EventType.TOKEN_STREAMED))
    print(f"Sent 1000 volatile events in {time.time() - start:.4f}s")
    
    print("\n--- Testing Durable Event Persistence ---")
    start = time.time()
    for i in range(100):
        await eb.publish(Event(source="StressTest", type=EventType.PLAN_APPROVED))
    print(f"Sent 100 durable events in {time.time() - start:.4f}s")
    
    print("\n--- Testing Job Queueing ---")
    start = time.time()
    for i in range(500):
        await js.submit_job(Job(owner="StressTest", module="Builder", trace_id=f"job-{i}"))
    print(f"Submitted 500 jobs in {time.time() - start:.4f}s")

    print("\n--- Simulating Module Crash (HealthMonitor) ---")
    health = registry.get_service("HealthMonitor")
    await health.stop()
    await health.shutdown()
    
    print("Waiting 20 seconds for SelfHealingRuntime to detect and revive HealthMonitor...")
    await asyncio.sleep(20)
    
    health_status = health.health().value
    print(f"HealthMonitor status after healing cycle: {health_status}")

    print("\n--- Initiating Graceful Shutdown ---")
    await kernel.shutdown()
    
    print("=== RRK STRESS TEST COMPLETE ===")

if __name__ == "__main__":
    asyncio.run(stress_test())
