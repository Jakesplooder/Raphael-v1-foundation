"""Safe inactive n8n workflow studio domain."""

from ._domain import get as __getattr__, names as _names

__all__ = [name for name in _names() if name.startswith("n8n_") or name.startswith("N8N_")]
