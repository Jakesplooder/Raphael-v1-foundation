import asyncio
import json
import os
import time
from typing import Dict, List, Set

from .observability import ObservabilityLayer
from .registry import registry
from .state import store

class Kernel:
    """
    80.0 Raphael Runtime Kernel (RRK)
    The singleton orchestrator that computes the DAG boot order and manages the main event loop.
    """
    def __init__(self, mode: str = "production"):
        self.mode = mode
        self._running = False
        self._boot_time = 0.0
        self.version = "2.0.0"

    def _compute_dag(self) -> List[str]:
        """Compute the boot order based on service depends_on declarations."""
        services = {svc.name: svc for svc in registry.get_all_services()}
        
        # Simple topological sort
        in_degree = {name: 0 for name in services}
        adj = {name: [] for name in services}
        
        for name, svc in services.items():
            for dep in svc.depends_on:
                if dep in services:
                    adj[dep].append(name)
                    in_degree[name] += 1
                else:
                    ObservabilityLayer.warning("Kernel", f"Service {name} depends on missing service {dep}")

        queue = [name for name, deg in in_degree.items() if deg == 0]
        boot_order = []

        while queue:
            curr = queue.pop(0)
            boot_order.append(curr)
            for neighbor in adj[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(boot_order) != len(services):
            raise RuntimeError("Cycle detected in Service dependencies!")

        return boot_order

    async def boot(self) -> None:
        """Boot the RRK by initializing and starting all registered services in DAG order."""
        start_ms = time.time() * 1000
        ObservabilityLayer.info("Kernel", f"Booting Raphael Runtime Kernel (RRK) v{self.version} in {self.mode} mode.")
        
        self._running = True
        
        try:
            boot_order = self._compute_dag()
            ObservabilityLayer.info("Kernel", f"Computed boot order: {' -> '.join(boot_order)}")
            
            # Phase 1: Initialize
            for name in boot_order:
                svc = registry.get_service(name)
                ObservabilityLayer.debug("Kernel", f"Initializing {name}...")
                await svc.initialize()
                
            # Phase 2: Start
            for name in boot_order:
                svc = registry.get_service(name)
                ObservabilityLayer.debug("Kernel", f"Starting {name}...")
                await svc.start()
                
            self._boot_time = time.time()
            duration_ms = (time.time() * 1000) - start_ms
            
            ObservabilityLayer.info("Kernel", f"RRK boot completed successfully in {duration_ms:.2f}ms")
            
            self._write_manifest(duration_ms)
            
        except Exception as e:
            ObservabilityLayer.error("Kernel", f"FATAL ERROR during boot sequence: {e}")
            await self.shutdown()
            raise

    def _write_manifest(self, duration_ms: float) -> None:
        """Generate the runtime_manifest.json (Reproducible State Tracking)"""
        manifest = {
            "kernel_version": self.version,
            "boot_time": self._boot_time,
            "runtime_mode": self.mode,
            "services": [svc.name for svc in registry.get_all_services()],
            "plugins": [], # Future integration with PluginLoader state
            "providers": [],
            "health": "OK",
            "constitution_version": "1.0",
            "world_model_version": "2.0",
            "trace_seed": "RRK-" + str(time.time()),
            "startup_duration_ms": duration_ms
        }
        
        manifest_path = os.path.join(os.environ.get("RAPHAEL_DATA_DIR", "."), "runtime_manifest.json")
        try:
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2)
            ObservabilityLayer.info("Kernel", f"Wrote runtime_manifest.json to {manifest_path}")
        except Exception as e:
            ObservabilityLayer.error("Kernel", f"Failed to write manifest: {e}")

    async def shutdown(self) -> None:
        """Gracefully shutdown all services in reverse DAG order."""
        if not self._running:
            return
            
        self._running = False
        ObservabilityLayer.warning("Kernel", "Initiating graceful shutdown sequence...")
        
        try:
            boot_order = self._compute_dag()
            shutdown_order = list(reversed(boot_order))
            
            # Phase 1: Stop processing
            for name in shutdown_order:
                svc = registry.get_service(name)
                ObservabilityLayer.debug("Kernel", f"Stopping {name}...")
                try:
                    await asyncio.wait_for(svc.stop(), timeout=5.0)
                except Exception as e:
                    ObservabilityLayer.error("Kernel", f"Error stopping {name}: {e}")
                    
            # Phase 2: Shutdown resources
            for name in shutdown_order:
                svc = registry.get_service(name)
                ObservabilityLayer.debug("Kernel", f"Shutting down {name}...")
                try:
                    await asyncio.wait_for(svc.shutdown(), timeout=5.0)
                except Exception as e:
                    ObservabilityLayer.error("Kernel", f"Error shutting down {name}: {e}")
                    
        except Exception as e:
            ObservabilityLayer.error("Kernel", f"Error during shutdown sequence: {e}")
            
        ObservabilityLayer.info("Kernel", "RRK completely shut down.")
