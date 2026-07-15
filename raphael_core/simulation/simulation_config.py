from pydantic import BaseModel

class SimulationConfig(BaseModel):
    duration_months: int = 12
    allow_reality_transfer: bool = False
    
    @classmethod
    def quick_test(cls):
        return cls(duration_months=3)
        
    @classmethod
    def standard(cls):
        return cls(duration_months=12)
        
    @classmethod
    def deep_analysis(cls):
        return cls(duration_months=24)
