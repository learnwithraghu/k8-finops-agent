# Instructor Prerequisite: Cluster, MCP, LangSmith Env

**Audience:** Instructor only — run this before `1_guide.md`. Do not walk students through Docker pulls, pip install, or LangSmith signup during the live demo.

**Time Budget:** ~3 mins

---

## Before you start

Confirm the Kind cluster and airline workloads are healthy:

```bash
kubectl cluster-info
kubectl get namespaces
kubectl get deploy,svc -A
```

**What it does:** Verifies kubectl access and that application namespaces and services are present.

> *If namespaces or workloads are missing, complete Sections 01–02 before continuing.*

---

## 1) Start the MCP service

In a **dedicated terminal** (leave it running for Section 09):

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

**What it does:** Starts the Kubernetes MCP server on port 8000. Same container as Sections 06–07.

> *If already running from an earlier section, keep that terminal open and skip this step.*

---

## 2) Validate MCP is reachable

In a **second terminal** (repo root, virtualenv activated):

```bash
python3 sections/06-mcp-data-agent/code/validate_mcp.py
```

> *Expected: `MCP OK — N namespaces via kubectl_get`*

---

## 3) Confirm Python environment

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

**What it does:** Ensures LangChain (and transitive LangSmith client) are installed from the repo root.

---

## 4) Confirm OpenAI + LangSmith env vars

```bash
test -n "$OPENAI_API_KEY" && echo "OPENAI_API_KEY is set" || echo "OPENAI_API_KEY is not set"
grep -E '^(LANGSMITH_|OPENAI_)' .env
```

Repo-root `.env` must include (see `.env.example`):

```bash
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your-langsmith-api-key
LANGSMITH_PROJECT=k8-finops-agent
```

**What it does:** Confirms LLM and LangSmith settings load via `mcp_client.py`'s `load_dotenv`. No code changes required for tracing.

> *Create the LangSmith project in the UI ahead of class if it does not exist yet.*

---

## 5) Confirm the copied auditor

```bash
ls sections/09-langsmith-observability/code/
ls sections/09-langsmith-observability/config/
```

**What it does:** Shows the Section 07 copy — `structured_auditor.py`, `mcp_client.py`, and `tagging-rules.yaml`. Same scripts; observability comes from `.env`.

---

## 6) Ready to teach

When setup passes, start the live walkthrough with:

- `1_guide.md` — Theory: why trace the FinOps agent
- `2_guide.md` — Demo: LangSmith project and `.env`
- `3_guide.md` — Demo: run the same auditor
- `4_guide.md` — Demo: read the trace in LangSmith
