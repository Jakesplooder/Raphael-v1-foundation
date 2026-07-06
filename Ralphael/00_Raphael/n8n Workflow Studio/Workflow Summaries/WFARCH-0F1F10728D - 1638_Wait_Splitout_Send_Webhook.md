# Archived n8n Workflow WFARCH-0F1F10728D

## Workflow ID

WFARCH-0F1F10728D

## Name

1638_Wait_Splitout_Send_Webhook

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1638_Wait_Splitout_Send_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 35
- Connections: 26
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.toolWikipedia`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.wait`
- `n8n-nodes-base.whatsApp`
- `n8n-nodes-base.whatsAppTrigger`

## API and Service Analysis

- Agent
- Chain Llm
- Http Request
- Lm Chat Google Gemini
- Memory Buffer Window
- Set
- Split Out
- Sticky Note
- Switch
- Tool Wikipedia
- Wait
- Whats App
- Whats App Trigger

## Required Credentials

- googlePalmApi (type only; no credential value stored)
- whatsAppApi (type only; no credential value stored)
- whatsAppTriggerApi (type only; no credential value stored)

## Reuse Assessment

- Reusable trigger/transform pattern: Yes
- Category relationship: Automation
- The workflow exposes a standard node list for structural analysis.
- Review node settings, platform terms, privacy, rate limits, and credential requirements before any manual use.

## Safety

- Source modified: no
- Workflow imported into n8n: no
- Workflow activated: no
- Workflow executed: no
- Credential values stored: no
- External APIs called: no
