# Archived n8n Workflow WFARCH-AF019B4580

## Workflow ID

WFARCH-AF019B4580

## Name

N8N Financial Tracker Telegram Invoices to Notion with AI Summaries & Reports

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0931_Telegram_Splitout_Monitor_Scheduled.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 28
- Connections: 13
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `n8n-nodes-base.code`
- `n8n-nodes-base.editImage`
- `n8n-nodes-base.notion`
- `n8n-nodes-base.quickChart`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.summarize`
- `n8n-nodes-base.telegram`
- `n8n-nodes-base.telegramTrigger`

## API and Service Analysis

- Chain Llm
- Code
- Edit Image
- Lm Chat Google Gemini
- Notion
- Output Parser Structured
- Quick Chart
- Schedule Trigger
- Split Out
- Sticky Note
- Summarize
- Telegram
- Telegram Trigger

## Required Credentials

- googlePalmApi (type only; no credential value stored)
- notionApi (type only; no credential value stored)
- telegramApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Knowledge
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
