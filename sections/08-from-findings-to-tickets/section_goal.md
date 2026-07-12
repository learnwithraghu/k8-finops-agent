# Section 08 Goal: From Findings to Tickets — Issue Tracker & Agent Integration

## Goal
Stand up a lightweight FinOps issue tracker, understand its REST and MCP APIs, and wire the Section 06 MCP agent to post per-finding tickets automatically — closing the loop from cluster scan to actionable work.

## Prerequisites
- Docker running on your machine
- Sections 01–07 complete (Kind cluster, MCP container from Section 06, tagging rules from Section 07)
- Repo-root `.env` with OpenAI-compatible endpoint settings

## Instructor setup (before the live demo)
Run `0_prerequisite_guide.md` before teaching. It builds the tracker Docker image and confirms the agent code. Do not walk students through Docker build during the live demo.

## Video structure (6 videos)
| Video | Focus | Type | Time |
|-------|------------|------|-------|
| **1** | Issue tracker landscape: Jira, Linear, GitHub Issues, custom | Transcript + slides | 3–4 min |
| **2** | Launch the FinOps issue tracker | Demo | 2–3 min |
| **3** | Tracker backend: REST, MCP, ticket schema | Demo + code walk | 4–5 min |
| **4** | Whiteboard: wiring the MCP agent to the tracker | Transcript + slides | 3–4 min |
| **5** | Agent walkthrough: post tickets instead of printing | Code walk + demo | 4–5 min |
| **6** | Architecture update: the closed-loop FinOps pipeline | Transcript + slides | 3–4 min |

Transcripts: `transcript/1.md` (V1), `transcript/2.md` (V4), `transcript/3.md` (V6)

## Demo structure (3 parts)
| Demo | Guide | Maps to | Time |
|------|-------|---------|------|
| **1** | `1_guide.md` | V2 — run tracker, open board | 2–3 min |
| **2** | `2_guide.md` | V3 — API tour + manual curl | 3–4 min |
| **3** | `3_guide.md` | V5 — run agent, verify board | 3–4 min |

## Scope
- Run the tracker container locally (REST on port 8085, MCP on port 8086)
- Serve a Kanban board UI and expose `/create-issue` REST endpoint
- Expose MCP tools: `create_issue`, `list_issues`, `get_issue`, `update_issue`
- Copy Section 06 `mcp_client.py` and extend with `structure.py` + `tracker_client.py`
- Post per-finding tickets via tracker MCP instead of printing to console

## Out of scope
- Kubernetes scan logic re-teaching (Sections 05–06)
- Tagging rule authoring (Section 07)
- Agent refactoring into modules (Section 09)
- Kubernetes-native deployment (Section 10)
- Idempotency / deduplication across runs

## Success criteria
The learner can:
1. Run the tracker container and access the board UI
2. Create a ticket through `/create-issue` and explain the payload schema
3. Run `agent/tracker_auditor.py` and see per-finding tickets on the board
4. Explain the flow: K8s MCP → LLM audit → structure → tracker MCP → Kanban
5. Describe where this section sits in the full FinOps pipeline (Section 06 → 08 → 09 → 10)
