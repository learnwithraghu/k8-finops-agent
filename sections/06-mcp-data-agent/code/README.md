# Section 06 Code

LangChain agents that talk to a persistent Kubernetes MCP server over Streamable HTTP.

## Setup

1. Start the MCP container (leave running in a dedicated terminal) — see `2_guide.md`:

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

2. Install deps from the repo root: `pip install -r requirements.txt`

3. Validate MCP (no curl) — see `2_guide.md` (Part B):

```bash
python3 sections/06-mcp-data-agent/code/validate_mcp.py
```

## Run agents

```bash
python3 sections/06-mcp-data-agent/code/query_agent.py
python3 sections/06-mcp-data-agent/code/label_auditor.py
```

Both scripts load LLM settings from the repo-root `.env` via `mcp_client.py`.

## Guide order

| Guide | File | Video title |
|-------|------|-------------|
| 0 | `0_prerequisite_guide.md` | *(instructor only)* |
| 1 | `1_guide.md` | Standalone MCP vs Supergateway |
| 2 | `2_guide.md` | Start and Validate MCP |
| 3 | `3_guide.md` | LangChain Agent Shared Wiring |
| 4 | `4_guide.md` | Your First LangChain MCP Agent |
| 5 | `5_guide.md` | Audit Kubernetes Labels via MCP Agent |
