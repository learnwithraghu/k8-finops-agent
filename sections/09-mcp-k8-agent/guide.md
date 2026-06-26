# Section 09 Guide: MCP-Powered K8s FinOps Agent

This is the only file you need for Section 09.

## Goal
Use MCP tools to collect Kubernetes data, then send the raw snapshot through an LLM analyst and a tracker writer so actionable findings become Jira-style tickets.

## Tutor note
Keep the distinction clear:
- the collector just gathers data
- the analyst applies the policy
- the tracker writer turns violations into tickets

## What students will learn
- how MCP exposes Kubernetes operations as reusable tools
- how a simple collector function can talk to an MCP server over stdio
- how the raw cluster snapshot is assembled
- how the LLM analyst applies tagging rules to the snapshot
- how the LLM can draft tracker-ready tickets directly
- how a tiny tracker function just POSTs those tickets

## What you need before starting
Complete Sections 01 through 08 first.

You should already have:
- a working Kind cluster
- the airline app deployed
- the Section 08 agent code available
- a root `.env` file with the OpenAI-compatible API key and tracker URL

## Where the code lives
- `sections/09-mcp-k8-agent/mcp_server/`
- `sections/09-mcp-k8-agent/agent/`
- `sections/09-mcp-k8-agent/config/tagging-rules.yaml`

The root `.env` file is the source of truth for runtime settings.

## Step 0: Make sure the issue tracker is running
The pipeline posts actionable findings to the Section 06 tracker service.

What to check:
- the `finops-issue-tracker` container is running
- `ISSUE_TRACKER_URL` in the root `.env` points to it

## Step 1: Read the section goal
Open:
```bash
cat sections/09-mcp-k8-agent/section_goal.md
```

What to look for:
- the collector/analyst/tracker split
- how actionable findings move into the tracker

## Step 2: Inspect the MCP server
Open:
```bash
cat sections/09-mcp-k8-agent/mcp_server/server.py
cat sections/09-mcp-k8-agent/mcp_server/k8s_client.py
```

What to look for:
- the six Kubernetes tools
- namespace filtering
- the thin Kubernetes client wrapper
- no dependency on `kubectl` subprocess calls

## Step 3: Inspect the collector function
Open:
```bash
cat sections/09-mcp-k8-agent/agent/collector.py
```

What to look for:
- a single function that connects to the MCP server over stdio
- it calls `list_namespaces` first
- it iterates namespaces and gathers raw resource data
- it does not score or judge resources

## Step 4: Inspect the tiny models
Open:
```bash
cat sections/09-mcp-k8-agent/agent/models.py
```

What to look for:
- the ticket model matches `/create-issue`
- the batch model only wraps the LLM output
- no compliance report layer
- no envelope object between the analyst and tracker

## Step 5: Inspect the analyst
Open:
```bash
cat sections/09-mcp-k8-agent/agent/analyser.py
```

What to look for:
- the full tagging policy is injected at runtime
- the snapshot is sent as JSON
- the LLM returns tracker-ready ticket drafts directly
- the code does not compute a separate compliance report

## Step 6: Inspect the orchestrator
Open:
```bash
cat sections/09-mcp-k8-agent/agent/main.py
```

What to look for:
- the collector runs first
- the analyst runs second
- the tracker runs third
- the code reads like a straight script, not a framework demo
- the LLM already produced the final ticket payloads

## Step 7: Run the agent locally
```bash
PYTHONPATH=sections/09-mcp-k8-agent python3 -m agent.main
```

What to look for:
- the collector connects to the MCP server
- the snapshot includes all non-system namespaces and their resources
- the analyst returns structured compliance output
- actionable items are POSTed to the tracker

## What to notice
- MCP removes the need for a bespoke scanner module
- the collector is deterministic and reusable
- the LLM is only used where judgment is needed
- the tracker step is separate and only sees structured output

## Expected outcome
You should be able to explain:
- why MCP is a better seam than a custom scanner
- how the collector, analyst, and tracker responsibilities differ
- how the raw JSON snapshot feeds the compliance report
- how actionable findings land in the issue tracker
