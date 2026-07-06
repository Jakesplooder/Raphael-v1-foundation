# Archived n8n Workflow WFARCH-B281E78369

## Workflow ID

WFARCH-B281E78369

## Name

🌐 Confluence Page AI Powered Chatbot

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1919_Telegram_Splitout_Automate_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 16
- Connections: 11
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.manualChatTrigger`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.markdown`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.telegram`

## API and Service Analysis

- Agent
- Http Request
- Lm Chat Open Ai
- Manual Chat Trigger
- Markdown
- Memory Buffer Window
- Set
- Split Out
- Sticky Note
- Telegram

## Required Credentials

- httpHeaderAuth (type only; no credential value stored)
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
