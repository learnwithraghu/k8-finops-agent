# Instructor Prerequisite: MCP Image & Python Environment

**Audience:** Instructor only — run this before `0_guide.md`. Do not walk students through Docker pulls or pip install during the live demo.

**Time Budget:** 2–3 mins

---

## Before you start

Confirm earlier sections are complete:

- Kind cluster `finops-cluster` is running
- kubectl works against the cluster

Quick check:

```bash
kubectl cluster-info
kubectl get namespaces
```

**What it does:** Verifies cluster connectivity and that expected namespaces are present.

---

## 1) Pull the MCP image

```bash
docker pull mcp/kubernetes:latest
```

**What it does:** Downloads the Kubernetes MCP server image. Section 06 runs it with native Streamable HTTP — no Supergateway.

> *Talking point: "Same image as Section 05 — we just enable HTTP directly instead of wrapping stdio with Supergateway."*

---

## 2) Set up the Python virtualenv

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**What it does:** Creates a virtualenv at the repo root and installs dependencies from the repo-root `requirements.txt` (including `mcp`, `langchain-mcp-tools`, `langgraph`, `openai`, and `python-dotenv`).

> *Re-activate in new shells with: `source .venv/bin/activate`*

---

## 3) Confirm API key is set

```bash
test -n "$OPENAI_API_KEY" && echo "API key is set" || echo "OPENAI_API_KEY is not set"
```

**What it does:** Checks that the OpenAI API key environment variable is present. The agent scripts also load the repo-root `.env` through `code/mcp_client.py`.

> *If using a `.env` file, confirm it exists at the repo root: `grep OPENAI .env`*

---

## 4) Inspect the scripts

```bash
cat sections/06-mcp-data-agent/code/mcp_client.py
cat sections/06-mcp-data-agent/code/validate_mcp.py
cat sections/06-mcp-data-agent/code/query_agent.py
cat sections/06-mcp-data-agent/code/snapshot_collector.py
```

**What it does:** Shows the four files in the section's `code/` folder — shared MCP wiring, validation script, query agent, and inventory agent.

> *Talking point: "Students start the MCP container live in Guide 0, validate with Python, then run both agents against the same persistent endpoint."*

---

## 5) Ready to teach

When setup passes, start the live walkthrough with:

- `0_guide.md` — Start persistent MCP container and validate with Python
- `1_guide.md` — Walk through agent code
- `2_guide.md` — Run `code/query_agent.py` and observe the LLM answer
- `3_guide.md` — Run `code/snapshot_collector.py` and inspect the inventory summary

Do **not** start the MCP container during this prereq — students do that live in Guide 0.
