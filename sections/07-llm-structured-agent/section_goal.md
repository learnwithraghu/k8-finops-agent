# Section 07 Goal: LLM Policy-Aware Label Audit

## Goal
Take the free-text label audit from Section 06, load `config/tagging-rules.yaml` as policy, and let the agent evaluate cluster labels against those rules. Same agent path as Section 06 — prompt in, MCP tools out — with rules read from file and a plain-English answer on screen.

## Prerequisites
Sections 01–06 complete.

You should already have:
- a working Kind cluster (`finops-cluster`)
- the Section 06 MCP container running on `http://localhost:8000/mcp`
- repo-root `.env` with OpenAI-compatible endpoint settings
- Python virtualenv with `pip install -r requirements.txt`

## Instructor setup (before the live demo)
Run `0_prerequisite_guide.md` before teaching. It confirms the cluster is healthy, starts the MCP service, validates the endpoint, and inspects the policy auditor code. Do not walk students through pip install during the live demo.

## Guide structure (6 parts)
| Guide | Type | Video title | Time |
|-------|------|-------------|------|
| **0** (`0_prerequisite_guide.md`) | Instructor | *(prereq only)* | 3–4 min |
| **1** (`1_guide.md`) | Theory | Free Text Plus Rules | ~2 min |
| **2** (`2_guide.md`) | Theory | Walk the Rules File | 3–4 min |
| **3** (`3_guide.md`) | Demo | Walk the Policy Auditor | 4–5 min |
| **4** (`4_guide.md`) | Demo | Run the Policy Auditor | 3–4 min |
| **5** (`5_guide.md`) | Demo | Fix Truncated Audit Output | 2–3 min |

Transcripts: `transcript/1.md`, `transcript/2.md`

Students go from "Section 06 free-text label audit" to "policy-aware label audit on screen" in under 15 minutes.

## Scope
- Reuse Section 06 HTTP MCP wiring (`code/mcp_client.py`; validate via Section 06 `validate_mcp.py`)
- Let the LangChain agent call MCP tools (same pattern as `label_auditor.py`)
- Load `config/tagging-rules.yaml` from file and pass it separately to the agent
- Print the agent's plain-English audit to screen

## Out of scope
- Ticketing, Jira, or issue-tracker integration (Sections 08–09)
- Pydantic schemas or structured JSON output
- Supergateway (Section 05 only)
- Building or recreating the MCP server (Section 05–06)

## Success criteria
The learner can:
1. Run `code/structured_auditor.py` and see a policy-aware label audit on screen
2. Explain how tagging rules loaded from file shape the agent's answer
3. Articulate what Section 07 adds on top of Section 06's `label_auditor.py`
4. Raise `max_tokens` when a namespace-by-namespace audit truncates before finishing

## Artifacts
| File | Purpose |
|---|---|
| `code/mcp_client.py` | Shared MCP URL, root `.env` load, `run_agent` with optional tagging rules |
| `code/structured_auditor.py` | Thin prompt + load rules from file + print agent answer |
| `config/tagging-rules.yaml` | FinOps tagging policy — required tags, label mappings, exclusions |
| `code/README.md` | Quick reference for MCP startup and policy auditor runs |
