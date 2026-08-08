import logging
from typing import Dict, Any, List, Optional, Type, TypeVar
from ..models.business_objects import (
    BusinessObject, Business, Initiative, Campaign, ContentAsset,
    AffiliateLink, Product, Supplier, Order, Revenue, Expense, KPI
)
from ..event_bus import global_event_bus
from ..interfaces import Event, EventType
from ..storage import KernelStorage

logger = logging.getLogger("kernel.business_manager")

T = TypeVar("T", bound=BusinessObject)

class BusinessManager:
    """
    Manages the lifecycle of Business Objects and ensures all state changes
    are durably stored and emitted to the EventBus.
    """
    def __init__(self):
        self.storage = KernelStorage(base_dir="raphael_storage")
        
    def _domain_for_class(self, cls: Type[T]) -> str:
        return cls.__name__.lower() + "s"

    async def create(self, obj: T) -> T:
        domain = self._domain_for_class(type(obj))
        self.storage.save(domain, f"{obj.id}.json", obj.model_dump())
        
        # Emit event
        event_name = f"{type(obj).__name__.upper()}_CREATED"
        event = Event(
            source="BusinessManager",
            type=EventType.SYSTEM_INFO,
            council="Operations Council",
            agent="BusinessManager",
            payload={
                "action": event_name,
                "object_id": obj.id,
                "data": obj.model_dump()
            }
        )
        await global_event_bus.publish(event)
        return obj

    async def update(self, obj: T) -> T:
        domain = self._domain_for_class(type(obj))
        self.storage.save(domain, f"{obj.id}.json", obj.model_dump())
        
        # Emit event
        event_name = f"{type(obj).__name__.upper()}_UPDATED"
        event = Event(
            source="BusinessManager",
            type=EventType.SYSTEM_INFO,
            council="Operations Council",
            agent="BusinessManager",
            payload={
                "action": event_name,
                "object_id": obj.id,
                "data": obj.model_dump()
            }
        )
        await global_event_bus.publish(event)
        return obj

    def get(self, cls: Type[T], obj_id: str) -> Optional[T]:
        domain = self._domain_for_class(cls)
        data = self.storage.load(domain, f"{obj_id}.json")
        if data:
            return cls(**data)
        return None

    def list_all(self, cls: Type[T]) -> List[T]:
        domain = self._domain_for_class(cls)
        filenames = self.storage.query(domain)
        objects = []
        for filename in filenames:
            data = self.storage.load(domain, filename)
            if data:
                objects.append(cls(**data))
        return objects

global_business_manager = BusinessManager()
