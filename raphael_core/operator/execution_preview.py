from typing import Dict, Any
from .models import MissionProposal

class ExecutionPreview:
    """
    Formats the MissionProposal into a readable card for the dashboard chat.
    Also handles OS Mode and conversational responses.
    """
    
    def format_proposal_card(self, proposal: MissionProposal) -> str:
        lines = []
        
        # Header block based on intent
        intent_display = proposal.intent.replace('_', ' ').upper()
        if intent_display in ["CONVERSATION", "RESEARCH"]:
            lines.append(f"**Mode: {intent_display.title()}**")
            lines.append("")
            lines.append("No execution required.")
            if proposal.reasoning_summary:
                lines.append("")
                lines.append(proposal.reasoning_summary)
            return "\n".join(lines)
            
        lines.append(f"**{intent_display} REQUEST DETECTED**")
        lines.append("")
        
        if proposal.workflow_name:
            lines.append(f"**Workflow:** {proposal.workflow_name}")
            lines.append("")
            
        if proposal.agents or proposal.tools or proposal.capabilities_used:
            lines.append("**Using:**")
            for cap in proposal.capabilities_used:
                lines.append(f"✓ {cap}")
            for agent in proposal.agents:
                lines.append(f"✓ {agent}")
            for tool in proposal.tools:
                lines.append(f"✓ {tool}")
            lines.append("")
            
        if proposal.simulation and isinstance(proposal.simulation, dict):
            lines.append("**Simulation:**")
            if "cost" in proposal.simulation:
                lines.append(f"- Cost: {proposal.simulation['cost']}")
            if "runtime" in proposal.simulation:
                lines.append(f"- Runtime: {proposal.simulation['runtime']}")
            lines.append(f"- Risk: {proposal.risk_level}")
            lines.append("")
            
        if proposal.requires_approval:
            lines.append("**Awaiting Approval**")
            
        return "\n".join(lines)

    def format_os_indicator(self) -> str:
        """
        Generates the RAPHAEL EXECUTIVE OS status block.
        Normally this could be dynamic, but for UI rendering we provide the string template.
        """
        # In a real UI this might be HTML or Markdown table, we'll do Markdown formatting.
        return """
**RAPHAEL EXECUTIVE OS**
Business: ✓ Commerce Council, ✓ Agency Council, ✓ Creator Council
Creation: ✓ Video Generation, ✓ POD Studio, ✓ Asset Library
Automation: ✓ n8n, ✓ Workflow Studio
Engineering: ✓ Builder, ✓ Developer Agents
Intelligence: ✓ Memory, ✓ World Model, ✓ Simulation
"""

execution_preview = ExecutionPreview()
