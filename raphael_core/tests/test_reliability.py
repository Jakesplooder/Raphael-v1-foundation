import logging
import asyncio
import time
import random
import os
import sys
from typing import Dict, Any

sys.path.insert(0, ".")
from raphael_core.kernel.providers.workflow.automation_provider import AutomationProvider
from raphael_core.kernel.providers.workflow.executor_provider import ExecutorProvider, IDEMPOTENT_ACTIONS
from raphael_core.kernel.models.workflow import WorkflowExecution, WorkflowStep, WorkflowStatus

logger = logging.getLogger("rrk.tests.reliability")
logging.basicConfig(level=logging.INFO)

# Global tracker for mock external API to ensure it wasn't called twice
EXTERNAL_SYSTEM_CALLS = []

class MockAutomationProvider(AutomationProvider):
    @property
    def provider_name(self) -> str:
        return "mock"
        
    async def execute_step(self, action: str, parameters: Dict[str, Any], idempotency_key: str = None) -> Dict[str, Any]:
        # Simulate race condition: hard crash DURING execution
        if parameters.get("simulate_crash_before_return"):
            # We record the external call
            EXTERNAL_SYSTEM_CALLS.append({"action": action, "key": idempotency_key})
            # Then we crash!
            raise SystemExit("Simulated Hard Crash (SIGKILL) right after external execution!")
            
        # Standard execution
        if action in IDEMPOTENT_ACTIONS:
            # Check if our mock external system already saw this key
            for call in EXTERNAL_SYSTEM_CALLS:
                if call["key"] == idempotency_key:
                    # External API respects idempotency. Returns cached success, not an error.
                    return {"status": "success", "action": action, "idempotent_replay": True}
                    
            EXTERNAL_SYSTEM_CALLS.append({"action": action, "key": idempotency_key})
            
        await asyncio.sleep(0.1) # Simulate work
        return {"status": "success", "action": action}


class ReliabilityTestSuite:
    async def run(self):
        print("==========================================")
        print("   STARTING RELIABILITY ACCEPTANCE TEST   ")
        print("==========================================")
        
        # Clear out any previous idempotency db for clean test
        try:
            if os.path.exists(".system_generated/idempotency.db"):
                os.remove(".system_generated/idempotency.db")
        except Exception:
            pass
            
        recovery_pass = await self.test_recovery()
        
        print("\n==========================================")
        print("            RELIABILITY REPORT            ")
        print("==========================================")
        print(f"Recovery Metric      : {'[PASS] (>=80%)' if recovery_pass else '[FAIL] (<80%)'}")
        print("==========================================\n")
        
        return recovery_pass

    async def _run_workflow_with_simulated_crash(self, crash_type: str, crash_step_idx: int) -> bool:
        global EXTERNAL_SYSTEM_CALLS
        EXTERNAL_SYSTEM_CALLS.clear()
        
        steps = [
            WorkflowStep(id="step_1", name="Compile", action="builder.compile", parameters={}),
            WorkflowStep(id="step_2", name="Test", action="builder.test", parameters={}),
            WorkflowStep(id="step_3", name="Publish", action="commerce.publish", parameters={}), # Idempotent action
            WorkflowStep(id="step_4", name="Notify", action="notifications.send", parameters={})
        ]
        
        execution = WorkflowExecution(workflow_id="test_wf_123")
        provider = MockAutomationProvider()
        executor = ExecutorProvider(provider)
        
        # --- PHASE 1: INITIAL RUN (THAT CRASHES) ---
        print(f"  -> Initial run... (Injecting {crash_type} at step {crash_step_idx+1})")
        
        try:
            for idx, step in enumerate(steps):
                if idx == crash_step_idx:
                    if crash_type == "hard_kill_race_condition":
                        step.parameters["simulate_crash_before_return"] = True
                        await executor.execute_step(step, execution)
                    elif crash_type == "clean_kill":
                        raise KeyboardInterrupt("Simulated clean kill mid-workflow")
                
                await executor.execute_step(step, execution)
        except (KeyboardInterrupt, SystemExit) as e:
            print(f"  -> Daemon crashed: {e}")
            
        # --- PHASE 2: DAEMON REBOOT & RESUMPTION ---
        print("  -> Daemon Rebooted. Resuming Workflow...")
        
        # In a real system, the workflow service fetches the execution from DB.
        # We simulate that by just looping over steps that aren't COMPLETED.
        for step in steps:
            if execution.step_executions.get(step.id) != WorkflowStatus.COMPLETED:
                print(f"  -> Resuming at {step.id} ({step.action})...")
                # Ensure the crash flag is removed for the retry
                step.parameters.pop("simulate_crash_before_return", None) 
                
                try:
                    await executor.execute_step(step, execution)
                except Exception as e:
                    print(f"  -> [FAIL] Workflow failed during resumption: {e}")
                    return False
                    
        # Verify no duplicates in the external system mock
        actions = [call["action"] for call in EXTERNAL_SYSTEM_CALLS]
        if actions.count("commerce.publish") > 1:
            print("  -> [FAIL] Duplicate commerce.publish detected!")
            return False
            
        print("  -> [OK] Workflow finished gracefully. No duplicates.")
        return True

    async def test_recovery(self) -> bool:
        print("\n--- Testing Recovery Across Varied Failure Modes ---")
        
        scenarios = [
            ("clean_kill", 0), # Crash at step 1 (early)
            ("clean_kill", 2), # Crash right before commerce.publish (mid)
            ("hard_kill_race_condition", 2), # Crash during commerce.publish, after external execution but before local IdempotencyStore save
            ("clean_kill", 3)  # Crash at step 4 (late)
        ]
        
        # We will run 10 tests total, cycling through the scenarios
        successes = 0
        total_runs = 10
        
        for i in range(1, total_runs + 1):
            scenario = scenarios[i % len(scenarios)]
            print(f"\nRun {i}/{total_runs}: Scenario = {scenario[0]} at step {scenario[1]+1}")
            
            success = await self._run_workflow_with_simulated_crash(scenario[0], scenario[1])
            if success:
                successes += 1
                
        score = (successes / total_runs) * 100
        print(f"\nRecovery Score: {score}%")
        return score >= 80

if __name__ == "__main__":
    asyncio.run(ReliabilityTestSuite().run())
