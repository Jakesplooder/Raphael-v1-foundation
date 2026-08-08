import json
import logging
from typing import Dict, Any
from raphael_core.llm.router import LLMRouter
from .capability_aggregator import capability_aggregator
from .models import MissionProposal

logger = logging.getLogger("operator.planner")

class CommandPlanner:
    def __init__(self):
        self.llm = LLMRouter()
        
    def generate_plan(self, prompt: str, intent: str) -> MissionProposal:
        """
        Uses Gemini to generate a structured MissionProposal based on the user's intent.
        """
        capabilities = capability_aggregator.load()
        
        system_prompt = f"""You are the RAPHAEL EXECUTIVE OS Planner.
Your job is to generate a formal Mission Proposal for the user's request.
You must select from ONLY the available workflows and agents below. Do NOT invent new workflows.

AVAILABLE CAPABILITIES:
{json.dumps(capabilities, indent=2)}

Detected Intent: {intent}

Respond EXACTLY in this JSON format:
{{
  "objective": "A one sentence clear objective",
  "workflow_id": "The exact name of the selected workflow from capabilities, or null",
  "workflow_name": "Friendly name of the workflow, or null",
  "agents": ["Agent1", "Agent2"],
  "tools": ["Tool1"],
  "capabilities_used": ["Domain/Capability"],
  "simulation": {{
    "cost": "$X",
    "runtime": "X minutes"
  }},
  "risk_level": "Low/Medium/High",
  "confidence_score": 0.95,
  "reasoning_summary": "Why this workflow was chosen.",
  "requires_approval": true
}}
"""
        try:
            result = self.llm.execute(
                system_prompt=system_prompt,
                context="",
                task=prompt,
                capability="planning" # Routes to Gemini
            )
            
            text = result.response.strip()
            if text.startswith("```json"):
                text = text[7:-3].strip()
            
            plan_data = json.loads(text)
            
            return MissionProposal(
                intent=intent,
                objective=plan_data.get("objective", "Unknown objective"),
                workflow_id=plan_data.get("workflow_id"),
                workflow_name=plan_data.get("workflow_name"),
                agents=plan_data.get("agents", []),
                tools=plan_data.get("tools", []),
                capabilities_used=plan_data.get("capabilities_used", []),
                simulation=plan_data.get("simulation", {"cost": "$0", "runtime": "Unknown"}),
                risk_level=plan_data.get("risk_level", "Unknown"),
                confidence_score=plan_data.get("confidence_score", 0.0),
                reasoning_summary=plan_data.get("reasoning_summary", ""),
                requires_approval=plan_data.get("requires_approval", True)
            )
            
        except Exception as e:
            logger.error(f"Planner failed: {e}")
            return MissionProposal(
                intent=intent,
                objective=f"Error generating plan: {e}",
                requires_approval=True,
                status="Error"
            )

planner = CommandPlanner()
