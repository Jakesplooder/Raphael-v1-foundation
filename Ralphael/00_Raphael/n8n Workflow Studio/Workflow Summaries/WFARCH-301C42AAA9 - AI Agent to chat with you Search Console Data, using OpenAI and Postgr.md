# Archived n8n Workflow WFARCH-301C42AAA9

## Workflow ID

WFARCH-301C42AAA9

## Name

AI Agent to chat with you Search Console Data, using OpenAI and Postgres

## Category

Research

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1252_Webhook_Respondtowebhook_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 30
- Connections: 14
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryPostgresChat`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.respondToWebhook`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Agent
- Aggregate
- Execute Workflow Trigger
- Http Request
- Lm Chat Open Ai
- Memory Postgres Chat
- Respond To Webhook
- Set
- Sticky Note
- Switch
- Tool Workflow
- Webhook

## Required Credentials

- httpBasicAuth (type only; no credential value stored)
- oAuth2Api (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- postgres (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Research
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
