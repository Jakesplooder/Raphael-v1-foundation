import asyncio
import threading
from typing import Dict, Any

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

from .interfaces import ServiceModule, ModuleHealth
from .observability import ObservabilityLayer
from .state import store


class KernelDashboard(ServiceModule):
    """
    80.7 Kernel Dashboard
    Dedicated FastAPI server on port 8788 strictly for Kernel Diagnostics.
    """
    
    def __init__(self):
        self._running = False
        self._server = None
        self._thread = None

        self.app = FastAPI(title="Raphael Runtime Kernel (RRK) Dashboard")
        
        @self.app.get("/")
        def read_root():
            return {"message": "Raphael Runtime Kernel (RRK) is online."}
            
        @self.app.get("/api/state")
        def get_full_state():
            return store.get_full_state()
            
        @self.app.get("/api/health")
        def get_health():
            return store.get_module_state("System")
            
        @self.app.post("/api/world-model/query")
        def query_world_model(payload: Dict[str, Any]):
            from .registry import registry
            svc = registry.get_service("WorldModelService")
            if not svc:
                return {"error": "WorldModelService not registered in Kernel"}
            return svc.query(
                payload.get("agent_id", "Unknown"),
                payload.get("purpose", "api query"),
                payload.get("question", "")
            )
            
        @self.app.get("/api/world-model/graph")
        def get_world_model_graph():
            from .registry import registry
            svc = registry.get_service("WorldModelService")
            if not svc:
                return {"error": "WorldModelService not registered in Kernel"}
            return svc.get_graph()

        @self.app.get("/api/inspector")
        def get_inspector():
            return store.get_full_state()

        @self.app.get("/api/goals")
        def get_goals():
            from .registry import registry
            mgr = registry.get_service("GoalsManager")
            if not mgr:
                return {"error": "GoalsManager not registered in Kernel"}
            return {"items": mgr.get_all_goals()}

        @self.app.get("/api/tasks")
        def get_tasks():
            from .registry import registry
            mgr = registry.get_service("TasksManager")
            if not mgr:
                return {"error": "TasksManager not registered in Kernel"}
            return {"items": mgr.get_tasks(scope="agent")}

        @self.app.get("/api/council_tasks")
        def get_council_tasks():
            from .registry import registry
            mgr = registry.get_service("TasksManager")
            if not mgr:
                return {"error": "TasksManager not registered in Kernel"}
            return {"items": mgr.get_tasks(scope="council")}

        @self.app.get("/api/tasks_overview")
        def get_tasks_overview():
            from .registry import registry
            mgr = registry.get_service("TasksManager")
            if not mgr:
                return {"error": "TasksManager not registered in Kernel"}
            return {"items": mgr.get_tasks(scope="all")}

        @self.app.get("/api/system/modules")
        def get_system_modules():
            from .registry import registry
            import inspect
            
            modules = {}
            for name, service in registry._services.items():
                try:
                    mod_name = name.replace("Manager", "").lower()
                    metadata = service.manifest().get("metadata", {})
                    
                    # Check composition dynamically
                    has_repo = hasattr(service, "repository")
                    has_service = hasattr(service, "service")
                    has_provider = hasattr(service, "providers") or hasattr(service, "provider")
                    
                    try:
                        health_val = service.health().value
                    except AttributeError:
                        health_val = str(service.health())
                    
                    modules[mod_name] = {
                        "repository": has_repo,
                        "service": has_service,
                        "manager": True,
                        "provider": has_provider,
                        "version": metadata.get("version", "1.0.0"),
                        "health": health_val,
                        "schema": metadata.get("schema", 1),
                        "migration": metadata.get("migration", "Unknown")
                    }
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    print(f"Error processing service {name}: {e}")
            return modules

        # Phase 2: RESTful RRK Infrastructure APIs
        @self.app.get("/api/infrastructure/runtime")
        def get_infra_runtime():
            from .registry import registry
            infra = registry.get_service("InfrastructureManager")
            if not infra:
                return {"error": "InfrastructureManager not registered"}
            # Return snapshot as a dict. Pydantic's .dict() or .model_dump() handles this.
            return infra.get_snapshot().dict()

        @self.app.get("/api/infrastructure/services")
        def get_infra_services():
            from .registry import registry
            infra = registry.get_service("InfrastructureManager")
            if not infra:
                return {"error": "InfrastructureManager not registered"}
            snap = infra.get_snapshot()
            return {sid: svc.dict() for sid, svc in snap.services.items()}

        @self.app.get("/api/infrastructure/service/{service_id}")
        def get_infra_service(service_id: str):
            from .registry import registry
            infra = registry.get_service("InfrastructureManager")
            if not infra:
                return {"error": "InfrastructureManager not registered"}
            snap = infra.get_snapshot()
            svc = snap.services.get(service_id)
            if not svc:
                return {"error": "Service not found"}
            return svc.dict()

        @self.app.post("/api/infrastructure/service/{service_id}/start")
        def start_infra_service(service_id: str):
            from .registry import registry
            infra = registry.get_service("InfrastructureManager")
            if not infra:
                return {"error": "InfrastructureManager not registered"}
            svc_info = infra.registry.get_service(service_id)
            if not svc_info:
                return {"error": "Service not found in registry"}
            
            exec_info = svc_info.get("execution", {})
            backend = exec_info.get("backend", "internal")
            
            # Fire lifecycle hook
            infra.publish_event("SERVICE_BEFORE_START", service_id)
            
            if backend == "host_agent":
                success = infra.host.start(service_id, exec_info.get("start_command", ""), exec_info.get("working_directory", ""))
            elif backend == "docker":
                container_name = exec_info.get("container_name", f"raphaelos_{service_id}")
                success = infra.docker.start_container(container_name)
            else:
                success = False
                
            if success:
                infra.publish_event("SERVICE_AFTER_START", service_id)
                
            return {"status": "started" if success else "failed", "service_id": service_id}

        @self.app.post("/api/infrastructure/service/{service_id}/stop")
        def stop_infra_service(service_id: str):
            from .registry import registry
            infra = registry.get_service("InfrastructureManager")
            if not infra:
                return {"error": "InfrastructureManager not registered"}
            svc_info = infra.registry.get_service(service_id)
            if not svc_info:
                return {"error": "Service not found in registry"}
            
            exec_info = svc_info.get("execution", {})
            backend = exec_info.get("backend", "internal")
            
            infra.publish_event("SERVICE_BEFORE_STOP", service_id)
            
            if backend == "host_agent":
                success = infra.host.stop(service_id)
            elif backend == "docker":
                container_name = exec_info.get("container_name", f"raphaelos_{service_id}")
                success = infra.docker.stop_container(container_name)
            else:
                success = False
                
            if success:
                infra.publish_event("SERVICE_AFTER_STOP", service_id)
                
            return {"status": "stopped" if success else "failed", "service_id": service_id}

        @self.app.post("/api/infrastructure/service/{service_id}/restart")
        def restart_infra_service(service_id: str):
            from .registry import registry
            infra = registry.get_service("InfrastructureManager")
            if not infra:
                return {"error": "InfrastructureManager not registered"}
            svc_info = infra.registry.get_service(service_id)
            if not svc_info:
                return {"error": "Service not found in registry"}
            
            exec_info = svc_info.get("execution", {})
            backend = exec_info.get("backend", "internal")
            
            infra.publish_event("SERVICE_BEFORE_STOP", service_id)
            
            if backend == "host_agent":
                success = infra.host.restart(service_id, exec_info.get("start_command", ""), exec_info.get("working_directory", ""))
            elif backend == "docker":
                container_name = exec_info.get("container_name", f"raphaelos_{service_id}")
                success = infra.docker.restart_container(container_name)
            else:
                success = False
                
            if success:
                infra.publish_event("SERVICE_AFTER_START", service_id)
                
            return {"status": "restarted" if success else "failed", "service_id": service_id}

        @self.app.get("/api/infrastructure/docker")
        def get_infra_docker():
            from .registry import registry
            infra = registry.get_service("InfrastructureManager")
            if not infra:
                return {"error": "InfrastructureManager not registered"}
            return infra.docker.health().dict()

        @self.app.get("/api/infrastructure/capabilities")
        def get_infra_capabilities():
            from .registry import registry
            infra = registry.get_service("InfrastructureManager")
            if not infra:
                return {"error": "InfrastructureManager not registered"}
            return {"capabilities": [cap.value for cap in infra.get_snapshot().capabilities]}

        @self.app.get("/api/infrastructure/events")
        def get_infra_events():
            from .registry import registry
            infra = registry.get_service("InfrastructureManager")
            if not infra:
                return {"error": "InfrastructureManager not registered"}
            return {"events": [evt.model_dump() for evt in infra._events]}

        @self.app.get("/api/infrastructure/summary")
        def get_infra_summary():
            from .registry import registry
            infra = registry.get_service("InfrastructureManager")
            if not infra:
                return {"error": "InfrastructureManager not registered"}
            snap = infra.get_snapshot()
            
            warnings = 0
            critical = 0
            for sid, svc in snap.services.items():
                if svc.severity.value == "warning": warnings += 1
                elif svc.severity.value == "critical": critical += 1
                elif svc.severity.value == "degraded": warnings += 1
                
            return {
                "overall_health": snap.overall_health.value,
                "service_counts": {
                    "total": len(snap.services),
                    "healthy": sum(1 for s in snap.services.values() if s.severity.value == "healthy"),
                    "offline": sum(1 for s in snap.services.values() if s.severity.value == "offline"),
                },
                "active_capabilities": [c.value for c in snap.capabilities],
                "warnings": warnings,
                "critical_failures": critical
            }

        @self.app.get("/api/infrastructure/topology")
        def get_infra_topology():
            from .registry import registry
            infra = registry.get_service("InfrastructureManager")
            if not infra:
                return {"error": "InfrastructureManager not registered"}
            snap = infra.get_snapshot()
            
            return {
                "host": {
                    "agent_available": infra.host.host_agent_url is not None
                },
                "docker": snap.docker.model_dump(),
                "services": [s.model_dump() for s in snap.services.values()]
            }

        @self.app.get("/api/inspector")
        def get_inspector():
            from .registry import registry
            services = registry.get_all_services()
            manifests = {}
            heartbeats = store.get_module_state("Heartbeats") or {}
            
            for svc in services:
                if hasattr(svc, "manifest"):
                    m = svc.manifest()
                    hb = heartbeats.get(svc.name, {})
                    if hb.get("type") == "agent":
                        m["inspector"] = {
                            "generation": hb.get("generation"),
                            "state": hb.get("state"),
                            "current_job": hb.get("last_job"),
                            "queue_position": hb.get("queue_depth"),
                            "model": hb.get("provider"),
                            "context_mb": hb.get("memory_mb"),
                            "tokens": hb.get("tokens"),
                            "last_latency_sec": hb.get("latency_sec")
                        }
                    manifests[svc.name] = m
                    
            sys_metrics = {}
            metrics_mgr = registry.get_service("RuntimeMetricsManager")
            if metrics_mgr:
                sys_metrics = metrics_mgr.metrics()
                
            return {"manifests": manifests, "system_metrics": sys_metrics}
            
        @self.app.get("/dashboard", response_class=HTMLResponse)
        def render_html():
            state = store.get_full_state()
            
            html = "<html><head><title>RRK Diagnostics</title><style>"
            html += "body { font-family: monospace; background: #0d1117; color: #c9d1d9; padding: 20px; }"
            html += ".module { border: 1px solid #30363d; margin-bottom: 10px; padding: 10px; border-radius: 5px; }"
            html += "h1 { color: #58a6ff; }"
            html += "</style></head><body>"
            html += "<h1>Raphael Runtime Kernel (RRK)</h1>"
            
            # System Health
            sys_health = state.get("System", {}).get("overall_health", "Unknown")
            html += f"<h2>System Health: {sys_health}%</h2>"
            
            for mod_name, mod_data in state.items():
                if mod_name == "System": continue
                html += f"<div class='module'><h3>{mod_name}</h3>"
                for k, v in mod_data.items():
                    html += f"<div><b>{k}:</b> {v}</div>"
                html += "</div>"
                
            html += "</body></html>"
            return html

    @property
    def name(self) -> str:
        return "KernelDashboard"

    @property
    def depends_on(self) -> list[str]:
        return ["RuntimeStateStore", "HealthMonitor"]

    async def initialize(self) -> None:
        store.set_state(self.name, "status", "initialized")

    def _run_uvicorn(self):
        # We run uvicorn in a separate thread so it doesn't block the RRK event loop
        # Uvicorn uses its own asyncio loop
        config = uvicorn.Config(self.app, host="0.0.0.0", port=8788, log_level="warning")
        self._server = uvicorn.Server(config)
        self._server.run()

    async def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._run_uvicorn, daemon=True)
        self._thread.start()
        
        store.set_state(self.name, "status", "running")
        ObservabilityLayer.info(self.name, "Kernel Dashboard started on port 8788")

    async def heartbeat(self) -> bool:
        return self._running and (self._thread is not None and self._thread.is_alive())

    async def stop(self) -> None:
        self._running = False
        if self._server:
            # Uvicorn server has a should_exit flag
            self._server.should_exit = True
        store.set_state(self.name, "status", "stopped")

    async def shutdown(self) -> None:
        if self._thread:
            # Let the thread die natively since it's a daemon thread
            pass
        store.set_state(self.name, "status", "shutdown")
        ObservabilityLayer.info(self.name, "Kernel Dashboard shut down")

    def health(self) -> ModuleHealth:
        if self._running and self._thread and self._thread.is_alive():
            return ModuleHealth.OK
        return ModuleHealth.FAILED

    def status(self) -> str:
        return "Serving dashboard on http://localhost:8788/dashboard"

    def metrics(self) -> Dict[str, Any]:
        return {}
