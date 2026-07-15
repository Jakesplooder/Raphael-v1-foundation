from ..core.base_agent import BaseAgent

class ChiefOfStaffAgent(BaseAgent):
    def __init__(self, memory_service=None):
        super().__init__("ChiefOfStaffAgent", memory_service)

class DeveloperAgent(BaseAgent):
    def __init__(self, memory_service=None):
        super().__init__("DeveloperAgent", memory_service)

class CommerceAgent(BaseAgent):
    def __init__(self, memory_service=None):
        super().__init__("CommerceAgent", memory_service)

class ResearchAgent(BaseAgent):
    def __init__(self, memory_service=None):
        super().__init__("ResearchAgent", memory_service)

class FinanceAgent(BaseAgent):
    def __init__(self, memory_service=None):
        super().__init__("FinanceAgent", memory_service)
