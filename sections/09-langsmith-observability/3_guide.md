# Video 3: Same Auditor, Now Observable

**Time Budget:** 3–4 mins

**Prerequisites:** [`2_guide.md`](2_guide.md) — LangSmith env vars set; MCP container running; virtualenv activated.

> **Legend:** Blockquote lines are on-screen actions — do not read them aloud. Everything else is your script.

---

### Opening (~15 sec)

The code is a copy of Section 07. We are not adding a tracer class or a new script — we run the same policy auditor and let LangSmith capture the run.

> **Do:** Open a terminal at the repo root. Activate the virtualenv.

---

### Step 1 — Confirm cluster and MCP (quick)

```bash
source .venv/bin/activate
kubectl get namespaces
python3 sections/06-mcp-data-agent/code/validate_mcp.py
```

**What it does:** Same health checks as Section 07. Skip the long MCP start if the container is already up.

> **Expected:** Namespaces listed; `MCP OK — N namespaces via kubectl_get`.

---

### Step 2 — Glance at the copied script (optional beat)

Open `sections/09-langsmith-observability/code/structured_auditor.py`.

**What to notice:** Same prompt, same `load_tagging_rules()`, same `run_agent(...)` call as Section 07. Observability did not change this file's job.

> **Say:** "If you can run Section 07, you can run Section 09 — only the folder path and `.env` differ."

---

### Step 3 — Run the policy auditor

```bash
python3 sections/09-langsmith-observability/code/structured_auditor.py
```

This loads `config/tagging-rules.yaml`, connects to MCP, lets the agent call tools, prints a plain-English audit — and, with `LANGSMITH_TRACING=true`, sends the run to LangSmith.

> **Expected:** Multi-paragraph audit grouped by namespace (same shape as Section 07). Terminal may also show a LangSmith run URL depending on client version.

> **Do:** Let the run finish. Scroll the on-screen audit briefly — then we leave the deep UI walk for Video 4.

---

### Step 4 — Confirm this was not a new agent

Compare paths:

| Section | Command |
|---------|---------|
| 07 | `python3 sections/07-llm-structured-agent/code/structured_auditor.py` |
| 09 | `python3 sections/09-langsmith-observability/code/structured_auditor.py` |

Same agent path. Section 09 adds a place to inspect how the answer was produced.

> **Say:** "Screen output is the answer. LangSmith is the flight recorder."

---

### Close (~10 sec)

Audit printed. Next we open LangSmith and read the trace — LLM spans and MCP tool calls.

> **Do:** Keep the MCP container running. Open `4_guide.md`.
