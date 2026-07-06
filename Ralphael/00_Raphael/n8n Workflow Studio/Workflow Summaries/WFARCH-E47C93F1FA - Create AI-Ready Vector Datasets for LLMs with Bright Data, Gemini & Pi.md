# Archived n8n Workflow WFARCH-E47C93F1FA

## Workflow ID

WFARCH-E47C93F1FA

## Name

Create AI-Ready Vector Datasets for LLMs with Bright Data, Gemini & Pinecone

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0933_Manual_Stickynote_Create_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 21
- Connections: 17
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chainLlm`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsGoogleGemini`
- `@n8n/n8n-nodes-langchain.informationExtractor`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.outputParserStructured`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `@n8n/n8n-nodes-langchain.vectorStorePinecone`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Chain Llm
- Document Default Data Loader
- Embeddings Google Gemini
- Http Request
- Information Extractor
- Lm Chat Google Gemini
- Manual Trigger
- Output Parser Structured
- Set
- Sticky Note
- Text Splitter Recursive Character Text Splitter
- Vector Store Pinecone

## Required Credentials

- googlePalmApi (type only; no credential value stored)
- httpHeaderAuth (type only; no credential value stored)
- pineconeApi (type only; no credential value stored)

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
