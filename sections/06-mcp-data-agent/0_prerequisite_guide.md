# Instructor Prerequisite: Supergateway & Python Environment

**Audience:** Instructor only — run this before `1_guide.md`. Do not walk students through pip install during the live demo.

**Time Budget:** 1–2 mins

---

## Before you start

Confirm Supergateway from Section 05 is still running:

```bash
curl -s http://localhost:8000/healthz
```

**What it does:** Checks the MCP endpoint is alive. Should return `ok`.

> *If this fails, restart Supergateway using the command in `sections/05-mcp-k8-agent/0_prerequisite_guide.md` step 3.*

---

## 1) Set up the Python environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r sections/06-mcp-data-agent/requirements.txt
```

**What it does:** Creates a virtualenv and installs the MCP Python client.

---

## 2) Inspect the agent code

```bash
cat sections/06-mcp-data-agent/agent.py
```

**What it does:** Shows the Python agent. It connects to the MCP endpoint via SSE, calls `kubectl_get` for each resource type, and prints a JSON snapshot.

> *Talking point: "This is the simplest MCP client — connect, call tools, print results. No analysis, no LLM, no policy."*

---

## 3) Ready to teach

When setup passes, start the live walkthrough with:

- `1_guide.md` — Run the data agent
- `2_guide.md` — Inspect the snapshot

## Reset for another run (optional)

```bash
rm -f k8s_metadata.json
```

**What it does:** Cleans up output files from previous runs.
