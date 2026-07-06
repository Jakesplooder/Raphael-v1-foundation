# Archived n8n Workflow WFARCH-A3F868DB2B

## Workflow ID

WFARCH-A3F868DB2B

## Name

Play with Spotify from Telegram

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1448_Telegram_Stickynote_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 14
- Connections: 18
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.openAi`
- `n8n-nodes-base.if`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.set`
- `n8n-nodes-base.spotify`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.telegramTrigger`

## API and Service Analysis

- If
- Merge
- Open Ai
- Set
- Spotify
- Sticky Note
- Telegram
- Telegram Trigger

## Required Credentials

- openAiApi (type only; no credential value stored)
- spotifyOAuth2Api (type only; no credential value stored)
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
