# Archived n8n Workflow WFARCH-309BC54BED

## Workflow ID

WFARCH-309BC54BED

## Name

Google Drive Automation

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1906_Code_Extractfromfile_Automate_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 14
- Connections: 12
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.chatTrigger`
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsGoogleGemini`
- `@n8n/n8n-nodes-langchain.lmChatOpenRouter`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `@n8n/n8n-nodes-langchain.vectorStorePinecone`
- `n8n-nodes-base.code`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.googleDriveTrigger`

## API and Service Analysis

- Agent
- Chat Trigger
- Code
- Document Default Data Loader
- Embeddings Google Gemini
- Extract From File
- Google Drive
- Google Drive Trigger
- Lm Chat Open Router
- Text Splitter Recursive Character Text Splitter
- Vector Store Pinecone

## Required Credentials

- googleDriveOAuth2Api (type only; no credential value stored)
- googlePalmApi (type only; no credential value stored)
- openRouterApi (type only; no credential value stored)
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
