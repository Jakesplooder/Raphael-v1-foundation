# Archived n8n Workflow WFARCH-649F55CB55

## Workflow ID

WFARCH-649F55CB55

## Name

🤖 Telegram Messaging Agent for Text/Audio/Images

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

2051_Telegram_Webhook_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 39
- Connections: 28
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.openAi`
- `@n8n/n8n-nodes-langchain.textClassifier`
- `n8n-nodes-base.convertToFile`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Convert To File
- Extract From File
- Http Request
- If
- Lm Chat Open Ai
- Open Ai
- Set
- Sticky Note
- Switch
- Telegram
- Text Classifier
- Webhook

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
