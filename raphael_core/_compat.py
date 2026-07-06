"""Helpers for behavior-preserving domain facades."""

from __future__ import annotations

from . import legacy


def exports(names: list[str]) -> dict[str, object]:
    return {name: getattr(legacy, name) for name in names}
