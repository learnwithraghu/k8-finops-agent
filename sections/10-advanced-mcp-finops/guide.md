# Section 10 Guide: Advanced MCP FinOps Pipeline

This section is the advanced pipeline track after Section 09 setup.

## Goal
Run a full three-step pipeline:
1. collect cluster snapshot through MCP tools
2. analyze snapshot with LLM policy logic
3. post actionable findings to the issue tracker

## What students will learn
- how a deterministic collector uses MCP tools over stdio via Docker
- how tagging policy is injected into LLM analysis
- how tracker-ready tickets are produced and posted
- how advanced analysis layers differ from setup-only MCP usage

## Prerequisites
Complete Section 09 first.

You should already have:
- a working Kind cluster with app workloads
- Section 06 issue tracker running
- root `.env` configured for API key and tracker URL

## Where the code lives
- `sections/10-advanced-mcp-finops/agent/`
- `sections/10-advanced-mcp-finops/config/tagging-rules.yaml`

## Step 1: Read section goal
```bash
cat sections/10-advanced-mcp-finops/section_goal.md
```

## Step 2: Pull MCP image and configure runtime
Run:

```bash
docker pull mcp/kubernetes:latest
export KUBECONFIG_FILE="${KUBECONFIG:-$HOME/.kube/config}"
export MCP_SERVER_COMMAND=docker
export MCP_SERVER_ARGS="run --rm -i --user 0:0 -v ${KUBECONFIG_FILE}:/kubeconfig:ro -e KUBECONFIG=/kubeconfig mcp/kubernetes:latest"
```

What to look for:
- image pulls successfully
- collector has a deterministic MCP runtime command
- kubeconfig is mounted read-only into the container

## Step 3: Inspect collector
```bash
cat sections/10-advanced-mcp-finops/agent/collector.py
```

What to look for:
- stdio MCP session startup with Docker command/args
- ordered tool calls per namespace
- deterministic snapshot assembly

## Step 4: Inspect analyzer and ticket schema
```bash
cat sections/10-advanced-mcp-finops/agent/models.py
cat sections/10-advanced-mcp-finops/agent/analyser.py
```

What to look for:
- ticket schema for `/create-issue`
- policy prompt and structured output discipline
- no hidden compliance engine outside prompt+schema

## Step 5: Inspect orchestration and tracker handoff
```bash
cat sections/10-advanced-mcp-finops/agent/main.py
cat sections/10-advanced-mcp-finops/agent/tracker.py
```

What to look for:
- clear collector -> analyst -> tracker sequence
- environment-driven runtime configuration
- explicit success/failure reporting on ticket creation

## Step 6: Run advanced pipeline
```bash
PYTHONPATH=sections/10-advanced-mcp-finops python3 -m agent.main
```

Expected:
- snapshot collection succeeds
- LLM returns structured tickets
- actionable findings post to tracker service

## Cleanup
If you started any temporary services for this run, stop them and remove temporary containers.

## Expected outcome
You should be able to explain:
- when setup-only MCP (Section 09) is sufficient
- when advanced pipeline orchestration (Section 10) is worth the extra complexity
- how MCP output flows into analysis and issue management
