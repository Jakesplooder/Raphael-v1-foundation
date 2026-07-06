# Archived n8n Workflow WFARCH-D3EE9E1EA5

## Workflow ID

WFARCH-D3EE9E1EA5

## Name

Telegram-bot AI Da Nang

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1380_Telegram_Code_Automate_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 23
- Connections: 14
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.lmChatOpenRouter`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `n8n-nodes-base.code`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.telegramTrigger`

## API and Service Analysis

- Agent
- Chat Trigger
- Code
- Google Sheets
- Lm Chat Open Router
- Memory Buffer Window
- No Op
- Set
- Sticky Note
- Switch
- Telegram
- Telegram Trigger

## Required Credentials

- googleSheetsOAuth2Api (type only; no credential value stored)
- openRouterApi (type only; no credential value stored)
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
