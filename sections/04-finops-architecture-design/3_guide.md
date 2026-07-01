# Video 3: Component Design & Trade-offs

**Time Budget:** 3 min

**Format:** Whiteboard / talking head with slides

**Slides:** `slides/slide3_components.svg` (create later)

---

## Transcript

### Opening (10s)

Last video we drew the pipeline. Now let's zoom into each component — what it does, what it takes, and what trade-offs we made.

---

### MCP Server — Section 05 (40s)

**Responsibility:** Expose kubectl as a standard tool interface over HTTP.

**Input:** MCP tool calls (e.g. "get all namespaces", "get deployments in payment").

**Output:** Structured JSON from the Kubernetes API.

**Why prebuilt?** We could write our own MCP server. But the `mcp/kubernetes` image already wraps kubectl — it handles authentication, output formatting, and error cases. We skip the implementation and go straight to validation.

**Trade-off:** We depend on an external image. If it has bugs, we work around them. But the time saved is worth it — we validate with curl in minutes instead of building from scratch.

> *Talking point: "Section 05 is three curl calls. Health check, MCP handshake, real cluster read. If curl works, everything downstream works."*

---

### Collector — Section 06 (40s)

**Responsibility:** Call MCP tools, assemble a JSON snapshot of the cluster.

**Input:** MCP endpoint URL.

**Output:** JSON file with namespaces, deployments, pods, services, PVCs, configmaps.

**Why separate from analysis?** Collection is deterministic. Same cluster state → same snapshot every time. You can test it, diff it, cache it. If you mix collection and analysis, you cannot verify either independently.

**Trade-off:** Extra step. More code. But testability pays for itself — when something breaks, you know whether the problem is in collection or analysis.

> *Talking point: "The collector is a thin loop: list namespaces, fetch resources per namespace, write JSON. No logic, no decisions. Just data."*

---

### LLM Analyzer — Section 07 (40s)

**Responsibility:** Take the raw snapshot plus tagging rules, produce structured findings.

**Input:** JSON snapshot + `tagging-rules.yaml`.

**Output:** `TicketBatch` JSON — each ticket has a title, namespace, resource, category, priority, and reasoning.

**Why an LLM?** The tagging rules define what "good" looks like. But applying rules to raw data requires reasoning — "this PVC is orphaned because no pod mounts it" is not a simple lookup. An LLM can do that reasoning. A rule engine can too, but every new case is new code.

**Trade-off:** LLM output is non-deterministic. We fix that with a Pydantic schema — the LLM must return valid JSON matching our `TicketBatch` model. The structure is enforced; the content varies.

> *Talking point: "We do not ask the LLM for free text. We ask for JSON. Pydantic validates it. If the LLM returns garbage, we catch it before it reaches the tracker."*

---

### Tracker — Section 08 (30s)

**Responsibility:** Receive findings as tickets, display them on a Kanban board.

**Input:** REST POST `/create-issue` or MCP `create_issue` tool call.

**Output:** Tickets visible on the board UI.

**Why not Jira?** Jira is the real-world target. But for teaching, we need something we control, run locally, and demo without API keys. A lightweight FastAPI service with a board UI is enough to teach the pattern.

**Trade-off:** Simpler than Jira — no workflows, no permissions, no webhooks. But the integration code (POST a JSON payload) is identical to what you would write for Jira.

> *Talking point: "The tracker is a teaching tool. The pattern is production-ready. Swap the endpoint URL and you are talking to Jira."*

---

### Integration — Section 09 (20s)

**Responsibility:** Wire Collect → Analyze → Act into one command.

One Python script. Three phases. One button.

> *Talking point: "That is the architecture. Five components, five sections. Now we build it."*

---

## Key takeaways
- Each component has a clear responsibility, input, and output
- Trade-offs favor speed and teachability: prebuilt MCP, thin collector, LLM with schema validation, simple tracker
- Separation of concerns: you can test, swap, or replace any component independently
- The architecture transfers to production: swap the MCP image, swap the tracker endpoint, keep the pipeline
