# Archived n8n Workflow WFARCH-A00D5EE75E

## Workflow ID

WFARCH-A00D5EE75E

## Name

mails2notion V2

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1921_Code_Filter_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 38
- Connections: 24
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `@n8n/n8n-nodes-langchain.toolCalculator`
- `n8n-nodes-base.airtable`
- `n8n-nodes-base.code`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.gmailTrigger`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Airtable
- Code
- Filter
- Gmail
- Gmail Trigger
- Http Request
- Lm Chat Open Ai
- Manual Trigger
- No Op
- Output Parser Structured
- Set
- Sticky Note
- Tool Calculator

## Required Credentials

- airtableTokenApi (type only; no credential value stored)
- gmailOAuth2 (type only; no credential value stored)
- openAiApi (type only; no credential value stored)

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
