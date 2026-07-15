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

from raphael_core.kernel.services.builder.ollama_gateway import OllamaGateway
import os

class LiveMissionOrchestrator:
    def __init__(self):
        self.gateway = OllamaGateway(model="qwen2.5-coder:14b")
        self.fsm = BuilderFSMActions(self.gateway)
        self.max_retries_per_stage = 3
        self.max_total_rewinds = 6

    async def run_mission(self) -> str:
        stage_retries = {stage: 0 for stage in PIPELINE}
        total_rewinds = 0
        current_index = 0
        workspace_id = "sandbox_landing_page"
        
        # Context to share data between stages
        context = {
            "stage_retries": stage_retries
        }
        
        print("\n==========================================")
        print("   STARTING MISSION 1 LIVE ORCHESTRATION   ")
        print("==========================================")
        
        while current_index < len(PIPELINE):
            action = PIPELINE[current_index]
            method_name = action.split(".")[1]
            method = getattr(self.fsm, method_name)
            
            print(f"\n[ORCHESTRATOR] Executing Stage: {action}")
            
            try:
                result = method(workspace_id=workspace_id, context=context)
                print(f"[ORCHESTRATOR] [OK] Stage {action} PASSED -> {result['state']}")
                current_index += 1
            except Exception as e:
                print(f"[ORCHESTRATOR] [FAIL] Stage {action} FAILED with error: {e}")
                
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
                
        print("\n[ORCHESTRATOR] [SUCCESS] Mission completed successfully!")
        return "COMPLETED"

if __name__ == "__main__":
    asyncio.run(LiveMissionOrchestrator().run_mission())
