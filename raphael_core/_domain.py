"""Utilities for lazy domain-module compatibility exports."""

from __future__ import annotations

from . import legacy


def get(name: str):
    return getattr(legacy, name)


def names() -> list[str]:
    return [name for name in dir(legacy) if not name.startswith("_")]
