import abc
from dataclasses import dataclass
from typing import Any

@dataclass
class ReasoningResult:
    provider_name: str
    model_name: str
    response: str
    latency_sec: float
    token_count: int
    raw_output: dict[str, Any]

class BaseProvider(abc.ABC):
    """
    Abstract base class for all LLM providers in Raphael.
    Rule: LLMs reason. Raphael decides.
    """
    
    @property
    @abc.abstractmethod
    def provider_name(self) -> str:
        pass
        
    @abc.abstractmethod
    def reason(self, model: str, system_prompt: str, context: str, task: str) -> ReasoningResult:
        """
        Executes a reasoning task against the provider.
        """
        pass
