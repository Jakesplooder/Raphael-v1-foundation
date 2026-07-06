"""Executive brief domain."""

from ._domain import get as __getattr__, names as _names

__all__ = [name for name in _names() if "brief" in name.lower() or name in {"morning_brief", "evening_review", "monthly_review"}]
