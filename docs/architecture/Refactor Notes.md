# Phase 64C Refactor Notes

## Completed

- Reduced `raphael.py` from roughly 26,500 lines to a thin entrypoint.
- Extracted the implementation into `raphael_core`.
- Added stable domain-module import surfaces.
- Preserved legacy imports through module attribute forwarding.
- Added an isolated test harness and `python raphael.py test`.
- Added pytest configuration without installing dependencies.

## Transitional Design

`raphael_core.legacy` remains large. This compatibility kernel prevents a risky
all-at-once redesign. Future work should extract one domain at a time:

1. Move implementation into its domain module.
2. Keep temporary forwarding imports.
3. Run `python raphael.py test`.
4. Run dashboard, Command Bus, and voice smoke checks.
5. Remove forwarding only after all callers use the stable module.

No product behavior or safety policy was intentionally changed.
