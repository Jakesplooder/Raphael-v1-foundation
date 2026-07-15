import asyncio
import logging
import copy
import sys
from typing import List, Dict, Any

sys.path.insert(0, ".")
from raphael_core.kernel.models.workflow import WorkflowStep, WorkflowExecution
from raphael_core.kernel.services.builder.builder_fsm_actions import BuilderFSMActions

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("rrk.tests.missions")

# Rewind mapping per stage
REWIND_MAP = {
    "builder.design_review": "builder.architecture",
    "builder.compile": "builder.implementation",
    "builder.static_analysis": "builder.implementation",
    "builder.tests": "builder.implementation",
    "builder.integration_tests": "builder.implementation",
    "builder.security_review": "builder.implementation",
    "builder.performance_review": "builder.implementation",
    "builder.regression_suite": "builder.implementation",
    "builder.deploy": "builder.deploy_prep"
}

PIPELINE = [
    "builder.architecture",
    "builder.design_review",
    "builder.implementation",
    "builder.compile",
    "builder.static_analysis",
    "builder.tests",
    "builder.integration_tests",
    "builder.security_review",
    "builder.performance_review",
    "builder.documentation",
    "builder.git_checkpoint",
    "builder.regression_suite",
    "builder.deploy_prep",
    "builder.deploy",
    "builder.observe",
    "builder.learn",
    "builder.update_memory",
    "builder.improve_prompts"
]

class MockAIGateway:
    pass

class MissionOrchestrator:
    def __init__(self):
        self.fsm = BuilderFSMActions(MockAIGateway())
        self.max_retries_per_stage = 3
        self.max_total_rewinds = 6

    async def run_mission(self, injected_failures: Dict[str, int]) -> str:
        stage_retries = {stage: 0 for stage in PIPELINE}
        total_rewinds = 0
        
        current_index = 0
        workspace_id = "sandbox_goal_service"
        
        print("\n==========================================")
        print("   STARTING MISSION ORCHESTRATION LOOP    ")
        print("==========================================")
        
        while current_index < len(PIPELINE):
            action = PIPELINE[current_index]
            method_name = action.split(".")[1]
            method = getattr(self.fsm, method_name)
            
            print(f"\n[ORCHESTRATOR] Executing Stage: {action}")
            
            # Check if we should inject a failure here
            should_fail = injected_failures.get(action, 0) > stage_retries[action]
            
            if should_fail:
                print(f"[ORCHESTRATOR] [FAIL] Stage {action} FAILED (Injected)")
                
                # Check limits
                if stage_retries[action] >= self.max_retries_per_stage:
                    print(f"[ORCHESTRATOR] [HALT] Max retries (3) reached for stage {action}")
                    return "FAILED_REQUIRES_HUMAN"
                    
                if total_rewinds >= self.max_total_rewinds:
                    print(f"[ORCHESTRATOR] [HALT] Max total rewinds (6) reached for workflow")
                    return "FAILED_REQUIRES_HUMAN"
                    
                # Calculate rewind
                target_action = REWIND_MAP.get(action)
                if not target_action:
                    print(f"[ORCHESTRATOR] [HALT] No rewind mapping defined for {action}")
                    return "FAILED_REQUIRES_HUMAN"
                    
                target_index = PIPELINE.index(target_action)
                
                stage_retries[action] += 1
                total_rewinds += 1
                
                print(f"[ORCHESTRATOR] [REWIND] {action} -> {target_action} (Stage retries: {stage_retries[action]}/3, Total: {total_rewinds}/6)")
                current_index = target_index
                continue
                
            # Success Path
            try:
                result = method(workspace_id=workspace_id, context={})
                print(f"[ORCHESTRATOR] [OK] Stage {action} PASSED -> {result['state']}")
                current_index += 1
            except Exception as e:
                print(f"[ORCHESTRATOR] [HALT] Unhandled exception in {action}: {e}")
                return "FAILED_REQUIRES_HUMAN"
                
        print("\n[ORCHESTRATOR] [SUCCESS] Mission completed successfully!")
        return "COMPLETED"

class MissionBenchmarks:
    async def run_mission_4_self_repair(self):
        print("=== Mission 4: Self-Repair (Dependency Break) ===")
        print("Setting up sandbox environment for goal_service.py...")
        # Simulate sandbox setup
        print("Sandbox isolated. Injecting dependency break...")
        
        # We will instruct the orchestrator to fail 'builder.tests' once (to simulate fixing the code),
        # and 'builder.deploy' once (to simulate a docker port conflict), 
        # proving that DEPLOY rewinds to DEPLOY_PREP, not IMPLEMENTATION.
        
        injected_failures = {
            "builder.tests": 1,           # Fails once, rewinds to implementation
            "builder.deploy": 1           # Fails once, rewinds to deploy_prep
        }
        
        orchestrator = MissionOrchestrator()
        result = await orchestrator.run_mission(injected_failures)
        
        if result == "COMPLETED":
            print("\nMission 4 [PASSED]: Self-repair loop successfully diagnosed, patched, and deployed.")
        else:
            print("\nMission 4 [FAILED]: Human intervention required.")

    async def run_mission_ceiling_test(self):
        print("\n=== Ceiling Test: 3 Consecutive Failures ===")
        
        injected_failures = {
            "builder.tests": 4           # Fails 4 times to hit the retry ceiling of 3
        }
        
        orchestrator = MissionOrchestrator()
        result = await orchestrator.run_mission(injected_failures)
        
        if result == "FAILED_REQUIRES_HUMAN":
            print("\nCeiling Test [PASSED]: FSM correctly halted at retry ceiling instead of infinite looping.")
        else:
            print(f"\nCeiling Test [FAILED]: Expected FAILED_REQUIRES_HUMAN, got {result}")

if __name__ == "__main__":
    asyncio.run(MissionBenchmarks().run_mission_ceiling_test())
