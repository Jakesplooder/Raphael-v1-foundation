import abc
from typing import Dict, Any, List

class GoalProvider(abc.ABC):
    @abc.abstractmethod
    def get_active_goals(self) -> List[str]: pass
    
    @abc.abstractmethod
    def get_strategic_priorities(self) -> List[str]: pass
    
    @abc.abstractmethod
    def get_risk_profile(self) -> str: pass

class SimulationProvider(abc.ABC):
    @property
    @abc.abstractmethod
    def name(self) -> str: pass

    @abc.abstractmethod
    async def simulate(self, context: Dict[str, Any], option: 'Option') -> Dict[str, Any]: pass
