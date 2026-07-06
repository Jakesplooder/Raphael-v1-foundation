# Archived n8n Workflow WFARCH-CE813B5FAF

## Workflow ID

WFARCH-CE813B5FAF

## Name

The Ultimate Guide to Optimize WordPress Blog Posts with AI

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1550_Wordpress_Manual_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 21
- Connections: 14
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatOpenRouter`
- `@n8n/n8n-nodes-langchain.openAi`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.wordpress`

## API and Service Analysis

- Chain Llm
- Google Sheets
- Http Request
- Lm Chat Open Router
- Manual Trigger
- Open Ai
- Output Parser Structured
- Set
- Sticky Note
- Wordpress

## Required Credentials

- googleSheetsOAuth2Api (type only; no credential value stored)
- httpBasicAuth (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- openRouterApi (type only; no credential value stored)
- wordpressApi (type only; no credential value stored)

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
