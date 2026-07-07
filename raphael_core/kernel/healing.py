import asyncio
from typing import Dict, Any

from .interfaces import ServiceModule, ModuleHealth
from .observability import ObservabilityLayer
from .registry import registry
from .state import store


class SelfHealingRuntime(ServiceModule):
    """
    80.8 Self Healing Runtime
    Detects failures via the Runtime State Store (updated by Health Monitor)
    and gracefully restarts modules.
    """
    
    def __init__(self):
        self._running = False
        self._healing_task = None
        self._restart_counts: Dict[str, int] = {}

    @property
    def name(self) -> str:
        return "SelfHealingRuntime"

    @property
    def depends_on(self) -> list[str]:
        return ["HealthMonitor", "RuntimeStateStore"]

    async def initialize(self) -> None:
        store.set_state(self.name, "status", "initialized")

    async def start(self) -> None:
        self._running = True
        self._healing_task = asyncio.create_task(self._healing_loop())
        store.set_state(self.name, "status", "running")
        ObservabilityLayer.info(self.name, "Self Healing Runtime started")

    async def heartbeat(self) -> bool:
        return self._running and (self._healing_task is not None and not self._healing_task.done())

    async def stop(self) -> None:
        self._running = False
        if self._healing_task:
            self._healing_task.cancel()
            try:
                await self._healing_task
            except asyncio.CancelledError:
                pass
        store.set_state(self.name, "status", "stopped")

    async def shutdown(self) -> None:
        store.set_state(self.name, "status", "shutdown")
        ObservabilityLayer.info(self.name, "Self Healing Runtime shut down")

    def health(self) -> ModuleHealth:
        return ModuleHealth.OK if self._running else ModuleHealth.FAILED

    def status(self) -> str:
        return "Monitoring for module failures."

    def metrics(self) -> Dict[str, Any]:
        return {
            "restart_counts": dict(self._restart_counts)
        }

    async def _healing_loop(self) -> None:
        """Continuously check state store for failures and attempt restarts."""
        while self._running:
            try:
                full_state = store.get_full_state()
                
                for module_name, state_dict in full_state.items():
                    # Don't try to heal the self healer or registry this way
                    if module_name in (self.name, "RuntimeRegistry", "System"):
                        continue
                        
                    health_status = state_dict.get("health")
                    if health_status in ("FAILED", "TIMEOUT", "ERROR"):
                        await self._attempt_restart(module_name)

                await asyncio.sleep(15) # Check every 15 seconds
            except asyncio.CancelledError:
                break
            except Exception as e:
                ObservabilityLayer.error(self.name, f"Healing loop error: {e}")
                await asyncio.sleep(5)

    async def _attempt_restart(self, module_name: str) -> None:
        count = self._restart_counts.get(module_name, 0)
        
        # Max retries before we assume catastrophic unrecoverable failure
        if count >= 3:
            ObservabilityLayer.error(self.name, f"Module {module_name} failed {count} times. Giving up.")
            return

        self._restart_counts[module_name] = count + 1
        ObservabilityLayer.warning(self.name, f"Attempting restart of {module_name} (Attempt {count + 1})")
        
        svc = registry.get_service(module_name)
        if not svc:
            ObservabilityLayer.error(self.name, f"Cannot heal unknown module {module_name}")
            return
            
        try:
            store.set_state(module_name, "status", "restarting")
            
            # Follow the strict service contract
            try:
                await asyncio.wait_for(svc.stop(), timeout=5.0)
            except Exception as stop_e:
                ObservabilityLayer.error(self.name, f"Error stopping {module_name} during heal: {stop_e}")
                
            try:
                await asyncio.wait_for(svc.shutdown(), timeout=5.0)
            except Exception as shut_e:
                ObservabilityLayer.error(self.name, f"Error shutting down {module_name} during heal: {shut_e}")
                
            await asyncio.sleep(1) # Brief pause to clear sockets/handles
            
            await svc.initialize()
            await svc.start()
            
            ObservabilityLayer.info(self.name, f"Successfully restarted {module_name}")
            store.set_state(module_name, "health", "OK")
            
        except Exception as e:
            ObservabilityLayer.error(self.name, f"Failed to restart {module_name}: {e}")
            store.set_state(module_name, "health", "FAILED")
