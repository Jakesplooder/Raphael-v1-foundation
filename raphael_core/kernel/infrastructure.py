import asyncio
import json
import logging
import os
import subprocess
import time
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

from .interfaces import ServiceModule, ModuleHealth, Event, EventType, EventPriority
from .registry import registry
from .models.infrastructure import (
    HealthSeverity, DependencyState, ServiceCapability, DependencyInfo,
    HostProcess, ContainerStatus, DockerHealth, ServiceStatus, InfrastructureSnapshot,
    InfrastructureEvent, InfrastructureState, ServicePolicy, ServicePolicyState,
    ServiceIdentity, ServiceExecution
)

logger = logging.getLogger("rrk.infrastructure")

class ServiceRegistry:
    def __init__(self, registry_path: Path):
        self.registry_path = registry_path
        self._data = {}

    def load(self):
        try:
            if self.registry_path.exists():
                with open(self.registry_path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load service registry: {e}")

    def get_services(self) -> List[Dict[str, Any]]:
        return self._data.get("services", [])

    def get_service(self, service_id: str) -> Optional[Dict[str, Any]]:
        for s in self.get_services():
            if s.get("identity", {}).get("service_id") == service_id:
                return s
        return None

class HostManager:
    def __init__(self):
        self.host_agent_url = os.environ.get("HOST_AGENT_URL")

    def _request(self, method: str, path: str, payload: dict = None) -> Optional[Dict[str, Any]]:
        if not self.host_agent_url:
            return None
        url = f"{self.host_agent_url.rstrip('/')}{path}"
        try:
            req = urllib.request.Request(url, method=method)
            if payload is not None:
                data = json.dumps(payload).encode("utf-8")
                req.add_header("Content-Type", "application/json")
                req.data = data
            with urllib.request.urlopen(req, timeout=3.0) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as e:
            logger.error(f"HostManager request failed for {url}: {e}")
            return None

    def status(self, service_id: str) -> HostProcess:
        res = self._request("GET", f"/process/status?id={service_id}")
        if res and res.get("status") == "running":
            return HostProcess(
                pid=res.get("pid"),
                running=True,
                logs=res.get("logs", ""),
                metrics=res.get("metrics", {})
            )
        return HostProcess(running=False)

    def start(self, service_id: str, command: str, cwd: str) -> bool:
        res = self._request("POST", f"/process/start", {"id": service_id, "command": command, "cwd": cwd})
        return res is not None and res.get("status") == "started"

    def stop(self, service_id: str) -> bool:
        res = self._request("POST", f"/process/stop", {"id": service_id})
        return res is not None and res.get("status") == "stopped"

    def restart(self, service_id: str, command: str, cwd: str) -> bool:
        self.stop(service_id)
        time.sleep(1)
        return self.start(service_id, command, cwd)


class DockerManager:
    def __init__(self):
        self.cli_available = self._check_cli()

    def _check_cli(self) -> bool:
        try:
            subprocess.run(["docker", "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def health(self) -> DockerHealth:
        if not self.cli_available:
            return DockerHealth(available=False, last_error="Docker CLI not found in container")
        try:
            res = subprocess.run(["docker", "ps", "-a", "--format", "{{json .}}"], capture_output=True, text=True)
            containers = []
            for line in res.stdout.strip().split("\n"):
                if not line:
                    continue
                data = json.loads(line)
                containers.append(ContainerStatus(
                    container_id=data.get("ID", ""),
                    name=data.get("Names", ""),
                    image=data.get("Image", ""),
                    state=data.get("State", ""),
                    status=data.get("Status", ""),
                    ports=[data.get("Ports", "")]
                ))
            return DockerHealth(available=True, containers=containers)
        except Exception as e:
            return DockerHealth(available=False, last_error=str(e))

    def start_container(self, container_name: str) -> bool:
        try:
            subprocess.run(["docker", "start", container_name], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def stop_container(self, container_name: str) -> bool:
        try:
            subprocess.run(["docker", "stop", container_name], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def restart_container(self, container_name: str) -> bool:
        try:
            subprocess.run(["docker", "restart", container_name], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False


class HealthManager:
    def __init__(self, host_manager: HostManager, docker_manager: DockerManager):
        self.host = host_manager
        self.docker = docker_manager

    def evaluate_comfyui(self, host_process: HostProcess, health_target: str) -> tuple[HealthSeverity, Dict[str, Any]]:
        details = {
            "Running": False,
            "Listening": False,
            "Responsive": False,
            "CUDA Available": False,
            "Models Loaded": False,
            "Queue Length": 0,
            "VRAM Usage": "0GB",
            "Last Error": host_process.last_error
        }
        if not host_process.running:
            return HealthSeverity.OFFLINE, details
        
        details["Running"] = True
        
        try:
            req = urllib.request.Request(health_target)
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                if resp.status == 200:
                    details["Listening"] = True
                    details["Responsive"] = True
                    details["CUDA Available"] = True
                    details["Models Loaded"] = True
                    return HealthSeverity.HEALTHY, details
        except Exception as e:
            details["Last Error"] = str(e)
            return HealthSeverity.CRITICAL, details
            
        return HealthSeverity.WARNING, details

    def evaluate(self, service_info: Dict[str, Any]) -> ServiceStatus:
        ident = service_info.get("identity", {})
        exec_info = service_info.get("execution", {})
        policy = service_info.get("policy", {})
        health_cfg = service_info.get("health", {})
        
        sid = ident.get("service_id", "unknown")
        backend = exec_info.get("backend", "internal")
        
        status = ServiceStatus(
            identity=ServiceIdentity(
                service_id=sid,
                display_name=ident.get("display_name", sid),
                category=ident.get("category", "unknown")
            ),
            execution=ServiceExecution(
                backend=backend
            ),
            policy=ServicePolicyState(
                startup=ServicePolicy(policy.get("startup", "manual")),
                notes=policy.get("notes", "")
            ),
            capabilities=[ServiceCapability(c) for c in service_info.get("capabilities", [])],
        )

        if backend == "host_agent":
            hp = self.host.status(sid)
            status.execution.host_process = hp
            if sid == "comfyui":
                sev, det = self.evaluate_comfyui(hp, health_cfg.get("endpoint", ""))
                status.severity = sev
                status.health_details = det
            else:
                if hp.running:
                    status.severity = HealthSeverity.HEALTHY
                    status.health_details = {"Running": True}
                else:
                    status.severity = HealthSeverity.OFFLINE
        elif backend == "docker":
            dh = self.docker.health()
            container_name = exec_info.get("container_name", "")
            c_stat = next((c for c in dh.containers if c.name == container_name or c.name == sid), None)
            status.execution.container = c_stat
            if c_stat and "Up" in c_stat.status:
                status.severity = HealthSeverity.HEALTHY
            elif c_stat:
                status.severity = HealthSeverity.CRITICAL
            else:
                status.severity = HealthSeverity.OFFLINE
        
        return status


class DependencyManager:
    def resolve(self, services: Dict[str, ServiceStatus]):
        for sid, status in services.items():
            if sid == "pod_helpers":
                comfy = services.get("comfyui")
                if comfy and comfy.severity == HealthSeverity.HEALTHY:
                    status.dependencies.append(DependencyInfo(service_id="comfyui", state=DependencyState.SATISFIED))
                elif comfy:
                    status.dependencies.append(DependencyInfo(service_id="comfyui", state=DependencyState.WAITING))
                    if status.severity == HealthSeverity.HEALTHY:
                        status.severity = HealthSeverity.DEGRADED
                else:
                    status.dependencies.append(DependencyInfo(service_id="comfyui", state=DependencyState.MISSING))

class InfrastructureManager(ServiceModule):
    def __init__(self):
        self._running = False
        self.registry = ServiceRegistry(Path("C:/RaphaelOS/launcher/service_registry.json") if os.name == "nt" else Path("/app/runtime/launcher/service_registry.json"))
        self.host = HostManager()
        self.docker = DockerManager()
        self.health_manager = HealthManager(self.host, self.docker)
        self.dependencies = DependencyManager()
        self._last_snapshot: Optional[InfrastructureSnapshot] = None
        self._loop_task = None
        self._events: List[InfrastructureEvent] = []

    def publish_event(self, event_type: str, service_id: Optional[str] = None, details: Dict[str, Any] = None):
        evt = InfrastructureEvent(event_type=event_type, service_id=service_id, details=details or {})
        self._events.append(evt)
        # Keep last 100 events
        if len(self._events) > 100:
            self._events.pop(0)
            
        event_bus = registry.get_service("EventBus")
        if event_bus:
            event_bus.publish(Event(
                type=EventType.INFRASTRUCTURE_ALERT,
                source="InfrastructureManager",
                priority=EventPriority.HIGH,
                payload=evt.model_dump()
            ))

    @property
    def name(self) -> str:
        return "InfrastructureManager"

    async def initialize(self) -> None:
        self.publish_event("INFRASTRUCTURE_INITIALIZING")
        self.registry.load()

    async def start(self) -> None:
        self._running = True
        self.publish_event("INFRASTRUCTURE_READY")
        self._loop_task = asyncio.create_task(self._monitor_loop())

    async def _monitor_loop(self):
        while self._running:
            try:
                snapshot = self.build_snapshot()
                
                if self._last_snapshot:
                    for sid, s in snapshot.services.items():
                        old_s = self._last_snapshot.services.get(sid)
                        if old_s and old_s.severity != s.severity:
                            self.publish_event("SERVICE_HEALTH_CHANGED", sid, {
                                "old_severity": old_s.severity.value,
                                "new_severity": s.severity.value
                            })
                            if s.severity == HealthSeverity.HEALTHY:
                                self.publish_event("SERVICE_STARTED", sid)
                            elif s.severity == HealthSeverity.OFFLINE:
                                self.publish_event("SERVICE_STOPPED", sid)
                                
                    for cap in snapshot.capabilities:
                        if cap not in self._last_snapshot.capabilities:
                            self.publish_event("CAPABILITY_AVAILABLE", details={"capability": cap.value})
                            
                    for cap in self._last_snapshot.capabilities:
                        if cap not in snapshot.capabilities:
                            self.publish_event("CAPABILITY_LOST", details={"capability": cap.value})
                
                self._last_snapshot = snapshot
            except Exception as e:
                logger.error(f"Error in monitor loop: {e}")
            await asyncio.sleep(5)

    def build_snapshot(self) -> InfrastructureSnapshot:
        snap = InfrastructureSnapshot()
        snap.state = InfrastructureState.READY if self._running else InfrastructureState.OFFLINE
        snap.docker = self.docker.health()
        
        all_capabilities = set()
        policies_active = {}
        
        for svc_info in self.registry.get_services():
            policy = svc_info.get("policy", {}).get("startup", "manual")
            policies_active[policy] = policies_active.get(policy, 0) + 1
            
            if policy == ServicePolicy.DISABLED.value:
                continue
                
            status = self.health_manager.evaluate(svc_info)
            snap.services[status.identity.service_id] = status
            
            if status.severity == HealthSeverity.HEALTHY:
                for cap in status.capabilities:
                    all_capabilities.add(cap)
            
        self.dependencies.resolve(snap.services)
        
        snap.capabilities = list(all_capabilities)
        snap.policies_active = policies_active
        
        # Calculate overall health
        severities = [s.severity for s in snap.services.values()]
        if HealthSeverity.CRITICAL in severities:
            snap.overall_health = HealthSeverity.CRITICAL
        elif HealthSeverity.DEGRADED in severities:
            snap.overall_health = HealthSeverity.DEGRADED
        elif HealthSeverity.WARNING in severities:
            snap.overall_health = HealthSeverity.WARNING
        else:
            snap.overall_health = HealthSeverity.HEALTHY
            
        return snap
        
    def get_snapshot(self) -> InfrastructureSnapshot:
        if not self._last_snapshot:
            return self.build_snapshot()
        return self._last_snapshot

    async def heartbeat(self) -> bool | Dict[str, Any]:
        return {"snapshot_ready": self._last_snapshot is not None}

    async def stop(self) -> None:
        self._running = False
        if self._loop_task:
            self._loop_task.cancel()

    async def shutdown(self) -> None:
        pass

    def health(self) -> ModuleHealth:
        return ModuleHealth.OK if self._running else ModuleHealth.SHUTDOWN

    def status(self) -> str:
        return "Monitoring infrastructure state"

    def metrics(self) -> Dict[str, Any]:
        return {}
