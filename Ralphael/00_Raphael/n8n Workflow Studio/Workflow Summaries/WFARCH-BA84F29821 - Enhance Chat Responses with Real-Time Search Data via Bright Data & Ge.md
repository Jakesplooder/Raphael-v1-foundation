# Archived n8n Workflow WFARCH-BA84F29821

## Workflow ID

WFARCH-BA84F29821

## Name

Enhance Chat Responses with Real-Time Search Data via Bright Data & Gemini AI

## Category

Agency

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1183_Manual_Stickynote_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 18
- Connections: 11
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.toolHttpRequest`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-mcp.mcpClient`
- `n8n-nodes-mcp.mcpClientTool`

## API and Service Analysis

- Agent
- Chat Trigger
- Lm Chat Google Gemini
- Manual Trigger
- Mcp Client
- Mcp Client Tool
- Memory Buffer Window
- Set
- Sticky Note
- Tool Http Request

## Required Credentials

- googlePalmApi (type only; no credential value stored)
- mcpClientApi (type only; no credential value stored)

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
