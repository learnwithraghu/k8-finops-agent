# Demo 1: Run the Tracker

**Time Budget:** 2–3 mins

**Narrative:** We need a place for FinOps findings to become actionable tickets. This service is a lightweight Jira — a Kanban board with a REST API and an MCP server. Agents post findings here; humans review them on the board.

---

### 1) Run the tracker container

In a **dedicated terminal**:

```bash
docker run --rm -p 8085:8000 -p 8086:8001 --name finops-issue-tracker finops-issue-tracker:latest
```

**What it does:** Starts the tracker container. Port 8085 serves the REST API and board UI. Port 8086 serves the MCP server.

> *Expected: FastAPI startup logs, "Uvicorn running on http://0.0.0.0:8000".*

---

### 2) Open the board UI

Open `http://localhost:8085` in your browser.

**What it does:** Shows the Kanban board — columns for ticket status (open, in progress, done). Empty for now.

> *Talking point: "This is where FinOps findings land as tickets. Right now it is empty — we will populate it in the next demo."*

---

### 3) Open the API docs

Open `http://localhost:8085/docs` in your browser.

**What it does:** Shows the FastAPI Swagger UI — interactive API documentation. You can test endpoints directly from the browser.

> *Talking point: "The docs show every endpoint the tracker exposes. The `/create-issue` POST is the one agents use to create tickets."*

---

**Next:** Tracker is running. Next we create our first ticket via the REST API → `2_guide.md`
