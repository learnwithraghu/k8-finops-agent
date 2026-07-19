# Video 5 (Optional): Minimal LangSmith Trace Example

**Time Budget:** 2–3 mins

**Prerequisites:** [`2_guide.md`](2_guide.md) — LangSmith env vars set in repo-root `.env`; virtualenv activated.

> **Legend:** Blockquote lines are on-screen actions — do not read them aloud. Everything else is your script.

---

### Opening (~15 sec)

The policy auditor trace is the full flight recorder — MCP tools, long prompts, many spans. Before that complexity, this optional script shows the same LangSmith wiring in under a minute. No cluster, no MCP container.

> **Do:** Open `sections/09-langsmith-observability/example_langsmith.py`.

---

### Step 1 — How it loads config

Find the `load_dotenv` line near the top:

```python
load_dotenv(Path(__file__).parents[2] / ".env")
```

**The chain:**
1. Script lives at section root — two parents up is the repo root
2. Same `OPENAI_*` and `LANGSMITH_*` keys as the auditor
3. LangChain sends traces when `LANGSMITH_TRACING=true` — no extra tracer setup

> **Say:** "Same `.env` file as the rest of the course. Only the script path differs from `mcp_client.py`."

---

### Step 2 — Spot the nested spans

Scroll to the `@traceable` decorators:

```python
@traceable(name="fetch_mock_cluster_context")
def fetch_mock_cluster_context() -> str:
    ...

@traceable(name="finops_trace_demo")
def run_trace_demo() -> str:
    context = fetch_mock_cluster_context()
    llm = build_llm()
    response = llm.invoke(...)
```

**What it does:**
1. `fetch_mock_cluster_context` — child span; mock cluster text instead of a real MCP call
2. `finops_trace_demo` — parent span; calls the child, then one LLM invoke
3. The LLM call adds its own LangChain span automatically

> **Say:** "Parent and child spans you control, plus the model span LangChain adds for free."

---

### Step 3 — Run the example

```bash
source .venv/bin/activate
python3 sections/09-langsmith-observability/example_langsmith.py
```

**What it does:** Prints a one-sentence FinOps answer and confirms which LangSmith project received the run.

> **Expected:** A short answer on screen, then `Trace sent to LangSmith project: k8-finops-agent` (or your `LANGSMITH_PROJECT` value).

> **Do:** Let the run finish. Note the timestamp — you will match it in LangSmith.

---

### Step 4 — Read the smaller trace

Open [https://smith.langchain.com](https://smith.langchain.com) → your project → the latest run from this script.

**What to look for:**
- Root span: `finops_trace_demo`
- Nested span: `fetch_mock_cluster_context`
- LLM span under the parent (prompt + response, token usage)

Compare mentally to the Section 09 auditor trace from [`4_guide.md`](4_guide.md): same UI, fewer tool spans.

> **Say:** "Same project, simpler tree. Use this when you want to confirm tracing works before running the full audit."

---

### Close (~10 sec)

Optional beat complete. The main Section 09 path remains the traced policy auditor — this script is a quick sanity check for LangSmith env and span nesting.

> **Do:** Re-run [`3_guide.md`](3_guide.md) when you want the full MCP + policy trace again.
