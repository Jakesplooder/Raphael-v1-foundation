# Archived n8n Workflow WFARCH-7E02274D3C

## Workflow ID

WFARCH-7E02274D3C

## Name

Github Releases

## Category

Research

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1695_Limit_Code_Automation_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 24
- Connections: 20
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.informationExtractor`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `n8n-nodes-base.code`
- `n8n-nodes-base.dateTime`
- `n8n-nodes-base.if`
- `n8n-nodes-base.limit`
- `n8n-nodes-base.redis`
- `n8n-nodes-base.rssFeedRead`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.slack`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Code
- Date Time
- If
- Information Extractor
- Limit
- Lm Chat Google Gemini
- Redis
- Rss Feed Read
- Schedule Trigger
- Set
- Slack
- Split In Batches
- Sticky Note

## Required Credentials

- googlePalmApi (type only; no credential value stored)
- redis (type only; no credential value stored)
- slackApi (type only; no credential value stored)

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
