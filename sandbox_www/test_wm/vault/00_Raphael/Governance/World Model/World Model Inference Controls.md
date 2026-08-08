# World Model Inference Controls

```json
{
  "version": 1,
  "sensitive_correlations": [
    [
      "Finance",
      "Health"
    ],
    [
      "Finance",
      "Journal"
    ],
    [
      "Finance",
      "Schedule"
    ],
    [
      "Revenue",
      "Personal Events"
    ],
    [
      "Relationship Data",
      "External Agent"
    ],
    [
      "Journal",
      "Any Non-Core Agent"
    ],
    [
      "Health",
      "Productivity"
    ],
    [
      "Location",
      "Schedule"
    ],
    [
      "Private Notes",
      "Business Performance"
    ]
  ],
  "owners": [
    "Aaron"
  ],
  "blocked_actions": [
    "spend_money",
    "publish",
    "upload",
    "message_people",
    "create_accounts",
    "modify_safety_policy",
    "bypass_approvals",
    "bypass_workflow_runner",
    "bypass_command_bus"
  ]
}
```
