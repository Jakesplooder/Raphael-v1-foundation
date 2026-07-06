# Archived n8n Workflow WFARCH-7F3EF25E7F

## Workflow ID

WFARCH-7F3EF25E7F

## Name

LinkedIn Web Scraping with Bright Data MCP Server & Google Gemini

## Category

Agency

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1402_Code_Manual_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 20
- Connections: 18
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.informationExtractor`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.code`
- `n8n-nodes-base.function`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.readWriteFile`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-mcp.mcpClient`

## API and Service Analysis

- Aggregate
- Code
- Function
- Http Request
- Information Extractor
- Lm Chat Google Gemini
- Manual Trigger
- Mcp Client
- Merge
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
