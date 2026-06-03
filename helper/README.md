# Helper Scripts

Scripts for managing the local teaching environment.

## setup-to-02.sh
Spins up the full environment through Section 02a in one go:
1. Validates prerequisites (docker, kind, kubectl, helm)
2. Creates the Kind cluster `finops-cluster`
3. Creates all app namespaces
4. Deploys Section 02 — Airline App
5. Deploys Section 02a — Payment Gateway (broken API scenario)

Examples:
```bash
bash helper/setup-to-02.sh           # interactive (asks for confirmation)
bash helper/setup-to-02.sh --yes     # skip confirmation prompts
```

---

## cleanup.sh
Removes the Kind cluster, lesson namespaces, project Docker images, and optional Docker leftovers.

Examples:
```bash
bash helper/cleanup.sh
bash helper/cleanup.sh --yes
bash helper/cleanup.sh --yes --aggressive
```
