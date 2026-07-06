# Safety Boundaries

Phase 64C does not change Raphael's authority or execution model.

- Approved read/write roots remain enforced.
- `K:/` can be read when configured but is not an approved write root.
- Builder generation remains inside `builder_workspace`.
- POD artifacts remain inside configured POD vault/runtime roots.
- Asset imports do not alter source originals.
- External execution remains disabled.
- n8n execution, activation, credential storage, and external calls remain disabled.
- Publishing, uploads, spending, email, installs, credentials, and arbitrary shell commands remain blocked.
- Dashboard Chat continues to route through Command Bus without fallback.
- Existing confirmation gates remain active.

Tests replace all writable paths with temporary vault/runtime roots.
