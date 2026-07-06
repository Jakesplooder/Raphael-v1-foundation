# Improvement Request IMPROVE-20260616-97DD232B

## Improvement ID

IMPROVE-20260616-97DD232B

## Description

Build requests previously produced code in chat instead of files.

## Problem

Build requests previously produced code in chat instead of files.

## Evidence

Dashboard Chat Log contains code-block style app generation responses.

## Proposed Fix

Continue improving Builder Mode so code-like responses become sandboxed build requests with generated files and review status.

## Risk Level

Medium

## Affected Files

raphael.py, C:/RaphaelOS/voice_gateway.py, C:/RaphaelOS/dashboard/app.py

## Codex Should Implement

Yes, after Aaron approves.

## Approval Required

Yes

## Status

Planned

## Created Date

2026-06-16T06:46:08

## Tests Or Smoke Checks Required

- Run relevant CLI command smoke tests.
- Verify dashboard/voice behavior if UI or routing changed.
- Confirm no destructive actions or source-folder edits occur without approval.

## Boundary

Raphael created this request as an advisory proposal. Raphael did not edit core code, execute workflows, approve actions, or modify source project folders.

## Improvement Plan

## Implementation Plan

1. Confirm Aaron approves the improvement request.
2. Identify the smallest safe code or documentation change.
3. Implement in a focused patch.
4. Run smoke tests listed below.
5. Capture lessons learned after verification.

## Smoke Tests

- `python -m py_compile raphael.py C:/RaphaelOS/voice_gateway.py C:/RaphaelOS/dashboard/app.py`
- Run the affected Raphael CLI command.
- If dashboard-related, verify `http://localhost:8787`.
- If voice-related, run `python C:/RaphaelOS/voice_gateway.py test-intent "..."`

## Approval Gate

Code changes require Aaron approval before implementation.
