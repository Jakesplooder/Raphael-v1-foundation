from enum import Enum

class EmployeeState(str, Enum):
    CREATED = "CREATED"
    TRAINING = "TRAINING"
    ACTIVE = "ACTIVE"
    PERFORMING = "PERFORMING"
    IMPROVING = "IMPROVING"
    PROMOTED = "PROMOTED"
    RETIRED = "RETIRED"
