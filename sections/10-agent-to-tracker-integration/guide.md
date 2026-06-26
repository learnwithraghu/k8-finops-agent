# Section 10 Guide: Agent to Tracker Integration

This is the only file you need for Section 10.

## Goal
Take the LLM decisions from Section 08 and turn the actionable ones into tickets in the Section 09 issue tracker service.

## Tutor note
Make sure the tracker from Section 09 is already running before starting this section. The agent will send tickets to that service.

## What students will learn
- how the Section 08 decision output maps to a tracker ticket payload
- how a tiny HTTP client (`tracker`, moved from the previous advanced pipeline) can POST issues to the local tracker
- how to verify tickets appear in the tracker UI

## What you need before starting
Complete Sections 01, 02, 03, 04, 08, and 09 first.

You should already have:
- a working Kind cluster
- the airline app deployed
- the Section 08 LLM agent running locally
- an API key for the OpenAI-compatible endpoint
- the issue tracker container running on `http://localhost:8085`

## Where the integration code lives
- `sections/10-agent-to-tracker-integration/agent/`

## Step 0: Start the issue tracker first
Open a terminal and run the Section 09 tracker if it is not already running:
```bash
docker run --rm -p 8085:8000 --name finops-issue-tracker finops-issue-tracker:latest
```

What to look for:
- the tracker must be up before the agent can create tickets
- the agent will call `http://localhost:8085/create-issue`

## Step 1: Check the environment file
Make sure the environment points to the local tracker and has the LLM credentials:
```bash
grep -nE '^(OPENAI_BASE_URL|OPENAI_API_KEY|OPENAI_MODEL_ID|ISSUE_TRACKER_URL)=' .env
```

What to look for:
- `OPENAI_API_KEY` is set
- `ISSUE_TRACKER_URL` points to the local tracker service (`http://localhost:8085`)
- the same OpenAI-compatible settings from Section 08 are present

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
cat sections/10-agent-to-tracker-integration/agent/tracker.py
```

What to look for:
- `IssueTrackerClient` checks `/health` before sending issues
- `build_payload` maps a `ResourceDecision` to the tracker `IssueCreate` schema
- `create_issues` sends one `POST /create-issue` per actionable finding
- the client is intentionally small; it only knows how to map a decision to a payload and POST it

## Step 3: Read the integration orchestrator
```bash
cat sections/10-agent-to-tracker-integration/agent/main.py
```

What to look for:
- the same scan + LLM flow as Section 08, always scanning all namespaces
- after the report, the agent filters decisions where `should_create_issue=True`
- those decisions are sent to the tracker via `IssueTrackerClient`
- the tracker must be reachable or the agent exits with an error

## Step 4: Create tickets in the tracker
```bash
PYTHONPATH=sections/10-agent-to-tracker-integration python3 -m agent.main
```

What to look for:
- the agent scans Kubernetes resources in all namespaces
- the LLM produces decisions
- actionable decisions are POSTed to `http://localhost:8085/create-issue`
- new tickets appear in the Section 09 board

## Step 5: Open the tracker UI
Visit:
```text
http://localhost:8085
```

What to look for:
- new cards should appear on the board
- each card shows the issue key, title, priority, namespace, and suggested owner

## What to notice
- Section 08 decides *what* to do.
- Section 10 does one new thing: it turns those decisions into tracker tickets.
- The tracker client is intentionally small — it only knows how to map a decision to a payload and POST it.
- The agent always scans all namespaces, so the board reflects the whole cluster.

## Expected outcome
You should be able to explain:
- why the tracker must be running first
- how a `ResourceDecision` becomes a tracker payload
- how to verify the tickets landed in the board

## Handoff to Section 11
Once the agent-to-tracker flow works, move to:
- `sections/11-k8-native-agent/guide.md`