# Archived n8n Workflow WFARCH-80B012FB6B

## Workflow ID

WFARCH-80B012FB6B

## Name

0700_Code_Respondtowebhook_Send_Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0700_Code_Respondtowebhook_Send_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 24
- Connections: 15
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.toolHttpRequest`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.code`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.microsoftOutlook`
- `n8n-nodes-base.respondToWebhook`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`

## API and Service Analysis

- Agent
- Chat Trigger
- Code
- Execute Workflow Trigger
- Http Request
- If
- Lm Chat Open Ai
- Memory Buffer Window
- Microsoft Outlook
- Respond To Webhook
- Set
- Sticky Note
- Switch
- Tool Http Request
- Tool Workflow

## Required Credentials

- microsoftOutlookOAuth2Api (type only; no credential value stored)
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
