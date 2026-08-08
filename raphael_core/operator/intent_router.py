from typing import Dict, Any, Tuple
import enum
import json
from raphael_core.kernel.registry import registry
from raphael_core.llm.router import LLMRouter

class IntentClass(str, enum.Enum):
    CAPABILITY_QUERY = "capability_query"
    WORKFLOW_QUERY = "workflow_query"
    STATUS_QUERY = "status_query"
    CONVERSATION = "conversation"
    RESEARCH = "research"
    CREATION = "creation"
    AUTOMATION = "automation"
    BUSINESS = "business"
    EXECUTION = "execution"
    DECISION = "decision"
    APPROVAL = "approval"
    REJECTION = "rejection"
    MODIFICATION = "modification"
    CAPABILITY_DISPATCH = "capability_dispatch"
    EXECUTIVE_COMMAND = "executive_command"
    UNKNOWN = "unknown"

CAPABILITY_TRIGGERS = [
    "what can you do",
    "what are you capable of",
    "what tools",
    "what systems"
]

WORKFLOW_TRIGGERS = [
    "what workflows"
]

CREATION_TRIGGERS = [
    "create",
    "make",
    "build",
    "generate",
    "design"
]

BUSINESS_TRIGGERS = [
    "store",
    "business",
    "shop",
    "brand",
    "product"
]

VIDEO_TRIGGERS = [
    "video",
    "animation",
    "movie",
    "storyboard"
]

class HybridIntentRouter:
    """
    Operator Shell Intent Router.
    Uses hard interceptors before falling back to LLM intent routing.
    """
    def __init__(self):
        self.llm = LLMRouter()
        
    def _emit_event(self, intent_val: str, confidence: float):
        from raphael_core.kernel.event_bus import emit
        emit("INTENT_DETECTED", "dashboard_chat", {
            "intent": intent_val,
            "confidence": confidence,
            "source": "dashboard_chat"
        })

    def route(self, prompt: str) -> Tuple[IntentClass, Dict[str, Any]]:
        p = prompt.strip().lower()
        
        # Stage 1: Deterministic Routing / Hard Interceptors
        if p in ["approve", "/approve", "yes", "execute", "[execute]", "confirm"]:
            self._emit_event("approval", 1.0)
            return IntentClass.APPROVAL, {"action": "approve"}
            
        if p in ["reject", "/reject", "no", "cancel", "[cancel]", "stop"]:
            self._emit_event("rejection", 1.0)
            return IntentClass.REJECTION, {"action": "reject"}
            
        if p in ["modify", "edit", "change"] or p.startswith("modify ") or p.startswith("edit ") or p.startswith("change "):
            self._emit_event("modification", 1.0)
            return IntentClass.MODIFICATION, {"action": "modify"}
            
        if p in ["what should i prioritize today", "what should i do today", "prioritize"]:
            self._emit_event("executive_command", 1.0)
            return IntentClass.EXECUTIVE_COMMAND, {"command": "priority"}
            
        if p in ["list councils", "show councils", "what councils exist"]:
            self._emit_event("executive_command", 1.0)
            return IntentClass.EXECUTIVE_COMMAND, {"command": "councils"}
            
        if p in ["show agents", "list agents"]:
            self._emit_event("executive_command", 1.0)
            return IntentClass.EXECUTIVE_COMMAND, {"command": "agents"}
            
        if p in ["show missions", "list missions"]:
            self._emit_event("executive_command", 1.0)
            return IntentClass.EXECUTIVE_COMMAND, {"command": "missions"}
            
        if p in ["start storyboard", "run storyboard", "create video", "make me a video"]:
            self._emit_event("capability_dispatch", 1.0)
            return IntentClass.CAPABILITY_DISPATCH, {"workflow_id": "video.generate"}
            
        if p in ["start pod", "create product", "run pod pipeline"]:
            self._emit_event("capability_dispatch", 1.0)
            return IntentClass.CAPABILITY_DISPATCH, {"workflow_id": "pod.generate"}
            
        if p in ["start build", "build this", "run builder"]:
            self._emit_event("capability_dispatch", 1.0)
            return IntentClass.CAPABILITY_DISPATCH, {"workflow_id": "builder.application"}
            
        # Legacy CommandBus fallbacks
        if any(trigger in p for trigger in ["save to knowledge", "raw json", "show sources", "show snippets", "save source", "remember this"]):
            self._emit_event("conversation", 1.0)
            return IntentClass.CONVERSATION, {"action": "legacy_fallback"}
            
        if any(trigger in p for trigger in ["status", "how is the", "status of", "statua", "ststus"]):
            self._emit_event("status_query", 1.0)
            return IntentClass.STATUS_QUERY, {"query": "status"}
            
        if any(trigger in p for trigger in CAPABILITY_TRIGGERS):
            self._emit_event("capability_query", 1.0)
            return IntentClass.CAPABILITY_QUERY, {"query": "capabilities"}
            
        if any(trigger in p for trigger in WORKFLOW_TRIGGERS):
            self._emit_event("workflow_query", 1.0)
            return IntentClass.WORKFLOW_QUERY, {"query": "workflows"}
            
        # Infer creation/business intents deterministically first if it has clear verbs
        is_creation = any(trigger in p for trigger in CREATION_TRIGGERS)
        is_business = any(trigger in p for trigger in BUSINESS_TRIGGERS)
        
        if is_creation and is_business:
            self._emit_event("business", 0.9)
            return IntentClass.BUSINESS, {"source": "hard_interceptor"}
            
        if is_creation:
            self._emit_event("creation", 0.9)
            return IntentClass.CREATION, {"source": "hard_interceptor"}

        # Stage 2: LLM Classification Fallback for ambiguous statements
        system_prompt = """Classify the user's intent into exactly one of these categories:
conversation, research, creation, automation, business, execution, decision.

Return a JSON object: {"intent": "category", "confidence": 0.95}"""

        try:
            result = self.llm.execute(
                system_prompt=system_prompt,
                context="",
                task=prompt,
                capability="reasoning"
            )
            text = result.response.strip()
            if text.startswith("```json"):
                text = text[7:-3].strip()
            data = json.loads(text)
            
            intent_val = data.get("intent", "unknown").lower()
            confidence = data.get("confidence", 0.0)
            
            try:
                intent_type = IntentClass(intent_val)
            except ValueError:
                intent_type = IntentClass.UNKNOWN
                
            self._emit_event(intent_type.value, confidence)
            return intent_type, data
            
        except Exception as e:
            self._emit_event("unknown", 0.0)
            return IntentClass.UNKNOWN, {"error": str(e)}

intent_router = HybridIntentRouter()
