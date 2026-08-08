"""
RRK Workflow Engine.

The generic, reusable orchestrator that powers all Raphael autonomous workflows.
Concrete workflows (PodWorkflow, AppWorkflow, WebsiteWorkflow, ...) subclass
RRKWorkflow and declare their states + action methods.  The engine handles:

  - Sequential state execution with rewind/retry
  - Exception → WorkflowEvent conversion via RecoveryRegistry
  - Prompt rewriting via WorkflowMemory
  - Telemetry emission for Command Center observability
  - Dashboard-friendly progress reporting (job_id, status, progress, message)

Architecture:

  Dashboard Chat
       │
    WebSocket
       │
   Job Manager
       │
  WorkflowEngine.run(workflow)
       │
  ┌────┴────┐
  │ State 1 │──▶ State 2 ──▶ ... ──▶ State N ──▶ COMPLETE
  └─────────┘
       │ (on failure)
       ▼
  RecoveryRegistry.classify(exc)
       │
       ▼
  WorkflowEvent(QUALITY_FAILURE, ...)
       │
       ▼
  PromptRewriter.rewrite(prompt)
       │
       ▼
  REWIND → State K
"""

import abc
import logging
import time
import uuid
from typing import Any, Callable, Dict, List, Optional, Tuple

from .workflow_state import (
    RecoveryStrategy,
    StepDefinition,
    WorkflowEvent,
    WorkflowExecution,
    WorkflowPhase,
)
from .workflow_recovery import (
    PromptRewriter,
    recovery_registry,
    workflow_memory,
    WorkflowMemoryEntry,
)

)

from raphael_core.kernel.registry import registry
from raphael_core.kernel.interfaces import Event, EventType

logger = logging.getLogger("rrk.workflow.engine")


# ---------------------------------------------------------------------------
# Abstract base for all concrete workflows
# ---------------------------------------------------------------------------

class RRKWorkflow(abc.ABC):
    """
    Base class for all Raphael autonomous workflows.

    Subclasses must implement:
      - workflow_type   (property)  e.g. "pod_generation"
      - steps           (property)  list of StepDefinition
      - execute_step    (method)    run a single step by name

    Subclasses may override:
      - on_recovery     hook called after a recovery event is classified
      - on_complete     hook called when the workflow finishes successfully
    """

    @property
    @abc.abstractmethod
    def workflow_type(self) -> str:
        """Unique identifier for this workflow type."""
        ...

    @property
    @abc.abstractmethod
    def steps(self) -> List[StepDefinition]:
        """Ordered list of states in this workflow's pipeline."""
        ...

    @abc.abstractmethod
    def execute_step(
        self, step_name: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a single step.  Must return a dict with at least {"status": "success"}.
        Raise an exception on failure — the engine will classify it.
        """
        ...

    def on_recovery(
        self, event: WorkflowEvent, context: Dict[str, Any]
    ) -> None:
        """
        Hook called when a recovery event is classified.
        Subclasses can use this to modify context (e.g. rewrite prompts).
        """
        pass

    def on_complete(self, context: Dict[str, Any]) -> None:
        """Hook called on successful workflow completion."""
        pass


# ---------------------------------------------------------------------------
# Telemetry callback type
# ---------------------------------------------------------------------------

TelemetryCallback = Callable[[Dict[str, Any]], None]


# ---------------------------------------------------------------------------
# The engine itself
# ---------------------------------------------------------------------------

class WorkflowEngine:
    """
    Generic FSM orchestrator.

    Usage:
        engine = WorkflowEngine()
        result = engine.run(my_workflow, initial_context={...})
    """

    def __init__(
        self,
        telemetry_callback: Optional[TelemetryCallback] = None,
    ):
        self._telemetry_callback = telemetry_callback

    def _emit_telemetry(self, execution: WorkflowExecution, step_name: str, extra: Dict[str, Any] = None) -> None:
        """Emit a telemetry event for Command Center observability."""
        steps = execution.context.get("_step_definitions", [])
        total = len(steps) if steps else 1
        current = execution.current_step
        progress = int((current / total) * 100) if total > 0 else 0

        payload = {
            "workflow": execution.workflow_type,
            "execution_id": execution.execution_id,
            "state": step_name,
            "phase": execution.phase.value,
            "attempt": execution.step_retries.get(step_name, 0) + 1,
            "max_attempts": 3,
            "total_rewinds": execution.total_rewinds,
            "progress": progress,
            "timestamp": time.time(),
        }
        if extra:
            payload.update(extra)

        logger.info(
            f"[TELEMETRY] workflow={execution.workflow_type} "
            f"state={step_name} phase={execution.phase.value} "
            f"progress={progress}%"
        )

        if self._telemetry_callback:
            try:
                self._telemetry_callback(payload)
            except Exception as e:
                logger.warning(f"Telemetry callback failed: {e}")

    def run(
        self,
        workflow: RRKWorkflow,
        initial_context: Optional[Dict[str, Any]] = None,
    ) -> WorkflowExecution:
        """
        Execute a workflow from start to finish.

        Returns a WorkflowExecution record with phase=COMPLETED or FAILED.
        The Dashboard only needs to poll this record for status updates.
        """
        steps = workflow.steps
        execution = WorkflowExecution(
            workflow_type=workflow.workflow_type,
            phase=WorkflowPhase.RUNNING,
            context=initial_context or {},
        )
        execution.context["_step_definitions"] = [s.name for s in steps]

        logger.info(
            f"\n{'=' * 50}\n"
            f"  STARTING WORKFLOW: {workflow.workflow_type.upper()}\n"
            f"  Execution ID: {execution.execution_id}\n"
            f"  Steps: {[s.name for s in steps]}\n"
            f"{'=' * 50}"
        )

        while execution.current_step < len(steps):
            step = steps[execution.current_step]

            self._emit_telemetry(execution, step.name)

            logger.info(f"\n[ENGINE] Executing: {step.display_name or step.name}")

            event_bus = registry.get_service("EventBus")
            if event_bus:
                # Fire and forget publishing since we're not inside an async loop here
                import asyncio
                payload = {
                    "step_name": step.name,
                    "workflow_type": workflow.workflow_type
                }
                started_event = Event(
                    source="WorkflowEngine",
                    type=EventType.NODE_STARTED,
                    execution_id=execution.execution_id,
                    node_id=step.name,
                    payload=payload
                )
                try:
                    loop = asyncio.get_running_loop()
                    loop.create_task(event_bus.publish(started_event))
                except RuntimeError:
                    asyncio.run(event_bus.publish(started_event))
                except Exception:
                    pass

            try:
                result = workflow.execute_step(step.name, execution.context)
                logger.info(
                    f"[ENGINE] [OK] {step.name} → {result.get('state', 'success')}"
                )
                
                if event_bus:
                    try:
                        import asyncio
                        completed_event = Event(
                            source="WorkflowEngine",
                            type=EventType.NODE_COMPLETED,
                            execution_id=execution.execution_id,
                            node_id=step.name,
                            payload=result
                        )
                        try:
                            loop = asyncio.get_running_loop()
                            loop.create_task(event_bus.publish(completed_event))
                        except RuntimeError:
                            asyncio.run(event_bus.publish(completed_event))
                        except Exception:
                            pass
                    except Exception:
                        pass
                        
                execution.current_step += 1

            except Exception as exc:
                logger.warning(f"[ENGINE] [FAIL] {step.name} → {exc}")

                # --- Convert exception to a structured recovery event ---
                event = recovery_registry.classify(workflow.workflow_type, exc)

                if event is None:
                    # No recovery rule registered — unrecoverable
                    logger.error(
                        f"[ENGINE] [HALT] No recovery rule for "
                        f"{type(exc).__name__} in {workflow.workflow_type}"
                    )
                    execution.phase = WorkflowPhase.FAILED
                    execution.result = f"Unrecoverable: {exc}"
                    execution.completed_at = time.time()
                    self._emit_telemetry(
                        execution, step.name,
                        extra={"recovery": "none", "error": str(exc)},
                    )
                    return execution

                execution.events.append(event)
                execution.phase = WorkflowPhase.RECOVERING

                self._emit_telemetry(
                    execution, step.name,
                    extra={
                        "recovery": event.recovery.value,
                        "failure_type": event.event_type,
                        "detail": event.detail,
                    },
                )

                # --- Check retry limits ---
                retries = execution.step_retries.get(step.name, 0)
                if retries >= step.max_retries:
                    logger.error(
                        f"[ENGINE] [HALT] Max retries ({step.max_retries}) "
                        f"exhausted for {step.name}"
                    )
                    execution.phase = WorkflowPhase.FAILED
                    execution.result = (
                        f"Max retries exhausted for {step.name}: {exc}"
                    )
                    execution.completed_at = time.time()

                    # Record failure in memory
                    workflow_memory.record(WorkflowMemoryEntry(
                        workflow_type=workflow.workflow_type,
                        failure_source=event.source,
                        failure_type=type(exc).__name__,
                        original_context={
                            k: v for k, v in execution.context.items()
                            if not k.startswith("_")
                        },
                        resolution="",
                        recovery_strategy_used=event.recovery,
                        success=False,
                    ))
                    return execution

                if execution.total_rewinds >= execution.max_total_rewinds:
                    logger.error(
                        f"[ENGINE] [HALT] Max total rewinds "
                        f"({execution.max_total_rewinds}) exhausted"
                    )
                    execution.phase = WorkflowPhase.FAILED
                    execution.result = (
                        f"Max total rewinds exhausted: {exc}"
                    )
                    execution.completed_at = time.time()
                    return execution

                # --- Apply recovery strategy ---
                execution.step_retries[step.name] = retries + 1
                execution.total_rewinds += 1

                # Let the workflow react to the recovery event
                workflow.on_recovery(event, execution.context)

                # If strategy is MODIFY_PROMPT, rewrite the prompt in context
                if event.recovery == RecoveryStrategy.MODIFY_PROMPT:
                    original_prompt = execution.context.get("generation_prompt", "")
                    rewritten = PromptRewriter.rewrite(
                        original_prompt,
                        type(exc).__name__,
                        workflow_memory,
                        workflow.workflow_type,
                    )
                    execution.context["generation_prompt"] = rewritten
                    logger.info("[ENGINE] [PROMPT_REWRITE] Applied learned mitigations")

                # Rewind to the target step
                target_name = step.rewind_target or step.name
                target_index = next(
                    (i for i, s in enumerate(steps) if s.name == target_name),
                    execution.current_step,
                )

                logger.info(
                    f"[ENGINE] [REWIND] {step.name} → {target_name} "
                    f"(attempt {retries + 2}/{step.max_retries + 1}, "
                    f"total rewinds: {execution.total_rewinds}/{execution.max_total_rewinds})"
                )

                execution.current_step = target_index
                execution.phase = WorkflowPhase.RUNNING

        # --- Success ---
        execution.phase = WorkflowPhase.COMPLETED
        execution.completed_at = time.time()
        execution.result = "Workflow completed successfully."

        workflow.on_complete(execution.context)

        logger.info(
            f"\n[ENGINE] [SUCCESS] {workflow.workflow_type} completed in "
            f"{execution.completed_at - execution.created_at:.1f}s "
            f"({execution.total_rewinds} rewind(s))"
        )

        self._emit_telemetry(
            execution, "COMPLETE",
            extra={"total_rewinds": execution.total_rewinds},
        )

        return execution
