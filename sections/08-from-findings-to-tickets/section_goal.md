# Section 08 Goal: From Findings to Actionable Tickets

## Goal
Stand up a lightweight FinOps issue tracker, understand its REST and MCP APIs, and wire the Section 06 MCP agent to post per-finding tickets automatically — closing the loop from cluster scan to actionable work.

## Prerequisites
- Docker running on your machine
- Sections 01–07 complete (Kind cluster, MCP container from Section 06, tagging rules from Section 07)
- Repo-root `.env` with OpenAI-compatible endpoint settings

## Instructor setup (before the live demo)
Run `0_prerequisite_guide.md` before teaching. It builds the tracker Docker image, starts **both** MCP servers in separate terminals (K8s MCP + issue tracker), and health-checks them. Do not walk students through Docker build during the live demo.

## Video structure
| Video | Focus | Type | Time |
|-------|------------|------|-------|
| **1** | Issue tracker landscape: Jira, Linear, GitHub Issues, custom | Transcript + slides | 3–4 min |
| **2** | Launch the FinOps issue tracker | Demo | 2–3 min |
| **3a** | Test tracker MCP tools with a tiny LLM prompt | Demo | 2–3 min |
| **3b** | Code walkthrough: what changed vs Section 07 | Code walk | 3–4 min |
| **3c** | Tracker backend: REST, MCP, ticket schema + manual curl | Demo + code walk | 3–4 min |
| **4** | Whiteboard: wiring the MCP agent to the tracker | Transcript + slides | 3–4 min |
| **5** | Agent walkthrough: post tickets instead of printing | Code walk + demo | 4–5 min |
| **5b** | Widen prompt: scan all namespaces | Demo | 2–3 min |
| **6** | Architecture update: the closed-loop FinOps pipeline | Transcript + slides | 3–4 min |

Transcripts: `transcript/1.md` (V1), `transcript/2.md` (V4), `transcript/3.md` (V6)

## Demo structure (6 parts)
| Demo | Guide | Maps to | Time |
|------|-------|---------|------|
| **1** | `1_guide.md` | V2 — run tracker, open board | 2–3 min |
| **2** | `2_guide.md` | V3a — LLM lists tracker MCP tools | 2–3 min |
| **3** | `3_guide.md` | V3b — agent code delta vs Section 07 | 3–4 min |
| **4** | `4_guide.md` | V3c — API tour + manual curl | 3–4 min |
| **5** | `5_guide.md` | V5 — run agent on `payment`, verify board | 3–4 min |
| **6** | `6_guide.md` | V5b — widen prompt to all namespaces | 2–3 min |

## Scope
- Run both MCP servers locally (K8s on :8000, tracker REST on :8085 / MCP on :8086)
- Serve a Kanban board UI and expose `/create-issue` REST endpoint
- Expose MCP tools: `create_issue`, `list_issues`, `get_issue`, `update_issue`
- Demo tracker MCP discovery with a tiny standalone LLM script
- Extend `mcp_client.py` with both K8s and tracker MCP servers
- Run a unified LangChain agent that audits the cluster and calls `create_issue` per finding

## Out of scope
- Kubernetes scan logic re-teaching (Sections 05–06)
- Tagging rule authoring (Section 07)
- LangSmith observability (Section 09)
- Kubernetes-native deployment (later section)
- Idempotency / deduplication across runs

## Success criteria
The learner can:
1. Run both MCP terminals and access the board UI
2. Use a tiny LLM script to list tracker MCP tools
3. Explain what changed in `mcp_client.py` / `tracker_auditor.py` vs Section 07
4. Create a ticket through `/create-issue` and explain the payload schema
5. Run `agent/tracker_auditor.py` (payment-scoped) and see per-finding tickets on the board
6. Widen one prompt line to scan all namespaces and re-run for more tickets
7. Explain the flow: one LangChain agent with K8s MCP + tracker MCP tools → Kanban
8. Describe where this section sits in the full FinOps pipeline (Section 06 → 08 → 09 observability)
