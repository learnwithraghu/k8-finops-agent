# Plan: Section 06 — MCP-Powered K8s FinOps Agent

## Where We Are After Section 05

Section 05 (`05-llm-agent-langchain`) showed how to wire an LLM into the FinOps loop.
The agent can now read Kubernetes resources, apply a tagging policy, and draft
GitHub issues — all in one run. The code works.

But look at `main.py` again:

```python
from agent.scanner import K8sScanner
...
scanner = K8sScanner(...)
scanner.connect()
resources = scanner.scan_all()
```

And `scanner.py` is ~300 lines of hand-written Kubernetes client code.

---

## The Question We Should Be Asking

> **Why do we even need `scanner.py`?**

Think about what it actually does:

| What `scanner.py` does | How many lines | Could something else do this? |
|---|---|---|
| Load kubeconfig | ~10 | Yes — any K8s client |
| List namespaces | ~15 | Yes — `kubectl get ns` |
| Scan deployments (CPU/mem parsing) | ~60 | Yes |
| Scan services | ~30 | Yes |
| Scan configmaps | ~25 | Yes |
| Scan PVCs + orphan detection | ~50 | Yes |
| Parse CPU/memory/storage strings | ~30 | Yes |

Every one of those tasks is already solved. The Kubernetes API is already there.
`scanner.py` is a bespoke wrapper we maintain ourselves — with its own bugs,
edge cases, and update burden.

### The Problems with `scanner.py`

1. **It's tightly coupled to the agent.** The scanner is imported and called
   directly. If you want to use the same data from a different tool or agent
   framework, you have to copy the file.

2. **The LLM cannot drive it.** The LLM tells the scanner nothing. The scanner
   always runs in full, even if the LLM only needs one namespace.

3. **It cannot be composed.** If two agents need cluster data they each need
   their own scanner instance.

4. **It leaks implementation detail into the agent.** `main.py` has to know
   about `K8sScanner`, `scan_all()`, excluded namespaces, and `K8sResource`.
   None of that is the agent's job.

### What We Want Instead

We want the LLM to be able to ask: *"Show me all deployments in the `airline`
namespace"* — and get an answer — without any of that wiring living inside the
agent itself.

That is exactly what **MCP (Model Context Protocol)** was designed for.

---

## Section 06: MCP K8s Agent

**Goal:** Replace `scanner.py` with an MCP server that exposes Kubernetes
operations as callable tools. Build a two-agent pipeline where:

- **Agent 1** uses MCP tools to collect raw cluster metrics and dumps them as
  structured JSON.
- **Agent 2** receives that JSON plus the tagging rules YAML in its system
  prompt, then produces a structured output that is ready to become a Jira
  ticket.

### New Repo Location

```
sections/06-mcp-k8-agent/
```

Existing sections 06-08 shift to 07-09.

---

## Step 1: Set Up the MCP Server (kind cluster, local)

We will use the **`kubernetes-mcp-server`** approach — a thin MCP server backed
by the Kubernetes Python client. It calls the K8s API directly (no `kubectl`
subprocess). Because we are running against a local **kind** cluster, the
server reads the existing kubeconfig at `~/.kube/config` with no extra setup.

### MCP server tools to expose

| Tool name | What it does |
|---|---|
| `list_namespaces` | Returns all non-system namespaces |
| `list_deployments(namespace)` | Returns deployments with CPU/mem requests and labels |
| `list_pods(namespace)` | Returns pods with status, node, and resource usage |
| `list_services(namespace)` | Returns services and their types |
| `list_pvcs(namespace)` | Returns PVCs with size and mount status |
| `list_configmaps(namespace)` | Returns configmaps (excluding system ones) |

The server is a standalone Python process started with `uvx mcp` or run
directly. Claude Code / any MCP-aware agent connects via stdio.

### Why this beats `scanner.py`

- The LLM decides **which tools to call** and **which namespaces to target**.
- Any agent (or Claude Code itself) can reuse the same server without importing
  any custom code.
- The server can be tested independently with `mcp inspect`.

---

## Step 2: Agent 1 — Raw Metrics Collector

**Model:** GPT-4o (OpenAI API key already configured)

**Role:** Drive the MCP server to collect raw cluster state and emit a JSON
payload. This agent does **no analysis** — it only fetches.

### System Prompt (Agent 1)

```
You are a Kubernetes cluster scanner.
Your job is to collect raw resource data from a local kind cluster using
the tools available to you. Do not analyze, score, or judge any resource.

Call the tools in this order:
1. list_namespaces — collect all non-system namespaces.
2. For each namespace: list_deployments, list_pods, list_services,
   list_pvcs, list_configmaps.

Return a single JSON object structured as:
{
  "scanned_at": "<ISO timestamp>",
  "namespaces": ["..."],
  "resources": [
    {
      "kind": "Deployment",
      "namespace": "...",
      "name": "...",
      "labels": {},
      "annotations": {},
      "cpu_request_m": 0,
      "memory_request_mi": 0,
      "replicas": 1,
      "pvcs": []
    },
    ...
  ]
}

Do not add any explanatory text outside the JSON block.
```

### What Agent 1 produces

A raw JSON dump of every non-system resource. No opinions. No compliance
verdicts. Just data.

---

## Step 3: Agent 2 — Tagging Compliance Analyser

**Model:** GPT-4o

**Role:** Receive Agent 1's JSON output, apply the tagging rules, and produce a
structured report that is ready to feed into Jira ticket creation (the next
section).

### System Prompt (Agent 2)

The system prompt is constructed at runtime by injecting the full contents of
`config/tagging-rules.yaml` verbatim:

```
You are a FinOps compliance analyser for a Kubernetes-based airline platform.

You will receive a JSON snapshot of cluster resources collected by a scanner
agent. Apply the tagging policy below and produce a structured compliance
report.

--- TAGGING POLICY (tagging-rules.yaml) ---
<< full YAML injected here at runtime >>
-------------------------------------------

For each resource produce one entry in the `violations` array.
Return ONLY valid JSON matching the schema described below — no markdown,
no explanation outside the JSON block.
```

### Output Schema (Pydantic — Jira-compatible)

```python
class ResourceViolation(BaseModel):
    # Identity
    kind: str
    namespace: str
    name: str

    # Compliance verdict
    is_compliant: bool
    missing_tags: List[str]
    category: Literal["tagged", "unallocated", "unowned", "orphaned", "unknown"]
    priority: Literal["critical", "high", "medium", "low"]
    reason: str

    # Jira-ready fields (next section feeds these in directly)
    jira_summary: str        # e.g. "[FinOps] airline/booking-api - unowned"
    jira_description: str    # markdown body with context and remediation steps
    jira_labels: List[str]   # e.g. ["finops", "unowned", "high-priority"]
    jira_priority: str       # Jira priority name: "High", "Medium", "Low"
    jira_components: List[str]  # e.g. ["Platform", "Booking Engine"]

    # Suggested remediation
    suggested_cost_center: str
    suggested_owner: str
    suggested_tags: Dict[str, str]


class ComplianceReport(BaseModel):
    scanned_at: str
    cluster: str
    total_resources: int
    compliant_count: int
    violation_count: int
    violations: List[ResourceViolation]
```

The `jira_*` fields are populated by the LLM based on the resource context and
tagging rules. The next section (Jira integration) will consume this output
directly without any transformation.

---

## Pipeline Flow

```
kind cluster
     │
     │  K8s API calls (MCP tools)
     ▼
┌─────────────────────────────────┐
│  kubernetes-mcp-server          │
│  (local stdio process)          │
└────────────────┬────────────────┘
                 │  raw tool responses
                 ▼
┌─────────────────────────────────┐
│  Agent 1 — Raw Metrics          │
│  Model: GPT-4o                  │
│  System prompt: "collect only"  │
│  Output: raw JSON               │
└────────────────┬────────────────┘
                 │  raw JSON payload
                 ▼
┌─────────────────────────────────┐
│  Agent 2 — Compliance Analyser  │
│  Model: GPT-4o                  │
│  System prompt:                 │
│    + tagging-rules.yaml (full)  │
│  Input: raw JSON from Agent 1   │
│  Output: ComplianceReport JSON  │
└────────────────┬────────────────┘
                 │  structured output
                 ▼
        Jira ticket creation
           (Section 07)
```

---

## Section 06 Directory Structure

```
sections/06-mcp-k8-agent/
├── section_goal.md
├── guide.md
├── config/
│   └── tagging-rules.yaml        # copy from section 05
├── mcp_server/
│   ├── __init__.py
│   ├── server.py                 # MCP server: exposes list_* tools
│   └── k8s_client.py             # thin wrapper around kubernetes-python
├── agent/
│   ├── __init__.py
│   ├── main.py                   # orchestrates Agent 1 → Agent 2
│   ├── collector.py              # Agent 1: drives MCP, emits raw JSON
│   ├── analyser.py               # Agent 2: receives JSON, returns ComplianceReport
│   └── models.py                 # ResourceViolation + ComplianceReport Pydantic models
├── requirements.txt
└── .env.example
```

---

## Implementation Checklist

- [ ] Create `sections/06-mcp-k8-agent/` with `section_goal.md` and `guide.md`
- [ ] Build `mcp_server/server.py` with the 6 tools listed above
- [ ] Verify MCP server against local kind cluster with `mcp inspect`
- [ ] Write `agent/collector.py` (Agent 1) with system prompt and MCP client
- [ ] Write `agent/models.py` with `ResourceViolation` and `ComplianceReport`
- [ ] Write `agent/analyser.py` (Agent 2) with YAML-injected system prompt
- [ ] Wire both agents in `agent/main.py`
- [ ] End-to-end test: run `python -m agent.main` against kind cluster
- [ ] Confirm `ComplianceReport` JSON structure is accepted by the Jira section stub

---

## What Changes in Existing Sections

| Section | Change |
|---|---|
| 05-llm-agent-langchain | No change — `scanner.py` stays as the "before" artifact |
| 06-issue-tracker-service | Renumbered to 07 |
| 07-agent-to-tracker-integration | Renumbered to 08 |
| 08-k8-native-agent | Renumbered to 09 |
