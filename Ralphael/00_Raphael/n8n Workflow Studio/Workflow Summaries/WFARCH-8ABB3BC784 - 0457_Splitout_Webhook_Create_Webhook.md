# Archived n8n Workflow WFARCH-8ABB3BC784

## Workflow ID

WFARCH-8ABB3BC784

## Name

0457_Splitout_Webhook_Create_Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0457_Splitout_Webhook_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 40
- Connections: 29
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.code`
- `n8n-nodes-base.dhl`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.respondToWebhook`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.webhook`
- `n8n-nodes-base.wooCommerce`

## API and Service Analysis

- Agent
- Aggregate
- Chat Trigger
- Code
- Dhl
- Execute Workflow Trigger
- Http Request
- If
- Lm Chat Open Ai
- Memory Buffer Window
- Merge
- Respond To Webhook
- Set
- Split Out
- Sticky Note
- Tool Workflow
- Webhook
- Woo Commerce

## Required Credentials

- dhlApi (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- wooCommerceApi (type only; no credential value stored)

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
