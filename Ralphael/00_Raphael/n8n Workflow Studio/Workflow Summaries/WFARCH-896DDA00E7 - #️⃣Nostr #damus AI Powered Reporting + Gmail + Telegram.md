# Archived n8n Workflow WFARCH-896DDA00E7

## Workflow ID

WFARCH-896DDA00E7

## Name

#️⃣Nostr #damus AI Powered Reporting + Gmail + Telegram

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

C:\RaphaelOS\n8n-archive-smoke.zip

## Source Workflow

0001_Telegram_Schedule_Automation_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 24
- Connections: 17
- Source marked active: True (not activated or imported by Raphael)

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.markdown`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.telegram`
- `n8n-nodes-nostrobots.nostrobotsread`

## API and Service Analysis

- Aggregate
- Chain Llm
- Gmail
- Lm Chat Google Gemini
- Manual Trigger
- Markdown
- Merge
- Nostrobotsread
- Schedule Trigger
- Sticky Note
- Telegram

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- googlePalmApi (type only; no credential value stored)
- telegramApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Notifications
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
