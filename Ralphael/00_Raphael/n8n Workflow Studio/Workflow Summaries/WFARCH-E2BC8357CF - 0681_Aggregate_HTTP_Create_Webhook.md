# Archived n8n Workflow WFARCH-E2BC8357CF

## Workflow ID

WFARCH-E2BC8357CF

## Name

0681_Aggregate_HTTP_Create_Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0681_Aggregate_HTTP_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 41
- Connections: 33
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.toolCode`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.airtable`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`

## API and Service Analysis

- Agent
- Aggregate
- Airtable
- Chat Trigger
- Execute Workflow Trigger
- Http Request
- If
- Lm Chat Open Ai
- Memory Buffer Window
- Merge
- Set
- Sticky Note
- Switch
- Tool Code
- Tool Workflow

## Required Credentials

- airtableTokenApi (type only; no credential value stored)
- httpQueryAuth (type only; no credential value stored)
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
