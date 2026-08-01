# Demo 2: Test Tracker MCP Tools with a Tiny LLM Prompt

**Time Budget:** 2–3 mins  
**Video:** V3a — Standalone demo: list issue-tracker MCP tools via LLM

**Narrative:** Before we walk the agent code changes, prove the tracker MCP path with the smallest possible LLM script. One prompt. Tracker tools only. No cluster audit. No ticket creation.

**Prerequisites:** Tracker MCP running on `:8086` (Terminal 2 from `0_prerequisite_guide.md` / `1_guide.md`). Repo-root `.env` with OpenAI settings.

---

### 1) Confirm the tracker MCP is up

```bash
python3 sections/08-from-findings-to-tickets/agent/list_tracker_tools.py
```

**What it does:** Deterministic catalog check — connects to tracker MCP and prints tool names. No LLM.

> *Expected: `Tracker MCP OK — 4 tools via http://localhost:8086/sse` plus `create_issue`, `list_issues`, `get_issue`, `update_issue`.*

> *Talking point: "`list_tracker_tools.py` is the smoke test. Next we let the LLM see the same tool list."*

---

### 2) Run the standalone LLM demo

```bash
python3 sections/08-from-findings-to-tickets/agent/prompt_list_tracker_tools.py
```

**What it does:** Connects **only** to the tracker MCP, builds a LangChain agent with those tools, and asks the LLM to list every tool it can use. The prompt explicitly says not to call tools or create issues.

> *Expected: A short LLM answer naming `create_issue`, `list_issues`, `get_issue`, and `update_issue` with one-line descriptions. No tickets created on the board.*

---

### 3) Glance at the script (keep it tiny)

Open `agent/prompt_list_tracker_tools.py`:

- Fully standalone — loads `.env`, connects to tracker MCP only, no `mcp_client` import
- Creates a LangChain agent with those tools
- One `HumanMessage` prompt: list tools, do not call them
- Always `cleanup()` in `finally`

> *Talking point: "This is a demo script, not the FinOps auditor. Same MCP handshake the real agent uses — just the smallest prompt that proves the tracker tools are visible to an LLM."*

---

### 4) Contrast with the deterministic catalog

| Script | Uses LLM? | Purpose |
|--------|-----------|---------|
| `list_tracker_tools.py` | No | Print MCP tool catalog |
| `prompt_list_tracker_tools.py` | Yes | Ask the model to list the same tools |

> *Talking point: "Both hit the same SSE endpoint. One is a connectivity check. The other shows the LLM can see the tracker tools before we wire them into the full auditor."*

---

**Next:** Walk what changed in the agent code vs Section 07 → `3_guide.md`
