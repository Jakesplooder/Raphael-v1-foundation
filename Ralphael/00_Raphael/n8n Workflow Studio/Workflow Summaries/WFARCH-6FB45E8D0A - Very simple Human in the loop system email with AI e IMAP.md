# Archived n8n Workflow WFARCH-6FB45E8D0A

## Workflow ID

WFARCH-6FB45E8D0A

## Name

Very simple Human in the loop system email with AI e IMAP

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1571_Markdown_Stickynote_Send.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 16
- Connections: 9
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chainSummarization`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `n8n-nodes-base.emailReadImap`
- `n8n-nodes-base.emailSend`
- `n8n-nodes-base.if`
- `n8n-nodes-base.markdown`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Chain Summarization
- Email Read Imap
- Email Send
- If
- Lm Chat Open Ai
- Markdown
- Set
- Sticky Note

## Required Credentials

- imap (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- smtp (type only; no credential value stored)

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
