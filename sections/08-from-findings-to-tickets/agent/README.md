# Section 08 Agent

Minimal fork of the Section 06 label auditor that posts per-finding tickets to the issue tracker.

## Files

| File | Purpose |
|---|---|
| `mcp_client.py` | Copied from Section 06 — LangChain + K8s MCP wiring |
| `tracker_auditor.py` | Audit prompt, structure, post (replaces console-only output) |
| `structure.py` | LLM call: audit text → `TicketBatch` |
| `tracker_client.py` | MCP client: calls tracker `create_issue` tool |
| `models.py` | `TrackerTicket` / `TicketBatch` schema |

## Prerequisites

- Section 06 MCP container on `http://localhost:8000/mcp`
- Issue tracker on ports 8085 (REST/UI) and 8086 (MCP SSE)
- Repo-root `.env` with OpenAI and `TRACKER_MCP_URL=http://localhost:8086/sse`

## Run

```bash
python3 sections/08-from-findings-to-tickets/agent/tracker_auditor.py
```

Open `http://localhost:8085` to verify tickets on the Kanban board.
