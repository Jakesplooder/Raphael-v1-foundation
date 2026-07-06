# Archived n8n Workflow WFARCH-2B4ADC0703

## Workflow ID

WFARCH-2B4ADC0703

## Name

1293_Wait_Splitout_Automation_Webhook

## Category

Knowledge

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1293_Wait_Splitout_Automation_Webhook.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 88
- Connections: 91
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`
- `@n8n/n8n-nodes-langchain.embeddingsGoogleGemini`
- `@n8n/n8n-nodes-langchain.informationExtractor`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.textClassifier`
- `@n8n/n8n-nodes-langchain.textSplitterRecursiveCharacterTextSplitter`
- `@n8n/n8n-nodes-langchain.vectorStoreQdrant`
- `n8n-nodes-base.aggregate`
- `n8n-nodes-base.code`
- `n8n-nodes-base.executeWorkflow`
- `n8n-nodes-base.executeWorkflowTrigger`
- `n8n-nodes-base.executionData`
- `n8n-nodes-base.filter`
- `n8n-nodes-base.googleDrive`
- `n8n-nodes-base.googleSheets`
- `n8n-nodes-base.httpRequest`
- `n8n-nodes-base.if`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.removeDuplicates`
- `n8n-nodes-base.set`
- `n8n-nodes-base.splitInBatches`
- `n8n-nodes-base.splitOut`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.switch`
- `n8n-nodes-base.wait`

## API and Service Analysis

- Aggregate
- Code
- Document Default Data Loader
- Embeddings Google Gemini
- Execute Workflow
- Execute Workflow Trigger
- Execution Data
- Filter
- Google Drive
- Google Sheets
- Http Request
- If
- Information Extractor
- Lm Chat Google Gemini
- Manual Trigger
- Remove Duplicates
- Set
- Split In Batches
- Split Out
- Sticky Note
- Switch
- Text Classifier
- Text Splitter Recursive Character Text Splitter
- Vector Store Qdrant
- Wait

## Required Credentials

- googleSheetsOAuth2Api (type only; no credential value stored)

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
