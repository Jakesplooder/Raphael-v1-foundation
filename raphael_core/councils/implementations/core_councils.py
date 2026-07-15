from typing import Dict, Any
from ..core.base_council import BaseCouncil
from ..core.decision import CouncilDecision

class ArchitectureCouncil(BaseCouncil):
    def __init__(self):
        super().__init__("Architecture Council")

class SecurityCouncil(BaseCouncil):
    def __init__(self):
        super().__init__("Security Council")

class CommerceCouncil(BaseCouncil):
    def __init__(self):
        super().__init__("Commerce Council")

class BrandCouncil(BaseCouncil):
    def __init__(self):
        super().__init__("Brand Council")

class FinanceCouncil(BaseCouncil):
    def __init__(self):
        super().__init__("Finance Council")
