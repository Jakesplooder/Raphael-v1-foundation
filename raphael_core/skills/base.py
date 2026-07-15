import abc
from typing import Dict, Any, List

class BaseSkill(abc.ABC):
    """
    Abstract base class for all Raphael Shared Skills.
    Skills are pure, stateless tool implementations shared across all agents.
    """
    
    @property
    @abc.abstractmethod
    def skill_id(self) -> str:
        """Unique identifier for the skill, e.g. SKILL-DOCKER-START"""
        pass

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Human-readable or function name."""
        pass

    @property
    @abc.abstractmethod
    def version(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def constitutional_class(self) -> str:
        """
        'operational' or 'authority'.
        Authority skills require approval workflows before executing.
        """
        pass

    @property
    @abc.abstractmethod
    def allowed_trust_tiers(self) -> List[int]:
        """List of integer trust tiers allowed to invoke this skill (e.g., [1, 2, 3, 4])."""
        pass
        
    @property
    def rate_limit_per_hour(self) -> int:
        return 1000  # Default generous limit

    @abc.abstractmethod
    def parameters_schema(self) -> Dict[str, Any]:
        """JSON Schema defining required parameters for this skill."""
        pass

    @abc.abstractmethod
    async def execute(self, params: Dict[str, Any], trace_id: str) -> Dict[str, Any]:
        """
        Core execution logic.
        Returns a dictionary indicating success and the payload result.
        """
        pass
