"""Advisory execution-planning domain."""

from ._domain import get as __getattr__, names as _names

__all__ = [name for name in _names() if "execution_plan" in name.lower()]
