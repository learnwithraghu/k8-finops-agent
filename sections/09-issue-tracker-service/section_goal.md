# Section 09 Goal: Issue Tracker Service

## Goal
Build a lightweight Jira-style tracker with FastAPI that later FinOps agent sections can use to create, open, assign, and move findings as tickets.

## Scope
- Run the tracker container locally
- Serve a simple Kanban board UI
- Expose `/create-issue` as the main ticket-creation endpoint
- Expose `/issue/{id}` to open a ticket
- Allow assignment and status movement
- Show the API response and docs

## Out of scope
- Kubernetes scan logic
- Bedrock prompt engineering
- Kubernetes-native deployment

## Success criteria
The learner can create a ticket through `/create-issue`, open it in the UI, assign it, and move it across the board.
