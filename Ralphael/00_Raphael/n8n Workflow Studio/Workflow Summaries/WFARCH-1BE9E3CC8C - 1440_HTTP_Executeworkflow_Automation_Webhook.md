# Archived n8n Workflow WFARCH-1BE9E3CC8C

## Workflow ID

WFARCH-1BE9E3CC8C

## Name

1440_HTTP_Executeworkflow_Automation_Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1440_HTTP_Executeworkflow_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 29
- Connections: 26
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryPostgresChat`
- `@n8n/n8n-nodes-langchain.openAi`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`

## API and Service Analysis

- Agent
- Chat Trigger
- Execute Workflow Trigger
- Http Request
- Lm Chat Open Ai
- Memory Postgres Chat
- Open Ai
- Set
- Sticky Note
- Switch
- Tool Workflow

## Required Credentials

- httpQueryAuth (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- postgres (type only; no credential value stored)

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
