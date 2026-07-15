import logging
import json
from typing import Dict, Any, Callable
from ..models.agent import AgentInstance, AgentDefinition
from ..providers.agents.llm_provider import LLMProvider
from ..providers.agents.tool_provider import ToolProvider, PermissionDeniedError

logger = logging.getLogger("rrk.services.agent_reasoning")

class AgentReasoningService:
    """The cognitive loop for Agents. Produces Intents, not direct executions."""
    
    def __init__(self, llm_provider: LLMProvider, tool_provider: ToolProvider):
        self.llm = llm_provider
        self.tools = tool_provider
        # Function to emit events, injected by Manager
        self.emit_event: Callable[[str, dict], None] = lambda t, p: None
        
    async def reason_about_goal(self, agent_inst: AgentInstance, agent_def: AgentDefinition, goal: str) -> None:
        """
        Executes a single step of reasoning.
        """
        await self.emit_event("agent_reasoning_started", {
            "agent_id": agent_inst.id,
            "goal": goal
        })
        
        try:
            # 1. Ask LLM for next move
            response = await self.llm.generate_reasoning(
                model_name=agent_def.default_model,
                prompt=goal,
                context=agent_inst.context
            )
            
            # Simple parser for mock implementation
            parsed = json.loads(response)
            
            # 2. If the LLM requests a tool, push through PermissionGate
            if parsed.get("intent") == "tool":
                tool_name = parsed.get("name")
                parameters = parsed.get("parameters", {})
                
                # Check permission and generate Workflow Intent
                workflow_intent = self.tools.request_tool(agent_def, tool_name, parameters)
                
                # Emit Workflow Request explicitly (Contract Rule 1)
                await self.emit_event("agent_workflow_requested", {
                    "agent_id": agent_inst.id,
                    "workflow": workflow_intent["workflow"],
                    "importance": "strategic" if "strategic" in goal else "normal"
                })
                
            # 3. Successful Reasoning Cycle
            await self.emit_event("agent_reasoning_completed", {
                "agent_id": agent_inst.id,
                "result": "Generated workflow intent",
                "importance": "strategic" if "strategic" in goal else "normal"
            })
            
        except PermissionDeniedError as e:
            logger.warning(f"Agent {agent_inst.id} permission denied: {e}")
            await self.emit_event("agent_permission_denied", {
                "agent_id": agent_inst.id,
                "error": str(e)
            })
            await self.emit_event("agent_failed", {
                "agent_id": agent_inst.id,
                "error": str(e),
                "importance": "normal"
            })
            
        except Exception as e:
            logger.error(f"Agent {agent_inst.id} reasoning failed: {e}")
            await self.emit_event("agent_failed", {
                "agent_id": agent_inst.id,
                "error": str(e),
                "importance": "normal"
            })
