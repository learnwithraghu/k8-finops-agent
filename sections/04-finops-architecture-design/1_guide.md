# Video 1: The Problem We're Soloring

**Time Budget:** 3 min

**Format:** Whiteboard / talking head with slides

**Slides:** `slides/slide1_problem.svg` (create later)

---

## Transcript

### Opening (20s)

In Section 02a, we had a real incident. The payment API was down. The UI loaded fine — you could open the browser, see the AirPay page, fill in the form. But when you hit submit, it failed.

We debugged it with kubectl. We found the root cause — the API deployment was scaled to zero replicas. We even fixed it.

But there was a bigger problem we could not fix.

---

### The Ownership Wall (60s)

When we looked at the failing deployment, we asked a simple question: who owns this?

The answer was nowhere.

No `owner` label. No `cost-center` label. No `team` label. Nothing.

In a real incident, this is where everything breaks down. Not the technical failure — that was one `kubectl scale` command. The organizational failure. You have a broken service and you cannot answer:

- Who do I page?
- What Slack channel do I post in?
- Whose budget pays for this?
- Is this service even supposed to exist?

We tried searching across all namespaces. We grepped labels. We found nothing. The resource was untagged, unowned, and invisible to any FinOps process.

> *Talking point: "This is not a Kubernetes problem. This is a governance problem. Kubernetes runs the workload. It does not tell you who is accountable for it."*

---

### The Real Cost (40s)

In a small demo, this is annoying. In production, this is expensive.

Every untagged resource is a billing gap. Every missing owner is an incident that takes 30 minutes longer to resolve. Every orphaned PVC is money spent on storage nobody owns.

And the worst part: the more services you run, the worse it gets. You cannot manually check every deployment for labels. You cannot grep your way to compliance across 200 namespaces.

> *Talking point: "At scale, manual FinOps does not work. You need automation."*

---

### The System Question (30s)

So here is the problem we need to solve:

**How do we go from a running cluster to actionable FinOps findings — automatically?**

Not manually. Not with 20 kubectl commands. Not with someone checking labels in a spreadsheet.

We need a system that:
1. Reads the cluster
2. Applies policy — what labels are required, what looks orphaned
3. Produces action — tickets, alerts, something a team can act on

That is the architecture we are designing. Three phases: Collect, Analyze, Act.

> *Talking point: "Next video, we pick the tools and draw the pipeline."*

---

## Key takeaways
- The 02a incident was a technical failure (0 replicas), but the bigger failure was organizational (no ownership metadata)
- Manual kubectl does not scale — you need automation for FinOps
- The system needs three phases: Collect → Analyze → Act
