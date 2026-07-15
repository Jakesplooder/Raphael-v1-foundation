from typing import Dict, Any, List
from ..base import BaseSkill
from ...legacy import load_config, DEFAULT_SETTINGS_PATH
from ...docker_manager import docker_list, docker_start

class DockerListContainersSkill(BaseSkill):
    @property
    def skill_id(self) -> str:
        return "SKILL-DOCKER-LIST"

    @property
    def name(self) -> str:
        return "docker_list_containers"

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
        return {}

    async def execute(self, params: Dict[str, Any], trace_id: str) -> Dict[str, Any]:
        config = load_config(DEFAULT_SETTINGS_PATH)
        # Using the legacy docker_list wrapper
        result = docker_list(config)
        return {"success": True, "data": result}
