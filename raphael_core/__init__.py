"""Modular Raphael OS core.

Domain modules provide stable import surfaces while ``legacy`` remains the
behavior-preserving compatibility kernel during the gradual extraction.
"""

from .config import DEFAULT_SETTINGS, DEFAULT_SETTINGS_PATH, RaphaelConfig, load_config

__all__ = [
    "DEFAULT_SETTINGS",
    "DEFAULT_SETTINGS_PATH",
    "RaphaelConfig",
    "load_config",
]
