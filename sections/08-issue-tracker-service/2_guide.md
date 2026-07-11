# Demo 2: Create Tickets via REST

**Time Budget:** 3–4 mins

**Narrative:** Let's simulate what the agent does — POST a FinOps finding as a ticket. This is the same payload shape Section 07 produces. We are doing it by hand first; Section 09 automates it.

---

### 1) Create a ticket via curl

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

> *Expected: JSON response with the ticket details and a generated ID.*

> *Talking point: "This is the exact payload shape Section 07 produces. The agent automates this curl call — we are doing it manually to see what happens."*

---

### 2) Verify the ticket on the board

Open `http://localhost:8085` in your browser.

**What it does:** Refreshes the Kanban board. The new ticket should appear in the "Open" column.

> *Expected: One ticket visible — "[FinOps] payment/payment-processor - UNALLOCATED".*

> *Talking point: "The board is a human view of what the agent produces. Ops teams use this to triage and assign findings."*

---

### 3) Create a second ticket (optional)

```bash
curl -X POST http://localhost:8085/create-issue \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "[FinOps] flight-search/flight-search-service - MISSING OWNER",
    "summary": "No owner label on deployment",
    "namespace": "flight-search",
    "resource_name": "flight-search-service",
    "resource_kind": "Deployment",
    "category": "missing-owner",
    "priority": "medium",
    "suggested_owner": "flight-team",
    "reasoning": "No owner label means no team is accountable for this workload.",
    "source": "manual-demo"
  }'
```

**What it does:** Creates a second ticket. Refresh the board to see both.

> *Talking point: "In a real run, the agent creates one ticket per finding. You might get 5, 10, or 20 tickets from a single scan."*

---

**Next:** Tickets work via REST. Next we automate the full flow — agent posts findings directly → `sections/09-agent-to-tracker-integration`
