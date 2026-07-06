# Archived n8n Workflow WFARCH-A21F0753FD

## Workflow ID

WFARCH-A21F0753FD

## Name

1556_Splitout_Code_Monitor_Scheduled

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1556_Splitout_Code_Monitor_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 37
- Connections: 33
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatAnthropic`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.code`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.limit`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.spotify`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Chain Llm
- Code
- Filter
- Google Sheets
- Http Request
- Limit
- Lm Chat Anthropic
- Merge
- No Op
- Output Parser Structured
- Schedule Trigger
- Set
- Split Out
- Spotify
- Sticky Note

## Required Credentials

- anthropicApi (type only; no credential value stored)
- googleSheetsOAuth2Api (type only; no credential value stored)
- spotifyOAuth2Api (type only; no credential value stored)

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
