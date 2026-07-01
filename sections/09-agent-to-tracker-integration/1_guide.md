# Demo 1: Run the Full Agent

**Time Budget:** 3 mins

**Narrative:** The agent does three things in sequence: collect cluster data via MCP, analyze it with the LLM, and post findings as tickets to the tracker. One command, end to end.

---

### 1) Confirm both services are running

```bash
curl -s http://localhost:8000/healthz
curl -s http://localhost:8085/docs | head -1
```

**What it does:** Quick health checks — Supergateway (MCP) and Issue Tracker (REST). Both should respond.

> *Talking point: "If either service is down, the agent fails. In production you would have retries and health checks. For the demo, we just confirm before running."*

---

### 2) Run the full agent

```bash
python3 sections/09-agent-to-tracker-integration/agent.py
```

**What it does:** Connects to the Kubernetes MCP, collects the cluster snapshot, analyzes it with the LLM using tagging rules, and posts each finding as a ticket to the tracker via MCP.

> *Expected: Log lines showing connection, scanning, analysis, and ticket creation. Final line: "ALL ISSUES POSTED TO TRACKER".*

> *Talking point: "Watch the logs. Three phases — collect, analyze, post. Each one is a separate concern. That is why Section 10 refactors them into separate files."*

---

**Next:** Agent ran and posted tickets. Next we verify they landed on the board → `2_guide.md`
