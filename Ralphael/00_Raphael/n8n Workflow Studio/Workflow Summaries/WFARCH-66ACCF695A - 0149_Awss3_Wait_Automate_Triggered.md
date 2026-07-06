# Archived n8n Workflow WFARCH-66ACCF695A

## Workflow ID

WFARCH-66ACCF695A

## Name

0149_Awss3_Wait_Automate_Triggered

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0149_Awss3_Wait_Automate_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 8
- Connections: 7
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `n8n-nodes-base.awsS3`
- `n8n-nodes-base.awsTranscribe`
- `n8n-nodes-base.googleDriveTrigger`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.set`
- `n8n-nodes-base.wait`

## API and Service Analysis

- Aws S3
- Aws Transcribe
- Google Drive Trigger
- Google Sheets
- Set
- Wait

## Required Credentials

- aws (type only; no credential value stored)
- googleDriveOAuth2Api (type only; no credential value stored)
- googleSheetsOAuth2Api (type only; no credential value stored)

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
