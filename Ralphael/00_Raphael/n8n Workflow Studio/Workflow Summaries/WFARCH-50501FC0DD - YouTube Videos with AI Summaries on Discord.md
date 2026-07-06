# Archived n8n Workflow WFARCH-50501FC0DD

## Workflow ID

WFARCH-50501FC0DD

## Name

YouTube Videos with AI Summaries on Discord

## Category

Creator

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1536_Rssfeedread_Extractfromfile_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 8
- Connections: 6
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.openAi`
- `n8n-nodes-base.discord`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.rssFeedReadTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Discord
- Extract From File
- Http Request
- Open Ai
- Rss Feed Read Trigger
- Set
- Sticky Note

## Required Credentials

- discordWebhookApi (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- youTubeOAuth2Api (type only; no credential value stored)

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
