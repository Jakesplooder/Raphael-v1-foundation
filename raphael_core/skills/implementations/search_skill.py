from typing import Dict, Any, List
from ..base import BaseSkill
from ...legacy import load_config, DEFAULT_SETTINGS_PATH
from ...internet_access import perform_search

class SearchPublicWebSkill(BaseSkill):
    @property
    def skill_id(self) -> str:
        return "SKILL-SEARCH-PUBLIC"

    @property
    def name(self) -> str:
        return "search_public_web"

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
                "query": {"type": "string"},
                "num_results": {"type": "integer", "default": 5}
            },
            "required": ["query"]
        }

    async def execute(self, params: Dict[str, Any], trace_id: str) -> Dict[str, Any]:
        config = load_config(DEFAULT_SETTINGS_PATH)
        query = params.get("query", "")
        # The legacy search logic
        results = perform_search(config, query)
        return {"success": True, "data": results}
