# Archived n8n Workflow WFARCH-15D1D5A86E

## Workflow ID

WFARCH-15D1D5A86E

## Name

0537_Localfile_Wait_Create_Triggered

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0537_Localfile_Wait_Create_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 42
- Connections: 38
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.chainRetrievalQa`
- `@n8n/n8n-nodes-langchain.chainSummarization`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsMistralCloud`
- `@n8n/n8n-nodes-langchain.lmChatMistralCloud`
- `@n8n/n8n-nodes-langchain.outputParserItemList`
- `@n8n/n8n-nodes-langchain.retrieverVectorStore`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `@n8n/n8n-nodes-langchain.vectorStoreQdrant`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.convertToFile`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.localFileTrigger`
- `n8n-nodes-base.merge`
- `n8n-nodes-base.readWriteFile`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.wait`

## API and Service Analysis

- Aggregate
- Chain Llm
- Chain Retrieval Qa
- Chain Summarization
- Convert To File
- Document Default Data Loader
- Embeddings Mistral Cloud
- Extract From File
- Lm Chat Mistral Cloud
- Local File Trigger
- Merge
- Output Parser Item List
- Read Write File
- Retriever Vector Store
- Set
- Split In Batches
- Split Out
- Sticky Note
- Switch
- Text Splitter Recursive Character Text Splitter
- Vector Store Qdrant
- Wait

## Required Credentials

- mistralCloudApi (type only; no credential value stored)
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
