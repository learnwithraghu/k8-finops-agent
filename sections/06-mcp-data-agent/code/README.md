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

3. Validate MCP (no curl) — see `4_guide.md`:

```bash
python3 sections/06-mcp-data-agent/code/validate_mcp.py
```

## Run agents

```bash
python3 sections/06-mcp-data-agent/code/query_agent.py
python3 sections/06-mcp-data-agent/code/snapshot_collector.py
```

Both scripts load LLM settings from the repo-root `.env` via `mcp_client.py`.

## Guide order

| Guide | File |
|-------|------|
| 0 | `0_prerequisite_guide.md` (instructor) |
| 1 | `1_guide.md` — standalone vs Supergateway transcript |
| 2 | `2_guide.md` — start MCP container |
| 3 | `3_guide.md` — `mcp_client.py` walkthrough |
| 4 | `4_guide.md` — `validate_mcp.py` |
| 5 | `5_guide.md` — `query_agent.py` |
| 6 | `6_guide.md` — `snapshot_collector.py` |
