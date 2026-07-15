import logging
import urllib.request
import json

from .event_bus import global_event_bus, emit
from .storage import KernelStorage
from .models.model_router import ModelRouter
from ..execution.executor import Executor
from ..execution.planner import ExecutionPlanner
from ..workforce.agency.agent_runtime import AgentRuntime
from ..perception.vision.vision_provider import VisionProvider

logger = logging.getLogger("rrk.kernel.runtime")

class HostManagerInterface:
    def __init__(self):
        self.url = "http://127.0.0.1:8789"
        
    def check_health(self):
        try:
            req = urllib.request.urlopen(f"{self.url}/health", timeout=2)
            return json.loads(req.read().decode())
        except Exception:
            return {"status": "unreachable"}

class RaphaelRuntime:
    """
    The official RRK OS entry point.
    Initializes and orchestrates the foundational operational domains.
    """
    def __init__(self):
        logger.info("Initializing RaphaelRuntime...")
        self.event_bus = global_event_bus
        self.storage = KernelStorage()
        self.host_manager = HostManagerInterface()
        self.model_router = ModelRouter()
        
        self.planner = ExecutionPlanner()
        self.executor = Executor()
        self.agent_runtime = AgentRuntime()
        self.vision = VisionProvider()

    def start(self):
        logger.info("Booting Raphael Cognitive OS...")
        
        hm_health = self.host_manager.check_health()
        if hm_health.get("status") == "healthy":
            logger.info("Host Manager is connected and healthy.")
        else:
            logger.warning("Host Manager is unreachable. Hardware metrics will be unavailable.")
            
        emit("RUNTIME_STARTED", "RaphaelRuntime", {"status": "online"})
        logger.info("RaphaelRuntime boot complete.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    runtime = RaphaelRuntime()
    runtime.start()
