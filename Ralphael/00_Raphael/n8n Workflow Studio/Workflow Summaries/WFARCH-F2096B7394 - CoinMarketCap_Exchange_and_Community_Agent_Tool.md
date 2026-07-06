# Archived n8n Workflow WFARCH-F2096B7394

## Workflow ID

WFARCH-F2096B7394

## Name

CoinMarketCap_Exchange_and_Community_Agent_Tool

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1902_Stickynote_Executeworkflow_Update_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 12
- Connections: 8
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.toolHttpRequest`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Execute Workflow Trigger
- Lm Chat Open Ai
- Memory Buffer Window
- Sticky Note
- Tool Http Request

## Required Credentials

- httpHeaderAuth (type only; no credential value stored)
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
