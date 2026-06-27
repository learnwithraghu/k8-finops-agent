# Section 08 Guide: Issue Tracker Service

This is the only file you need for Section 08.

## Goal
Build a simple Jira-style Kanban board with FastAPI so FinOps findings can be created programmatically, opened, assigned, and moved. The tracker exposes both a REST API and an MCP server, so agents can create tickets through either protocol.

## Tutor note
Keep this section simple: show the board, show the `/create-issue` endpoint, create one ticket, and then assign or move it through the API.

## What students will learn
- how to start a local tracker with Docker
- how the Jira-style board works
- how the `/create-issue` endpoint creates a ticket
- how to use Swagger to send the payload
- how to assign and move a ticket across backlog, to do, in progress, and done
- how the tracker exposes MCP tools on a separate port for agent integration

## What you need before starting
Complete Sections 01, 02, 03, 04, and 08 first.

## Where the tracker code lives
- `sections/08-issue-tracker-service/service/`

## Step 1: Clean up any old tracker container
```bash
docker stop finops-issue-tracker 2>/dev/null || true
docker rm finops-issue-tracker 2>/dev/null || true
```

What to look for:
- this clears the old container name before starting again

## Step 2: Inspect the tracker files
```bash
find sections/08-issue-tracker-service/service -maxdepth 3 -type f | sort
```

What to look for:
- FastAPI backend files
- HTML, CSS, and JavaScript for the board UI
- the Dockerfile

## Step 3: Build the Docker image
```bash
docker build -t finops-issue-tracker:latest sections/08-issue-tracker-service/service
```

What to look for:
- the image builds locally
- this is the tracker you will run in a separate terminal

## Step 4: Run the tracker container
Open a second terminal and run:
```bash
docker run --rm -p 8085:8000 -p 8086:8001 --name finops-issue-tracker finops-issue-tracker:latest
```

What to look for:
- the REST API listens inside the container on port 8000, exposed on host port 8085
- the MCP server listens inside the container on port 8001, exposed on host port 8086
- both processes share the same `data/issues.json` store

## Step 5: Open the board UI
Visit:
```text
http://localhost:8085
```

What to look for:
- a simple Jira-style Kanban board
- columns for backlog, to do, in progress, and done
- cards can be dragged between columns
- clicking a card opens the issue details panel

## Step 6: Open the FastAPI docs
Visit:
```text
http://localhost:8085/docs
```

What to look for:
- the `/create-issue` endpoint
- the `/issue` and `/raise-issue` aliases for compatibility
- the `/issue/{id}` endpoint for opening a ticket
- the `PATCH /issue/{id}` endpoint for moving or assigning it

## Step 7: Create a ticket through the API
Run this in a third terminal:
```bash
curl -X POST http://localhost:8085/create-issue \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "[FinOps] payment/payment-processor - UNALLOCATED ($8.47/month)",
    "summary": "Missing cost-center and owner metadata",
    "body": "Bedrock flagged this as a tech-debt item.",
    "namespace": "payment",
    "resource_name": "payment-processor",
    "resource_kind": "Deployment",
    "category": "unallocated",
    "priority": "high",
    "cost_impact": 8.47,
    "suggested_owner": "payment-team",
    "suggested_cost_center": "payment",
    "reasoning": "Missing cost-center tag means the workload cannot be billed correctly.",
    "source": "bedrock"
  }'
```

What to look for:
- the response should include `id`
- the response should include a Jira-style key like `FINOPS-0001`
- the response should include the stored issue

## Step 8: Open Swagger and inspect the request body
Visit:
```text
http://localhost:8085/docs
```

What to look for:
- the `/create-issue` endpoint shows the payload schema
- the description explains how to send JSON to the tracker
- the `PATCH /issue/{id}` endpoint is available for assignment and status updates

## Step 9: Move or assign the ticket through the API
Use Swagger or curl to call `PATCH /issue/{id}`.

What to look for:
- backlog → to do → in progress → done
- assignment should show on the card
- the issue details panel should update when you open a card

## Step 10: Inspect the MCP server code
```bash
cat sections/08-issue-tracker-service/service/app/mcp_server.py
```

What to look for:
- the MCP server uses `FastMCP` from the `mcp` SDK
- it exposes four tools: `create_issue`, `list_issues`, `get_issue`, `update_issue`
- each tool delegates to the same `IssueStore` that the REST API uses
- the server runs on port 8001 with SSE transport

## Step 11: Validate the MCP endpoint with curl
List available tools:
```bash
curl -s http://localhost:8086/mcp -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python3 -m json.tool
```

What to look for:
- four tools listed: `create_issue`, `list_issues`, `get_issue`, `update_issue`
- each tool has a description and input schema

## Step 12: Create a ticket through MCP
```bash
curl -s http://localhost:8086/mcp -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "id": 2,
    "params": {
      "name": "create_issue",
      "arguments": {
        "title": "[MCP] payment/payment-processor - UNALLOCATED",
        "summary": "Created via MCP tool call",
        "namespace": "payment",
        "resource_name": "payment-processor",
        "resource_kind": "Deployment",
        "category": "unallocated",
        "priority": "high",
        "cost_impact": 8.47,
        "suggested_owner": "payment-team",
        "source": "mcp-agent"
      }
    }
  }' | python3 -m json.tool
```

What to look for:
- the response includes a new issue with `id` and `key` like `FINOPS-0002`
- the ticket appears in the Kanban board UI at `http://localhost:8085`
- the same data store backs both REST and MCP

## What to notice
- the tracker is intentionally simple
- it behaves like a lightweight Jira board
- you can move cards by dragging them
- you can open a card to inspect and edit its details
- the `/create-issue` REST endpoint is the main contract
- the MCP server exposes the same operations as tools
- both protocols share the same data store
- the board is enough to demo the handoff from Bedrock to work tracking

## Expected outcome
You should be able to explain:
- how to run the tracker locally with both REST and MCP ports
- how the board is organized
- how to create an issue through `/create-issue` (REST)
- how to create an issue through the `create_issue` MCP tool
- how to use the API to inspect, assign, and move it
- why both protocols share the same data store

## Handoff to Section 09
Once the tracker is clear, move to:
- `sections/09-agent-to-tracker-integration/guide.md`

Section 09 connects the agent output to this tracker service.
