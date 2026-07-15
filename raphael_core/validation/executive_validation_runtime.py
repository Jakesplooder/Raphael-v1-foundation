import os
import shutil
import logging
from .modes.validation_mode import ValidationMode

logger = logging.getLogger("rrk.validation.runtime")

class SandboxManager:
    def __init__(self, base_dir="tests/sandbox/ventures"):
        self.base_dir = base_dir
        
    def setup_sandbox(self, venture_id: str) -> str:
        sandbox_path = os.path.join(self.base_dir, venture_id)
        os.makedirs(sandbox_path, exist_ok=True)
        logger.info(f"Sandbox initialized at {sandbox_path}")
        return sandbox_path
        
    def teardown_sandbox(self, venture_id: str):
        sandbox_path = os.path.join(self.base_dir, venture_id)
        if os.path.exists(sandbox_path):
            shutil.rmtree(sandbox_path)
            logger.info(f"Sandbox torn down at {sandbox_path}")

class ExecutiveValidationRuntime:
    def __init__(self, mode: ValidationMode = ValidationMode.SIMULATED):
        self.mode = mode
        self.sandbox_manager = SandboxManager()
        
    def execute_builder_workflow(self, venture_id: str, plan: dict) -> dict:
        if self.mode == ValidationMode.SIMULATED:
            logger.info("Executing SIMULATED builder workflow")
            return {"success": True, "artifacts_generated": 12, "compile_attempts": 1}
            
        elif self.mode == ValidationMode.SANDBOX:
            sandbox_dir = self.sandbox_manager.setup_sandbox(venture_id)
            logger.info(f"Executing SANDBOX builder workflow in {sandbox_dir}")
            
            frontend_dir = os.path.join(sandbox_dir, "frontend")
            os.makedirs(frontend_dir, exist_ok=True)
            with open(os.path.join(frontend_dir, "package.json"), "w") as f:
                f.write('{"name": "secureflow-ai"}')
                
            backend_dir = os.path.join(sandbox_dir, "backend")
            os.makedirs(backend_dir, exist_ok=True)
            with open(os.path.join(backend_dir, "app.py"), "w") as f:
                f.write('print("Backend initialized")')
                
            with open(os.path.join(sandbox_dir, "build_report.json"), "w") as f:
                f.write('{"success": true, "artifacts_generated": 2}')
                
            return {"success": True, "sandbox_dir": sandbox_dir}
            
        elif self.mode == ValidationMode.PRODUCTION:
            raise NotImplementedError("Production deployment not active")
