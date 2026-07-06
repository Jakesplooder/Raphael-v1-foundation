# Archived n8n Workflow WFARCH-1DD314EB9A

## Workflow ID

WFARCH-1DD314EB9A

## Name

0884_Telegram_Filter_Export_Triggered

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0884_Telegram_Filter_Export_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 17
- Connections: 11
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenRouter`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.gmailTool`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.telegramTrigger`

## API and Service Analysis

- Agent
- Aggregate
- Filter
- Gmail
- Gmail Tool
- Lm Chat Open Router
- Manual Trigger
- Sticky Note
- Telegram
- Telegram Trigger

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
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
