import logging
from typing import Callable, Dict, List

logger = logging.getLogger("rrk.world.events")

class WorldEventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        
    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
        
    def publish(self, event_type: str, payload: dict):
        logger.info(f"[WorldEventBus] Publishing {event_type}")
        for callback in self._subscribers.get(event_type, []):
            callback(payload)
