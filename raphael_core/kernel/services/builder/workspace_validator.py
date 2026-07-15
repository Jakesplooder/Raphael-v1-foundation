import logging
import os
from typing import List

logger = logging.getLogger("rrk.services.builder.workspace_validator")

class WorkspaceValidator:
    """
    Layer 3: Workspace Validator
    Ensures that requisite project configuration files exist before attempting to compile.
    """

    @staticmethod
    def validate(workspace_path: str, project_type: str = "python") -> List[str]:
        errors = []
        
        if project_type == "python":
            if not os.path.exists(os.path.join(workspace_path, "requirements.txt")):
                errors.append("Missing requirements.txt in Python workspace.")
        elif project_type == "node":
            if not os.path.exists(os.path.join(workspace_path, "package.json")):
                errors.append("Missing package.json in Node workspace.")
                
        # General checks
        if not os.path.exists(os.path.join(workspace_path, "README.md")):
            logger.warning("Missing README.md in workspace (Warning only).")
            
        return errors
