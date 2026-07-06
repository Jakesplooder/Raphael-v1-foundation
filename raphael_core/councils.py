"""Council review, debate, and delegation domain."""

from ._domain import get as __getattr__, names as _names

__all__ = [name for name in _names() if "council" in name.lower() or name in {"delegate_task", "executive_summary"}]
