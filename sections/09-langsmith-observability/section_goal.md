# Section 09 Goal: Observability with LangSmith

## Goal
Copy the Section 07 policy auditor as-is, turn on LangSmith with environment variables only, re-run the same audit, and read the trace in the LangSmith UI. No new Python modules — observability is configuration, not a rewrite.

## Prerequisites
Sections 01–07 complete (Kind cluster, MCP container, policy auditor understood). Section 08 optional for this section’s demo path.

You should already have:
- a working Kind cluster (`finops-cluster`)
- the Section 06 MCP container running on `http://localhost:8000/mcp`
- repo-root `.env` with OpenAI-compatible endpoint settings
- a LangSmith account, API key, and project name
- Python virtualenv with `pip install -r requirements.txt`

## Instructor setup (before the live demo)
Run `0_prerequisite_guide.md` before teaching. It confirms the cluster and MCP service, verifies LangSmith env vars, and checks the copied auditor. Do not walk students through account signup during the live demo.

## Guide structure (5 parts)
| Guide | Type | Video title | Time |
|-------|------|-------------|------|
| **0** (`0_prerequisite_guide.md`) | Instructor | *(prereq only)* | ~3 min |
| **1** (`1_guide.md`) | Theory | Why Trace the FinOps Agent | ~2 min |
| **2** (`2_guide.md`) | Demo | LangSmith Project & `.env` | ~3 min |
| **3** (`3_guide.md`) | Demo | Same Auditor, Now Observable | 3–4 min |
| **4** (`4_guide.md`) | Demo | Read the Trace in LangSmith | 3–4 min |

Students go from "Section 07 audit on screen" to "same audit with a full LangSmith trace" in under 15 minutes.

## Scope
- Copy Section 07 `code/` and `config/` into this section
- Enable LangSmith via `.env` only (`LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`)
- Run `code/structured_auditor.py` unchanged in behavior
- Open the LangSmith UI and walk LLM + tool-call spans

## Out of scope
- New Python modules or agent refactoring (deferred)
- LangSmith evaluations / datasets
- Custom spans or metadata instrumentation
- Issue-tracker integration (Section 08)
- Kubernetes-native deployment (later section)

## Success criteria
The learner can:
1. Explain why tracing matters for an MCP + LLM FinOps agent
2. Set LangSmith env vars in the repo-root `.env`
3. Run the copied policy auditor and see the same plain-English audit on screen
4. Find the run in LangSmith and identify LLM calls and MCP tool calls in the trace

## Artifacts
| File | Purpose |
|---|---|
| `code/mcp_client.py` | Copied from Section 07; loads root `.env` (LangSmith included) |
| `code/structured_auditor.py` | Same thin policy auditor as Section 07 |
| `config/tagging-rules.yaml` | Same FinOps tagging policy |
| `code/README.md` | Quick reference for MCP + LangSmith-enabled runs |
