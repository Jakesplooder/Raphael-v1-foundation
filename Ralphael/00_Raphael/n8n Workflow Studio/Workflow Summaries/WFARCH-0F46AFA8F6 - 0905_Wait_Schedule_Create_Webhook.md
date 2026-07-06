# Archived n8n Workflow WFARCH-0F46AFA8F6

## Workflow ID

WFARCH-0F46AFA8F6

## Name

0905_Wait_Schedule_Create_Webhook

## Category

Creator

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0905_Wait_Schedule_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 26
- Connections: 17
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.facebookGraphApi`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.wait`

## API and Service Analysis

- Chain Llm
- Facebook Graph Api
- Google Sheets
- Http Request
- Lm Chat Google Gemini
- Output Parser Structured
- Schedule Trigger
- Set
- Sticky Note
- Wait

## Required Credentials

- facebookGraphApi (type only; no credential value stored)
- googlePalmApi (type only; no credential value stored)
- googleSheetsOAuth2Api (type only; no credential value stored)
- httpHeaderAuth (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Creator
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
