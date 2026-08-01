# Demo 3: Code Walkthrough — What Changed vs Section 07

**Time Budget:** 3–4 mins  
**Video:** V3b — Agent code delta: dual MCP + ticket posting

**Narrative:** Section 07 audits labels and prints a report. Section 08 keeps the same agent pattern and adds tracker MCP tools so findings become tickets. This video walks only what is new.

**Prerequisites:** `2_guide.md` — tracker MCP tools visible to the LLM. Both MCP terminals still running.

---

### 1) Compare the MCP client wiring

Open side by side:

- Section 07: `sections/07-llm-structured-agent/code/mcp_client.py`
- Section 08: `sections/08-from-findings-to-tickets/agent/mcp_client.py`

**What is new in Section 08:**

```python
MCP_SERVERS = {
    "k8s": {
        "url": K8S_MCP_URL,          # streamable_http :8000
        "transport": "streamable_http",
    },
    "tracker": {
        "url": TRACKER_MCP_URL,      # sse :8086  ← NEW
        "transport": "sse",
    },
}

TRACKER_MCP_SERVERS = {
    "tracker": MCP_SERVERS["tracker"],
}
```

**What to look for:**

- Section 07 registers **one** server (`k8s`)
- Section 08 registers **two** (`k8s` + `tracker`) with different transports
- The tiny demos in `2_guide.md` (`list_tracker_tools.py`, `prompt_list_tracker_tools.py`) are **standalone** — they connect to tracker MCP directly and do not import `mcp_client`
- `get_mcp_tools()` / `run_agent()` still load `.env`, build the LLM, attach tools, and always `cleanup()` — same shape as Section 07
- Tagging rules still arrive via optional `SystemMessage` in `run_agent`

> *Talking point: "One LangChain agent, two MCP servers. K8s for cluster reads. Tracker for create_issue. Same convert_mcp_to_langchain_tools call — bigger tool list."*

---

### 2) Compare the auditor entrypoint

Open side by side:

- Section 07: `sections/07-llm-structured-agent/code/structured_auditor.py`
- Section 08: `sections/08-from-findings-to-tickets/agent/tracker_auditor.py`

**What changed in the prompt:**

| Section 07 | Section 08 |
|------------|------------|
| Audit labels via K8s MCP | Audit labels via K8s MCP |
| Print a plain-English report | Call tracker `create_issue` per finding |
| Done when the summary is written | Done when tickets exist; confirm with `list_issues` |

**What to look for in `tracker_auditor.py`:**

- Still a thin wrapper around `run_agent(...)`
- Still loads Section 07's `config/tagging-rules.yaml` (path points at the previous section)
- `PROMPT` tells the agent to skip compliant resources and create one ticket per distinct finding
- `source: "mcp-llm-agent"` marks tickets created by this loop
- Final print points at `http://localhost:8085` instead of ending on stdout alone

> *Talking point: "We did not invent a second posting client. The ReAct loop already knows how to call tools — we just gave it tracker tools and changed the job description."*

---

### 3) Map the data flow

```
LangChain agent (tracker_auditor.py)
  ├── K8s MCP (:8000)      → kubectl_get, etc.
  └── Tracker MCP (:8086)  → create_issue, list_issues
         └── Kanban board (:8085)
```

> *Talking point: "Section 07 stopped at the English summary. Section 08 closes the loop — same findings, now as backlog tickets."*

---

**Next:** Walk the tracker backend schema and create one ticket by hand with curl → `4_guide.md`
