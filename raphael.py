#!/usr/bin/env python3
"""Raphael OS compatibility CLI entrypoint.

The implementation lives in :mod:`raphael_core`. Existing commands and
imports remain available through this wrapper.
"""

from __future__ import annotations

from raphael_core import legacy as _legacy
from raphael_core.cli import main


def __getattr__(name: str):
    return getattr(_legacy, name)


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(dir(_legacy)))


if __name__ == "__main__":
    raise SystemExit(main())
