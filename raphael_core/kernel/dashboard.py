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
