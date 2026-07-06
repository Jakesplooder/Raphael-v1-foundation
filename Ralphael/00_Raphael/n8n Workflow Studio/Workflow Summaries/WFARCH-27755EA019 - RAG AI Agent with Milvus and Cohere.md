# Archived n8n Workflow WFARCH-27755EA019

## Workflow ID

WFARCH-27755EA019

## Name

RAG AI Agent with Milvus and Cohere

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

0741_Extractfromfile_Stickynote_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 14
- Connections: 11
- Source marked active: True (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsCohere`
- `@n8n/n8n-nodes-langchain.lmChatOpenAi`
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `@n8n/n8n-nodes-langchain.vectorStoreMilvus`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.googleDriveTrigger`
- `n8n-nodes-base.stickyNote`

## API and Service Analysis

- Agent
- Chat Trigger
- Document Default Data Loader
- Embeddings Cohere
- Extract From File
- Google Drive
- Google Drive Trigger
- Lm Chat Open Ai
- Memory Buffer Window
- Sticky Note
- Text Splitter Recursive Character Text Splitter
- Vector Store Milvus

## Required Credentials

- cohereApi (type only; no credential value stored)
- googleDriveOAuth2Api (type only; no credential value stored)
- milvusApi (type only; no credential value stored)
- openAiApi (type only; no credential value stored)

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
