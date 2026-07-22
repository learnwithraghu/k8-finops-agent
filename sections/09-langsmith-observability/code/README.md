# Section 09 Code — Observability with LangSmith

Same policy auditor as Section 07. LangSmith tracing is enabled via the repo-root `.env` — no new Python modules.

## Setup

1. Start the MCP container (leave running in a dedicated terminal):

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

3. Set LangSmith in the repo-root `.env` (see `.env.example`):

```bash
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your-langsmith-api-key
LANGSMITH_PROJECT=k8-finops-agent
```

4. Validate MCP:

```bash
python3 sections/06-mcp-data-agent/code/validate_mcp.py
```

## Run the policy auditor (traced)

```bash
python3 sections/09-langsmith-observability/code/structured_auditor.py
```

Loads LLM + LangSmith settings from the repo-root `.env` via `mcp_client.py`. Prints the audit on screen and sends the run to LangSmith.

Open [https://smith.langchain.com](https://smith.langchain.com) → your project → latest run to inspect LLM and tool spans.

## Guide order

| Guide | File | Video title |
|-------|------|-------------|
| 0 | `0_prerequisite_guide.md` | *(instructor only)* |
| 1 | `1_guide.md` | Why Trace the FinOps Agent |
| 2 | `2_guide.md` | LangSmith Project & `.env` |
| 3 | `3_guide.md` | Same Auditor, Now Observable |
| 4 | `4_guide.md` | Read the Trace in LangSmith |
| 5 | `5_guide.md` | Full Traced Policy Auditor Run |
