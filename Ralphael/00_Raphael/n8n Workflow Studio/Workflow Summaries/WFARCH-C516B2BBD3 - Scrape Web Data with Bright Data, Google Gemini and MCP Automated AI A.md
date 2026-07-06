# Archived n8n Workflow WFARCH-C516B2BBD3

## Workflow ID

WFARCH-C516B2BBD3

## Name

Scrape Web Data with Bright Data, Google Gemini and MCP Automated AI Agent

## Category

Agency

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1707_Manual_Stickynote_Automate_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 19
- Connections: 14
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `n8n-nodes-base.function`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.readWriteFile`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-mcp.mcpClient`
- `n8n-nodes-mcp.mcpClientTool`

## API and Service Analysis

- Agent
- Function
- Http Request
- Lm Chat Google Gemini
- Manual Trigger
- Mcp Client
- Mcp Client Tool
- Memory Buffer Window
- Read Write File
- Set
- Sticky Note

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
