# ADR 001: Executive Learning & Continuous Improvement

**Date**: 2026-07-06
**Status**: Accepted
**Context**: Raphael previously relied on static capability profiles for LLMs, immutable pattern confidence scores, and predictions that were never graded against reality. This led to intelligence accumulation, but not compounding capability.
**Decision**: We are implementing a closed-loop learning architecture (Phase 69.5) where every executed plan's prediction is graded against observed outcomes. This evaluation deterministically influences Pattern Evolution (decaying or splitting patterns) and dynamically updates Provider Capability Profiles based on historical task accuracy.
**Consequences**:
1. Adds `prediction_evaluator.py`, `executive_reflection.py`, `pattern_evolution.py`, and `learning_metrics.py`.
2. Changes LLM Router provider selection to use dynamic, historically-backed scores rather than hardcoded assumptions.
3. Necessitates a continuous reflection cadence (daily, weekly, monthly hooks).
4. Establishes the "Executive Humility" principle in the Constitution.
