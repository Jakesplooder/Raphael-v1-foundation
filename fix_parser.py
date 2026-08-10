import os
from pathlib import Path

LEGACY_PATH = Path(r"R:\RalphaelOS_Repo\raphael_core\legacy.py")

with open(LEGACY_PATH, "r", encoding="utf-8") as f:
    leg = f.read()

# Remove the duplicate build-status add_parser I injected
leg = leg.replace('sub.add_parser("build-status", help="Show status of a Builder workspace")\n', '')

# Remove the duplicate elif args.command == "build-status": I injected
leg = leg.replace('''elif args.command == "build-status":
            print(f"Builder Workspace Status for {args.tail[0]}\\nPreview: index.html\\nRun Instructions: Open index.html")
        ''', '')

with open(LEGACY_PATH, "w", encoding="utf-8") as f:
    f.write(leg)

print("Parser fixed")
