# Archived n8n Workflow WFARCH-2643C7D6FD

## Workflow ID

WFARCH-2643C7D6FD

## Name

Telegram Chat with Buffering

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1411_Telegram_Wait_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 22
- Connections: 12
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryPostgresChat`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.if`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.sort`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.supabase`
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.telegramTrigger`
- `n8n-nodes-base.wait`

## API and Service Analysis

- Agent
- Aggregate
- If
- Lm Chat Open Ai
- Memory Postgres Chat
- No Op
- Sort
- Sticky Note
- Supabase
- Telegram
- Telegram Trigger
- Wait

## Required Credentials

- openAiApi (type only; no credential value stored)
- postgres (type only; no credential value stored)
- supabaseApi (type only; no credential value stored)
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
