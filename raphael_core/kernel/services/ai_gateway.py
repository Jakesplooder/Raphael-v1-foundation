import logging
from typing import Dict, Any, Optional
from ...llm.router import LLMRouter

logger = logging.getLogger("rrk.services.ai_gateway")

class AIGateway:
    """
    The central interface for all Language Model interactions in the RRK.
    Services (like the Builder) request capabilities (e.g., 'coding', 'reasoning') 
    and the Gateway routes the request to the correct underlying model.
    """
    
    def __init__(self, config: Any):
        self.config = config
        self.router = LLMRouter()
        self.metrics_logger = logging.getLogger("rrk.telemetry.ai_gateway")
        self.capability_map = {
            "coding": "qwen2.5-coder:14b",
            "planning": "qwen3",
            "reasoning": "deepseek-r1",
            "reviewing": "qwen2.5-coder:14b",
        }
        self._arch_spec = None

    def _get_architecture_spec(self) -> str:
        if self._arch_spec is None:
            import os
            spec_path = os.path.join(os.path.dirname(__file__), "../../../docs/architecture/Architecture Specification.md")
            try:
                with open(spec_path, "r", encoding="utf-8") as f:
                    self._arch_spec = f.read()
            except Exception:
                self._arch_spec = "Architecture Specification not found."
        return self._arch_spec

    def generate(self, capability: str, task: str, context: Dict[str, Any] = None, schema_model: Any = None, max_retries: int = 3) -> Dict[str, Any]:
        """
        Executes a generation task using the best model for the requested capability.
        Supports schema validation (Pydantic), retries, and automatic Architecture Spec injection for coding.
        """
        import json
        model = self.capability_map.get(capability, "llama3.1:8b")
        logger.info(f"[AIGateway] Routing capability. Capability: {capability} | Model: {model} | Task length: {len(task)}")
        
        # 1. Prompt Construction & Context Injection
        system_prompt = f"You are Raphael's Builder Engine executing a {capability} task. Always respond in valid JSON."
        if schema_model:
            system_prompt += f"\nYour response must strictly conform to this JSON schema:\n{json.dumps(schema_model.model_json_schema(), indent=2)}"
            
        full_context = context or {}
        if capability in ["coding", "reviewing"]:
            full_context["architecture_specification"] = self._get_architecture_spec()
            
        context_str = json.dumps(full_context)
        
        # 2. Retry Loop & Execution
        last_error = None
        current_task = task
        
        for attempt in range(max_retries):
            try:
                result = self.router.execute(
                    system_prompt=system_prompt,
                    context=context_str,
                    task=current_task,
                    capability=capability,
                    category="builder"
                )
                
                # Telemetry
                self.metrics_logger.info(f"Capability: {capability} | Attempt: {attempt+1} | Latency: {result.latency_sec}s | Tokens: {result.token_count}")
                
                # 3. Parse Response
                try:
                    parsed = json.loads(result.response)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Failed to parse JSON response: {e}. Raw: {result.response[:100]}...")
                
                # 4. Schema Validation
                if schema_model:
                    try:
                        # Validate against the Pydantic model
                        validated = schema_model(**parsed)
                        parsed = validated.model_dump()
                    except Exception as e:
                        raise ValueError(f"Schema validation failed: {e}")
                        
                return {
                    "capability": capability,
                    "response": parsed,
                    "status": "success",
                    "telemetry": {
                        "latency_sec": result.latency_sec,
                        "tokens": result.token_count,
                        "attempts": attempt + 1
                    }
                }
                
            except Exception as e:
                last_error = str(e)
                logger.warning(f"[AIGateway] Attempt {attempt+1} failed: {last_error}")
                # Inject the error into the prompt for the next retry
                current_task = f"{task}\n\nPREVIOUS ERROR: Your last attempt failed with this error. Fix it.\n{last_error}"
                
        logger.error(f"[AIGateway] Failed after {max_retries} attempts. Last error: {last_error}")
        return {"status": "error", "error": last_error}
