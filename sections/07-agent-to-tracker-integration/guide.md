# Section 07 Guide: Agent to Tracker Integration

This is the only file you need for Section 07.

## Goal
Connect the Kubernetes scan, Bedrock decision flow, and the issue tracker so actionable findings become tickets.

## Tutor note
Make sure the tracker from Section 06 is already running before starting this section. The agent will send tickets to that service.

## What students will learn
- how the local scan becomes Bedrock input
- how Bedrock decisions become tracker payloads
- how to send issue data to `POST /create-issue`
- how to confirm tickets appear in the tracker UI

## What you need before starting
Complete Sections 01, 02, 03, 04, 05, and 06 first.

You should already have:
- a working Kind cluster
- the airline app deployed
- the Bedrock decision flow working
- the issue tracker container running on `http://localhost:8085`

## Step 0: Start the issue tracker first
Open a terminal and run the Section 06 tracker if it is not already running:
```bash
docker run --rm -p 8085:8000 --name finops-issue-tracker finops-issue-tracker:latest
```

What to look for:
- the tracker must be up before the agent can create tickets
- the agent will call `http://localhost:8085/create-issue`

## Where the integration code lives
- `sections/07-agent-to-tracker-integration/agent/`

## Step 1: Check the tracker URL in `.env`
Make sure the environment points to the local tracker:
```bash
grep -n '^ISSUE_TRACKER_URL=' .env || echo 'ISSUE_TRACKER_URL=http://localhost:8085'
```

What to look for:
- the agent should post to the local tracker service
- the default should be `http://localhost:8085`

## Step 2: Read the integration agent
```bash
cat sections/07-agent-to-tracker-integration/agent/main.py
```

What to look for:
- the `IssueTrackerClient`
- the mapping from Bedrock output into the tracker payload
- the `POST /create-issue` call

## Step 3: Run the agent with Bedrock enabled
```bash
PYTHONPATH=sections/07-agent-to-tracker-integration python sections/07-agent-to-tracker-integration/agent/main.py --log-level INFO
```

What to look for:
- the agent scans Kubernetes resources
- Bedrock produces issue drafts
- the agent sends actionable drafts to the tracker
- new tickets appear in the Section 06 board

## Step 4: Use mock mode if you want a local-only demo
```bash
PYTHONPATH=sections/07-agent-to-tracker-integration python sections/07-agent-to-tracker-integration/agent/main.py --mock --log-level INFO
```

What to look for:
- the same tracker flow still works
- the issues are created from mock decisions instead of Bedrock

## Step 5: Open the tracker UI
Visit:
```text
http://localhost:8085
```

What to look for:
- new cards should appear on the board
- the card should show the issue key, title, priority, namespace, and owner/assignee info

## What to notice
- Section 04 gives the scan data
- Section 05 turns scan data into decisions
- Section 06 stores those decisions as tickets
- Section 07 connects all three pieces

## Expected outcome
You should be able to explain:
- why the tracker must be running first
- how Bedrock output becomes a ticket payload
- how to verify the tickets landed in the board

## Handoff to Section 08
Once the agent-to-tracker flow works, move to:
- `sections/08-k8-native-agent/guide.md`
