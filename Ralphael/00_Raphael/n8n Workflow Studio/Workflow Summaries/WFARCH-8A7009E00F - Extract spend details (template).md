# Archived n8n Workflow WFARCH-8A7009E00F

## Workflow ID

WFARCH-8A7009E00F

## Name

Extract spend details (template)

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1443_Splitout_Extractfromfile_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 24
- Connections: 21
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.lmChatGroq`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.gmailTrigger`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.html`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`

## API and Service Analysis

- Chain Llm
- Extract From File
- Gmail Trigger
- Google Sheets
- Html
- Lm Chat Google Gemini
- Lm Chat Groq
- Merge
- Output Parser Structured
- Set
- Split Out
- Sticky Note
- Switch

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- googlePalmApi (type only; no credential value stored)
- googleSheetsOAuth2Api (type only; no credential value stored)
- groqApi (type only; no credential value stored)

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
