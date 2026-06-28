# Demo 2: Auditing the Structured Findings

**Time Budget:** 2-3 mins

### 1) Target Output Format (TicketBatch)
*(Review the output from Demo 1. It should look like this:)*
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

### 2) Discussion
> *Talking point: This structured output is what Section 09 will POST to our Issue Tracker. We separated collection (06) from analysis (07) to keep the pipeline deterministic and testable.*

---

**Try it:** Open [`architecture_builder/index.html`](architecture_builder/index.html) in your browser to wire the **before/after analysis** pipeline — messy snapshot and policy in, structured ticket fields out. Use **Need a hint?** if stuck, then press **Run Analysis** to validate.
