# Instructor Prerequisite: Python Environment & Config Setup

**Audience:** Instructor only — run this before `1_guide.md`. Do not walk students through pip install during the live demo.

**Time Budget:** 2–3 mins

---

## Before you start

Confirm earlier sections are complete:

- Kind cluster `finops-cluster` is running
- kubectl works against the cluster
- Airline app is deployed (Section 02)
- Section 02a scenario is understood

Quick check:

```bash
kubectl cluster-info
kubectl get all -A | grep -v kube-system
```

**What it does:** Verifies cluster connectivity and that airline workloads are running.

---

## 1) Set up the Python environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r sections/04-local-python-agent/requirements.txt
```

**What it does:** Creates a virtualenv and installs the Kubernetes Python client plus dependencies.

---

## 2) Inspect the tagging rules

```bash
cat sections/04-local-python-agent/config/tagging-rules.yaml
```

**What it does:** Shows the policy the agent checks against — required labels like `owner`, `cost-center`, `tier`, and `environment`.

> *Talking point: "These rules define what 'good' looks like. The collector reads the cluster; the rules say what is missing."*

---

## 3) Inspect the collector code

```bash
cat sections/04-local-python-agent/agent/collect.py
```

**What it does:** Shows the Python code that reads the cluster. The collector uses the Kubernetes Python client to dump resources as JSON — no kubectl needed.

> *Talking point: "We are not doing analysis here. The collector just dumps raw data. Logic comes later."*

---

## 4) Ready to teach

When setup passes, start the live walkthrough with:

- `1_guide.md` — Run the collector
- `2_guide.md` — Compare to manual kubectl

## Reset for another run (optional)

```bash
rm -f k8s_metadata.json booking_api_metadata.json
```

**What it does:** Cleans up output files from previous runs.
