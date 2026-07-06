# Archived n8n Workflow WFARCH-43E9A3B853

## Workflow ID

WFARCH-43E9A3B853

## Name

AI Voice Chat using Webhook, Memory Manager, OpenAI, Google Gemini & ElevenLabs

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1262_Limit_Webhook_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 15
- Connections: 11
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.memoryManager`
- `@n8n/n8n-nodes-langchain.openAi`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.limit`
- `n8n-nodes-base.respondToWebhook`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Aggregate
- Chain Llm
- Http Request
- Limit
- Lm Chat Google Gemini
- Memory Buffer Window
- Memory Manager
- Open Ai
- Respond To Webhook
- Sticky Note
- Webhook

## Required Credentials

- googlePalmApi (type only; no credential value stored)
- httpCustomAuth (type only; no credential value stored)
- openAiApi (type only; no credential value stored)

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
