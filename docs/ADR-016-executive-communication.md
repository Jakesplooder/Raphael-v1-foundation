# ADR-016: Executive Communication Separation of Powers

## Status
Accepted

## Context
As Raphael grows from a single autonomous loop into a Multi-Business Operator (Phase 9), uncontrolled communication channels become an operational failure point. The system requires a structural boundary between information logging, discussion, and executive authority.

## Decision
We establish the **Communication Constitution**:

1. **Discord = Operations Command Center & Boardroom**
   - **Role**: Information flow, intelligence, operational memory, and council debates.
   - **Questions Answered**: What happened? Why? What evidence exists? What are the arguments?
   - **Allowed Events**: `MISSION.CREATED`, `MISSION.STARTED`, `MISSION.COMPLETED`, `MISSION.FAILED`, `MISSION.RECOVERED`, `BUSINESS.PATTERN_DISCOVERED`, `STRATEGY.*`
   - **Structure**: Divided into functional channels (`#mission-feed`, `#incidents`, `#analytics`, `#council`).

2. **Telegram = CEO Black Phone**
   - **Role**: Executive interruption and decision authority.
   - **Questions Answered**: "What requires Aaron's attention right now?"
   - **Allowed Events**: `APPROVAL.REQUIRED`, `SYSTEM.DAILY_BRIEF`, and `MISSION.FAILURE` (ONLY if severity is `CRITICAL`).

3. **Quiet Hours & Routing Audit**
   - Telegram enforces quiet hours (e.g. 22:00 - 07:00), bypassing ONLY for CRITICAL INCIDENTS, SECURITY EVENTS, FINANCIAL LOSS, or APPROVAL EXPIRATIONS.
   - Every route decision is explicitly logged in `routing_decisions.jsonl` to explain "Why did you wake me up?".

## Consequences
- The CEO is completely shielded from agent chatter, debug logs, and mission spam.
- Discord becomes a rich, searchable context engine where Raphael "thinks publicly."
- Telegram becomes a high-signal control interface where Raphael exclusively asks for authority.
