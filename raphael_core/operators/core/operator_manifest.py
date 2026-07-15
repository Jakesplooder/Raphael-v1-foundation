from pydantic import BaseModel
from typing import List

class OperatorManifest(BaseModel):
    name: str
    type: str = "venture_operator"
    venture_domain: str
    mission: str
    authorized_actions: List[str]
    restricted_actions: List[str]
    primary_kpis: List[str]
