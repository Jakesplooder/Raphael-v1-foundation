import logging
from typing import Dict, Any, List
from ...models.agent import AgentDefinition

logger = logging.getLogger("rrk.providers.agents.tools")

class PermissionDeniedError(Exception):
    pass

class PermissionService:
    """Gates Agent access to tools based on their Identity and capabilities."""
    
    def check_permission(self, agent: AgentDefinition, tool_name: str) -> bool:
        # Strict checking based on Capabilities
        if tool_name not in agent.capabilities:
            logger.warning(f"Permission denied: Agent {agent.name} lacks capability '{tool_name}'")
            return False
            
        # Example domain checking based on Permissions
        if tool_name == "finance_transfer" and "finance" not in agent.permissions:
            logger.warning(f"Permission denied: Agent {agent.name} lacks permission 'finance'")
            return False
            
        return True


class ToolProvider:
    """
    Translates validated tool requests into Workflow Intents.
    Does NOT execute tools directly!
    """
    def __init__(self):
        self.permission_service = PermissionService()
        
    def request_tool(self, agent: AgentDefinition, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates the request and returns a WORKFLOW_REQUEST dictionary intent.
        Raises PermissionDeniedError if the agent is unauthorized.
        """
        if not self.permission_service.check_permission(agent, tool_name):
            raise PermissionDeniedError(f"Agent {agent.name} is not permitted to use tool {tool_name}")
            
        # Returns a Workflow Intent, NOT execution result
        return {
            "type": "WORKFLOW_REQUEST",
            "workflow": {
                "name": f"Agent Tool Request: {tool_name}",
                "steps": [
                    {
                        "name": f"Execute {tool_name}",
                        "action": tool_name,
                        "parameters": parameters
                    }
                ]
            }
        }
