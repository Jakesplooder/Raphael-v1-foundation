# n8n Workflow WF-1C2500D05B

## Workflow ID

WF-1C2500D05B

## Name

Agency lead intake architecture

## Category

Agency

## Status

Plan Only

## Purpose

Create an inactive n8n workflow draft that supports: Agency lead intake architecture.

## Inputs

- Operator-supplied records or trigger data
- Manually configured non-secret workflow settings

## Outputs

- Validated internal workflow result
- Draft export data for operator review

## Nodes

| Node | Type | Purpose |
|---|---|---|
| Start | `n8n-nodes-base.manualTrigger` | Start only when an operator later imports and explicitly configures the draft. |
| Load Input | `n8n-nodes-base.set` | Define or normalize workflow inputs without embedding secrets. |
| Transform Data | `n8n-nodes-base.code` | Apply deterministic data transformation logic. |
| Validate Output | `n8n-nodes-base.if` | Check required fields before any downstream handoff. |
| Draft Result | `n8n-nodes-base.set` | Produce an internal draft result only. |

## Required Credentials

- None required by the current draft.

## Risks

- External service schemas may differ from the placeholders.
- A future operator could activate the workflow without completing review.
- Rate limits, privacy rules, and platform terms require manual validation.
- Generated transformation logic is a draft and requires testing in a safe n8n environment.

## Business Use

- Category: Agency
- Use the draft as an architecture starting point and review it before manual import.
- Keep platform actions, outreach, publishing, financial actions, and external calls unconfigured.

## Suggested JSON Structure

```json
{
  "name": "Draft - Agency lead intake architecture",
  "active": false,
  "nodes": [
    {
      "id": "WF-1C2500D05B-NODE-1",
      "name": "Start",
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [
        0,
        0
      ],
      "parameters": {},
      "disabled": true
    },
    {
      "id": "WF-1C2500D05B-NODE-2",
      "name": "Load Input",
      "type": "n8n-nodes-base.set",
      "typeVersion": 1,
      "position": [
        260,
        0
      ],
      "parameters": {
        "assignments": {
          "assignments": []
        },
        "options": {}
      },
      "disabled": true
    },
    {
      "id": "WF-1C2500D05B-NODE-3",
      "name": "Transform Data",
      "type": "n8n-nodes-base.code",
      "typeVersion": 1,
      "position": [
        520,
        0
      ],
      "parameters": {
        "jsCode": "// Draft only. Add reviewed transformation logic before manual import.\\nreturn $input.all();"
      },
      "disabled": true
    },
    {
      "id": "WF-1C2500D05B-NODE-4",
      "name": "Validate Output",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [
        780,
        0
      ],
      "parameters": {
        "conditions": {
          "options": {},
          "conditions": [],
          "combinator": "and"
        },
        "options": {}
      },
      "disabled": true
    },
    {
      "id": "WF-1C2500D05B-NODE-5",
      "name": "Draft Result",
      "type": "n8n-nodes-base.set",
      "typeVersion": 1,
      "position": [
        1040,
        0
      ],
      "parameters": {
        "assignments": {
          "assignments": []
        },
        "options": {}
      },
      "disabled": true
    }
  ],
  "connections": {
    "Start": {
      "main": [
        [
          {
            "node": "Load Input",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Load Input": {
      "main": [
        [
          {
            "node": "Transform Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Transform Data": {
      "main": [
        [
          {
            "node": "Validate Output",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Validate Output": {
      "main": [
        [
          {
            "node": "Draft Result",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "settings": {
    "executionOrder": "v1"
  },
  "meta": {
    "raphaelWorkflowId": "WF-1C2500D05B",
    "draftOnly": true,
    "credentialsStored": false,
    "activationAuthorized": false
  },
  "pinData": {}
}
```

## Workflow Diagram

```mermaid
flowchart LR
    N0["Start"]
    N1["Load Input"]
    N0 --> N1
    N2["Transform Data"]
    N1 --> N2
    N3["Validate Output"]
    N2 --> N3
    N4["Draft Result"]
    N3 --> N4
```

## JSON Draft

Not generated. Run `n8n-workflow-generate` to create an inactive JSON draft.

## Safety

- Executed: no
- Activated: no
- Credentials stored: no
- External calls made: no
- Source workflows modified: no
