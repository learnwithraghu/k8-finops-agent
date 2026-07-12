# Instructor Prerequisite: Cluster, MCP Service & Python Environment

**Audience:** Instructor only — run this before `1_guide.md`. Do not walk students through Docker pulls or pip install during the live demo.

**Time Budget:** 3–4 mins

---

## Before you start

Confirm the Kind cluster and airline workloads are healthy:

```bash
kubectl cluster-info
kubectl get namespaces
kubectl get deploy,svc -A
```

**What it does:** Verifies kubectl access and that application namespaces and services are present. You should see airline namespaces such as `booking-api`, `flight-search`, `inventory`, and `payment`, with deployments and services in `Running` / available state.

> *If namespaces or workloads are missing, complete Sections 01–02 before continuing.*

---

## 1) Start the MCP service

In a **dedicated terminal** (leave it running for Section 07):

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

**What it does:** Starts the Kubernetes MCP server with native Streamable HTTP on port 8000. Same container as Section 06 — no Supergateway.

> *Talking point: "One container, one port. The policy auditor connects straight over HTTP."*

---

## 2) Validate MCP is reachable

In a **second terminal** (repo root, virtualenv activated):

```bash
python3 sections/06-mcp-data-agent/code/validate_mcp.py
```

**What it does:** Connects to `http://localhost:8000/mcp` and lists namespaces via `kubectl_get`. Confirms the MCP service can read the same cluster you checked with kubectl.

> *Expected: `MCP OK — N namespaces via kubectl_get` with the same namespace list.*

> *If this fails, confirm the MCP container terminal is still running and port 8000 is free.*

---

## 3) Set up the Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**What it does:** Creates a virtualenv at the repo root and installs LangChain, OpenAI, and MCP client dependencies.

> *Re-activate in new shells with: `source .venv/bin/activate`*

---

## 4) Confirm API key is set

```bash
test -n "$OPENAI_API_KEY" && echo "API key is set" || echo "OPENAI_API_KEY is not set"
```

**What it does:** Checks that the OpenAI API key environment variable is present. The policy auditor needs this to call the LLM.

> *If using a `.env` file, confirm it exists at the repo root: `grep OPENAI .env`*

---

## 5) Inspect the policy auditor code

```bash
cat sections/07-llm-structured-agent/code/structured_auditor.py
```

**What it does:** Shows the agent — same thin pattern as Section 06's `label_auditor.py`. It loads tagging rules from file, lets the LLM call MCP tools, and prints a plain-English audit.

> *Talking point: "Same agent path as Section 06. We add a rules file read from disk."*

---

## 6) Inspect the tagging rules

```bash
cat sections/07-llm-structured-agent/config/tagging-rules.yaml
```

**What it does:** Shows the policy the agent uses to judge resources. This defines required labels, label mappings, and excluded namespaces.

> *Talking point: "The tagging rules are the policy. The agent applies them to cluster data returned by MCP."*

---

## 7) Ready to teach

When setup passes, start the live walkthrough with:

- `1_guide.md` — Theory: free text plus rules file
- `2_guide.md` — Theory: walk the rules file
- `3_guide.md` — Demo: walk `structured_auditor.py`
- `4_guide.md` — Demo: run and read screen output
- `5_guide.md` — Demo: raise `max_tokens` when the audit truncates
