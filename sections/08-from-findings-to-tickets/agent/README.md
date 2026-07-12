# Section 08 Agent

Unified LangChain agent with both K8s MCP and issue tracker MCP tools.

## Files

| File | Purpose |
|---|---|
| `mcp_client.py` | LangChain wiring for K8s MCP + tracker MCP (both tool sets) |
| `tracker_auditor.py` | Unified prompt: audit cluster and call `create_issue` per finding |

## Prerequisites

- Section 06 MCP container on `http://localhost:8000/mcp`
- Issue tracker on ports 8085 (REST/UI) and 8086 (MCP SSE)
- Repo-root `.env` with OpenAI and `TRACKER_MCP_URL=http://localhost:8086/sse`

## Run

```bash
python3 sections/08-from-findings-to-tickets/agent/tracker_auditor.py
```

Open `http://localhost:8085` to verify tickets on the Kanban board.
