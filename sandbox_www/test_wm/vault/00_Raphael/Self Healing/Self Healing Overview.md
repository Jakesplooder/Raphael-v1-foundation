# Self Healing Overview

Raphael observes local operational health, explains detected issues, prepares
safe repair plans, and only runs allowlisted local repairs after approval.

## Safety Boundary

- No repair runs without approval
- No arbitrary shell commands
- No deleting user files
- No publishing, uploading, spending, account access, or credentials
- No killing unmanaged processes
- No Docker prune
- Repairs are restricted to fixed allowlisted actions
