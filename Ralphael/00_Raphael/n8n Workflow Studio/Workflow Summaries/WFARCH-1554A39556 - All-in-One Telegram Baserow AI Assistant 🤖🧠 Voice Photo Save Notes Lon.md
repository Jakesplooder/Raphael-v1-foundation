# Archived n8n Workflow WFARCH-1554A39556

## Workflow ID

WFARCH-1554A39556

## Name

All-in-One Telegram/Baserow AI Assistant 🤖🧠 Voice/Photo/Save Notes/Long Term Mem

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1305_Telegram_Splitout_Export_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 48
- Connections: 33
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.memoryPostgresChat`
- `@n8n/n8n-nodes-langchain.openAi`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.baserow`
- `n8n-nodes-base.baserowTool`
- `n8n-nodes-base.convertToFile`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.if`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Agent
- Aggregate
- Baserow
- Baserow Tool
- Convert To File
- Extract From File
- If
- Lm Chat Open Ai
- Memory Buffer Window
- Memory Postgres Chat
- Merge
- Open Ai
- Set
- Split Out
- Sticky Note
- Switch
- Telegram
- Webhook

## Required Credentials

- baserowApi (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- postgres (type only; no credential value stored)
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
