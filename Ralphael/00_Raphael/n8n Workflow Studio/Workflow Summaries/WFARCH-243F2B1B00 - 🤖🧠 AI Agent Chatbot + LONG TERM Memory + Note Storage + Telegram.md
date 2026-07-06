# Archived n8n Workflow WFARCH-243F2B1B00

## Workflow ID

WFARCH-243F2B1B00

## Name

🤖🧠 AI Agent Chatbot + LONG TERM Memory + Note Storage + Telegram

## Category

Notifications

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

2053_Telegram_Googledocs_Automate_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 21
- Connections: 12
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.googleDocs`
- `n8n-nodes-base.googleDocsTool`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.telegram`

## API and Service Analysis

- Agent
- Aggregate
- Chat Trigger
- Google Docs
- Google Docs Tool
- Lm Chat Open Ai
- Memory Buffer Window
- Merge
- Set
- Sticky Note
- Telegram

## Required Credentials

- googleDocsOAuth2Api (type only; no credential value stored)
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
