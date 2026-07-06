# Archived n8n Workflow WFARCH-839E70B71B

## Workflow ID

WFARCH-839E70B71B

## Name

Supabase Setup Postgres

## Category

Automation

## Status

Cataloged from read-only archive

## Source

K:\n8n-workflows-main\n8n-workflows-main\workflows

## Source Workflow

1866_Manual_Supabase_Automation_Triggered.json

## Purpose

Reusable automation candidate inferred from the workflow name and node composition.

## Node Analysis

- Nodes: 6
- Connections: 5
- Source marked active: False (not activated or imported by Raphael)
- Standard n8n workflow schema detected: True

- `@n8n/n8n-nodes-langchain.agent`
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`
- `@n8n/n8n-nodes-langchain.memoryPostgresChat`
- `n8n-nodes-base.manualTrigger`
- `n8n-nodes-base.set`
- `n8n-nodes-base.supabase`

## API and Service Analysis

- Agent
- Lm Chat Google Gemini
- Manual Trigger
- Memory Postgres Chat
- Set
- Supabase

## Required Credentials

- googlePalmApi (type only; no credential value stored)
- postgres (type only; no credential value stored)
- supabaseApi (type only; no credential value stored)

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
