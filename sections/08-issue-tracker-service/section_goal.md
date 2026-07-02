# Section 08 Goal: Issue Tracker Service

## Goal
Stand up a lightweight Jira-style tracker with FastAPI that FinOps agents can use to create, view, and manage findings as tickets. The tracker exposes both a REST API and an MCP server so agents can integrate through either protocol.

## Prerequisites
Docker running on your machine.

## Instructor setup (before the live demo)
Run `0_prerequisite_guide.md` before teaching. It cleans old containers and builds the Docker image. Do not walk students through Docker build during the live demo.

## Video structure (2 videos)
| Video | Focus | Time |
|-------|------------|-------|------|
| **1** | Why JSON files don't close loops; Kanban for FinOps | 3–4 min |
| **2** | `/create-issue`, severity, owner fields | 3–4 min |

## Demo structure (2 parts)
| Demo | Focus | Time |
|------|-------|------|
| **1** | Run the tracker container, open the board UI and API docs | 2–3 min |
| **2** | Create a ticket via REST API, verify on the board | 3–4 min |

Each demo is one clear beat. Students go from "no tracker" to "running service with a ticket created via API" in under 7 minutes.

## Scope
- Run the tracker container locally with REST on port 8085 and MCP on port 8086
- Serve a simple Kanban board UI
- Expose `/create-issue` as the main ticket-creation REST endpoint
- Expose MCP tools: `create_issue`, `list_issues`, `get_issue`, `update_issue`
- Show the API response and board

## Out of scope
- Kubernetes scan logic (Sections 04–07)
- LLM prompt engineering (Section 07)
- Kubernetes-native deployment (Section 10)

## Success criteria
The learner can:
1. Run the tracker container and access the board UI
2. Create a ticket through `/create-issue` (REST)
3. See the ticket appear on the Kanban board
4. Understand that agents use the same endpoint to post findings automatically
