# Archived n8n Workflow WFARCH-F866527458

## Workflow ID

WFARCH-F866527458

## Name

Google Maps FULL

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1964_HTTP_Aggregate_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 17
- Connections: 11
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.toolSerpApi`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Aggregate
- Chat Trigger
- Execute Workflow Trigger
- Google Sheets
- Http Request
- Lm Chat Open Ai
- Memory Buffer Window
- Sticky Note
- Tool Serp Api
- Tool Workflow

## Required Credentials

- googleSheetsOAuth2Api (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- serpApi (type only; no credential value stored)

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
