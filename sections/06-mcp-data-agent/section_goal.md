# Section 06 Goal: Persistent HTTP MCP + LangChain Agents

## Goal
Start a persistent Kubernetes MCP server with native Streamable HTTP (no Supergateway), validate it with Python, then run two LangChain agent scripts against it:

1. **`code/validate_mcp.py`** — Python check that MCP is up and `kubectl_get` works
2. **`code/query_agent.py`** — small prompt → LangChain agent → MCP tools → plain-English answer
3. **`code/snapshot_collector.py`** — inventory prompt → LangChain agent → MCP tools → LLM-written inventory summary

All code lives in `code/`. Both agents use the repo-root `.env`, repo-root `requirements.txt`, a virtualenv, and `http://localhost:8000/mcp`.

## Prerequisites
Sections 01–05 complete.

You should already have:
- a working Kind cluster (`finops-cluster`)
- `.env` with OpenAI-compatible endpoint settings
- Python virtualenv with `pip install -r requirements.txt`
- `mcp/kubernetes:latest` Docker image available

## Instructor setup (before the live demo)
Run `0_prerequisite_guide.md` before teaching. It pulls the MCP image, sets up the venv, and inspects the scripts. Do not walk students through pip install during the live demo. Students start the MCP container live in Guide 2.

## Guide structure (7 parts)
| Guide | Focus | Time |
|-------|------------|-------|
| **0** (`0_prerequisite_guide.md`) | Instructor prereq — image, venv, API key | 2–3 min |
| **1** | Standalone MCP vs Supergateway (video transcript) | 1:30 |
| **2** | Start persistent MCP Docker container | 4–5 min |
| **3** | Trainer notes — `code/mcp_client.py` block by block | 4–5 min |
| **4** | Trainer notes — `code/validate_mcp.py`; run and read output | 3–4 min |
| **5** | Trainer notes — `code/query_agent.py`; run; change prompt to `kube-system` | 4–5 min |
| **6** | Trainer notes — `code/snapshot_collector.py`; run and read output | 4–5 min |

Students go from "Section 05 curl + Supergateway" to "direct HTTP MCP + LangChain agents" in under 25 minutes.

## Scope
- Start `mcp/kubernetes:latest` with native Streamable HTTP on port 8000 (no Supergateway)
- Validate MCP with `code/validate_mcp.py` instead of curl
- Connect OpenAI-compatible LLM from `.env` via LangChain
- Let the LLM choose MCP tools and arguments in both agent scripts
- Share MCP wiring in `code/mcp_client.py` via `langchain-mcp-tools`

## Out of scope
- Supergateway (Section 05 only)
- Structured JSON snapshots / Pydantic ticket schema (Section 07)
- Tagging rules / compliance evaluation (Section 07)
- Posting to the issue tracker (Section 09)

## Success criteria
The learner can:
1. Start the persistent MCP Docker container and validate it with `code/validate_mcp.py`
2. Run `code/query_agent.py` against the local Kind cluster and get a plain-English answer
3. Change the query prompt (e.g. to a `kube-system` question) and re-run without changing plumbing
4. Run `code/snapshot_collector.py` and get an LLM-written inventory summary
5. Explain why Section 06 drops Supergateway but keeps the same `kubectl_get` tools over HTTP

## Artifacts
| File | Purpose |
|---|---|
| `code/mcp_client.py` | Shared MCP URL, root `.env` load, LangChain tool bootstrap, `run_agent` |
| `code/validate_mcp.py` | Python MCP validation (no curl) |
| `code/query_agent.py` | Natural-language cluster query agent |
| `code/snapshot_collector.py` | Broader inventory prompt; prints the LLM's final output |
| `code/README.md` | Quick reference for MCP startup and agent runs |
