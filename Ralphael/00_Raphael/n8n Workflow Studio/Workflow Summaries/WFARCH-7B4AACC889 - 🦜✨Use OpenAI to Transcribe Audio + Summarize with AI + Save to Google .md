# Archived n8n Workflow WFARCH-7B4AACC889

## Workflow ID

WFARCH-7B4AACC889

## Name

🦜✨Use OpenAI to Transcribe Audio + Summarize with AI + Save to Google Drive

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1368_Telegram_Limit_Export_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 33
- Connections: 26
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.openAi`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.googleDriveTrigger`
- `n8n-nodes-base.limit`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.telegram`

## API and Service Analysis

- Filter
- Gmail
- Google Drive
- Google Drive Trigger
- Limit
- Manual Trigger
- Merge
- Open Ai
- Set
- Sticky Note
- Telegram

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- googleDriveOAuth2Api (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- telegramApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Notifications
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
