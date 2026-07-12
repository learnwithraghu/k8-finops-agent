# Archived Plan (v1): Prompt-First MCP FinOps Demo

## Status
This document captures the original authoring-first design and is preserved as history. Section numbers below refer to the **old** numbering. For the current numbering see `sections/README.md` and `sections/structure-plan.md`.

Reorg note (applies to this historical doc only):
- old Section 05 LLM LangChain  → retired
- old Section 06 Issue Tracker  → now Section 08 (merged with integration)
- old Section 07 Integration      → merged into Section 08
- old Section 08 K8s-Native       → now Section 10
- old Section 09 MCP Setup        → now Section 05
- old Section 10 Advanced MCP     → decommissioned; code split into new Section 06 (collector) and Section 07 (analyser/models/main + tagging rules)
- langchain-only agent track retired — the MCP-agent track (05 → 06 → 07 → 08) now covers collection, policy, tracker, and integration

Current curriculum split:
- Section 05: curl-validated prebuilt MCP setup
- Section 06: first MCP data agent (prompt → MCP → unstructured data)
- Section 07: LLM structured agent (snapshot + tagging rules → policy-aware audit)
- Section 08: issue tracker service + agent integration (from findings to tickets)
- Section 09: agent refactoring best practices
- Section 10: Kubernetes-native agent (Helm)

## Why This Section Exists

Section 05 proved the first big lesson: a few prompts can do a lot more than a pile of hand-written logic.

Section 10 now carries the handoff where MCP reads cluster data, prompts do the reasoning, and the Section 06 tracker service receives the final tickets.

The point of this section is **not** to teach a bigger codebase.
The point is to show a learner that:

- MCP gives us tools, not a new framework to babysit
- prompts can do the heavy lifting
- the code can stay tiny
- the pipeline can still end in tracker tickets

If this section grows more complex than Section 05, we missed the point.

---

## Core Teaching Idea

**Less code. More prompt.**

Instead of building many classes, wrappers, and models, the demo should use:

- one thin MCP server
- one simple prompt-driven collector
- one simple prompt-driven analyst
- one tiny tracker writer step

The learner should feel:
> “Oh — this is mostly prompt design and orchestration, not a huge Python architecture.”

---

## Section 10 Goal

Build a **three-step pipeline** with minimal code:

1. **Agent 1 — Collector**
   - uses MCP tools
   - gathers raw Kubernetes facts
   - outputs plain JSON

2. **Agent 2 — Analyst**
   - receives Agent 1’s JSON
   - receives tagging rules in the prompt
   - outputs structured compliance JSON

3. **Agent 3 — Tracker writer**
   - receives the structured compliance JSON
   - POSTs only the violations to the Section 06 issue tracker service (`POST /create-issue`)

**Important:** avoid creating a new class hierarchy for each step.
The whole lesson is that prompts + a little glue are enough.

---

## What We Are Simplifying

We should deliberately avoid the kind of code that makes the lesson feel heavy:

- no collector class just to loop namespaces
- no analyzer service layer
- no deep model hierarchy
- no tracker domain objects unless absolutely needed
- no custom abstraction over MCP that hides what is happening

The learner should still be able to read the whole section in one sitting.

---

## Repo Location

```text
sections/10-advanced-mcp-finops/
```

### Existing sections remain unchanged

No renumbering of Sections 06–08.

---

## Simplified Architecture

```text
kind cluster
     │
     ▼
┌─────────────────────────────────┐
│ MCP server                      │
│ 6 read-only Kubernetes tools    │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ Agent 1 — Collector             │
│ prompt + tool calls              │
│ raw JSON                         │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ Agent 2 — Analyst               │
│ prompt + tagging rules           │
│ compliance JSON                  │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ Agent 3 — Tracker writer        │
│ tiny POST step                   │
│ Jira-style ticket(s)             │
└─────────────────────────────────┘
```

---

## Step 1: Keep the MCP server thin

The MCP server should expose only the Kubernetes reads we need:

| Tool | Purpose |
|---|---|
| `list_namespaces` | Return non-system namespaces |
| `list_deployments(namespace)` | Return basic deployment metadata |
| `list_pods(namespace)` | Return pod metadata and status |
| `list_services(namespace)` | Return service metadata |
| `list_pvcs(namespace)` | Return PVC metadata |
| `list_configmaps(namespace)` | Return configmap metadata |

### Keep it simple

- return plain JSON-friendly dicts
- avoid optional features for the first pass
- do not require metrics-server
- do not add clever wrappers just to normalize every field

### Why this matters

The MCP server should feel like a thin adapter over the cluster, not another mini-framework.

---

## Step 2: Make Agent 1 mostly prompt-driven

Agent 1 should be a **small orchestrator**, not a rich Python subsystem.

### What it does

- call `list_namespaces`
- call the resource tools for each namespace
- assemble a raw snapshot
- emit plain JSON

### What it should not do

- no compliance judgments
- no cost interpretation
- no tracker logic
- no custom domain object graph

### Teaching angle

This is where we show that the “collector” is mostly just a prompt-guided loop over tools.
The learner should not feel like they are building an SDK.

---

## Step 3: Make Agent 2 a pure prompt + schema step

Agent 2 receives:

- the raw JSON from Agent 1
- the tagging rules YAML

It returns:

- one structured report in JSON
- one entry per resource
- compliance verdicts and remediation hints

### Keep the output shape minimal

Only keep the fields that help the lesson:

- resource identity
- compliance flag
- category
- missing tags
- reason
- suggested owner / cost center
- suggested tags

### Avoid

- Jira fields in the compliance model
- extra nested objects
- long-form “analysis” blobs
- multiple schema classes for the same idea

### Teaching angle

The learner should see that the LLM is doing the policy application, not the code.

---

## Step 4: Make Agent 3 a tiny tracker writer

Agent 3 should be the smallest piece of the whole demo.
It should treat the Section 06 tracker as the final ticket sink, not another subsystem.

### What it does

- read the structured compliance JSON
- filter non-compliant items
- POST one issue per finding to the tracker

### What it should feel like

Not a separate subsystem.
Just a final transport step.

### Keep the lesson clear

Agent 3 exists only to prove the output from Agent 2 is already structured enough to become work items.
No extra transformation layer should be needed.

---

## Step 5: Keep the prompt bounded

This is the main learning payoff.

The prompt should do the work that classes usually do in heavier designs.

### Prompt pattern

- **System prompt**: role, rules, output discipline
- **User prompt**: raw JSON snapshot
- **User prompt**: tagging policy YAML
- **User prompt**: output schema instructions

### Why this matters

We want the student to notice that the difference between “a lot of code” and “a useful system” is often prompt structure, not architecture.

---

## Step 6: Keep files and code surface small

The section should be teachable in one short walkthrough.

### Suggested file set

```text
sections/10-advanced-mcp-finops/
├── section_goal.md
├── guide.md
├── config/
│   └── tagging-rules.yaml
├── mcp_server/
│   └── server.py
├── agent/
│   └── main.py
└── requirements.txt
```

### Optional only if truly needed

- `prompts.py` if it keeps `main.py` shorter
- `schemas.py` if the output shape becomes hard to read inline

### What to avoid

If the code starts producing `collector.py`, `analyser.py`, `tracker.py`, `models.py`, and helper classes for each, that is a sign the demo has become too heavy.

---

## Step 7: Keep the section docs aligned with the simplicity message

The docs should reinforce the same lesson:

- Section 06 provides the ticket sink

- this is a prompt-first demo
- MCP is just the tool seam
- the pipeline is small
- the LLM is doing the real work
- the tracker step is only the handoff into Section 06

The docs should not over-teach implementation details the learner does not need.

---

## Implementation Checklist

- [ ] Keep the MCP server thin and tool-focused
- [ ] Keep Agent 1 as a minimal tool-orchestrated collector
- [ ] Keep Agent 2 as a prompt-first analyzer with a small output schema
- [ ] Keep Agent 3 as a tiny tracker POST step
- [ ] Avoid class-heavy design unless a single tiny schema is unavoidable
- [ ] Use the root `.env` as the only runtime source of truth
- [ ] Keep the code surface smaller than Section 05 if possible
- [ ] Make the section easy to teach in one pass

---

## Success Criteria

A learner should be able to say:

- “MCP gave us tools.”
- “Prompts did the heavy lifting.”
- “The code stayed small.”
- “We still got a compliance report and tracker tickets.”

That is the whole point of the section.
