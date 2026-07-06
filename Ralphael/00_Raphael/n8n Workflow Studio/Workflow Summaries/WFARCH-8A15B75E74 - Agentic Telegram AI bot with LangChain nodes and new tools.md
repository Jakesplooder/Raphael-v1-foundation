# Archived n8n Workflow WFARCH-8A15B75E74

## Workflow ID

WFARCH-8A15B75E74

## Name

Agentic Telegram AI bot with LangChain nodes and new tools

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1300_Telegram_Stickynote_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 8
- Connections: 6
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.toolHttpRequest`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.telegramTool`
- `n8n-nodes-base.telegramTrigger`

## API and Service Analysis

- Agent
- Lm Chat Open Ai
- Memory Buffer Window
- Sticky Note
- Telegram
- Telegram Tool
- Telegram Trigger
- Tool Http Request

## Required Credentials

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
