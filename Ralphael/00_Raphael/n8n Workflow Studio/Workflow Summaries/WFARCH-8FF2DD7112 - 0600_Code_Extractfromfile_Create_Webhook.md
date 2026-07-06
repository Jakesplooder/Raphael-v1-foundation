# Archived n8n Workflow WFARCH-8FF2DD7112

## Workflow ID

WFARCH-8FF2DD7112

## Name

0600_Code_Extractfromfile_Create_Webhook

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0600_Code_Extractfromfile_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 50
- Connections: 37
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`
- `@n8n/n8n-nodes-langchain.informationExtractor`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `@n8n/n8n-nodes-langchain.toolVectorStore`
- `@n8n/n8n-nodes-langchain.vectorStoreQdrant`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.airtable`
- `n8n-nodes-base.airtableTool`
- `n8n-nodes-base.airtableTrigger`
- `n8n-nodes-base.code`
- `n8n-nodes-base.compression`
- `n8n-nodes-base.convertToFile`
- `n8n-nodes-base.editImage`
- `n8n-nodes-base.executeWorkflow`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.noOp`
- `n8n-nodes-base.set`
- `n8n-nodes-base.sort`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Aggregate
- Airtable
- Airtable Tool
- Airtable Trigger
- Chain Llm
- Chat Trigger
- Code
- Compression
- Convert To File
- Document Default Data Loader
- Edit Image
- Embeddings Open Ai
- Execute Workflow
- Execute Workflow Trigger
- Extract From File
- Http Request
- If
- Information Extractor
- Lm Chat Open Ai
- Manual Trigger
- Memory Buffer Window
- Merge
- No Op
- Set
- Sort
- Sticky Note
- Text Splitter Recursive Character Text Splitter
- Tool Vector Store
- Vector Store Qdrant

## Required Credentials

- airtableTokenApi (type only; no credential value stored)
- openAiApi (type only; no credential value stored)
- qdrantApi (type only; no credential value stored)

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
