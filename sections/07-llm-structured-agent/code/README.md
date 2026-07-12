# Section 07 Code

Ask a LangChain agent to audit cluster labels against tagging rules and print a plain-English audit.

## Setup

1. Start the MCP container (leave running in a dedicated terminal) — see `sections/06-mcp-data-agent/2_guide.md`:

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

3. Validate MCP (Section 06 script, no curl):

```bash
python3 sections/06-mcp-data-agent/code/validate_mcp.py
```

## Run the policy auditor

```bash
python3 sections/07-llm-structured-agent/code/structured_auditor.py
```

Loads LLM settings from the repo-root `.env` via `mcp_client.py`. Reads policy from `config/tagging-rules.yaml`. Agent calls MCP tools and prints a plain-English audit.

## Guide order

| Guide | File | Video title |
|-------|------|-------------|
| 0 | `0_prerequisite_guide.md` | *(instructor only)* |
| 1 | `1_guide.md` | Free Text Plus Rules |
| 2 | `2_guide.md` | Walk the Rules File |
| 3 | `3_guide.md` | Walk the Policy Auditor |
| 4 | `4_guide.md` | Run the Policy Auditor |
