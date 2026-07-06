# Archived n8n Workflow WFARCH-5FD8162226

## Workflow ID

WFARCH-5FD8162226

## Name

AI Customer-Support Assistant · WhatsApp Ready · Works for Any Business

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1521_Whatsapp_Stickynote_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 12
- Connections: 10
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryPostgresChat`
- `@n8n/n8n-nodes-langchain.toolHttpRequest`
- `n8n-nodes-base.code`
- `n8n-nodes-base.if`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.whatsApp`
- `n8n-nodes-base.whatsAppTrigger`

## API and Service Analysis

- Agent
- Code
- If
- Lm Chat Open Ai
- Memory Postgres Chat
- Sticky Note
- Tool Http Request
- Whats App
- Whats App Trigger

## Required Credentials

- openAiApi (type only; no credential value stored)
- postgres (type only; no credential value stored)
- whatsAppApi (type only; no credential value stored)
- whatsAppTriggerApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Automation
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
