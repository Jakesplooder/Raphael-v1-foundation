# Raphael OS Architecture Specification v1.0

This document defines the strict architectural contracts for Raphael OS natively migrated modules (RRK). **No future subsystem may violate this specification.** It serves as the definitive engineering handbook for building and maintaining Native RRK capabilities.

---

## 1. The Separation of Concerns Pattern
Every Native RRK module must adhere to the `Repository` -> `Service` -> `Manager` -> `Provider` orchestration pattern.

- **Repository (`module_repository.py`)**: Responsible ONLY for persistence (JSON/Markdown/DB), state retrieval, checkpointing, and IO.
- **Service (`module_service.py`)**: Responsible ONLY for core business logic, domain algorithms, validation, state mutations, and coordination of operations without side effects (except through Providers).
- **Manager (`module_manager.py`)**: Acts as the `ServiceModule`. Responsible for the lifecycle (`initialize`, `heartbeat`, `shutdown`), EventBus subscription/publishing, and API request handling (`handle_request`).
- **Provider (`module_providers.py`)**: Responsible for external side-effects (e.g., executing commands, parsing Docker, querying an LLM). Must be registered into the `CapabilityRegistry`.

---

## 2. The Service Contract
Native RRK managers must implement the `ServiceModule` abstract base class defined in `raphael_core.kernel.interfaces.ServiceModule`.

### Contract Implementation
- `@property name(self) -> str`: Must return the module's unique name.
- `@property depends_on(self) -> List[str]`: Must return a list of dependency strings.
- `version(self) -> Dict[str, Any]`: Must return schema version dictionary (inherited by default).
- `async initialize(self) -> None`: Perform one-time setup and EventBus subscriptions.
- `async shutdown(self) -> None`: Cleanup resources.
- `async heartbeat(self) -> bool | Dict[str, Any]`: Return liveness state for the Health Monitor.
- `async handle_request(self, method: str, path: str, payload: Dict[str, Any] = None) -> Any`: Gateway HTTP handler.

**CRITICAL**: `name` and `depends_on` must use `@property` decorators. `version` must be a standard method.

---

## 3. The Capability Registry Contract
Providers are strictly decoupled from Services through the `CapabilityRegistry`.

- A Service must not instantiate Providers directly.
- The `Manager` must instantiate the Providers and inject them into the `Service` during initialization, or register them within a local `CapabilityRegistry` (e.g., `BuilderManager.register_provider()`).
- All runtime resolutions must occur at the point of action (lazy execution) to permit dynamic routing.

---

## 4. The EventBus and Event Schema
Cross-module communication occurs asynchronously via the `EventBus` (`raphael_core.kernel.eventbus.EventBus`).

### Event Schema
```python
Event(
    event_type: EventType,
    source: str,
    payload: Dict[str, Any],
    correlation_id: str = None
)
```
- **EventType**: Must be a strongly-typed enum defined in `EventType`.
- **Source**: Must match the `ServiceModule.name`.
- **Payload**: Must be purely JSON-serializable primitives.
- Managers must subscribe to events during `initialize()`:
  `self.event_bus.subscribe(EventType.TARGET_EVENT, self._handle_event)`

---

## 5. Workflow and Execution Schema
Orchestration objects (e.g., Execution Plans, Steps) must prioritize machine-readable state.

- **Storage Structure**: Plans are stored in `Execution Plans/{plan_id}/`.
- **Source of Truth**: `plan.json` represents the definitive machine state.
- **Human Readability**: `README.md` is generated *from* `plan.json` for Obsidian/Git compatibility.
- **Artifacts & Logs**: Retained inside `artifacts/` and `logs/` directories relative to the plan ID.

---

## 6. The Feature Registry
The `raphael_core/feature_registry.json` defines how the Gateway routes REST API commands to the underlying implementation.
When migrating a module to Native RRK, its engine string MUST be swapped from `"legacy"` to `"rrk"`.

### Example
```json
"projects": {
  "description": "Project management operations",
  "engine": "rrk",
  "endpoint": "/api/projects"
}
```

---

## 7. Folder and Naming Conventions
- Native modules reside in `raphael_core/kernel/managers/`, `raphael_core/kernel/services/`, etc.
- **Managers**: `[module_name]_manager.py` -> Class: `ModuleNameManager`
- **Services**: `[module_name]_service.py` -> Class: `ModuleNameService`
- **Repositories**: `[module_name]_repository.py` -> Class: `ModuleNameRepository`
- **Models**: `[module_name].py` -> Dataclasses representing internal schema.
- **Providers**: `[module_name]_providers.py` -> Provider implementations and Registries.

---

## 8. Host and Infrastructure Contracts
- The RRK should not directly interact with host operating system shells.
- All OS-level actions (Docker, File System execution, GPU monitoring) must be routed through the Host Manager API (`http://127.0.0.1:8789`).
- `HOST_MANAGER_URL` must remain configurable, NOT hardcoded, to support future remote infrastructure nodes.

---
**Approval Context**: This architecture is frozen as of v1.0. Future expansions (like Epic J - Execution Engine) must build *on top* of these contracts, not alter them.
