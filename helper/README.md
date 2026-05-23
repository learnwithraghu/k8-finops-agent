# Helper Scripts

Use these scripts to clean up the local teaching environment.

## cleanup.sh
Removes the Kind cluster, lesson namespaces, project Docker images, and optional Docker leftovers.

Examples:
```bash
bash helper/cleanup.sh
bash helper/cleanup.sh --yes
bash helper/cleanup.sh --yes --aggressive
```
