# Video 2: The Architecture Pattern

**Time Budget:** 3 min

**Format:** Whiteboard / talking head with slides

**Slides:** `slides/slide2_architecture.svg` (create later)

---

## Transcript

### Opening (15s)

Last video we defined the problem: we need a system that Collects cluster data, Analyzes it against policy, and Takes action. Now let's pick the tools and draw the pipeline.

---

### Phase 1: Collect (60s)

We need to read the cluster. What are the options?

**Option A: kubectl.** We already know it. Works great for one-off checks. But it is a human tool — you run it in a terminal, read the output, decide what to do. Hard to automate.

**Option B: Kubernetes Python client.** We could write a Python script that calls the API directly. This works — we get structured JSON, we can loop over namespaces. But we are writing custom collection code. Every resource type, every edge case, every API quirk — we handle it ourselves.

**Option C: MCP — Model Context Protocol.** This is a standard way to expose tools over HTTP. A prebuilt MCP server already wraps kubectl as a tool interface. We call it with a standard protocol, it returns structured data. No custom collection code.

> *Talking point: "MCP is the choice. Why? Because it gives us a standard interface. Any client — Python, curl, VS Code — can call the same tools. And we do not write collection code; we reuse a prebuilt server."*

**The trade-off:** We depend on an external MCP server image. But we gain a protocol that works across the whole pipeline.

Draw on whiteboard: `Cluster → MCP Server (kubectl tools)`

---

### Phase 2: Analyze (60s)

We have raw data. Now we need to apply policy — what labels are required, what looks orphaned, what needs attention.

**Option A: Rule engine.** Write `if/else` logic. If `owner` label missing → flag it. If PVC not mounted → orphaned. This is deterministic — same input, same output. But it is brittle. Every new rule is code. Every edge case is a new `if` statement.

**Option B: LLM.** Send the raw data plus the tagging rules to a language model. Ask it to produce structured findings. The LLM can reason about context — "this PVC looks orphaned because no pod mounts it" — without us writing case-by-case rules.

> *Talking point: "The LLM is the choice. Why? Because the policy changes — new labels, new rules, new edge cases. With a rule engine, we rewrite code. With an LLM, we change the prompt."*

**The trade-off:** LLM output is non-deterministic. The same input might produce slightly different wording each time. But we constrain it with a JSON schema — the structure is fixed, only the details vary.

Draw on whiteboard: `Raw Data + Tagging Rules → LLM → Structured Findings`

---

### Phase 3: Act (45s)

We have structured findings. Now we need to do something with them.

**Option A: Write to a file.** Good for auditing. Bad for action — nobody checks a JSON file daily.

**Option B: Post to an issue tracker.** Create tickets. Assign them. Track them. This is what teams actually do with findings.

> *Talking point: "Issue tracker is the choice. And we use the same protocol — MCP — to post tickets. That keeps the pipeline consistent."*

**The trade-off:** We are building a simple tracker, not Jira. But the pattern transfers — swap the MCP endpoint for Jira's API and the integration code barely changes.

Draw on whiteboard: `Structured Findings → Tracker MCP → Tickets on Board`

---

### The Full Pipeline (30s)

Connect the pieces:

```
Cluster → MCP Server → Collector → LLM Analyzer → Tracker → Board
              ↓              ↓            ↓
         kubectl tools    JSON snapshot   Structured tickets
```

Each arrow is a section we will build:
- Section 05: MCP Server (curl validation)
- Section 06: Collector (Python MCP client)
- Section 07: LLM Analyzer (LangChain + structured output)
- Section 08: Tracker (FastAPI + MCP)
- Section 09: Integration (wire it all together)

> *Talking point: "Next video, we zoom into each component — what it does, what it takes, what it produces."*

---

## Key takeaways
- **Collect** via MCP — standard protocol, no custom collection code
- **Analyze** via LLM — flexible policy application, constrained by JSON schema
- **Act** via tracker — tickets, not files, using the same MCP protocol
- The pipeline is five sections: 05 through 09
