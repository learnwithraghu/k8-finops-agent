# Section 09 Goal: Agent to Tracker Integration

## Goal
Connect the Section 07 structured findings to the Section 08 issue tracker. The agent collects cluster data, analyzes it with the LLM, and posts each finding as a ticket to the tracker — fully automated end to end.

## Prerequisites
Sections 01–08 complete.

You should already have:
- a working Kind cluster (`finops-cluster`)
- Supergateway running from Section 05 (port 8000)
- Issue tracker running from Section 08 (ports 8085/8086)
- OpenAI API key set

## Instructor setup (before the live demo)
Run `0_prerequisite_guide.md` before teaching. It confirms both services are running and inspects the agent code. Do not walk students through service startup during the live demo.

## Video structure (2 videos)
| Video | Focus | Time |
|-------|------------|-------|------|
| **1** | Cluster → MCP → LLM → tracker; demo preview | 3–4 min |
| **2** | Same scan twice; stable correlation keys | 3–4 min |

Transcripts: `transcript/1.md`, `transcript/2.md`

## Demo structure (2 parts)
| Demo | Focus | Time |
|------|-------|------|
| **1** | Run the full agent end to end | 3 min |
| **2** | Verify tickets on the board, explain the MCP flow | 2–3 min |

Each demo is one clear beat. Students go from "separate pieces" to "one command, cluster → findings → tickets" in under 7 minutes.

## Scope
- Read the Section 07 `TicketBatch` JSON output
- Add an MCP tracker client that calls `create_issue` tool
- Map each `TrackerTicket` to MCP tool arguments
- Verify tickets show up in the Section 08 board UI

## Out of scope
- Collecting cluster data (Section 06)
- LLM analysis and tagging rule enforcement (Section 07)
- Kubernetes deployment of the agent (Section 10)
- De-duplication / persistent state across runs

## Notes on the current code
The agent is being rewritten to consume Section 07's `TicketBatch` directly. The current version still runs its own scan + analysis internally. The rewrite will drop the scanner and analyzer, accepting `--findings <file>` instead.

## Success criteria
The learner can:
1. Run the agent with the tracker running and see tickets created automatically
2. Verify tickets appear on the Kanban board
3. Explain the full flow: cluster → MCP → LLM → tracker
4. Articulate how the rewrite will simplify the agent to just consume + post
