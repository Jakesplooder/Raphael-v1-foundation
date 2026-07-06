"""Knowledge graph and relationship domain."""

from ._domain import get as __getattr__, names as _names

__all__ = [
    name for name in _names()
    if "knowledge_relationship" in name.lower()
    or name.startswith("knowledge_graph")
    or name.startswith("knowledge_related")
    or name.startswith("knowledge_path")
    or name.startswith("knowledge_cluster")
    or name.endswith("_map")
]
