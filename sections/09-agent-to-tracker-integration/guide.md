# Section 09 Guide: Agent to Tracker Integration

This is the only file you need for Section 09.

> **Status**: the current `agent/` code is transitional. It reproduces the legacy
> LangChain scanner pipeline (scan → LLM decision → tracker ticket) and by-passes
> Section 07. In the follow-up "work on 1st agent" session, this agent is being
> rewritten to consume Section 07's `TicketBatch` JSON and post each
> `TrackerTicket` to the Section 08 tracker. This guide describes both the
> current (transitional) flow and the target (post-rewrite) flow.

## Goal
Turn Section 07's structured findings into tracker tickets in the Section 08 issue tracker service.

## Tutor note
Make sure the tracker from Section 08 is already running before starting this section.

## What students will learn
- how a `TrackerTicket` (from Section 07) maps to the Section 08 tracker `IssueCreate` schema
- how a small HTTP client (`tracker.py`) POSTs issues to the local tracker
- how to verify tickets appear in the tracker UI
- why idempotency and stable correlation keys matter when creating tickets from agent output

## What you need before starting
Complete Sections 01, 02, 03, 04, 05, 06, 07, and 08 first.

You should already have:
- a working Kind cluster
- the airline app deployed
- the Section 07 LLM structured agent producing a `TicketBatch` JSON
- the Section 08 issue tracker container running on `http://localhost:8085`

## Where the integration code lives
- `sections/09-agent-to-tracker-integration/agent/`
  - `tracker.py` — HTTP client for the Section 08 tracker (this is the file that survives the rewrite)
  - `scanner.py`, `analyzer.py`, `main.py` — transitional LangChain scanner pipeline (removed in the rewrite)

## Step 0: Start the issue tracker first
Open a terminal and run the Section 08 tracker if it is not already running:
```bash
docker run --rm -p 8085:8000 --name finops-issue-tracker finops-issue-tracker:latest
```

What to look for:
- the tracker must be up before the agent can create tickets
- the agent will call `http://localhost:8085/create-issue`

## Step 1: Check the environment file
```bash
grep -nE '^(OPENAI_BASE_URL|OPENAI_API_KEY|OPENAI_MODEL_ID|ISSUE_TRACKER_URL)=' .env
```
What to look for:
- `OPENAI_API_KEY` is set (used by the transitional scanner today; after the rewrite this section reads structured findings from Section 07 and no longer calls the LLM)
- `ISSUE_TRACKER_URL` points to the Section 08 tracker (`http://localhost:8085`)

Example `.env` entries:
```env
OPENAI_BASE_URL=https://api.ai.kodekloud.com/v1
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL_ID=gpt-4o
OPENAI_MAX_TOKENS=1024
OPENAI_TEMPERATURE=0.3
ISSUE_TRACKER_URL=http://localhost:8085
ISSUE_TRACKER_TIMEOUT=10
```

## Step 2: Read the tracker client
```bash
cat sections/09-agent-to-tracker-integration/agent/tracker.py
```
What to look for:
- `IssueTrackerClient` checks `/health` before sending issues
- `build_payload` maps a `ResourceDecision` (transitional) to the tracker `IssueCreate` schema
- `create_issues` sends one `POST /create-issue` per actionable finding
- after the rewrite, `build_payload` will take a Section 07 `TrackerTicket` directly and the mapping becomes near-identity

## Step 3: Read the orchestrator (transitional)
```bash
cat sections/09-agent-to-tracker-integration/agent/main.py
```
What to look for in the transitional flow:
- scan + LLM flow, filtering decisions where `should_create_issue=True`
- POSTs those to the tracker via `IssueTrackerClient`
What the rewritten flow will look like instead:
- read Section 07's `TicketBatch` JSON (via `--findings /tmp/section07-findings.json`)
- POST each `TrackerTicket` to the tracker; no LLM call, no scanner

## Step 4: Create tickets in the tracker (transitional run command)
Until the rewrite lands, the agent still scans on its own:
```bash
PYTHONPATH=sections/09-agent-to-tracker-integration python3 -m agent.main
```
Expected:
- the agent scans Kubernetes resources in all namespaces
- the LLM produces decisions
- actionable decisions are POSTed to `http://localhost:8085/create-issue`
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

## Discussion
- Section 07 decides *what* to do; Section 09 turns those decisions into tracker tickets.
- Why idempotency matters: re-running the agent must not spam duplicate tickets. A stable correlation key (namespace + resource_name + rule) is the de-dup key in the tracker.
- After the rewrite, the agent in this section will be small (no scanner, no analyzer) — the LLM and tagging rules stay in Section 07, collection stays in Section 06.

## Cleanup
Stop the Section 08 tracker container when done. No cluster changes are made by this agent — it is read-only.

## Expected outcome
You should be able to explain:
- why the tracker must be running first
- how a `TrackerTicket` becomes a tracker payload
- how to verify the tickets landed in the board
- why the rewrite moves this section from "scanner + analyzer + tracker" to "tracker only"

## Handoff to Section 10
Once the agent-to-tracker flow works, move to:
- `sections/10-k8-native-agent/guide.md`