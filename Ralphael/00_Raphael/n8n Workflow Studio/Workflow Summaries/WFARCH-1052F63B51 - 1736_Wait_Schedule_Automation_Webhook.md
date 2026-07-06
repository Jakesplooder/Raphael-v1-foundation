# Archived n8n Workflow WFARCH-1052F63B51

## Workflow ID

WFARCH-1052F63B51

## Name

1736_Wait_Schedule_Automation_Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1736_Wait_Schedule_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 34
- Connections: 26
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.linear`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.wait`

## API and Service Analysis

- Aggregate
- Chain Llm
- Filter
- Google Drive
- Google Sheets
- Http Request
- Linear
- Lm Chat Google Gemini
- Manual Trigger
- Merge
- Output Parser Structured
- Schedule Trigger
- Set
- Split In Batches
- Sticky Note
- Wait

## Required Credentials

- googleDriveOAuth2Api (type only; no credential value stored)
- googlePalmApi (type only; no credential value stored)
- googleSheetsOAuth2Api (type only; no credential value stored)
- httpQueryAuth (type only; no credential value stored)
- linearApi (type only; no credential value stored)

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
