#!/bin/bash
# entrypoint.sh - Runs inside the container, supervised by Docker's restart policies

echo "Starting Raphael OS Kernel Daemon..."

# Execute the kernel process
python raphael_core/kernel_daemon.py

# Capture the exit code
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo "=========================================================="
    echo "CRITICAL: Raphael OS Kernel crashed with exit code $EXIT_CODE"
    echo "=========================================================="
    
    # Log the crash reason to the telemetry trace file
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    CRASH_LOG="{\"timestamp\": \"$TIMESTAMP\", \"event\": \"kernel_crash\", \"exit_code\": $EXIT_CODE, \"message\": \"Daemon crashed unexpectedly and is awaiting Docker restart.\"}"
    
    mkdir -p .system_generated
    echo "$CRASH_LOG" >> .system_generated/traces.jsonl
    
    # Exit non-zero so Docker knows to trigger the restart policy
    exit $EXIT_CODE
fi

exit 0
