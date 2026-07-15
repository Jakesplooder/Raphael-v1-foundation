from abc import ABC, abstractmethod
from typing import List
from ..world_entities import WorldSignal

class WorldProvider(ABC):
    @abstractmethod
    async def collect_signals(self) -> List[WorldSignal]:
        pass
