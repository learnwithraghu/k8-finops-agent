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

## 1) Set up the Python environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**What it does:** Creates a virtualenv and installs repo deps (including `mcp`, `openai`, and `python-dotenv`).

---

## 2) Confirm API key is set

```bash
test -n "$OPENAI_API_KEY" && echo "API key is set" || echo "OPENAI_API_KEY is not set"
```

**What it does:** Checks that the OpenAI API key environment variable is present. The script needs this to call the LLM.

> *If using a `.env` file, confirm it exists at the repo root: `grep OPENAI .env`*

---

## 3) Inspect the agent code

```bash
cat sections/06-mcp-data-agent/simple_mcp_llm.py
```

**What it does:** Shows the minimal agent — LLM picks `kubectl_get`, MCP reads the cluster, LLM returns a plain-English answer.

> *Talking point: "Under fifty lines. No logger, no try/except — just prompt → tool call → answer. This is the loop students need to understand before Section 07."*

---

## 4) Ready to teach

When setup passes, start the live walkthrough with:

- `0_guide.md` — Walk through `simple_mcp_llm.py`
- `2_guide.md` — Run it and observe the LLM answer

**Optional:** `1_guide.md` — full snapshot collector via `agent.py` (no LLM)

## Reset for another run (optional)

```bash
rm -f k8s_metadata.json
```

**What it does:** Cleans up output files from previous `agent.py` runs.
