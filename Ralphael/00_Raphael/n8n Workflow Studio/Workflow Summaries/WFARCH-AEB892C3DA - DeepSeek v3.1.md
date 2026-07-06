# Archived n8n Workflow WFARCH-AEB892C3DA

## Workflow ID

WFARCH-AEB892C3DA

## Name

DeepSeek v3.1

## Category

Agency

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1142_Gmailtool_Stickynote_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 10
- Connections: 7
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatDeepSeek`
- `n8n-nodes-base.gmailTool`
- `n8n-nodes-base.notionTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.wordpressTool`
- `n8n-nodes-mcp.mcpClientTool`

## API and Service Analysis

- Agent
- Gmail Tool
- Lm Chat Deep Seek
- Mcp Client Tool
- Notion Trigger
- Set
- Sticky Note
- Wordpress Tool

## Required Credentials

- deepSeekApi (type only; no credential value stored)
- gmailOAuth2 (type only; no credential value stored)
- mcpClientApi (type only; no credential value stored)
- notionApi (type only; no credential value stored)
- wordpressApi (type only; no credential value stored)

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
