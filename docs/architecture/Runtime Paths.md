# Runtime Paths

| Purpose | Default |
|---|---|
| CLI | Repository `raphael.py` |
| Vault | `vault_path` |
| Runtime | `runtime_path` |
| Dashboard | `<runtime>/dashboard` |
| Builder requests | `<runtime>/builder/requests` |
| Builder workspace | `builder_workspace` |
| POD runtime | `<runtime>/PODStudio` |
| POD typography/composition | `<runtime>/PODStudio/working/typography` |
| Asset runtime | `<runtime>/BrandLibrary` |
| Voice gateway | `<runtime>/voice_gateway.py` |
| Command Bus | `<runtime>/command_bus.py` |
| Bootstrap launcher | `<runtime>/launcher` |
| Managed service PID registry | `<runtime>/launcher/runtime/service_pids.json` |

The test harness redirects all writable paths to temporary directories.
