# Archived n8n Workflow WFARCH-FE41C3FD5B

## Workflow ID

WFARCH-FE41C3FD5B

## Name

RAG & GenAI App With WordPress Content

## Category

Creator

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1752_Postgres_Wordpress_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 53
- Connections: 45
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryPostgresChat`
- `@n8n/n8n-nodes-langchain.textSplitterTokenSplitter`
- `@n8n/n8n-nodes-langchain.vectorStoreSupabase`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.markdown`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.postgres`
- `n8n-nodes-base.respondToWebhook`
- `n8n-nodes-base.scheduleTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.supabase`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.wordpress`

## API and Service Analysis

- Agent
- Aggregate
- Chat Trigger
- Document Default Data Loader
- Embeddings Open Ai
- Filter
- Http Request
- Lm Chat Open Ai
- Manual Trigger
- Markdown
- Memory Postgres Chat
- Merge
- Postgres
- Respond To Webhook
- Schedule Trigger
- Set
- Split In Batches
- Sticky Note
- Supabase
- Switch
- Text Splitter Token Splitter
- Vector Store Supabase
- Wordpress

## Required Credentials

- None declared in source workflow.

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
