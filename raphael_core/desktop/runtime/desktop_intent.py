from pydantic import BaseModel
from typing import List

class DesktopIntent(BaseModel):
    id: str
    action: str
    application: str
    steps: List[str]
    risk_level: str = "LOW"
    authority_required: int = 0
    expected_result: str = ""
