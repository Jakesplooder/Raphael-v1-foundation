"""
RRK Workflow Engine Tests.

Test 1: Failure recovery (mock typography error -> FSM catches -> retry -> success)
Test 2: Max retry exhaustion (3 failures -> WorkflowFailed)
Test 3: Unrecoverable failure halts immediately
Test 4: Telemetry emission during workflow execution
Test 5: Multiple recovery then success
Test 6: Clean workflow with zero rewinds
"""

import sys
import os
import unittest
from typing import Any, Dict, List
from unittest.mock import MagicMock

# Ensure project root is on sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from raphael_core.kernel.services.execution.workflows import (
    RRKWorkflow,
    WorkflowEngine,
    WorkflowPhase,
    StepDefinition,
    RecoveryRule,
    RecoverySeverity,
    RecoveryStrategy,
    WorkflowEvent,
    recovery_registry,
    workflow_memory,
)


# ---------------------------------------------------------------------------
# Mock exceptions that simulate POD generation failures
# ---------------------------------------------------------------------------

class MockTypographyContaminationError(RuntimeError):
    """Simulates TypographyContaminationError from legacy.py."""
    pass


class MockUnrecoverableError(Exception):
    """An error with no registered recovery rule."""
    pass


# ---------------------------------------------------------------------------
# Test workflow that simulates the POD generation pipeline
# ---------------------------------------------------------------------------

class TestPodWorkflow(RRKWorkflow):
    """
    A test workflow with controllable failure injection.
    Simulates the POD pipeline with a quality_check step that can fail
    a configurable number of times before succeeding.
    """

    def __init__(self, fail_count: int = 1, unrecoverable: bool = False):
        self._fail_count = fail_count
        self._unrecoverable = unrecoverable
        self._attempt = 0

    @property
    def workflow_type(self) -> str:
        return "test_pod_generation"

    @property
    def steps(self) -> List[StepDefinition]:
        return [
            StepDefinition(name="init", display_name="Initialize"),
            StepDefinition(
                name="image_generation",
                display_name="Image Generation",
                rewind_target="image_generation",
                max_retries=3,
            ),
            StepDefinition(
                name="quality_check",
                display_name="Quality Check",
                rewind_target="image_generation",
                max_retries=3,
            ),
            StepDefinition(name="finalize", display_name="Finalize"),
        ]

    def execute_step(self, step_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        if step_name == "init":
            return {"status": "success", "state": "INITIALIZED"}

        elif step_name == "image_generation":
            context["images_generated"] = True
            return {"status": "success", "state": "IMAGES_GENERATED"}

        elif step_name == "quality_check":
            self._attempt += 1
            if self._attempt <= self._fail_count:
                if self._unrecoverable:
                    raise MockUnrecoverableError(
                        f"Unrecoverable failure on attempt {self._attempt}"
                    )
                raise MockTypographyContaminationError(
                    f"Typography contamination detected on attempt {self._attempt}. "
                    f"Rejected image(s): test_00001.png (74.04%)"
                )
            return {"status": "success", "state": "QUALITY_PASSED"}

        elif step_name == "finalize":
            return {"status": "success", "state": "FINALIZED"}

        raise NotImplementedError(f"Unknown step: {step_name}")


# ---------------------------------------------------------------------------
# Register recovery rules for the test workflow
# ---------------------------------------------------------------------------

recovery_registry.register(
    "test_pod_generation",
    RecoveryRule(
        exception_type=MockTypographyContaminationError,
        event_type="QUALITY_FAILURE",
        source="typography_scan",
        severity=RecoverySeverity.MEDIUM,
        strategy=RecoveryStrategy.MODIFY_PROMPT,
    ),
)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestWorkflowEngine(unittest.TestCase):

    def test_1_failure_recovery(self):
        """
        Test 1: Mock provider raises TypographyContaminationError on first
        attempt. FSM catches it, classifies as QUALITY_FAILURE, rewinds to
        image_generation, and succeeds on second attempt.
        """
        workflow = TestPodWorkflow(fail_count=1)
        engine = WorkflowEngine()

        result = engine.run(workflow, initial_context={"request_ref": "PODGEN-TEST-001"})

        self.assertEqual(result.phase, WorkflowPhase.COMPLETED)
        self.assertEqual(result.total_rewinds, 1)
        self.assertEqual(len(result.events), 1)

        event = result.events[0]
        self.assertEqual(event.event_type, "QUALITY_FAILURE")
        self.assertEqual(event.source, "typography_scan")
        self.assertEqual(event.recovery, RecoveryStrategy.MODIFY_PROMPT)

        print("\n[PASS] Test 1: Failure recovery works")
        print(f"   Rewinds: {result.total_rewinds}")
        print(f"   Recovery event: {event.event_type} -> {event.recovery.value}")
        print(f"   Result: {result.result}")

    def test_2_max_retry_exhaustion(self):
        """
        Test 2: Mock provider fails on every attempt (fail_count=10).
        FSM exhausts max retries (3) and transitions to FAILED.
        The engine records the failing event before checking the limit,
        so we expect max_retries + 1 = 4 events total (3 rewinds + 1 final halt).
        """
        workflow = TestPodWorkflow(fail_count=10)
        engine = WorkflowEngine()

        result = engine.run(workflow, initial_context={"request_ref": "PODGEN-TEST-002"})

        self.assertEqual(result.phase, WorkflowPhase.FAILED)
        self.assertIn("Max retries exhausted", result.result)
        # 3 successful rewinds, then the 4th failure triggers the halt
        self.assertGreaterEqual(result.total_rewinds, 3)

        print("\n[PASS] Test 2: Max retry exhaustion works")
        print(f"   Rewinds: {result.total_rewinds}")
        print(f"   Result: {result.result}")
        print(f"   Events: {len(result.events)}")

    def test_3_unrecoverable_failure(self):
        """
        Test 3: An exception with no registered recovery rule is raised.
        FSM immediately halts with FAILED and "Unrecoverable" message.
        """
        workflow = TestPodWorkflow(fail_count=1, unrecoverable=True)
        engine = WorkflowEngine()

        result = engine.run(workflow, initial_context={"request_ref": "PODGEN-TEST-003"})

        self.assertEqual(result.phase, WorkflowPhase.FAILED)
        self.assertIn("Unrecoverable", result.result)
        self.assertEqual(result.total_rewinds, 0)

        print("\n[PASS] Test 3: Unrecoverable failure halts correctly")
        print(f"   Result: {result.result}")

    def test_4_telemetry_emission(self):
        """
        Test 4: Verify that the engine emits telemetry events during execution.
        """
        telemetry_events = []

        def capture_telemetry(payload):
            telemetry_events.append(payload)

        workflow = TestPodWorkflow(fail_count=1)
        engine = WorkflowEngine(telemetry_callback=capture_telemetry)

        result = engine.run(workflow, initial_context={"request_ref": "PODGEN-TEST-004"})

        self.assertEqual(result.phase, WorkflowPhase.COMPLETED)
        self.assertGreater(len(telemetry_events), 0)

        # Check that telemetry contains expected fields
        for event in telemetry_events:
            self.assertIn("workflow", event)
            self.assertIn("state", event)
            self.assertIn("progress", event)
            self.assertEqual(event["workflow"], "test_pod_generation")

        # Check that recovery telemetry was emitted
        recovery_events = [e for e in telemetry_events if "recovery" in e]
        self.assertGreater(len(recovery_events), 0)
        self.assertEqual(recovery_events[0]["failure_type"], "QUALITY_FAILURE")

        print("\n[PASS] Test 4: Telemetry emission works")
        print(f"   Total telemetry events: {len(telemetry_events)}")
        print(f"   Recovery events: {len(recovery_events)}")

    def test_5_multiple_recovery_then_success(self):
        """
        Test 5: Fail twice, succeed on third attempt.
        Verifies the FSM correctly counts rewinds and continues.
        """
        workflow = TestPodWorkflow(fail_count=2)
        engine = WorkflowEngine()

        result = engine.run(workflow, initial_context={"request_ref": "PODGEN-TEST-005"})

        self.assertEqual(result.phase, WorkflowPhase.COMPLETED)
        self.assertEqual(result.total_rewinds, 2)
        self.assertEqual(len(result.events), 2)

        print("\n[PASS] Test 5: Multiple recovery then success")
        print(f"   Rewinds: {result.total_rewinds}")
        print(f"   Events: {len(result.events)}")

    def test_6_clean_workflow(self):
        """
        Test 6: No failures at all. Workflow completes cleanly with 0 rewinds.
        """
        workflow = TestPodWorkflow(fail_count=0)
        engine = WorkflowEngine()

        result = engine.run(workflow, initial_context={"request_ref": "PODGEN-TEST-006"})

        self.assertEqual(result.phase, WorkflowPhase.COMPLETED)
        self.assertEqual(result.total_rewinds, 0)
        self.assertEqual(len(result.events), 0)
        self.assertIsNotNone(result.completed_at)

        print("\n[PASS] Test 6: Clean workflow with zero rewinds")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  RRK WORKFLOW ENGINE TEST SUITE")
    print("=" * 60)
    unittest.main(verbosity=2)
