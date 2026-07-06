# Archived n8n Workflow WFARCH-35219E7BFB

## Workflow ID

WFARCH-35219E7BFB

## Name

🐋DeepSeek V3 Chat & R1 Reasoning Quick Start

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1519_HTTP_Stickynote_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 15
- Connections: 4
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.lmChatOllama`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Chain Llm
- Chat Trigger
- Http Request
- Lm Chat Ollama
- Lm Chat Open Ai
- Memory Buffer Window
- Sticky Note

## Required Credentials

- httpHeaderAuth (type only; no credential value stored)
- ollamaApi (type only; no credential value stored)
- openAiApi (type only; no credential value stored)

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
