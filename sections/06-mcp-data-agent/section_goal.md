# Section 06 Goal: Two MCP Python Scripts (Query + Snapshot)

## Goal
Build two complementary scripts that both talk to the Kubernetes MCP endpoint from Section 05:

1. **`query_agent.py`** — prompt → LangChain ReAct agent → MCP tools → plain-English answer
2. **`snapshot_collector.py`** — deterministic MCP loops → structured JSON snapshot (labels, kinds, namespaces)

Both use the repo-root `.env`, a virtualenv, and `http://localhost:8000/mcp`.

## Prerequisites
Sections 01–05 complete.

You should already have:
- a working Kind cluster (`finops-cluster`)
- Supergateway running from Section 05 (port 8000)
- `.env` with OpenAI-compatible endpoint settings
- Python virtualenv with `pip install -r requirements.txt`

## Instructor setup (before the live demo)
Run `0_prerequisite_guide.md` before teaching. It confirms Supergateway is alive, sets up the venv, and inspects both scripts. Do not walk students through pip install during the live demo.

## Video structure (2 videos)
| Video | Focus | Time |
|-------|------------|-------|
| **1** | Agent loop; LLM tool choice; MCP execution | 3–4 min |
| **2** | Snapshot collection; labels in structured JSON | 3–4 min |

Transcripts: `transcript/1.md`, `transcript/2.md`

## Demo structure (2 parts)
| Demo | Focus | Time |
|------|-------|------|
| **0** | Walk through `query_agent.py` code | 4–5 min |
| **1** | Run `query_agent.py`, spot-check with kubectl | 3–4 min |
| **2** | Run `snapshot_collector.py`, inspect JSON labels | 3 min |

Students go from "MCP endpoint exists" to "LLM-driven cluster query + structured snapshot" in under 12 minutes.

## Scope
- Reuse the curl-validated MCP endpoint from Section 05 (`http://localhost:8000/mcp`)
- Connect OpenAI-compatible LLM from `.env` via LangChain
- Let the LLM choose MCP tools and arguments in `query_agent.py`
- Collect a full JSON snapshot with labels in `snapshot_collector.py`
- Share MCP wiring in `mcp_client.py` via `langchain-mcp-tools`

## Out of scope
- Structured findings / Pydantic ticket schema (Section 07)
- Tagging rules / compliance evaluation (Section 07)
- Posting to the issue tracker (Section 09)
- Writing or customizing the MCP server itself (Section 05)

## Success criteria
The learner can:
1. Run `query_agent.py` against the local Kind cluster and get a plain-English answer
2. Run `snapshot_collector.py` and produce a JSON snapshot with resource labels
3. Explain the prompt → LLM tool choice → MCP call → answer flow
4. Explain why the snapshot is structured but not yet policy-scored — Section 07 adds that

## Artifacts
| File | Purpose |
|---|---|
| `mcp_client.py` | Shared MCP URL, `.env` load, LangChain tool bootstrap |
| `query_agent.py` | Natural-language cluster queries |
| `snapshot_collector.py` | Deterministic bulk collector for downstream analysis |
