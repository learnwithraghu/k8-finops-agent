# Demo 3: Run the Agent and Verify Tickets on the Board

**Time Budget:** 3–4 mins  
**Video:** V5 — Agent Walkthrough: Post Per-Finding Tickets Instead of Printing

**Narrative:** The agent uses the same MCP collection path as Section 06, then structures the audit into tickets and posts them to the tracker. One command closes the loop.

---

### 1) Confirm both services are running

```bash
curl -s http://localhost:8000/mcp -o /dev/null -w "%{http_code}\n"
curl -s http://localhost:8085/health
```

**What it does:** Quick health checks — K8s MCP (Section 06) and Issue Tracker (REST). Both should respond.

> *Talking point: "The agent needs the K8s MCP for collection and the tracker MCP for posting. Confirm both before running."*

---

### 2) Walk the agent code (before running)

Open these files:

- `agent/mcp_client.py` — copied unchanged from Section 06
- `agent/tracker_auditor.py` — same audit prompt; replaces `print()` with structure + post
- `agent/structure.py` — LLM converts audit text → `TicketBatch`
- `agent/tracker_client.py` — calls tracker MCP `create_issue` for each ticket

**What to look for:**

- Collection is identical to Section 06 — only the output destination changed
- `structure.py` is the small bridge between plain-English audit and typed tickets
- Tagging rules load from Section 07's `config/tagging-rules.yaml` by reference

---

### 3) Run the agent

```bash
python3 sections/08-from-findings-to-tickets/agent/tracker_auditor.py
```

**What it does:** Connects to K8s MCP, runs the label audit, structures findings, and posts each one to the tracker via MCP.

> *Expected: Log lines for MCP connection, structuring, and ticket creation. Final line: "Posted N ticket(s) to the issue tracker".*

---

### 4) Verify tickets in the UI

Open `http://localhost:8085` in your browser.

**What it does:** Shows the Kanban board. Tickets created by the agent should appear alongside any manual demo ticket.

> *Expected: Multiple tickets — one per finding. Each has title, namespace, resource, category, priority, and reasoning.*

Click a ticket to inspect the reasoning field — the LLM's explanation of why it was flagged.

---

### 5) Explain the full flow

> *Talking point: "Let's trace the closed loop:*
> 1. *Section 06: MCP agent collects cluster data via LangChain*
> 2. *Section 07: Tagging rules shape what counts as a finding*
> 3. *Section 08: Structure the audit → post per-finding tickets → Kanban board*
>
> *Next, Section 09 refactors this into maintainable modules before we deploy to Kubernetes in Section 10."*

---

### 6) Cleanup

Stop the tracker when done:

```bash
docker stop finops-issue-tracker
```

**Next:** End-to-end flow complete. Section 09 covers refactoring the agent into collector / analyzer / tracker modules.
