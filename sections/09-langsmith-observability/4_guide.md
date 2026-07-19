# Video 4: Read the Trace in LangSmith

**Time Budget:** 3–4 mins

**Prerequisites:** [`3_guide.md`](3_guide.md) — auditor run completed with LangSmith env vars set.

> **Legend:** Blockquote lines are on-screen actions — do not read them aloud. Everything else is your script.

---

### Opening (~15 sec)

The terminal showed the final answer. LangSmith shows the path — every model call and every MCP tool call that produced it.

> **Do:** Open [https://smith.langchain.com](https://smith.langchain.com) and select the project from `.env` (`LANGSMITH_PROJECT`).

---

### Step 1 — Find the latest run

In the project, open the most recent run from the Section 09 auditor.

**What to look for:**
- Timestamp matching your terminal run
- Status success (or error if something failed — useful too)
- A tree of nested spans, not a single blob

> **Say:** "One agent invoke becomes a tree of steps. That tree is what we could not see from print alone."

---

### Step 2 — Spot the LLM spans

Expand spans that represent chat / LLM calls.

**What it does:** Shows prompts, responses, token usage, and latency for each model round-trip.

> **Do:** Open one LLM span. Point at input vs output without reading the full audit aloud.

---

### Step 3 — Spot the MCP tool calls

Find tool / function spans — typically `kubectl_get` (or related Kubernetes MCP tools) under the agent.

**What to look for:**
- Tool name
- Arguments (namespace, resource kind)
- Returned payload size / content preview

> **Say:** "This is the same MCP traffic Section 06 validated — now it is attached to the agent timeline."

---

### Step 4 — Tie it back to FinOps

On screen, connect three layers:

1. **Cluster** — data via MCP  
2. **Policy** — `tagging-rules.yaml` shaping judgment  
3. **Trace** — LangSmith showing how the agent used tools to apply that policy  

When an audit looks wrong later, start here: wrong tool args, truncated tool output, or a weak model step — not only the final paragraph.

> **Do:** Collapse the tree. Show the run list once more so students know where to return.

---

### Close (~10 sec)

Section 09 complete: same auditor as Section 07, observability from `.env`, traces readable in LangSmith.

> **Do:** Leave LangSmith open if students want to re-run; stop the MCP container when the session ends. Optional: open `5_guide.md` for a smaller trace demo with `example_langsmith.py` (no MCP).
