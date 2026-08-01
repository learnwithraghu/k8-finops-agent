# Section 08 Agent

Unified LangChain agent with both K8s MCP and issue tracker MCP tools.

## Files

| File | Purpose |
|---|---|
| `mcp_client.py` | LangChain wiring for K8s MCP + tracker MCP (both tool sets) |
| `list_tracker_tools.py` | Standalone: connect to tracker MCP and print discovered tools (no LLM, no mcp_client) |
| `prompt_list_tracker_tools.py` | Standalone demo: tiny LLM prompt that lists tracker MCP tools (no mcp_client) |
| `tracker_auditor.py` | Unified prompt: audit cluster and call `create_issue` per finding |

## Prerequisites

- Section 06 MCP container on `http://localhost:8000/mcp` (Terminal 1)
- Issue tracker on ports 8085 (REST/UI) and 8086 (MCP SSE) (Terminal 2)
- Repo-root `.env` with OpenAI and `TRACKER_MCP_URL=http://localhost:8086/sse`

## Start both MCP servers

**Terminal 1 — Kubernetes MCP:**

```bash
kind get kubeconfig --name finops-cluster --internal > /tmp/kubeconfig-docker.yaml

docker run --rm -p 8000:8000 --network kind \
  -v /tmp/kubeconfig-docker.yaml:/home/appuser/.kube/config:ro \
  -e ENABLE_UNSAFE_STREAMABLE_HTTP_TRANSPORT=1 \
  -e PORT=8000 \
  -e HOST=0.0.0.0 \
  -e ALLOW_ONLY_READONLY_TOOLS=true \
  mcp/kubernetes:latest
```

**Terminal 2 — Issue tracker:**

```bash
docker run --rm -p 8085:8000 -p 8086:8001 --name finops-issue-tracker finops-issue-tracker:latest
```

## Run

```bash
# No LLM — print the MCP tool catalog
python3 sections/08-from-findings-to-tickets/agent/list_tracker_tools.py

# Tiny LLM demo — ask the model to list tracker tools
python3 sections/08-from-findings-to-tickets/agent/prompt_list_tracker_tools.py

# Full agent — audit cluster and post tickets
python3 sections/08-from-findings-to-tickets/agent/tracker_auditor.py
```

Open `http://localhost:8085` to verify tickets on the Kanban board.
