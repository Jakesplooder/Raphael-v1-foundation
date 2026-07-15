import logging
from typing import List, Callable, Dict, Any

logger = logging.getLogger("rrk.simulation.event_bus")

class SimulationEventBus:
    """
    Isolated EventBus for simulations. 
    Does not leak into the real global_event_bus unless explicitly bridged.
    """
    def __init__(self):
        self.subscribers = {}
        self.history = []

    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)

    def emit(self, type_str: str, source: str, payload: Dict[str, Any]):
        event = {"type": type_str, "source": source, "payload": payload}
        self.history.append(event)
        logger.debug(f"SIM EVENT: {type_str} from {source}: {payload}")
        for handler in self.subscribers.get(type_str, []):
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Error handling simulation event {type_str}: {e}")
