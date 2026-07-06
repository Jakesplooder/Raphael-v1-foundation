# Archived n8n Workflow WFARCH-1A928A20AA

## Workflow ID

WFARCH-1A928A20AA

## Name

AI Social Media Publisher from WordPress

## Category

Creator

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1709_Linkedin_Wordpress_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 20
- Connections: 15
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatOpenRouter`
- `@n8n/n8n-nodes-langchain.openAi`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.facebookGraphApi`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.linkedIn`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.twitter`
- `n8n-nodes-base.wordpress`

## API and Service Analysis

- Chain Llm
- Facebook Graph Api
- Google Sheets
- Http Request
- Linked In
- Lm Chat Open Router
- Manual Trigger
- Open Ai
- Output Parser Structured
- Sticky Note
- Twitter
- Wordpress

## Required Credentials

- facebookGraphApi (type only; no credential value stored)
- googleSheetsOAuth2Api (type only; no credential value stored)
- linkedInOAuth2Api (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- openRouterApi (type only; no credential value stored)
- twitterOAuth2Api (type only; no credential value stored)
- wordpressApi (type only; no credential value stored)

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
