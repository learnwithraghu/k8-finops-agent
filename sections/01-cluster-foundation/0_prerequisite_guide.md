# Instructor Prerequisite: Tool Verification & Cleanup

**Audience:** Instructor only — run this before `1_guide.md`. Do not walk students through tool installation during the live demo.

**Time Budget:** 1–2 mins

---

## Before you start

Ensure these tools are installed on your machine:

- Docker (or Docker Desktop)
- Kind
- kubectl
- Helm

If you are unsure, run the checks below.

---

## 1) Clean old Kind clusters

```bash
./helper/local-kind/cleanup.sh --yes
```

**What it does:** Removes any leftover Kind clusters from previous runs so the demo starts clean.

---

## 2) Verify Docker is running

```bash
docker info
```

**What it does:** Confirms the Docker daemon is active. Kind needs Docker to create clusters.

> *If this fails, start Docker Desktop or run `systemctl start docker` on Linux.*

---

## 3) Verify tools are installed

```bash
kind version
kubectl version --client
helm version --short
```

**What it does:** Confirms Kind, kubectl, and Helm are available. Versions do not matter as long as the commands succeed.

---

## 4) Ready to teach

When all checks pass, start the live walkthrough with:

- `1_guide.md` — Create the Kind cluster
- `2_guide.md` — Create namespaces
- `3_guide.md` — Verify the baseline
