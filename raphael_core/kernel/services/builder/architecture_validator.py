import logging
from typing import Dict, Any, List

logger = logging.getLogger("rrk.services.builder.architecture_validator")

class ArchitectureValidator:
    """
    Layer 2: Architecture Validator
    Ensures pre-disk checks such as naming conventions and dependency rules
    (e.g., Service imports Repository, Manager imports Service).
    """

    @staticmethod
    def validate(files: Dict[str, str]) -> List[str]:
        errors = []
        has_manager = False
        has_service = False
        has_repository = False

        for file_path, content in files.items():
            content_lower = content.lower()
            
            # Check naming conventions
            if "_manager.py" in file_path:
                has_manager = True
            elif "_service.py" in file_path:
                has_service = True
                # Service should not import Manager
                if "manager" in content_lower and "import" in content_lower:
                    if "manager.py" in file_path: continue # Ignore itself
                    # Simple heuristic
                    if "import " in content_lower and "manager" in content_lower.split("import ")[1]:
                        errors.append(f"Architectural Violation: Service {file_path} imports a Manager.")
            elif "_repository.py" in file_path:
                has_repository = True
                # Repository should not import Service or Manager
                if ("service" in content_lower or "manager" in content_lower) and "import" in content_lower:
                    errors.append(f"Architectural Violation: Repository {file_path} imports higher-level abstractions.")

        if not has_manager:
            errors.append("Missing Manager module (*_manager.py).")
        if not has_service:
            errors.append("Missing Service module (*_service.py).")
            
        return errors
