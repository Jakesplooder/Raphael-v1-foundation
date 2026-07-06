# Archived n8n Workflow WFARCH-1B7D24A3E4

## Workflow ID

WFARCH-1B7D24A3E4

## Name

HR Job Posting and Evaluation with AI

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1488_Extractfromfile_Form_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 36
- Connections: 29
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.openAi`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.airtable`
- `n8n-nodes-base.airtableTool`
- `n8n-nodes-base.emailSend`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.form`
- `n8n-nodes-base.formTrigger`
- `n8n-nodes-base.googleCalendarTool`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.if`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Airtable
- Airtable Tool
- Email Send
- Extract From File
- Form
- Form Trigger
- Google Calendar Tool
- Google Drive
- If
- Lm Chat Open Ai
- Open Ai
- Output Parser Structured
- Set
- Sticky Note

## Required Credentials

- airtableTokenApi (type only; no credential value stored)
- googleCalendarOAuth2Api (type only; no credential value stored)
- googleDriveOAuth2Api (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- smtp (type only; no credential value stored)

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
