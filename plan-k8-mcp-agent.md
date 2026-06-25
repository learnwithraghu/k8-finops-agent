# Plan: Section 09 — MCP-Powered K8s FinOps Agent

## Why This Section Exists

Section 08 teaches the packaged, Kubernetes-native agent. The next step is to remove the hand-written `scanner.py` layer and replace it with a protocol-based cluster interface.

The key idea:
- Kubernetes data collection should be exposed as tools
- the collector should be deterministic
- the LLM should only do compliance analysis
- the tracker writer should consume structured compliance output

---

## What We Are Fixing

The current Python scanner is doing too much:

- cluster discovery
- namespace iteration
- resource parsing
- orphan detection
- reporting shape

That creates a few problems:

1. **Tight coupling** — the scan logic only works inside this agent.
2. **No reuse** — another tool or agent cannot easily consume the same cluster data.
3. **No selective querying** — the whole cluster is scanned even when only one namespace is needed.
4. **Too much hidden behavior** — `main.py` knows scanner internals it should not own.

MCP solves the interface problem by making Kubernetes operations callable tools.

---

## Section Goal

Build a three-step pipeline:

- **Collector**: uses MCP tools to fetch raw cluster data and emit structured JSON.
- **Analyst**: uses the raw JSON + tagging policy to produce a compliance report.
- **Tracker**: converts non-compliant assessments into issue tracker tickets.

**Important:** the collector is not an LLM agent. It is a deterministic orchestrator.

---

## Repo Location

```text
sections/09-mcp-k8-agent/
```

### Existing sections remain unchanged

No renumbering of Sections 06–08.

---

## Architecture

```text
kind cluster
     │
     ▼
┌─────────────────────────────────┐
│ kubernetes-mcp-server           │
│ (stdio MCP process)             │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ Collector                        │
│ deterministic MCP client         │
│ raw JSON snapshot                │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ Analyst                          │
│ LLM + tagging rules              │
│ ComplianceReport JSON            │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│ Tracker                          │
│ HTTP client to local issue board  │
│ created tickets                  │
└─────────────────────────────────┘
```

---

## Step 1: Build the MCP server

Use a thin Kubernetes client wrapper that talks directly to the K8s API.

### Tools to expose

| Tool | Purpose |
|---|---|
| `list_namespaces` | Return non-system namespaces |
| `list_deployments(namespace)` | Return deployment metadata and resource requests |
| `list_pods(namespace)` | Return pod phase, node, owners, restarts, labels |
| `list_services(namespace)` | Return service type and selector info |
| `list_pvcs(namespace)` | Return PVC size, access mode, binding status |
| `list_configmaps(namespace)` | Return configmaps excluding system ones |

### Important constraint

Do **not** require `metrics-server` for the MVP.

- If pod CPU/memory usage is needed later, gate it behind an optional metrics API client.
- For the first version, keep the server usable on a plain kind cluster.

### Why this matters

This keeps the server portable and avoids a hidden cluster prerequisite.

---

## Step 2: Write the collector

The collector should:

- call `list_namespaces`
- query each namespace with the MCP tools
- build one raw JSON snapshot
- do **no compliance logic**
- do **no ticket logic**

### Output shape

```json
{
  "scanned_at": "<ISO timestamp>",
  "cluster": "kind",
  "namespaces": ["airline", "payment"],
  "resources": [
    {
      "kind": "Deployment",
      "namespace": "airline",
      "name": "booking-api",
      "labels": {},
      "annotations": {},
      "replicas": 2,
      "cpu_request_m": 100,
      "memory_request_mi": 128,
      "owners": []
    }
  ]
}
```

### Notes

- Keep it deterministic.
- Accept an optional namespace filter.
- Keep the raw snapshot stable so it can be reused by future tools.

---

## Step 3: Write the analyst

The analyst receives:

- the raw JSON snapshot
- the tagging rules YAML

It returns a structured compliance report.

### Model shape

Use a clean report model, not a Jira model.

Suggested fields:

- `kind`
- `namespace`
- `name`
- `is_compliant`
- `missing_tags`
- `category`
- `priority`
- `reason`
- `suggested_owner`
- `suggested_cost_center`
- `suggested_tags`

### What to avoid here

Do **not** put `jira_*` fields in the compliance model.
That mapping belongs to the tracker step.

---

## Step 4: Keep the prompt bounded

Inject the tagging policy as runtime context, but keep the prompt focused.

Recommended pattern:

- system message: role + output rules
- user message: raw JSON snapshot
- user message or appended context: tagging policy YAML

This is safer than relying on a huge system prompt and makes the policy easier to swap.

---

## Step 5: Add tests around the seams

Test each layer independently:

- MCP server tool responses
- collector JSON assembly
- analyst schema validation
- one end-to-end run against kind

### Keep the MCP tests realistic

Mock the Kubernetes client, not the JSON output.
That way the server contract stays honest.

---

## Directory Structure

```text
sections/09-mcp-k8-agent/
├── section_goal.md
├── guide.md
├── config/
│   └── tagging-rules.yaml
├── mcp_server/
│   ├── __init__.py
│   ├── server.py
│   └── k8s_client.py
├── agent/
│   ├── __init__.py
│   ├── main.py
│   ├── collector.py
│   ├── analyser.py
│   ├── tracker.py
│   └── models.py
├── requirements.txt
```

---

## Implementation Checklist

- [ ] Create `sections/09-mcp-k8-agent/` with `section_goal.md` and `guide.md`
- [ ] Build `mcp_server/server.py` with the six Kubernetes tools
- [ ] Keep the MCP server usable on plain kind without metrics-server
- [ ] Write `agent/collector.py` as a deterministic MCP client
- [ ] Write `agent/models.py` for the raw snapshot and compliance report
- [ ] Write `agent/analyser.py` with the tagging-policy prompt
- [ ] Wire the collector, analyst, and tracker in `agent/main.py`
- [ ] Add tests for server, collector, analyst, and tracker client
- [ ] Run an end-to-end validation against the local kind cluster

---

## What Changes in Existing Sections

| Section | Change |
|---|---|
| 05-llm-agent-langchain | No change |
| 06-issue-tracker-service | No change |
| 07-agent-to-tracker-integration | No change |
| 08-k8-native-agent | No change |

---

## Success Criteria

You should be able to:

- query Kubernetes through MCP tools
- collect a full raw cluster snapshot without `scanner.py`
- generate a compliance report from the snapshot
- explain why the collector is deterministic and the analyst is the only LLM step
- create issue tracker tickets from non-compliant results
