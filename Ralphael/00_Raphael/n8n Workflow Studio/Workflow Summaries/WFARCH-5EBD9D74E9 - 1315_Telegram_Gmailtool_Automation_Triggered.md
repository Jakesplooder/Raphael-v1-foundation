# Archived n8n Workflow WFARCH-5EBD9D74E9

## Workflow ID

WFARCH-5EBD9D74E9

## Name

1315_Telegram_Gmailtool_Automation_Triggered

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1315_Telegram_Gmailtool_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 15
- Connections: 13
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.openAi`
- `n8n-nodes-base.baserowTool`
- `n8n-nodes-base.gmailTool`
- `n8n-nodes-base.googleCalendarTool`
- `n8n-nodes-base.if`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.telegramTrigger`

## API and Service Analysis

- Agent
- Baserow Tool
- Gmail Tool
- Google Calendar Tool
- If
- Lm Chat Open Ai
- Memory Buffer Window
- Open Ai
- Set
- Sticky Note
- Telegram
- Telegram Trigger

## Required Credentials

- baserowApi (type only; no credential value stored)
- gmailOAuth2 (type only; no credential value stored)
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
