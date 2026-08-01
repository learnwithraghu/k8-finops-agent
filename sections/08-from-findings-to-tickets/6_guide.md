# Demo 6: Widen the Prompt — Scan All Namespaces

**Time Budget:** 2–3 mins  
**Video:** V5b — Prompt tweak: from `payment` to the full cluster

**Narrative:** Demo 5 scoped the agent to the `payment` namespace so tickets landed reliably. One prompt line controls that scope. Change it, re-run, and watch tickets appear for Deployments across the cluster.

**Prerequisites:** `5_guide.md` complete — board already has the three `payment` tickets. Both MCP terminals still running.

---

### 1) Find the scoped collect line

Open `agent/tracker_auditor.py` and look at **Step 1** in `PROMPT`:

```text
- kubectl_get resourceType=deployments namespace=payment output=json
```

**What it does:** Limits discovery to Deployments in `payment` only — that is why Demo 5 created three tickets.

---

### 2) Change that one line (manually)

Edit it to scan Deployments in **all** namespaces:

```text
- kubectl_get resourceType=deployments allNamespaces=true output=json
```

Do not change anything else yet. Save the file.

> *Talking point: "Same agent, same tools. The prompt is the dial — one line widens the scan from a demo slice to the whole cluster."*

---

### 3) Re-run the agent

```bash
python3 sections/08-from-findings-to-tickets/agent/tracker_auditor.py
```

**What it does:** Fetches Deployments cluster-wide, evaluates labels, and calls `create_issue` for each non-compliant Deployment outside the earlier `payment`-only set.

> *Expected: More `create_issue` calls. Board grows beyond the three `payment` tickets.*

---

### 4) Verify on the board

Open `http://localhost:8085` and refresh.

> *Expected: Tickets for other app namespaces (for example `booking-api`, `flight-search`, `inventory`, `default`) in addition to the Demo 5 `payment` tickets.*

---

### 5) Cleanup

When the section is done:

```bash
docker stop finops-issue-tracker
```

Stop the Kubernetes MCP terminal with Ctrl+C.

**Next:** End-to-end flow complete. Section 09 covers LangSmith observability for the FinOps agent.
