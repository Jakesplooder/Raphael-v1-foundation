from typing import Dict, Any, Type, Optional, List
from .interfaces import ServiceModule
from .observability import ObservabilityLayer
from .state import store

class RuntimeRegistry:
    """
    80.4 Runtime Registry
    Unified dependency injection container for Services, Plugins, Agents, Providers, and LLMs.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RuntimeRegistry, cls).__new__(cls)
            cls._instance._services = {}
            cls._instance._agents = {}
            cls._instance._providers = {}
        return cls._instance

    def register_service(self, service: ServiceModule) -> None:
        """Register a core RRK service."""
        if service.name in self._services:
            ObservabilityLayer.warning("RuntimeRegistry", f"Service {service.name} is already registered. Overwriting.")
            
        self._services[service.name] = service
        store.set_state("RuntimeRegistry", f"service_{service.name}", "registered")
        ObservabilityLayer.info("RuntimeRegistry", f"Registered service: {service.name}")

    def get_service(self, name: str) -> Optional[ServiceModule]:
        """Retrieve a registered service."""
        return self._services.get(name)

    def get_all_services(self) -> List[ServiceModule]:
        return list(self._services.values())

    def register_agent(self, name: str, agent_instance: Any) -> None:
        """Register a worker agent."""
        self._agents[name] = agent_instance
        store.set_state("RuntimeRegistry", f"agent_{name}", "registered")
        ObservabilityLayer.info("RuntimeRegistry", f"Registered agent: {name}")

    def get_agent(self, name: str) -> Optional[Any]:
        return self._agents.get(name)

    def register_provider(self, name: str, provider_instance: Any) -> None:
        """Register an LLM provider."""
        self._providers[name] = provider_instance
        store.set_state("RuntimeRegistry", f"provider_{name}", "registered")
        ObservabilityLayer.info("RuntimeRegistry", f"Registered provider: {name}")
        
    def get_provider(self, name: str) -> Optional[Any]:
        return self._providers.get(name)

    def inject_dependencies(self, target: Any, dependencies: List[str]) -> None:
        """
        Dynamically inject requested dependencies into a target object.
        Currently sets them as attributes.
        """
        for dep in dependencies:
            service = self.get_service(dep)
            if service:
                setattr(target, dep.lower(), service)
            else:
                ObservabilityLayer.error("RuntimeRegistry", f"Failed to inject dependency '{dep}' into '{target.__class__.__name__}'")

registry = RuntimeRegistry()
