# Archived n8n Workflow WFARCH-9FBB3560CF

## Workflow ID

WFARCH-9FBB3560CF

## Name

0768_Telegram_Stickynote_Create_Triggered

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0768_Telegram_Stickynote_Create_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 13
- Connections: 10
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.openAi`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.telegramTrigger`
- `n8n-nodes-base.todoist`

## API and Service Analysis

- Chain Llm
- Lm Chat Open Ai
- Open Ai
- Output Parser Structured
- Set
- Sticky Note
- Switch
- Telegram
- Telegram Trigger
- Todoist

## Required Credentials

- openAiApi (type only; no credential value stored)
- telegramApi (type only; no credential value stored)
- todoistApi (type only; no credential value stored)

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
