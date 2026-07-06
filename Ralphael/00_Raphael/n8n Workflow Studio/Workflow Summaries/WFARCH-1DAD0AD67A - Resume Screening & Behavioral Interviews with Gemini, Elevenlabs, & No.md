# Archived n8n Workflow WFARCH-1DAD0AD67A

## Workflow ID

WFARCH-1DAD0AD67A

## Name

Resume Screening & Behavioral Interviews with Gemini, Elevenlabs, & Notion ATS copy

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1639_Wait_Webhook_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 67
- Connections: 38
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.chainSummarization`
- `@n8n/n8n-nodes-langchain.informationExtractor`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.formTrigger`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.notion`
- `n8n-nodes-base.notionTool`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.wait`
- `n8n-nodes-base.webhook`

## API and Service Analysis

- Agent
- Chain Llm
- Chain Summarization
- Extract From File
- Filter
- Form Trigger
- Google Drive
- Google Sheets
- Http Request
- Information Extractor
- Lm Chat Google Gemini
- Merge
- Notion
- Notion Tool
- Output Parser Structured
- Set
- Sticky Note
- Wait
- Webhook

## Required Credentials

- googleDriveOAuth2Api (type only; no credential value stored)
- googlePalmApi (type only; no credential value stored)
- googleSheetsOAuth2Api (type only; no credential value stored)
- notionApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Knowledge
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
