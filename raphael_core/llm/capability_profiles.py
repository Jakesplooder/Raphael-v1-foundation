from dataclasses import dataclass
from typing import Dict

@dataclass
class CapabilityProfile:
    reasoning: int
    creativity: int
    coding: int
    planning: int
    prediction: int
    retrieval: int
    speed: int
    cost: int
    context_window: int
    tool_use: int
    json_reliability: int

# Central capability registry
PROFILES: Dict[str, CapabilityProfile] = {
    "claude": CapabilityProfile(
        reasoning=10,
        creativity=9,
        coding=9,
        planning=10,
        prediction=10,
        retrieval=8,
        speed=7,
        cost=4, # Lower is more expensive
        context_window=200000,
        tool_use=10,
        json_reliability=10
    ),
    "gemini": CapabilityProfile(
        reasoning=9,
        creativity=10,
        coding=8,
        planning=9,
        prediction=9,
        retrieval=10,
        speed=9,
        cost=8,
        context_window=2000000,
        tool_use=9,
        json_reliability=9
    ),
    "ollama": CapabilityProfile(
        reasoning=7,
        creativity=7,
        coding=8,
        planning=7,
        prediction=7,
        retrieval=6,
        speed=10,
        cost=10,
        context_window=8192,
        tool_use=6,
        json_reliability=8
    ),
    "openai": CapabilityProfile(
        reasoning=9,
        creativity=8,
        coding=9,
        planning=9,
        prediction=9,
        retrieval=8,
        speed=8,
        cost=5,
        context_window=128000,
        tool_use=10,
        json_reliability=10
    ),
    "local_reasoner": CapabilityProfile(
        reasoning=8,
        creativity=6,
        coding=7,
        planning=8,
        prediction=8,
        retrieval=7,
        speed=10,
        cost=10,
        context_window=32000,
        tool_use=7,
        json_reliability=9
    )
}

def get_profile(provider_name: str) -> CapabilityProfile:
    return PROFILES.get(provider_name.lower(), PROFILES["ollama"])
