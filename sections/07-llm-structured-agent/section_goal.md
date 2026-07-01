# Section 07 Goal: LLM Structured Agent (Snapshot + Tagging Rules → Structured Findings)

## Goal
Take the unstructured cluster snapshot from Section 06, add tagging rules as policy, send both to an LLM, and produce structured FinOps findings. This is the MCP → LLM → structured data step that was missing.

## Prerequisites
Sections 01–06 complete.

You should already have:
- a working Kind cluster (`finops-cluster`)
- Supergateway running from Section 05 (port 8000)
- Section 06 snapshot understood

## Instructor setup (before the live demo)
Run `0_prerequisite_guide.md` before teaching. It confirms Supergateway is alive, installs Python deps, and inspects the agent code. Do not walk students through pip install during the live demo.

## Demo structure (2 parts)
| Demo | Focus | Time |
|------|-------|------|
| **1** | Run the structured agent, see findings appear | 3 min |
| **2** | Audit the findings JSON, map to rules | 3–4 min |

Each demo is one clear beat. Students go from "unstructured snapshot" to "structured ticket-shaped findings" in under 7 minutes.

## Scope
- Consume the Section 06 raw snapshot as input
- Inject `config/tagging-rules.yaml` into the LLM prompt as policy context
- Produce deterministic structured findings (missing tags, ownership gaps, severity)
- Keep the agent prompt and schema together in this section

## Out of scope
- Collecting cluster data directly (Section 06)
- Posting findings to the issue tracker (Section 09)
- Building or recreating the MCP server (Section 05)
- Multi-cluster scale or metrics-server cost telemetry

## Success criteria
The learner can:
1. Run the structured agent and see `TicketBatch` output
2. Explain how tagging rules shape the LLM's structured output
3. Read the structured findings JSON and confirm each finding maps to a rule violation
4. Articulate why collection (06) and analysis (07) are separate steps
