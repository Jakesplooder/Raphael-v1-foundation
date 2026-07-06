# Archived n8n Workflow WFARCH-C1650FC709

## Workflow ID

WFARCH-C1650FC709

## Name

Fetch the Most Recent Document from Google Drive

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1806_GoogleDrive_GoogleSheets_Import_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 12
- Connections: 5
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.openAi`
- `@n8n/n8n-nodes-langchain.toolCalculator`
- `@n8n/n8n-nodes-langchain.toolWikipedia`
- `n8n-nodes-base.googleDocs`
- `n8n-nodes-base.googleDriveTrigger`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Google Docs
- Google Drive Trigger
- Google Sheets
- Open Ai
- Sticky Note
- Tool Calculator
- Tool Wikipedia

## Required Credentials

- googleDocsOAuth2Api (type only; no credential value stored)
- googleDriveOAuth2Api (type only; no credential value stored)
- googleSheetsOAuth2Api (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Knowledge
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
