from typing import Dict, Any, List, Optional
import abc
from ..models.workflow_plan import WorkflowPlan, WorkflowStep

class WorkflowProvider(abc.ABC):
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @abc.abstractmethod
    def capabilities(self) -> List[str]:
        return []

class PlanningProvider(WorkflowProvider):
    @abc.abstractmethod
    async def create_plan(self, goal: str, context: Dict[str, Any]) -> WorkflowPlan:
        pass
        
    @abc.abstractmethod
    async def refine_plan(self, plan: WorkflowPlan, feedback: str) -> WorkflowPlan:
        pass

class ExecutionProvider(WorkflowProvider):
    @abc.abstractmethod
    async def execute_step(self, step: WorkflowStep, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a workflow step and returns the result dictionary.
        """
        pass

class VerificationProvider(WorkflowProvider):
    @abc.abstractmethod
    async def verify_step(self, step: WorkflowStep, result: Dict[str, Any]) -> bool:
        pass

class CapabilityRegistry:
    """
    A universal registry resolving Models, Providers, Agents, Tools, Skills, and Workflows.
    """
    def __init__(self):
        self._providers: Dict[str, WorkflowProvider] = {}
        self._capabilities: Dict[str, List[str]] = {}

    def register(self, provider: WorkflowProvider) -> None:
        self._providers[provider.name()] = provider
        for cap in provider.capabilities():
            if cap not in self._capabilities:
                self._capabilities[cap] = []
            if provider.name() not in self._capabilities[cap]:
                self._capabilities[cap].append(provider.name())

    def unregister(self, provider_name: str) -> None:
        if provider_name in self._providers:
            provider = self._providers.pop(provider_name)
            for cap in provider.capabilities():
                if cap in self._capabilities:
                    self._capabilities[cap].remove(provider_name)

    def resolve(self, capability: str) -> List[WorkflowProvider]:
        """Returns all providers that support the given capability."""
        provider_names = self._capabilities.get(capability, [])
        return [self._providers[name] for name in provider_names if name in self._providers]

    def resolve_best(self, capability: str) -> Optional[WorkflowProvider]:
        """Returns the best (or first) provider for a capability."""
        providers = self.resolve(capability)
        if providers:
            return providers[0]
        return None
