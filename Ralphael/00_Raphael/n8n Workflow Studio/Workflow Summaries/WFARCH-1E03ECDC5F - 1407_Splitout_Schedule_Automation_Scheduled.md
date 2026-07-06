# Archived n8n Workflow WFARCH-1E03ECDC5F

## Workflow ID

WFARCH-1E03ECDC5F

## Name

1407_Splitout_Schedule_Automation_Scheduled

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1407_Splitout_Schedule_Automation_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 24
- Connections: 15
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.informationExtractor`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `n8n-nodes-base.airtable`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.html`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.removeDuplicates`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Airtable
- Gmail
- Html
- Http Request
- Information Extractor
- Lm Chat Open Ai
- Merge
- Remove Duplicates
- Schedule Trigger
- Split Out
- Sticky Note

## Required Credentials

- airtableTokenApi (type only; no credential value stored)
- gmailOAuth2 (type only; no credential value stored)
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
