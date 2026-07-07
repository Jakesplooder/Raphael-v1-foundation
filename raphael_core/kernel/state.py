import threading
from typing import Dict, Any, Optional
from .observability import ObservabilityLayer

class RuntimeStateStore:
    """
    80.05 Runtime State Store.
    A centralized, thread-safe store where every module publishes its state.
    Provides the single source of truth for the Kernel Dashboard.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(RuntimeStateStore, cls).__new__(cls)
                cls._instance._state = {}
                cls._instance._store_lock = threading.Lock()
        return cls._instance

    def set_state(self, module_name: str, key: str, value: Any, trace_id: Optional[str] = None) -> None:
        """Publish a state update for a module."""
        with self._store_lock:
            if module_name not in self._state:
                self._state[module_name] = {}
            self._state[module_name][key] = value
        
        # Emits a state change metric for observability
        ObservabilityLayer.debug(
            source="RuntimeStateStore", 
            message=f"State updated for [{module_name}]: {key} -> {value}",
            trace_id=trace_id
        )

    def get_state(self, module_name: str, key: str, default: Any = None) -> Any:
        """Retrieve a specific state value for a module."""
        with self._store_lock:
            return self._state.get(module_name, {}).get(key, default)

    def get_module_state(self, module_name: str) -> Dict[str, Any]:
        """Retrieve all state associated with a module."""
        with self._store_lock:
            # Return a copy to prevent accidental mutation outside the lock
            return dict(self._state.get(module_name, {}))

    def get_full_state(self) -> Dict[str, Dict[str, Any]]:
        """Retrieve the entire runtime state map (used by Dashboard)."""
        with self._store_lock:
            # Deepish copy for safety
            return {mod: dict(state) for mod, state in self._state.items()}

# Global singleton instance
store = RuntimeStateStore()
