# Archived n8n Workflow WFARCH-049B700EAF

## Workflow ID

WFARCH-049B700EAF

## Name

Colombian Invoices Processing

## Category

Finance

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1765_Code_Filter_Process_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 23
- Connections: 24
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `@n8n/n8n-nodes-langchain.toolCalculator`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.code`
- `n8n-nodes-base.compression`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.gmailTrigger`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.xml`

## API and Service Analysis

- Agent
- Aggregate
- Code
- Compression
- Extract From File
- Filter
- Gmail Trigger
- Google Drive
- Google Sheets
- Lm Chat Open Ai
- Merge
- No Op
- Output Parser Structured
- Split In Batches
- Sticky Note
- Switch
- Tool Calculator
- Xml

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- googleDriveOAuth2Api (type only; no credential value stored)
- googleSheetsOAuth2Api (type only; no credential value stored)
- openAiApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Finance
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
