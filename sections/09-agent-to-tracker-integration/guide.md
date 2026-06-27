# Section 09 Guide: Agent to Tracker Integration

This is the only file you need for Section 09.

> **Status**: the current `agent/` code is transitional. It reproduces the legacy
> LangChain scanner pipeline (scan → LLM decision → tracker ticket) and by-passes
> Section 07. In the follow-up "work on 1st agent" session, this agent is being
> rewritten to consume Section 07's `TicketBatch` JSON and post each
> `TrackerTicket` to the Section 08 tracker. This guide describes both the
> current (transitional) flow and the target (post-rewrite) flow.

## Goal
Turn Section 07's structured findings into tracker tickets in the Section 08 issue tracker service using MCP tools.

## Tutor note
Make sure the tracker from Section 08 is already running before starting this section. The tracker now exposes both REST (port 8085) and MCP (port 8086) endpoints.

## What students will learn
- how a `TrackerTicket` (from Section 07) maps to the Section 08 tracker `IssueCreate` schema
- how a small MCP client (`tracker.py`) calls the `create_issue` tool on the local tracker
- how to verify tickets appear in the tracker UI
- why idempotency and stable correlation keys matter when creating tickets from agent output
- the difference between HTTP REST calls and MCP tool calls

## What you need before starting
Complete Sections 01, 02, 03, 04, 05, 06, 07, and 08 first.

You should already have:
- a working Kind cluster
- the airline app deployed
- the Section 07 LLM structured agent producing a `TicketBatch` JSON
- the Section 08 issue tracker container running with both REST (port 8085) and MCP (port 8086)

## Where the integration code lives
- `sections/09-agent-to-tracker-integration/agent/`
  - `tracker.py` — MCP client for the Section 08 tracker (this is the file that survives the rewrite)
  - `scanner.py`, `analyzer.py`, `main.py` — transitional LangChain scanner pipeline (removed in the rewrite)

## Step 0: Start the issue tracker first
Open a terminal and run the Section 08 tracker if it is not already running:
```bash
docker run --rm -p 8085:8000 -p 8086:8001 --name finops-issue-tracker finops-issue-tracker:latest
```

What to look for:
- the tracker must be up before the agent can create tickets
- the REST API is available at `http://localhost:8085`
- the MCP server is available at `http://localhost:8086/mcp`

## Step 1: Check the environment file
```bash
grep -nE '^(OPENAI_BASE_URL|OPENAI_API_KEY|OPENAI_MODEL_ID|ISSUE_TRACKER_MCP_URL)=' .env
```
What to look for:
- `OPENAI_API_KEY` is set (used by the transitional scanner today; after the rewrite this section reads structured findings from Section 07 and no longer calls the LLM)
- `ISSUE_TRACKER_MCP_URL` points to the Section 08 tracker MCP endpoint (`http://localhost:8086/mcp`)

Example `.env` entries:
```env
OPENAI_BASE_URL=https://api.ai.kodekloud.com/v1
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL_ID=gpt-4o
OPENAI_MAX_TOKENS=1024
OPENAI_TEMPERATURE=0.3
ISSUE_TRACKER_MCP_URL=http://localhost:8086/mcp
```

## Step 2: Read the MCP tracker client
```bash
cat sections/09-agent-to-tracker-integration/agent/tracker.py
```
What to look for:
- `IssueTrackerClient` connects to the MCP server via SSE transport
- `create_issue` calls the `create_issue` MCP tool with the arguments
- `create_issues` iterates over actionable findings and calls the tool for each
- no HTTP session, no manual payload mapping — the MCP tool handles the schema
- compare this to the old REST version: ~70 lines vs 104 lines, and much simpler

## Step 3: Read the orchestrator (transitional)
```bash
cat sections/09-agent-to-tracker-integration/agent/main.py
```
What to look for in the transitional flow:
- scan + LLM flow, filtering decisions where `should_create_issue=True`
- calls the MCP `create_issue` tool via `IssueTrackerClient`
What the rewritten flow will look like instead:
- read Section 07's `TicketBatch` JSON (via `--findings /tmp/section07-findings.json`)
- call `create_issue` MCP tool for each `TrackerTicket`; no LLM call, no scanner

## Step 4: Create tickets in the tracker (transitional run command)
Until the rewrite lands, the agent still scans on its own:
```bash
PYTHONPATH=sections/09-agent-to-tracker-integration python3 -m agent.main
```
Expected:
- the agent scans Kubernetes resources in all namespaces
- the LLM produces decisions
- actionable decisions are sent to the tracker via MCP `create_issue` tool
- new tickets appear in the Section 08 board

After the rewrite the run command becomes approximately:
```bash
PYTHONPATH=sections/09-agent-to-tracker-integration \
  python3 -m agent.main --findings /tmp/section07-findings.json
```

## Step 5: Open the tracker UI
Visit:
```text
http://localhost:8085
```
What to look for:
- new cards appear on the board
- each card shows the issue key, title, priority, namespace, and suggested owner
- the `source` field shows `mcp-llm-agent` (created via MCP tool call)

## Discussion
- Section 07 decides *what* to do; Section 09 turns those decisions into tracker tickets via MCP.
- Compare the old REST client (104 lines with HTTP session, payload mapping, error handling) to the new MCP client (~70 lines, just call the tool).
- Why idempotency matters: re-running the agent must not spam duplicate tickets. A stable correlation key (namespace + resource_name + rule) is the de-dup key in the tracker.
- After the rewrite, the agent in this section will be small (no scanner, no analyzer) — the LLM and tagging rules stay in Section 07, collection stays in Section 06.

## Cleanup
Stop the Section 08 tracker container when done. No cluster changes are made by this agent — it is read-only.

## Expected outcome
You should be able to explain:
- why the tracker must be running first (both REST and MCP endpoints)
- how a `TrackerTicket` becomes a tracker payload via MCP tool call
- how to verify the tickets landed in the board
- the difference between REST and MCP integration
- why the rewrite moves this section from "scanner + analyzer + tracker" to "tracker only"

## Handoff to Section 10
Once the agent-to-tracker flow works, move to:
- `sections/10-k8-native-agent/guide.md`