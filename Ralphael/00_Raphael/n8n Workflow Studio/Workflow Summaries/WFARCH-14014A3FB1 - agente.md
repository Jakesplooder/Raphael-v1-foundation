# Archived n8n Workflow WFARCH-14014A3FB1

## Workflow ID

WFARCH-14014A3FB1

## Name

agente

## Category

Agency

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1103_Googletaskstool_Telegram_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 38
- Connections: 30
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.lmChatOpenRouter`
- `@n8n/n8n-nodes-langchain.mcpClientTool`
- `@n8n/n8n-nodes-langchain.memoryPostgresChat`
- `@n8n/n8n-nodes-langchain.openAi`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.convertToFile`
- `n8n-nodes-base.googleTasksTool`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.telegramTool`
- `n8n-nodes-base.telegramTrigger`
- `n8n-nodes-base.webhook`
- `n8n-nodes-evolution-api.evolutionApi`

## API and Service Analysis

- Agent
- Convert To File
- Evolution Api
- Google Tasks Tool
- Lm Chat Open Ai
- Lm Chat Open Router
- Mcp Client Tool
- Memory Postgres Chat
- Open Ai
- Schedule Trigger
- Set
- Sticky Note
- Switch
- Telegram
- Telegram Tool
- Telegram Trigger
- Tool Workflow
- Webhook

## Required Credentials

- evolutionApi (type only; no credential value stored)
- googleTasksOAuth2Api (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- openRouterApi (type only; no credential value stored)
- postgres (type only; no credential value stored)
- telegramApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Agency
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
