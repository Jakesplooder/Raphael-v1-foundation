# Archived n8n Workflow WFARCH-1FD6C45CB6

## Workflow ID

WFARCH-1FD6C45CB6

## Name

1606_Telegram_Webhook_Automation_Webhook

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1606_Telegram_Webhook_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 35
- Connections: 26
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.outputParserAutofixing`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `@n8n/n8n-nodes-langchain.toolHttpRequest`
- `n8n-nodes-base.code`
- `n8n-nodes-base.gmailTrigger`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.telegramTrigger`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Agent
- Chat Trigger
- Code
- Gmail Trigger
- Http Request
- If
- Lm Chat Google Gemini
- Merge
- Output Parser Autofixing
- Output Parser Structured
- Sticky Note
- Switch
- Telegram Trigger
- Tool Http Request
- Webhook

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- googlePalmApi (type only; no credential value stored)
- httpHeaderAuth (type only; no credential value stored)
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
