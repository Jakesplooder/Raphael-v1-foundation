# Archived n8n Workflow WFARCH-AE2C25BAF1

## Workflow ID

WFARCH-AE2C25BAF1

## Name

Extract expenses from emails and add to Google Sheet

## Category

Finance

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1188_GoogleSheets_Emailreadimap_Create.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 6
- Connections: 5
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.emailReadImap`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.if`
- `n8n-nodes-base.mindee`
- `n8n-nodes-base.set`

## API and Service Analysis

- Email Read Imap
- Google Sheets
- If
- Mindee
- Set

## Required Credentials

- googleSheetsOAuth2Api (type only; no credential value stored)
- imap (type only; no credential value stored)
- mindeeReceiptApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Finance
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
