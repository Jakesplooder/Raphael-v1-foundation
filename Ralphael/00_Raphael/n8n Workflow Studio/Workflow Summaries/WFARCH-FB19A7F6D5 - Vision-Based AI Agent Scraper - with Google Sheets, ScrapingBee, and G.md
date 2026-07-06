# Archived n8n Workflow WFARCH-FB19A7F6D5

## Workflow ID

WFARCH-FB19A7F6D5

## Name

Vision-Based AI Agent Scraper - with Google Sheets, ScrapingBee, and Gemini

## Category

Research

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

2041_Splitout_Manual_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 29
- Connections: 12
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `@n8n/n8n-nodes-langchain.toolWorkflow`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.markdown`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Execute Workflow Trigger
- Google Sheets
- Http Request
- Lm Chat Google Gemini
- Manual Trigger
- Markdown
- Output Parser Structured
- Set
- Split Out
- Sticky Note
- Tool Workflow

## Required Credentials

- googleApi (type only; no credential value stored)
- googlePalmApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Research
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
