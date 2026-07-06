# Archived n8n Workflow WFARCH-3B513B4BB9

## Workflow ID

WFARCH-3B513B4BB9

## Name

AI Email processing autoresponder with approval (Yes/No)

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1284_Emailreadimap_Markdown_Send.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 17
- Connections: 12
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chainSummarization`
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.vectorStoreQdrant`
- `n8n-nodes-base.emailReadImap`
- `n8n-nodes-base.emailSend`
- `n8n-nodes-base.gmail`
- `n8n-nodes-base.if`
- `n8n-nodes-base.markdown`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Chain Summarization
- Email Read Imap
- Email Send
- Embeddings Open Ai
- Gmail
- If
- Lm Chat Open Ai
- Markdown
- Set
- Sticky Note
- Vector Store Qdrant

## Required Credentials

- gmailOAuth2 (type only; no credential value stored)
- imap (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- qdrantApi (type only; no credential value stored)
- smtp (type only; no credential value stored)

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
