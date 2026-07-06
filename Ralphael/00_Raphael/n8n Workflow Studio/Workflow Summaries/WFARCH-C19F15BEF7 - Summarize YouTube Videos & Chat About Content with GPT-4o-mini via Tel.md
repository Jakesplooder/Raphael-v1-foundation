# Archived n8n Workflow WFARCH-C19F15BEF7

## Workflow ID

WFARCH-C19F15BEF7

## Name

Summarize YouTube Videos & Chat About Content with GPT-4o-mini via Telegram

## Category

Creator

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1533_Telegram_Splitout_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 22
- Connections: 16
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `n8n-nodes-base.code`
- `n8n-nodes-base.googleDocs`
- `n8n-nodes-base.googleDocsTool`
- `n8n-nodes-base.respondToWebhook`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.summarize`
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.telegramTrigger`
- `n8n-nodes-base.webhook`
- `n8n-nodes-youtube-transcription-kasha.youtubeTranscripter`

## API and Service Analysis

- Agent
- Chain Llm
- Chat Trigger
- Code
- Google Docs
- Google Docs Tool
- Lm Chat Open Ai
- Memory Buffer Window
- Respond To Webhook
- Set
- Split Out
- Sticky Note
- Summarize
- Telegram
- Telegram Trigger
- Webhook
- Youtube Transcripter

## Required Credentials

- googleDocsOAuth2Api (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- telegramApi (type only; no credential value stored)

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
