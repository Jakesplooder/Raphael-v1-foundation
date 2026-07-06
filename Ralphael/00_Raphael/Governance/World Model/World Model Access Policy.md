# World Model Access Policy

```json
{
  "version": 1,
  "agents": {
    "Aaron": {
      "trust_tier": 4,
      "roles": [
        "owner"
      ],
      "allowed_node_types": [
        "*"
      ]
    },
    "Raphael Core": {
      "trust_tier": 4,
      "roles": [
        "core"
      ],
      "allowed_node_types": [
        "*"
      ]
    },
    "Executive Agent": {
      "trust_tier": 3,
      "roles": [
        "executive"
      ],
      "allowed_node_types": [
        "*"
      ]
    },
    "Research Agent": {
      "trust_tier": 2,
      "roles": [
        "research"
      ],
      "allowed_node_types": [
        "Goal",
        "Project",
        "Business",
        "Workflow",
        "Service",
        "Resource",
        "KnowledgeItem",
        "Hypothesis",
        "Event"
      ]
    },
    "Standard Agent": {
      "trust_tier": 1,
      "roles": [
        "standard"
      ],
      "allowed_node_types": [
        "Goal",
        "Project",
        "Task",
        "Workflow",
        "Service",
        "Resource"
      ]
    },
    "Unknown Agent": {
      "trust_tier": 0,
      "roles": [
        "unknown"
      ],
      "allowed_node_types": [
        "Goal",
        "Project"
      ]
    }
  },
  "base_rate_limits_per_hour": {
    "Research Agent": 80,
    "Executive Agent": 150,
    "Standard Agent": 30,
    "Unknown Agent": 10
  },
  "trust_multipliers": {
    "0": 0.5,
    "1": 0.75,
    "2": 1.0,
    "3": 1.5,
    "4": 2.0
  },
  "burst_warning_per_minute": 10,
  "burst_block_per_minute": 25
}
```
