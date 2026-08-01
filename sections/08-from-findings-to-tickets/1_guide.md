# Demo 1: Launch the FinOps Issue Tracker

**Time Budget:** 2–3 mins  
**Video:** V2 — Launch the FinOps Issue Tracker

**Narrative:** We need a place for FinOps findings to become actionable tickets. This service is a lightweight Kanban board with a REST API and an MCP server. Agents post findings here; humans review them on the board.

**Prerequisites:** Both MCP terminals from `0_prerequisite_guide.md` should already be running:
- **Terminal 1** — Kubernetes MCP on `:8000`
- **Terminal 2** — Issue tracker on `:8085` (REST/UI) and `:8086` (MCP)

If the tracker is not up yet, start it in Terminal 2 now.

---

### 1) Run the tracker container (if not already running)

In **Terminal 2**:

```bash
docker run --rm -p 8085:8000 -p 8086:8001 --name finops-issue-tracker finops-issue-tracker:latest
```

**What it does:** Starts the tracker container. Port 8085 serves the REST API and board UI. Port 8086 serves the MCP server.

> *Expected: FastAPI startup logs, "Uvicorn running on http://0.0.0.0:8000". Leave Terminal 1 (K8s MCP) and Terminal 2 (tracker) running for the rest of the section.*

---

### 2) Open the board UI

Open `http://localhost:8085` in your browser.

**What it does:** Shows the Kanban board — columns for ticket status (backlog, todo, in progress, done). Empty for now.

> *Talking point: "This is where FinOps findings land as tickets. Right now it is empty — we will populate it in the next demos."*

---

### 3) Open the API docs

Open `http://localhost:8085/docs` in your browser.

**What it does:** Shows the FastAPI Swagger UI — interactive API documentation. You can test endpoints directly from the browser.

> *Talking point: "The docs show every REST endpoint the tracker exposes. The `/create-issue` POST is the one agents use to create tickets — when calling over HTTP."*

---

### 4) Quick connectivity check (no LLM)

In a **working terminal** (repo root, virtualenv activated):

```bash
python3 sections/08-from-findings-to-tickets/agent/list_tracker_tools.py
```

**What it does:** Connects to the tracker MCP server on port 8086 and prints the discovered tools (`create_issue`, `list_issues`, `get_issue`, `update_issue`). No LLM involved.

> *Talking point: "Swagger is for REST on 8085. Agents discover tools over MCP on 8086 — this script proves the MCP handshake works."*

---

**Next:** Prove the tracker MCP tools through a tiny LLM prompt → `2_guide.md`
