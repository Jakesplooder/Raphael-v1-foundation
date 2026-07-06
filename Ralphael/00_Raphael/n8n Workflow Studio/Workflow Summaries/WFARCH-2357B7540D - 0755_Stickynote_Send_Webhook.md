# Archived n8n Workflow WFARCH-2357B7540D

## Workflow ID

WFARCH-2357B7540D

## Name

0755_Stickynote_Send_Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0755_Stickynote_Send_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 6
- Connections: 4
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.toolHttpRequest`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Chat Trigger
- Lm Chat Open Ai
- Sticky Note
- Tool Http Request
- Tool Workflow

## Required Credentials

- openAiApi (type only; no credential value stored)
- sshPassword (type only; no credential value stored)

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
