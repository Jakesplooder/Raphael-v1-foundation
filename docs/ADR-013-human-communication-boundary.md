# ADR-013: Human Communication Boundary

**Date**: 2026-07-16
**Status**: Accepted

## Context
As Raphael transitions to Level 2 (Supervised Autonomy) and higher, the system requires an active communication loop with a human executive. Without a strict architectural boundary, applications, domains, and agents might begin sending notifications directly (e.g., `discord.send()`). This creates a coupled, chaotic "shadow subsystem" that bypasses the kernel and obscures operational visibility.

## Decision
We establish a strict **Human Communication Boundary**. 
- Applications do NOT send notifications.
- Domains do NOT send notifications.
- Agents do NOT send notifications.

Only the `NotificationService` operating inside the Kernel is permitted to communicate externally.

## Implementation Details
1. **Event-Driven Coupling**: Any component needing to alert the human must emit an event via the `EventBus` (e.g., `MISSION.REVIEW_REQUIRED`, `MISSION.FAILURE`).
2. **Notification Gateway**: The `NotificationService` subscribes to these events, classifies their priority, formats them via templates, and routes them to the appropriate provider (e.g., Discord, Telegram).
3. **Priority Classification**:
    - `normal`: Routine logs, lifecycle updates (routed to Discord Operations Console).
    - `high`: Approvals, significant changes (routed to Discord + Telegram).
    - `critical`: Mission failures, system blocks (routed to Telegram Executive feed immediately).

## Consequences
This ensures that Raphael's "voice" remains centralized, auditable, and decoupled from the business logic. It prevents rogue agents from spamming executives and enables the easy addition of future notification providers (e.g., Slack, Email) without refactoring any domain code.
