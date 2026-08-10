import logging
from typing import Dict, Any
from .agent_state import AgentState

logger = logging.getLogger("rrk.agents.runtime")

class AgentRuntime:
    """
    The universal Agent Kernel.
    Drives all agents through the standard lifecycle:
    Reason -> Plan -> Delegate -> Execute -> Review -> Learn
    """
    def __init__(self, event_bus, workflow_manager):
        self.event_bus = event_bus
        self.workflow_manager = workflow_manager

    async def execute_task(self, agent, task: str) -> Dict[str, Any]:
        try:
            logger.info(f"[{agent.name}] Starting lifecycle for task: {task}")
            
            agent.transition_to(AgentState.REASONING)
            intent = await agent.reason_about(task)
            
            agent.transition_to(AgentState.PLANNING)
            plan = await agent.create_plan(intent)
            
            agent.transition_to(AgentState.DELEGATING)
            # Hook for Council Review (Epic D11)
            approved = await self._propose_action(agent, plan)
            if not approved:
                agent.transition_to(AgentState.FAILED)
                return {"status": "rejected_by_council"}
                
            agent.transition_to(AgentState.EXECUTING)
            workflow_id = await self._dispatch_to_workflow(agent, plan)
            
            agent.transition_to(AgentState.REVIEWING)
            review = await agent.review_outcome(workflow_id)
            
            agent.transition_to(AgentState.LEARNING)
            await agent.extract_lessons(review)
            
            agent.transition_to(AgentState.COMPLETE)
            return {"status": "success", "review": review}
            
        except Exception as e:
            logger.error(f"[{agent.name}] Execution failed: {str(e)}")
            agent.transition_to(AgentState.FAILED)
            # In a real system, the agent would catch this, query AgentMemory for recovery strategies, and retry
            recovery_plan = await agent.recover_from_failure(e)
            if recovery_plan:
                return await self.execute_task(agent, recovery_plan)
            return {"status": "failed", "error": str(e)}

    async def _propose_action(self, agent, plan: Dict[str, Any]) -> bool:
        from ...kernel.interfaces import Event, EventType
        logger.info(f"[{agent.name}] Emitting AGENT_ACTION_PROPOSED")
        # In D11, this will block and await COUNCIL_REVIEW_REQUESTED -> APPROVED/REJECTED
        if self.event_bus:
            self.event_bus.publish(Event(
                source=agent.name,
                type=EventType.AGENT_ACTION_PROPOSED,
                payload={"plan": plan}
            ))
        return True
        
    async def _dispatch_to_workflow(self, agent, plan: Dict[str, Any]) -> str:
        # Pass to WorkflowPlanManager
        logger.info(f"[{agent.name}] Dispatching to WorkflowPlanManager: {plan.get('name', 'Untitled')}")
        import uuid
        return f"WF-{uuid.uuid4().hex[:8].upper()}"
