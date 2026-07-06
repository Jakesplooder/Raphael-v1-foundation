# Archived n8n Workflow WFARCH-3DFF2EA148

## Workflow ID

WFARCH-3DFF2EA148

## Name

Load Prompts from Github Repo and auto populate n8n expressions

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1453_Stopanderror_Code_Import_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 17
- Connections: 12
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatOllama`
- `n8n-nodes-base.code`
- `n8n-nodes-base.extractFromFile`
- `n8n-nodes-base.github`
- `n8n-nodes-base.if`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.stickyNote`
- `n8n-nodes-base.stopAndError`

## API and Service Analysis

- Agent
- Code
- Extract From File
- Github
- If
- Lm Chat Ollama
- Manual Trigger
- Set
- Sticky Note
- Stop And Error

## Required Credentials

- githubApi (type only; no credential value stored)
- ollamaApi (type only; no credential value stored)

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
