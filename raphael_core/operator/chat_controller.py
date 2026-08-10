from typing import Dict, Any
import logging
import os
import json
from .intent_router import intent_router, IntentClass
from .planner import planner
from .execution_preview import execution_preview
from .session_manager import session_manager
from .workflow_matcher import workflow_matcher
from .capability_aggregator import capability_aggregator

logger = logging.getLogger("operator.chat_controller")

class ChatController:
    """
    Main entry point for Operator Chat.
    Handles the flow: Intent Router -> Capability Match -> Mission Planner -> MissionProposal -> Approval -> Command Bus
    """
    def __init__(self):
        self.debug_mode = os.environ.get("RAPHAEL_ROUTING_DEBUG", "").lower() == "true"

    def _debug_log(self, title: str, details: Dict[str, Any]):
        if self.debug_mode:
            print(f"\n[CHAT ROUTER] {title}")
            for k, v in details.items():
                print(f"{k}: {v}")
            print()

    def process_message(self, session_id: str, message: str) -> Dict[str, Any]:
        """
        Processes a chat message and returns the response payload for the UI.
        """
        pending_plan = session_manager.get_pending_approval(session_id)
        
        # Route intent
        intent_type, route_info = intent_router.route(message)
        
        self._debug_log("Routing", {
            "Input": message,
            "Intent": intent_type.value,
            "Source": route_info.get("source", "heuristic")
        })
        
        # 1. Approval Logic
        if pending_plan:
            if intent_type == IntentClass.APPROVAL:
                session_manager.clear_pending_approval(session_id)
                session_manager.record_proposal_outcome(pending_plan, "Accepted")
                return {
                    "response": f"Executing approved plan for {pending_plan.get('intent', 'task')}...",
                    "intent": "execute",
                    "command": pending_plan.get("workflow_id", ""),
                    "status": "Executing",
                    "confirmation_required": False,
                    "awaiting_confirmation": False
                }
            elif intent_type == IntentClass.REJECTION:
                session_manager.clear_pending_approval(session_id)
                session_manager.record_proposal_outcome(pending_plan, "Rejected")
                return {
                    "response": "Execution cancelled. Proposal rejected.",
                    "intent": "cancel",
                    "command": "",
                    "status": "Cancelled",
                    "confirmation_required": False,
                    "awaiting_confirmation": False
                }
            else:
                session_manager.clear_pending_approval(session_id)
                session_manager.record_proposal_outcome(pending_plan, "Ignored/Modified")

        # 2. Hard capability intercepts
        if intent_type == IntentClass.CAPABILITY_QUERY:
            return {
                "response": execution_preview.format_os_indicator(),
                "intent": "capability_query",
                "command": "",
                "status": "Processed",
                "confirmation_required": False,
                "awaiting_confirmation": False
            }
            
        if intent_type == IntentClass.WORKFLOW_QUERY:
            manifest = capability_aggregator.load()
            lines = ["**Available Workflows**", ""]
            for wf in manifest.get("workflows", []):
                lines.append(f"- **{wf.get('name')}** ({wf.get('domain')})")
            return {
                "response": "\n".join(lines),
                "intent": "workflow_query",
                "command": "",
                "status": "Processed",
                "confirmation_required": False,
                "awaiting_confirmation": False
            }

        # 3. Handle Creation / Business with Workflow Matcher
        if intent_type in (IntentClass.CREATION, IntentClass.BUSINESS):
            matched_workflow = workflow_matcher.match(message)
            
            if matched_workflow:
                self._debug_log("Workflow Matcher", {
                    "Matched Workflow": matched_workflow.get("id"),
                    "Planner": "enabled"
                })
                
                # We found a workflow, now use planner to generate MissionProposal
                proposal = planner.generate_plan(message, intent_type.value)
                
                # Override the planner's selected workflow just in case it hallucinated
                proposal.workflow_id = matched_workflow["id"]
                proposal.workflow_name = matched_workflow["name"]
                
                if proposal.requires_approval:
                    session_manager.set_pending_approval(session_id, proposal)
                    card = execution_preview.format_proposal_card(proposal)
                    return {
                        "response": card,
                        "intent": proposal.intent,
                        "command": proposal.workflow_id or "",
                        "status": "Awaiting Approval",
                        "confirmation_required": True,
                        "awaiting_confirmation": True
                    }
                else:
                    card = execution_preview.format_proposal_card(proposal)
                    return {
                        "response": card,
                        "intent": proposal.intent,
                        "command": proposal.workflow_id or "",
                        "status": "Processed",
                        "confirmation_required": False,
                        "awaiting_confirmation": False
                    }
            else:
                self._debug_log("Workflow Matcher", {
                    "Matched Workflow": "None",
                    "Status": "Unknown Creation"
                })
                # Unknown creation fallback
                return {
                    "response": "No matching workflow found.\n\nAvailable creation systems:\n- Video\n- POD\n- Websites\n- Commerce\n\nWould you like to create a new workflow proposal?",
                    "intent": intent_type.value,
                    "command": "",
                    "status": "Refused",
                    "confirmation_required": False,
                    "awaiting_confirmation": False
                }

        # 3.5 Handlers for newly added intents
        if intent_type == IntentClass.GENERATE_ASSET:
            return {
                "response": "Generation started — I'll show progress in Active Jobs.",
                "intent": "execute",
                "command": "generate_asset",
                "status": "Executing",
                "confirmation_required": False,
                "awaiting_confirmation": False
            }

        # 4. Normal Conversation or other fallback
        self._debug_log("Conversation Fallback", {
            "Intent": intent_type.value,
            "LLM": "allowed"
        })
        return {
            "response": "", # Signify to caller to use legacy LLM
            "intent": intent_type.value,
            "command": "",
            "status": "Routed to LLM",
            "confirmation_required": False,
            "awaiting_confirmation": False
        }

chat_controller = ChatController()
