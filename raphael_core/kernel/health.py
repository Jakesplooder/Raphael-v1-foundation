import asyncio
from typing import Dict, Any, List
import inspect

from .interfaces import ServiceModule, ModuleHealth
from .observability import ObservabilityLayer
from .registry import registry
from .state import store


class HealthMonitor(ServiceModule):
    """
    80.5 Health Monitor
    4-Layer Health Architecture: Module, Runtime, Executive, System.
    Polls the ServiceContracts of registered RRK modules.
    """
    
    def __init__(self):
        self._running = False
        self._monitor_task = None
        self._overall_health = 100.0

    @property
    def name(self) -> str:
        return "HealthMonitor"

    @property
    def depends_on(self) -> list[str]:
        return ["RuntimeRegistry"]

    async def initialize(self) -> None:
        store.set_state(self.name, "status", "initialized")

    async def start(self) -> None:
        self._running = True
        self._monitor_task = asyncio.create_task(self._monitoring_loop())
        store.set_state(self.name, "status", "running")
        ObservabilityLayer.info(self.name, "Health Monitor started")

    async def heartbeat(self) -> bool:
        return self._running and (self._monitor_task is not None and not self._monitor_task.done())

    async def stop(self) -> None:
        self._running = False
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass
        store.set_state(self.name, "status", "stopped")

    async def shutdown(self) -> None:
        store.set_state(self.name, "status", "shutdown")
        ObservabilityLayer.info(self.name, "Health Monitor shut down")

    def health(self) -> ModuleHealth:
        return ModuleHealth.OK if self._running else ModuleHealth.FAILED

    def status(self) -> str:
        return f"System Health: {self._overall_health:.1f}%"

    def metrics(self) -> Dict[str, Any]:
        return {
            "system_health": self._overall_health
        }

    async def _monitoring_loop(self) -> None:
        while self._running:
            try:
                services = registry.get_all_services()
                total_services = len(services)
                if total_services == 0:
                    await asyncio.sleep(5)
                    continue

                healthy_count = 0
                for svc in services:
                    # 1. Module Health Layer
                    try:
                        is_alive = await asyncio.wait_for(svc.heartbeat(), timeout=2.0)
                        svc_health = svc.health()
                        if inspect.isawaitable(svc_health):
                            svc_health = await svc_health
                        
                        if is_alive and svc_health == ModuleHealth.OK:
                            healthy_count += 1
                            store.set_state(svc.name, "health", "OK")
                        else:
                            store.set_state(svc.name, "health", svc_health.value)
                            ObservabilityLayer.warning(self.name, f"Service {svc.name} is degraded or dead.")
                            
                    except asyncio.TimeoutError:
                        store.set_state(svc.name, "health", "TIMEOUT")
                        ObservabilityLayer.error(self.name, f"Service {svc.name} heartbeat timed out!")
                    except Exception as e:
                        store.set_state(svc.name, "health", "ERROR")
                        ObservabilityLayer.error(self.name, f"Service {svc.name} heartbeat error: {e}")

                # 4. System Health Layer (Aggregated)
                # In a full system, Runtime (CPU/Mem) and Executive (Prediction accuracy) layers
                # would also weight this calculation.
                self._overall_health = (healthy_count / total_services) * 100
                store.set_state("System", "overall_health", self._overall_health)
                
                # Emit metric for observability
                ObservabilityLayer.record_metric(self.name, "system_health", self._overall_health)

                await asyncio.sleep(10) # Poll every 10 seconds
            except asyncio.CancelledError:
                break
            except Exception as e:
                ObservabilityLayer.error(self.name, f"Monitoring loop error: {e}")
                await asyncio.sleep(5)
