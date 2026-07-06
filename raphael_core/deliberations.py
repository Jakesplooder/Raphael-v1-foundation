"""Council deliberation domain."""

from ._domain import get as __getattr__, names as _names

__all__ = [name for name in _names() if "deliberat" in name.lower()]
