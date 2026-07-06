# Archived n8n Workflow WFARCH-3F1C6BD977

## Workflow ID

WFARCH-3F1C6BD977

## Name

Code Review workflow

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1292_Code_GitHub_Automate_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 14
- Connections: 7
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `n8n-nodes-base.code`
- `n8n-nodes-base.github`
- `n8n-nodes-base.githubTrigger`
- `n8n-nodes-base.googleSheetsTool`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Code
- Github
- Github Trigger
- Google Sheets Tool
- Http Request
- Lm Chat Open Ai
- Sticky Note

## Required Credentials

- githubApi (type only; no credential value stored)
- githubOAuth2Api (type only; no credential value stored)
- googleSheetsOAuth2Api (type only; no credential value stored)
- openAiApi (type only; no credential value stored)

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
