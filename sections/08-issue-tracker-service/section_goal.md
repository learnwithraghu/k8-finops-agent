# Section 08 Goal: Issue Tracker Service

## Goal
Build a lightweight Jira-style tracker with FastAPI that later FinOps agent sections can use to create, open, assign, and move findings as tickets. The tracker exposes both a REST API and an MCP server so agents can integrate through either protocol.

## Scope
- Run the tracker container locally with REST on port 8085 and MCP on port 8086
- Serve a simple Kanban board UI
- Expose `/create-issue` as the main ticket-creation REST endpoint
- Expose MCP tools: `create_issue`, `list_issues`, `get_issue`, `update_issue`
- Expose `/issue/{id}` to open a ticket
- Allow assignment and status movement
- Show the API response and docs
- Validate MCP endpoint with curl

## Out of scope
- Kubernetes scan logic
- Bedrock prompt engineering
- Kubernetes-native deployment

## Success criteria
The learner can create a ticket through `/create-issue` (REST) or `create_issue` (MCP tool), open it in the UI, assign it, and move it across the board.
