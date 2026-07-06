# Archived n8n Workflow WFARCH-57D04885B0

## Workflow ID

WFARCH-57D04885B0

## Name

google drive to instagram, tiktok and youtube

## Category

Creator

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1237_Error_Telegram_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 15
- Connections: 12
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.openAi`
- `n8n-nodes-base.errorTrigger`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.googleDriveTrigger`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.readBinaryFile`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.writeBinaryFile`

## API and Service Analysis

- Error Trigger
- Google Drive
- Google Drive Trigger
- Http Request
- If
- Open Ai
- Read Binary File
- Sticky Note
- Telegram
- Write Binary File

## Required Credentials

- googleDriveOAuth2Api (type only; no credential value stored)
- httpHeaderAuth (type only; no credential value stored)
- openAiApi (type only; no credential value stored)

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
