# Archived n8n Workflow WFARCH-0E26AF1E4E

## Workflow ID

WFARCH-0E26AF1E4E

## Name

Google Calendar Event Reminder

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1679_Telegram_GoogleCalendar_Automation_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 9
- Connections: 5
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `n8n-nodes-base.googleCalendar`
- `n8n-nodes-base.removeDuplicates`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.telegram`

## API and Service Analysis

- Agent
- Google Calendar
- Lm Chat Open Ai
- Remove Duplicates
- Schedule Trigger
- Sticky Note
- Telegram

## Required Credentials

- googleCalendarOAuth2Api (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- telegramApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Notifications
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
