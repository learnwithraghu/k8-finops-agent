# Demo 1: Run the Structured Agent

**Time Budget:** 3 mins

**Narrative:** The agent reads the raw snapshot from the cluster, applies tagging rules as policy, and asks the LLM to produce structured findings. Same snapshot in, deterministic ticket-shaped data out.

---

### 1) Confirm MCP endpoint is alive

```bash
curl -s http://localhost:8000/healthz
```

**What it does:** Quick health check before running the agent.

> *Expected: `ok`*

---

### 2) Run the structured agent

```bash
python3 sections/07-llm-structured-agent/agent.py
```

**What it does:** Connects to the MCP endpoint, collects the cluster snapshot, loads tagging rules, sends both to the LLM, and prints structured findings as JSON.

> *Expected: A `TicketBatch` JSON object with one or more `TrackerTicket` entries — each representing a rule violation.*

> *Talking point: "The LLM sees the raw data and the policy. It produces structured output — not free text, not prose. Every finding has a title, namespace, resource, category, and severity."*

---

### 3) Review the output shape

The output should look like this:

```json
{
  "tickets": [
    {
      "title": "[FinOps] payment/payment-gateway missing owner label",
      "namespace": "payment",
      "resource_name": "payment-gateway",
      "resource_kind": "Deployment",
      "category": "missing-owner",
      "priority": "high",
      "suggested_owner": "payment-team",
      "reasoning": "Deployment payment-gateway has no owner label; ownership ambiguity blocks FinOps cost allocation.",
      "source": "mcp-llm-agent"
    }
  ]
}
```

> *Talking point: "This is the same shape Section 09 will POST to the issue tracker. We are building toward that."*

---

**Next:** Findings are structured. Next we audit them — trace each finding back to the rule and resource → `2_guide.md`
