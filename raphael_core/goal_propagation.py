"""Goal propagation and cascade domain."""

from ._domain import get as __getattr__, names as _names

__all__ = [
    name for name in _names()
    if "goal_propagation" in name.lower()
    or "goal_cascade" in name.lower()
    or name.startswith("propagate_goal")
]
