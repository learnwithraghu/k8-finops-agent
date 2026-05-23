# Section 06 Goal: Issue Tracker Service

## Goal
Build a simple Jira-style Kanban board with FastAPI so FinOps findings can be created programmatically, opened, assigned, and moved.

## Scope
- Build and run the tracker container locally
- Serve a simple Kanban board UI
- Expose `/create-issue` as the main creation endpoint
- Expose `/issue/{id}` to open a ticket
- Allow assignment and status movement
- Show the API response and docs

## Out of scope
- Kubernetes scan logic
- Bedrock prompt engineering
- Kubernetes-native deployment

## Success criteria
The learner can create a ticket through `/issue`, open it in the UI, assign it, and move it across the board.
