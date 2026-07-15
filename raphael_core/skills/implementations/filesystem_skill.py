from typing import Dict, Any, List
from pathlib import Path
from ..base import BaseSkill
from ...legacy import load_config, DEFAULT_SETTINGS_PATH

class FilesystemReadSkill(BaseSkill):
    @property
    def skill_id(self) -> str:
        return "SKILL-FS-READ"

    @property
    def name(self) -> str:
        return "filesystem_read"

    @property
    def version(self) -> str:
        return "1.0"

    @property
    def constitutional_class(self) -> str:
        return "operational"

    @property
    def allowed_trust_tiers(self) -> List[int]:
        return [1, 2, 3, 4]

    def parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {"type": "string"}
            },
            "required": ["file_path"]
        }

    async def execute(self, params: Dict[str, Any], trace_id: str) -> Dict[str, Any]:
        config = load_config(DEFAULT_SETTINGS_PATH)
        target = Path(params.get("file_path", ""))
        
        # Security check: must be inside RaphaelOS
        if not str(target.absolute()).startswith(str(config.os_root.absolute())):
            return {"success": False, "error": "Path is outside RaphaelOS sandbox."}
            
        if not target.exists() or not target.is_file():
            return {"success": False, "error": "File not found."}
            
        try:
            content = target.read_text(encoding="utf-8")
            return {"success": True, "data": content}
        except Exception as e:
            return {"success": False, "error": str(e)}

class FilesystemWriteSkill(BaseSkill):
    @property
    def skill_id(self) -> str:
        return "SKILL-FS-WRITE"

    @property
    def name(self) -> str:
        return "filesystem_write"

    @property
    def version(self) -> str:
        return "1.0"

    @property
    def constitutional_class(self) -> str:
        return "operational"  # Note: Operational but vault-scoped

    @property
    def allowed_trust_tiers(self) -> List[int]:
        return [1, 2, 3, 4]

    def parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["file_path", "content"]
        }

    async def execute(self, params: Dict[str, Any], trace_id: str) -> Dict[str, Any]:
        config = load_config(DEFAULT_SETTINGS_PATH)
        target = Path(params.get("file_path", ""))
        
        # Security check: must be inside Vault
        vault_root = config.os_root / "vault"
        if not str(target.absolute()).startswith(str(vault_root.absolute())):
            return {"success": False, "error": "Write operations are restricted to the Vault directory."}
            
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(params.get("content", ""), encoding="utf-8")
            return {"success": True, "data": "File written successfully."}
        except Exception as e:
            return {"success": False, "error": str(e)}
