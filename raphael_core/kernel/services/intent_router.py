import enum
import logging
from typing import Dict, Any, Tuple
from ..interfaces import ServiceModule, ModuleHealth
from ..state import store

logger = logging.getLogger("kernel.intent_router")

class IntentClass(str, enum.Enum):
    NAVIGATION = "NAVIGATION"     # Matrix UI transitions, opening panels
    QUERY = "QUERY"               # Fetching data, asking state (WorldModel)
    COMMAND = "COMMAND"           # Triggering missions/workflows
    CONVERSATION = "CONVERSATION" # General chat, reasoning, brainstorming
    UNKNOWN = "UNKNOWN"

class IntentRouter(ServiceModule):
    """
    80.8 Intent Router
    The cognitive entry point for all user inputs.
    Filters prompts into categories before dispatching to heavy orchestration.
    """
    def __init__(self):
        self._running = False
        
    @property
    def name(self) -> str:
        return "IntentRouter"
        
    @property
    def depends_on(self) -> list[str]:
        return []
        
    async def initialize(self) -> None:
        store.set_state(self.name, "status", "initialized")
        
    async def start(self) -> None:
        self._running = True
        store.set_state(self.name, "status", "running")
        
    async def heartbeat(self) -> bool:
        return self._running
        
    async def stop(self) -> None:
        self._running = False
        store.set_state(self.name, "status", "stopped")
        
    async def shutdown(self) -> None:
        pass
        
    def health(self) -> ModuleHealth:
        return ModuleHealth.OK if self._running else ModuleHealth.FAILED
        
    def status(self) -> str:
        return "Online and classifying intents."
        
    def metrics(self) -> Dict[str, Any]:
        return {}
        
    def classify_intent(self, prompt: str) -> IntentClass:
        """
        Heuristically classifies a prompt.
        In a fully-realized system, this calls a fast local LLM (e.g., Llama-3 8B)
        or relies on the AIGateway. For v1.0, we use strong keyword heuristics.
        """
        p = prompt.lower().strip()
        
        # Navigation Heuristics
        if any(p.startswith(w) for w in ["open", "show me", "zoom", "focus", "go to", "navigate to", "view"]):
            if "create" not in p and "generate" not in p and "build" not in p:
                return IntentClass.NAVIGATION
                
        # Command Heuristics
        if any(p.startswith(w) for w in ["create", "generate", "build", "publish", "deploy", "research", "start", "run", "make"]):
            return IntentClass.COMMAND
            
        # Query Heuristics
        if any(p.startswith(w) for w in ["what is", "how many", "who", "when", "where", "list", "status of"]):
            return IntentClass.QUERY
            
        # Fallback to conversation
        return IntentClass.CONVERSATION
        
    async def route_intent(self, prompt: str) -> Tuple[IntentClass, Dict[str, Any]]:
        """
        Classifies and prepares the route for the UI/Gateway.
        """
        intent = self.classify_intent(prompt)
        logger.info(f"Classified prompt '{prompt[:30]}...' as {intent}")
        
        route_info = {
            "intent": intent.value,
            "handled_by": None
        }
        
        if intent == IntentClass.COMMAND:
            # We defer execution logic to the Gateway, which will call MissionDispatcher
            route_info["handled_by"] = "MissionDispatcher"
        elif intent == IntentClass.NAVIGATION:
            route_info["handled_by"] = "MatrixUI"
        elif intent == IntentClass.QUERY:
            route_info["handled_by"] = "KnowledgeService"
        elif intent == IntentClass.CONVERSATION:
            route_info["handled_by"] = "AIGateway"
            
        return intent, route_info
