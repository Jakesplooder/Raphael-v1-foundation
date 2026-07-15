from enum import Enum

class ValidationMode(str, Enum):
    SIMULATED = "SIMULATED"
    SANDBOX = "SANDBOX"
    PRODUCTION = "PRODUCTION"
