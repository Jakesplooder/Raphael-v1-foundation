import logging
from typing import Dict, List

logger = logging.getLogger("rrk.workforce.skills")

class Skill:
    def __init__(self, name: str, category: str):
        self.name = name
        self.category = category
        self.usage_count = 0
        self.success_count = 0
        
    @property
    def success_rate(self) -> float:
        if self.usage_count == 0:
            return 0.0
        return (self.success_count / self.usage_count) * 100

class SkillRegistry:
    def __init__(self):
        self.skills: Dict[str, Skill] = {}
        
    def register_skill(self, name: str, category: str):
        if name not in self.skills:
            self.skills[name] = Skill(name, category)
            logger.info(f"Registered skill: {name} ({category})")
            
    def record_usage(self, skill_name: str, success: bool):
        if skill_name in self.skills:
            self.skills[skill_name].usage_count += 1
            if success:
                self.skills[skill_name].success_count += 1
                
    def find_by_category(self, category: str) -> List[Skill]:
        return [s for s in self.skills.values() if s.category == category]
        
    def get_skill(self, name: str) -> Skill:
        return self.skills.get(name, None)
