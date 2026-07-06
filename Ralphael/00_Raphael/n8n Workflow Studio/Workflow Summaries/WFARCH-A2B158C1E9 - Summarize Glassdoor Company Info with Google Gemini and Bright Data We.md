# Archived n8n Workflow WFARCH-A2B158C1E9

## Workflow ID

WFARCH-A2B158C1E9

## Name

Summarize Glassdoor Company Info with Google Gemini and Bright Data Web Scraper

## Category

Research

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1676_Manual_Wait_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 14
- Connections: 12
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainSummarization`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.wait`

## API and Service Analysis

- Chain Summarization
- Document Default Data Loader
- Http Request
- If
- Lm Chat Google Gemini
- Manual Trigger
- Set
- Sticky Note
- Text Splitter Recursive Character Text Splitter
- Wait

## Required Credentials

- googlePalmApi (type only; no credential value stored)
- httpHeaderAuth (type only; no credential value stored)

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
