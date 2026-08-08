from typing import Dict, Any, Optional
from datetime import datetime
import uuid

from raphael_core.kernel.registry import registry
from .state_models import PendingMission, WorkflowExecution, ExecutionContext
from .repositories import MissionRepository, ExecutionRepository, JsonMissionRepository, JsonExecutionRepository

class ExecutionManager:
    """
    The central orchestrator for all actions in Raphael OS.
    Owns the execution lifecycle, state transitions, and event broadcasting.
    """
    def __init__(
        self,
        mission_repo: Optional[MissionRepository] = None,
        execution_repo: Optional[ExecutionRepository] = None
    ):
        self.missions = mission_repo or JsonMissionRepository()
        self.executions = execution_repo or JsonExecutionRepository()

    def _generate_id(self, prefix: str) -> str:
        date_str = datetime.utcnow().strftime("%Y%m%d")
        unique_suffix = uuid.uuid4().hex[:4].upper()
        return f"{prefix}-{date_str}-{unique_suffix}"
        
    def _generate_correlation_id(self) -> str:
        return f"CORR-{uuid.uuid4().hex[:6].upper()}"

    def _publish_event(self, event_type: str, mission_id: str, execution_id: Optional[str], correlation_id: str, details: Dict[str, Any]):
        from raphael_core.kernel.event_bus import emit
        payload = {
            "mission_id": mission_id,
            "execution_id": execution_id,
            "correlation_id": correlation_id,
            **details
        }
        emit(event_type, "execution_manager", payload)
    def register_proposal(self, proposal: Any, source: str, session_id: str, initiated_by: str = "Aaron") -> PendingMission:
        """Creates a PENDING_APPROVAL mission from a proposal."""
        mission_id = self._generate_id("M")
        
        # We assume proposal is a MissionProposal object; convert to dict if needed
        proposal_dict = proposal.to_dict() if hasattr(proposal, "to_dict") else proposal
        workflow_id = proposal_dict.get("workflow_id")
        
        context = ExecutionContext(
            source=source,
            session_id=session_id,
            initiated_by=initiated_by,
            workflow_id=workflow_id
        )
        
        mission = PendingMission(mission_id=mission_id, proposal=proposal_dict, context=context)
        self.missions.save(mission)
        
        self._publish_event("MISSION_CREATED", mission_id, None, self._generate_correlation_id(), {"status": "PENDING_APPROVAL"})
        return mission

    def approve_latest(self, session_id: str) -> Optional[WorkflowExecution]:
        """Approves the most recent pending mission for the given session."""
        mission = self.missions.get_latest_for_session(session_id)
        if not mission:
            return None
            
        return self.approve_mission(mission.mission_id)

    def approve_mission(self, mission_id: str) -> WorkflowExecution:
        """State Machine: PENDING_APPROVAL -> APPROVED -> (Create Execution) -> QUEUED"""
        mission = self.missions.get(mission_id)
        if not mission:
            raise ValueError(f"Mission {mission_id} not found.")
            
        if mission.status != "PENDING_APPROVAL":
            raise ValueError(f"Cannot approve mission {mission_id} from state {mission.status}.")
            
        # Transition Mission State
        mission.status = "APPROVED"
        self.missions.save(mission)
        
        # Create Execution State
        execution_id = self._generate_id("EX")
        correlation_id = self._generate_correlation_id()
        
        execution = WorkflowExecution(
            execution_id=execution_id,
            mission_id=mission.mission_id,
            correlation_id=correlation_id,
            workflow_id=mission.context.workflow_id or "unknown",
            context=mission.context,
            status="QUEUED"
        )
        self.executions.save(execution)
        
        self._publish_event("MISSION_APPROVED", mission_id, execution_id, correlation_id, {"workflow_id": execution.workflow_id})
        
        # Immediately kick off the workflow via EventBus or CommandBus. 
        # For Phase 9, we update status to RUNNING locally to simulate the orchestrator starting it.
        # In the future, a WorkflowRunner component listens to MISSION_APPROVED or we call it directly here.
        self._start_execution(execution)
        
        return execution

    def reject_latest(self, session_id: str) -> Optional[PendingMission]:
        mission = self.missions.get_latest_for_session(session_id)
        if not mission:
            return None
        return self.reject_mission(mission.mission_id)

    def reject_mission(self, mission_id: str) -> PendingMission:
        mission = self.missions.get(mission_id)
        if not mission:
            raise ValueError(f"Mission {mission_id} not found.")
            
        if mission.status != "PENDING_APPROVAL":
            raise ValueError(f"Cannot reject mission {mission_id} from state {mission.status}.")
            
        mission.status = "REJECTED"
        self.missions.save(mission)
        return mission

    def _start_execution(self, execution: WorkflowExecution) -> None:
        """State Machine: QUEUED -> RUNNING"""
        if execution.status != "QUEUED":
            raise ValueError(f"Cannot start execution {execution.execution_id} from state {execution.status}.")
            
        execution.status = "RUNNING"
        execution.updated_at = datetime.utcnow().isoformat() + "Z"
        self.executions.save(execution)
        
        self._publish_event("WORKFLOW_STARTED", execution.mission_id, execution.execution_id, execution.correlation_id, {"workflow_id": execution.workflow_id})
        
        # Trigger capability asynchronously
        import threading
        from raphael_core.kernel.services.capability_service import CapabilityService
        
        def run_capability():
            try:
                # Execution context can be passed as context
                CapabilityService.execute(
                    capability_id=execution.workflow_id,
                    context=execution.context.to_dict() if hasattr(execution.context, "to_dict") else vars(execution.context),
                    execution_id=execution.execution_id
                )
            except Exception as e:
                import logging
                logging.getLogger("operator.execution_manager").error(f"Execution failed: {str(e)}")
                
        threading.Thread(target=run_capability, daemon=True).start()

    def get_latest_execution(self, session_id: str) -> Optional[WorkflowExecution]:
        return self.executions.get_latest_for_session(session_id)

    def get_execution(self, execution_id: str) -> Optional[WorkflowExecution]:
        return self.executions.get(execution_id)

execution_manager = ExecutionManager()
