from pydantic import BaseModel
from typing import List
from .visual_observation import VisualObservation

class VisualContext(BaseModel):
    observations: List[VisualObservation] = []
    
    def add_observation(self, obs: VisualObservation):
        self.observations.append(obs)
