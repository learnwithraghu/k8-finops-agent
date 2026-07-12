# Demo 2: Tracker Backend Walkthrough — REST, MCP, and Ticket Schema

**Time Budget:** 3–4 mins  
**Video:** V3 — Tracker Backend Walkthrough: REST, MCP, and the Ticket Schema

**Narrative:** Before the agent posts tickets automatically, we walk the backend code and create one ticket manually. This is the same payload shape the agent sends via MCP.

---

### 1) Tour the backend code

Open these files in your editor:

- `service/app/main.py` — FastAPI REST routes and static UI mount
- `service/app/models.py` — `IssueCreate` schema (title, namespace, priority, reasoning, etc.)
- `service/app/mcp_server.py` — MCP tools: `create_issue`, `list_issues`, `get_issue`, `update_issue`
- `service/app/store.py` — JSON file persistence

**What to look for:**

- REST and MCP share the same `IssueCreate` model — one schema, two interfaces
- `create_issue` MCP tool maps directly to the `/create-issue` REST handler
- Tickets get keys like `FINOPS-0001` and land in the backlog column

> *Talking point: "Agents call MCP on port 8086. Humans use REST on 8085. Same ticket, different door. Run `list_tracker_tools.py` to show the MCP tool catalog live."*

---

### 2) Create a ticket via curl

```bash
curl -X POST http://localhost:8085/create-issue \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "[FinOps] payment/payment-processor - UNALLOCATED ($8.47/month)",
    "summary": "Missing cost-center and owner metadata",
    "body": "The agent flagged this deployment as having no ownership labels.",
    "namespace": "payment",
    "resource_name": "payment-processor",
    "resource_kind": "Deployment",
    "category": "unallocated",
    "priority": "high",
    "cost_impact": 8.47,
    "suggested_owner": "payment-team",
    "suggested_cost_center": "payment",
    "reasoning": "Missing cost-center tag means the workload cannot be billed correctly.",
    "source": "manual-demo"
  }'
```

**What it does:** Sends a POST request to create a ticket. The tracker stores it and returns the created ticket with an ID.

> *Expected: JSON response with the ticket details and a generated key (e.g. FINOPS-0001).*

---

### 3) Verify the ticket on the board

Open `http://localhost:8085` in your browser.

**What it does:** Refreshes the Kanban board. The new ticket should appear in the backlog column.

> *Talking point: "This curl call is what the agent automates via MCP `create_issue`. One ticket per finding."*

---

**Next:** Manual ticket creation works. Next we wire the Section 06 agent to post findings automatically → `3_guide.md`
