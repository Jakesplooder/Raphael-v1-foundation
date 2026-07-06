# Archived n8n Workflow WFARCH-C947714D13

## Workflow ID

WFARCH-C947714D13

## Name

⚡AI-Powered YouTube Playlist & Video Summarization and Analysis v2

## Category

Creator

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0971_Limit_Splitout_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 72
- Connections: 64
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsGoogleGemini`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `@n8n/n8n-nodes-langchain.toolVectorStore`
- `@n8n/n8n-nodes-langchain.vectorStoreQdrant`
- `n8n-nodes-base.code`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.limit`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.redis`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.summarize`
- `n8n-nodes-base.switch`
- `n8n-nodes-youtube-transcription-dmr.youtubeTranscripter`

## API and Service Analysis

- Agent
- Chain Llm
- Chat Trigger
- Code
- Document Default Data Loader
- Embeddings Google Gemini
- Http Request
- If
- Limit
- Lm Chat Google Gemini
- Memory Buffer Window
- Merge
- Output Parser Structured
- Redis
- Set
- Split Out
- Sticky Note
- Summarize
- Switch
- Text Splitter Recursive Character Text Splitter
- Tool Vector Store
- Vector Store Qdrant
- Youtube Transcripter

## Required Credentials

- googlePalmApi (type only; no credential value stored)
- qdrantApi (type only; no credential value stored)
- redis (type only; no credential value stored)

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
