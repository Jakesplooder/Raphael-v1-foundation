"""
RRK Workflow Recovery.

Converts raw exceptions into structured WorkflowEvents so the engine can
reason about failures rather than blindly retrying. Each workflow type can
register its own exception-to-event mappings.
"""

import logging
from typing import Callable, Dict, Optional, Type

from .workflow_state import (
    RecoverySeverity,
    RecoveryStrategy,
    WorkflowEvent,
    WorkflowMemory,
    WorkflowMemoryEntry,
)

logger = logging.getLogger("rrk.workflow.recovery")


class RecoveryRule:
    """Maps an exception class to a structured recovery event."""

    def __init__(
        self,
        exception_type: Type[Exception],
        event_type: str,
        source: str,
        severity: RecoverySeverity = RecoverySeverity.MEDIUM,
        strategy: RecoveryStrategy = RecoveryStrategy.REGENERATE,
    ):
        self.exception_type = exception_type
        self.event_type = event_type
        self.source = source
        self.severity = severity
        self.strategy = strategy


class RecoveryRegistry:
    """
    Central registry of exception → recovery event mappings.
    Each workflow type registers its own rules.
    """

    def __init__(self):
        self._rules: Dict[str, list[RecoveryRule]] = {}  # keyed by workflow_type

    def register(self, workflow_type: str, rule: RecoveryRule) -> None:
        self._rules.setdefault(workflow_type, []).append(rule)

    def classify(self, workflow_type: str, exc: Exception) -> Optional[WorkflowEvent]:
        """
        Convert an exception into a structured WorkflowEvent.
        Returns None if no matching rule exists (unrecoverable).
        """
        for rule in self._rules.get(workflow_type, []):
            if isinstance(exc, rule.exception_type):
                event = WorkflowEvent(
                    event_type=rule.event_type,
                    source=rule.source,
                    severity=rule.severity,
                    recovery=rule.strategy,
                    detail=str(exc),
                    metadata={"exception_class": type(exc).__name__},
                )
                logger.info(
                    f"[RECOVERY] Classified {type(exc).__name__} as "
                    f"{rule.event_type} → strategy={rule.strategy.value}"
                )
                return event
        return None


# ---------------------------------------------------------------------------
# Prompt rewriting — the "learn from failure" mechanism
# ---------------------------------------------------------------------------

class PromptRewriter:
    """
    Applies learned negative-prompt injections to generation prompts
    based on past failure memory.
    """

    # Known failure type → negative prompt fragments
    KNOWN_MITIGATIONS: Dict[str, list[str]] = {
        "TypographyContaminationError": [
            "Do not include readable text or lettering in the image.",
            "Avoid typography, words, logos, or character-like patterns.",
        ],
    }

    @classmethod
    def rewrite(
        cls,
        original_prompt: str,
        failure_type: str,
        memory: WorkflowMemory,
        workflow_type: str,
    ) -> str:
        """
        Given the original prompt and the failure type, produce a modified
        prompt that avoids the known failure mode.
        """
        fragments: list[str] = []

        # 1. Check static mitigations
        static = cls.KNOWN_MITIGATIONS.get(failure_type, [])
        fragments.extend(static)

        # 2. Check learned resolutions from memory
        learned = memory.successful_resolutions(workflow_type, failure_type)
        fragments.extend(learned)

        if not fragments:
            return original_prompt

        # Deduplicate while preserving order
        seen = set()
        unique = []
        for f in fragments:
            if f not in seen:
                seen.add(f)
                unique.append(f)

        negative_clause = " ".join(unique)
        rewritten = f"{original_prompt}\n\nIMPORTANT CONSTRAINTS: {negative_clause}"

        logger.info(
            f"[PROMPT_REWRITE] Applied {len(unique)} mitigation(s) for {failure_type}"
        )
        return rewritten


# ---------------------------------------------------------------------------
# Global singleton
# ---------------------------------------------------------------------------
recovery_registry = RecoveryRegistry()
workflow_memory = WorkflowMemory()
