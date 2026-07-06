# Archived n8n Workflow WFARCH-67A8CBC9B1

## Workflow ID

WFARCH-67A8CBC9B1

## Name

Scrape Books from URL with Dumpling AI, Clean HTML, Save to Sheets, Email as CSV

## Category

Research

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1648_Splitout_Converttofile_Send_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 11
- Connections: 7
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.convertToFile`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.googleSheetsTrigger`
- `n8n-nodes-base.html`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.sort`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Convert To File
- Gmail
- Google Sheets Trigger
- Html
- Http Request
- Sort
- Split Out
- Sticky Note

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- googleSheetsTriggerOAuth2Api (type only; no credential value stored)
- httpBasicAuth (type only; no credential value stored)
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
