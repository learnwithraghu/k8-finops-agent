# Instructor Prerequisite: Supergateway & Python Environment

**Audience:** Instructor only — run this before `0_guide.md`. Do not walk students through pip install during the live demo.

**Time Budget:** 2–3 mins

---

## Before you start

Confirm Supergateway from Section 05 is still running:

```bash
curl -s http://localhost:8000/healthz
```

**What it does:** Checks the MCP endpoint is alive. Should return `ok`.

> *If this fails, restart Supergateway using the command in `sections/05-mcp-k8-agent/0_prerequisite_guide.md` step 3.*

---

## 1) Set up the Python virtualenv

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**What it does:** Creates a virtualenv at the repo root and installs deps (including `mcp`, `langchain-mcp-tools`, `langgraph`, `openai`, and `python-dotenv`).

> *Re-activate in new shells with: `source .venv/bin/activate`*

---

## 2) Confirm API key is set

```bash
test -n "$OPENAI_API_KEY" && echo "API key is set" || echo "OPENAI_API_KEY is not set"
```

**What it does:** Checks that the OpenAI API key environment variable is present. `query_agent.py` needs this to call the LLM.

> *If using a `.env` file, confirm it exists at the repo root: `grep OPENAI .env`*

---

## 3) Inspect the scripts

```bash
cat sections/06-mcp-data-agent/mcp_client.py
cat sections/06-mcp-data-agent/query_agent.py
cat sections/06-mcp-data-agent/snapshot_collector.py
```

**What it does:** Shows the three files — shared MCP wiring, LLM query agent, and deterministic snapshot collector.

> *Talking point: "Under eighty lines total across the two scripts. LangChain handles tool choice in `query_agent.py`; `snapshot_collector.py` is a reliable bulk collector for Section 07."*

---

## 4) Ready to teach

When setup passes, start the live walkthrough with:

- `0_guide.md` — Walk through `query_agent.py`
- `1_guide.md` — Run `query_agent.py` and observe the LLM answer
- `2_guide.md` — Run `snapshot_collector.py`, inspect labels

## Reset for another run (optional)

```bash
rm -f k8s_metadata.json
```

**What it does:** Cleans up output files from previous `snapshot_collector.py` runs.
