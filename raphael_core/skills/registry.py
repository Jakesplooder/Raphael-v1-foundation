import time
from typing import Dict, Any
from ..kernel.interfaces import ServiceModule, HealthStatus
from ..kernel.observability import ObservabilityLayer
from .base import BaseSkill

class SkillMetrics:
    def __init__(self):
        self.invocations = 0
        self.failures = 0
        self.skill_counts: Dict[str, int] = {}
        
    @property
    def top_skill(self) -> str:
        if not self.skill_counts:
            return "none"
        return max(self.skill_counts, key=self.skill_counts.get)

class SkillRegistry(ServiceModule):
    """
    Central registry and invocation router for all agent skills.
    Runs as a kernel ServiceModule to ensure observability and health tracking.
    """
    
    service_name = "SkillRegistry"
    depends_on = ["EventBus", "WorldModelService"]
    
    def __init__(self):
        super().__init__()
        self._skills: Dict[str, BaseSkill] = {}
        self._metrics = SkillMetrics()

    async def initialize(self) -> None:
        ObservabilityLayer.info(self.name, "Initializing SkillRegistry...")
        self._load_core_skills()

    def _load_core_skills(self) -> None:
        # We will import implementations here and register them
        from .implementations.filesystem_skill import FilesystemReadSkill, FilesystemWriteSkill
        from .implementations.search_skill import SearchPublicWebSkill
        from .implementations.docker_skill import DockerListContainersSkill
        
        skills = [
            FilesystemReadSkill(),
            FilesystemWriteSkill(),
            SearchPublicWebSkill(),
            DockerListContainersSkill()
        ]
        for s in skills:
            self.register_skill(s)

    def register_skill(self, skill: BaseSkill) -> None:
        self._skills[skill.name] = skill
        ObservabilityLayer.debug(self.name, f"Registered skill: {skill.name} ({skill.skill_id})")

    async def start(self) -> None:
        ObservabilityLayer.info(self.name, "SkillRegistry started.")

    async def stop(self) -> None:
        pass

    def heartbeat(self) -> HealthStatus:
        return {
            "registered_skills": len(self._skills),
            "skill_invocations_today": self._metrics.invocations,
            "failed_invocations_today": self._metrics.failures,
            "most_used_skill": self._metrics.top_skill,
        }

    async def invoke(self, skill_name: str, params: Dict[str, Any], trace_id: str, agent_tier: int = 1) -> Dict[str, Any]:
        """
        Invokes a skill, enforcing constitutional class and trust tiers.
        """
        if skill_name not in self._skills:
            return {"success": False, "error": f"Skill {skill_name} not found in registry."}
            
        skill = self._skills[skill_name]
        
        # Constitutional and Tier Enforcement
        if agent_tier not in skill.allowed_trust_tiers:
            self._metrics.failures += 1
            ObservabilityLayer.warning(self.name, f"Trust tier {agent_tier} denied for {skill_name}", trace_id=trace_id)
            return {"success": False, "error": f"Agent trust tier {agent_tier} is not authorized for {skill_name}"}
            
        if skill.constitutional_class == "authority":
            # TODO: Integrate with real approval queue system
            ObservabilityLayer.info(self.name, f"Authority skill {skill_name} flagged for approval.", trace_id=trace_id)
            return {"success": False, "error": f"Authority skill requires manual approval queue (Not implemented in MVP)"}
            
        # self.obs is available on ServiceModule
        ObservabilityLayer.info(self.name, f"Skill invoked", trace_id=trace_id, skill=skill_name)
        
        self._metrics.invocations += 1
        self._metrics.skill_counts[skill_name] = self._metrics.skill_counts.get(skill_name, 0) + 1
        
        try:
            start_time = time.time()
            result = await skill.execute(params, trace_id)
            latency = time.time() - start_time
            success = result.get("success", True)
            
            if not success:
                self._metrics.failures += 1
                
            ObservabilityLayer.info(self.name, f"Skill completed", trace_id=trace_id, skill=skill_name, success=success, latency=latency)
            return result
        except Exception as e:
            self._metrics.failures += 1
            ObservabilityLayer.error(self.name, f"Skill raised exception", trace_id=trace_id, skill=skill_name, error=str(e))
            return {"success": False, "error": str(e)}
