# Command Bus Overview

The Raphael Command Bus is the central safe routing layer for dashboard chat, voice chat, future orb commands, and future Matrix dashboard controls.

## Responsibilities

- Receive plain-language input.
- Detect command intent.
- Classify command type.
- Route to safe Raphael CLI commands.
- Detect confirmation requirements.
- Detect blocked or unsafe requests.
- Use general conversation fallback when no command matches.
- Return structured response objects.

## Boundary

The Command Bus centralizes routing and logging only. It does not weaken safety boundaries or add new execution powers.
