import asyncio
import time
from typing import Callable, Coroutine, Dict, Any, List

from .interfaces import ServiceModule, ModuleHealth
from .observability import ObservabilityLayer
from .state import store


class ExecutiveCalendar(ServiceModule):
    """
    80.3 Executive Calendar
    Event-driven and conditional execution engine replacing strict cron scheduling.
    Allows rules like "IF Aaron logged in AND Runtime healthy THEN generate morning brief"
    """

    def __init__(self):
        self._rules: List[Dict[str, Any]] = []
        self._running = False
        self._eval_task = None
        
    @property
    def name(self) -> str:
        return "ExecutiveCalendar"

    @property
    def depends_on(self) -> list[str]:
        return ["RuntimeStateStore", "EventBus"]

    async def initialize(self) -> None:
        store.set_state(self.name, "status", "initialized")

    async def start(self) -> None:
        self._running = True
        self._eval_task = asyncio.create_task(self._evaluation_loop())
        store.set_state(self.name, "status", "running")
        ObservabilityLayer.info(self.name, "Executive Calendar started")

    async def heartbeat(self) -> bool:
        return self._running and (self._eval_task is not None and not self._eval_task.done())

    async def stop(self) -> None:
        self._running = False
        if self._eval_task:
            self._eval_task.cancel()
            try:
                await self._eval_task
            except asyncio.CancelledError:
                pass
        store.set_state(self.name, "status", "stopped")

    async def shutdown(self) -> None:
        self._rules.clear()
        store.set_state(self.name, "status", "shutdown")
        ObservabilityLayer.info(self.name, "Executive Calendar shut down")

    def health(self) -> ModuleHealth:
        return ModuleHealth.OK if self._running else ModuleHealth.FAILED

    def status(self) -> str:
        return f"Tracking {len(self._rules)} active conditional rules."

    def metrics(self) -> Dict[str, Any]:
        return {
            "active_rules": len(self._rules)
        }

    def add_rule(self, condition: Callable[[], bool], action: Callable[[], Coroutine], name: str) -> None:
        """Register a conditional rule for event-driven execution."""
        self._rules.append({
            "name": name,
            "condition": condition,
            "action": action,
            "last_executed": 0
        })
        ObservabilityLayer.debug(self.name, f"Registered rule: {name}")

    async def _evaluation_loop(self) -> None:
        """Continuously evaluate conditional rules."""
        while self._running:
            try:
                for rule in self._rules:
                    # Very simple cooldown mechanism (e.g., execute once per 60 seconds at most)
                    if time.time() - rule["last_executed"] > 60:
                        if rule["condition"]():
                            ObservabilityLayer.info(self.name, f"Condition met for rule '{rule['name']}'. Executing.")
                            rule["last_executed"] = time.time()
                            try:
                                await rule["action"]()
                            except Exception as e:
                                ObservabilityLayer.error(self.name, f"Rule action failed: {e}")
                
                # Sleep to prevent tight CPU looping.
                # In a fully reactive system, this is triggered via EventBus wakeups.
                await asyncio.sleep(5)
            except asyncio.CancelledError:
                break
            except Exception as e:
                ObservabilityLayer.error(self.name, f"Evaluation loop error: {e}")
                await asyncio.sleep(5)
