# Demo 2: Verify the Automation

**Time Budget:** 2–3 mins

**Narrative:** The agent posted tickets. Let's confirm they landed on the board and understand the full flow.

---

### 1) Verify tickets in the UI

Open `http://localhost:8085` in your browser.

**What it does:** Shows the Kanban board. Tickets created by the agent should appear in the "Open" column.

> *Expected: Multiple tickets — one per finding the LLM identified. Each has a title, namespace, resource, category, and priority.*

> *Talking point: "These tickets came from the cluster, through the MCP, into the LLM, and onto this board. No manual steps. One command did it all."*

---

### 2) Inspect a ticket

Click on one of the tickets to see its details.

**What it does:** Shows the full ticket — title, summary, namespace, resource name, category, priority, suggested owner, and reasoning.

> *Talking point: "The reasoning field is the LLM's explanation. It tells you why this was flagged and what to do about it. That is the value of structured output — not just 'something is wrong' but 'this specific resource is missing this specific label for this reason.'"*

---

### 3) Explain the full flow

> *Talking point: "Let's trace the full pipeline:*
> 1. *Section 05: Supergateway exposes the MCP server as HTTP*
> 2. *Section 06: The agent calls MCP tools to collect cluster data*
> 3. *Section 07: The LLM applies tagging rules and produces structured findings*
> 4. *Section 08: The tracker receives tickets via MCP*
> 5. *Section 09: The agent connects all three — collect, analyze, post*
>
> *Each section is a building block. This section wires them together."*

---

### 4) Cleanup

Stop the tracker when done:

```bash
docker stop finops-issue-tracker
```

**What it does:** Stops the tracker container. Supergateway can also be stopped (Ctrl-C in its terminal).

---

**Next:** End-to-end flow complete. Section 10 covers refactoring this monolith into production-grade code with separation of concerns.
