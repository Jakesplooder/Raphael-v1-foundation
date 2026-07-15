import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from raphael_core.skills.base import BaseSkill
from raphael_core.skills.registry import SkillRegistry
from raphael_core.kernel.agent_base import AgentService
from raphael_core.kernel.interfaces import Job

class DummySkill(BaseSkill):
    @property
    def skill_id(self): return "SKILL-DUMMY-01"
    
    @property
    def name(self): return "dummy_skill"
    
    @property
    def version(self): return "1.0"
    
    @property
    def constitutional_class(self): return "operational"
    
    @property
    def allowed_trust_tiers(self): return [1, 2, 3]
    
    def parameters_schema(self): return {}
    
    async def execute(self, params, trace_id):
        return {"success": True, "data": "dummy output"}

class DummyAuthoritySkill(BaseSkill):
    @property
    def skill_id(self): return "SKILL-DUMMY-AUTH-01"
    
    @property
    def name(self): return "dummy_auth_skill"
    
    @property
    def version(self): return "1.0"
    
    @property
    def constitutional_class(self): return "authority"
    
    @property
    def allowed_trust_tiers(self): return [1]
    
    def parameters_schema(self): return {}
    
    async def execute(self, params, trace_id):
        return {"success": True, "data": "auth output"}

class DummyAgent(AgentService):
    service_name = "DummyAgent"
    async def process_job(self, job: Job):
        return await self.execute_skill("dummy_skill", {})

@pytest.mark.asyncio
async def test_skill_registry_registration_and_invoke():
    registry = SkillRegistry()
    registry.register_skill(DummySkill())
    
    result = await registry.invoke("dummy_skill", {}, trace_id="trace-123", agent_tier=1)
    assert result["success"] is True
    assert result["data"] == "dummy output"

@pytest.mark.asyncio
async def test_skill_registry_trust_tier_enforcement():
    registry = SkillRegistry()
    registry.register_skill(DummySkill())
    
    # Tier 4 is not in allowed_trust_tiers for DummySkill
    result = await registry.invoke("dummy_skill", {}, trace_id="trace-123", agent_tier=4)
    assert result["success"] is False
    assert "trust tier" in result["error"]

@pytest.mark.asyncio
async def test_skill_registry_authority_enforcement():
    registry = SkillRegistry()
    registry.register_skill(DummyAuthoritySkill())
    
    # Tier 1 is allowed, but constitutional class is authority
    result = await registry.invoke("dummy_auth_skill", {}, trace_id="trace-123", agent_tier=1)
    assert result["success"] is False
    assert "approval queue" in result["error"]
