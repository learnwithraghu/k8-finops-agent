# Section 06 Goal: Simple MCP + LLM Agent (Prompt → MCP Tool Call → Answer)

## Goal
Build the first agentic loop: a prompt goes to an OpenAI-compatible LLM, the LLM chooses `kubectl_get` through MCP, and the script returns a plain-English answer about a namespace. This is the prompt → MCP → LLM answer loop — minimal code, maximum teaching clarity.

## Prerequisites
Sections 01–05 complete.

You should already have:
- a working Kind cluster (`finops-cluster`)
- Supergateway running from Section 05 (port 8000)
- `.env` with OpenAI-compatible endpoint settings

## Instructor setup (before the live demo)
Run `0_prerequisite_guide.md` before teaching. It confirms Supergateway is alive, installs Python deps, and inspects `simple_mcp_llm.py`. Do not walk students through pip install during the live demo.

## Video structure (2 videos)
| Video | Focus | Time |
|-------|------------|-------|
| **1** | Agent loop; LLM tool choice; MCP execution | 3–4 min |
| **2** | Run and observe; compare to kubectl | 3–4 min |

Transcripts: `transcript/1.md`, `transcript/2.md`

## Demo structure (2 parts)
| Demo | Focus | Time |
|------|-------|------|
| **0** | Walk through `simple_mcp_llm.py` code | 4–5 min |
| **2** | Run the agent, observe LLM answers, spot-check with kubectl | 3–4 min |

Students go from "MCP endpoint exists" to "LLM-driven namespace query" in under 10 minutes.

**Optional secondary demo:** `1_guide.md` runs `agent.py` for a full unstructured JSON snapshot (no LLM).

## Scope
- Reuse the curl-validated MCP endpoint from Section 05
- Connect OpenAI-compatible LLM from `.env`
- Let the LLM choose `kubectl_get` arguments for a namespace query
- Return a plain-English answer — no tagging policy, no structured schema yet

## Out of scope
- Structured findings / Pydantic output (Section 07)
- Tagging rules / compliance evaluation (Section 07)
- Posting to the issue tracker (Section 09)
- Writing or customizing the MCP server itself (Section 05)

## Success criteria
The learner can:
1. Run `simple_mcp_llm.py` against the local Kind cluster
2. Explain the prompt → LLM tool choice → MCP call → LLM answer flow
3. Confirm the answer matches real cluster state (spot-check with kubectl)
4. Articulate why this output is useful but unstructured — and why Section 07 adds policy and schema

## Secondary artifact
`agent.py` + `1_guide.md` — deterministic bulk collector that assembles a full JSON snapshot across all namespaces and resource types. Kept for downstream sections and optional teaching.
