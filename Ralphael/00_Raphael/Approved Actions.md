# Approved Actions

Approved action types Raphael may recommend or prepare after Aaron grants approval. Phase 9 does not execute actions.

| Action Type | Scope | Requires Approval | Notes |
|---|---|---|---|
| Create generated vault notes | Obsidian vault | No | Safe write inside approved vault paths. |
| Update generated Raphael notes | Obsidian vault | No | Controlled by `allow_generated_note_updates`. |
| Read approved folders | Configured read roots | No | Must respect `config/settings.json`. |
| Run safe local analysis | Vault and approved read roots | No | No installs, uploads, deletes, or external side effects. |
