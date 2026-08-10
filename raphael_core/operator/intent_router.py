from typing import Dict, Any, Tuple
import enum
import json
from raphael_core.kernel.registry import registry
from raphael_core.llm.router import LLMRouter

class IntentClass(str, enum.Enum):
    CAPABILITY_QUERY = "capability_query"
    WORKFLOW_QUERY = "workflow_query"
    CONVERSATION = "conversation"
    RESEARCH = "research"
    CREATION = "creation"
    AUTOMATION = "automation"
    BUSINESS = "business"
    EXECUTION = "execution"
    DECISION = "decision"
    APPROVAL = "approval"
    REJECTION = "rejection"
    GENERATE_ASSET = "generate_asset"
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

GENERATE_ASSET_TRIGGERS = [
    "generate an image",
    "create a picture",
    "generate a picture",
    "create an image",
    "draw me",
    "draw a",
    "paint a",
    "generate art",
    "make an image"
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
        import logging
        logger = logging.getLogger("intent_router")
        logger.debug(f"INTENT_DETECTED: {intent_val} (confidence: {confidence})")

    def route(self, prompt: str) -> Tuple[IntentClass, Dict[str, Any]]:
        p = prompt.strip().lower()
        
        # Stage 1: Deterministic Routing / Hard Interceptors
        if p in ["approve", "/approve", "yes", "execute", "[execute]"]:
            self._emit_event("approval", 1.0)
            return IntentClass.APPROVAL, {"action": "approve"}
            
        if p in ["reject", "/reject", "no", "cancel", "[cancel]"]:
            self._emit_event("rejection", 1.0)
            return IntentClass.REJECTION, {"action": "reject"}
            
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
            
        is_generate_asset = any(trigger in p for trigger in GENERATE_ASSET_TRIGGERS)
        if is_generate_asset:
            self._emit_event("generate_asset", 1.0)
            return IntentClass.GENERATE_ASSET, {"source": "hard_interceptor"}
            
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
