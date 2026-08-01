# Demo 5: Run the Agent and Verify Tickets on the Board

**Time Budget:** 3–4 mins  
**Video:** V5 — Agent Walkthrough: Post Per-Finding Tickets Instead of Printing

**Narrative:** One LangChain agent with both K8s MCP and tracker MCP tools audits the cluster and calls `create_issue` for each finding. No separate posting step.

**Prerequisites:** Both MCP terminals running (`0_prerequisite_guide.md`). Code delta covered in `3_guide.md`. Optional manual ticket from `4_guide.md` may already be on the board.

---

### 1) Confirm both services are running

```bash
curl -s http://localhost:8000/mcp -o /dev/null -w "%{http_code}\n"
curl -s http://localhost:8085/health
```

**What it does:** Quick health checks — K8s MCP (Terminal 1) and Issue Tracker REST (Terminal 2). Both should respond.

> *Talking point: "The agent connects to both MCP servers — K8s for collection and tracker for posting. Confirm both before running."*

---

### 2) Recap the agent files (before running)

Open these files:

- `agent/mcp_client.py` — registers **both** MCP servers in `MCP_SERVERS` (K8s + tracker)
- `agent/tracker_auditor.py` — unified prompt: audit labels, call `create_issue` per finding

**What to look for:**

- `MCP_SERVERS` has `k8s` (streamable HTTP on :8000) and `tracker` (SSE on :8086)
- `convert_mcp_to_langchain_tools` exposes `kubectl_get` and `create_issue` in one tool list
- Tagging rules load from Section 07's `config/tagging-rules.yaml` via `SystemMessage`
- No separate structure or posting files — the ReAct loop handles everything

---

### 3) Run the agent

```bash
python3 sections/08-from-findings-to-tickets/agent/tracker_auditor.py
```

**What it does:** One agent loop: fetch cluster data via K8s MCP, evaluate against tagging rules, call tracker `create_issue` for each finding.

> *Expected: Log lines showing both `kubectl_get` and `create_issue` tool calls. Final line: "Done. Verify tickets at http://localhost:8085".*

---

### 4) Verify tickets in the UI

Open `http://localhost:8085` in your browser.

**What it does:** Shows the Kanban board. Tickets created by the agent should appear alongside any manual demo ticket.

> *Expected: Multiple tickets — one per finding. Each has title, namespace, resource, category, priority, and reasoning.*

Click a ticket to inspect the reasoning field — the LLM's explanation of why it was flagged.

---

### 5) Explain the full flow

> *Talking point: "Let's trace the closed loop:*
> 1. *Section 06: LangChain + MCP pattern for cluster access*
> 2. *Section 07: Tagging rules shape what counts as a finding*
> 3. *Section 08: Same agent pattern, but now with tracker MCP tools — audit and post in one loop*
>
> *The prompt currently scans only `payment` so the demo stays reliable. Next we widen that one line."*

---

**Next:** Widen the prompt to scan all namespaces and fill the board → `6_guide.md`
