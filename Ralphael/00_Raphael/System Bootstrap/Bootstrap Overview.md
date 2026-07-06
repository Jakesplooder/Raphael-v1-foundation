# Raphael Bootstrap Overview

The bootstrap supervisor starts and stops only explicitly allowlisted local
Raphael support services. PID ownership is recorded before a managed process
may be stopped.

Voice Gateway is disabled by default. Ollama and Qdrant are checked but are not
force-started or stopped.
