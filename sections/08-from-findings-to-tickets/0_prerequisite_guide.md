# Instructor Prerequisite: Build Tracker + Start Both MCP Servers

**Audience:** Instructor only — run this before `1_guide.md`. Do not walk students through Docker build during the live demo.

**Time Budget:** 4–5 mins

---

## 1) Clean old containers

```bash
docker stop finops-issue-tracker 2>/dev/null || true
docker rm finops-issue-tracker 2>/dev/null || true
```

**What it does:** Removes any leftover tracker container from previous runs.

---

## 2) Inspect the service structure

```bash
ls sections/08-from-findings-to-tickets/service/
```

**What it does:** Shows the service directory — `Dockerfile`, `app/`, `data/`, `requirements.txt`, `start.sh`.

---

## 3) Build the Docker image

```bash
docker build -t finops-issue-tracker:latest sections/08-from-findings-to-tickets/service
```

**What it does:** Builds the tracker image. Takes 30–60 seconds depending on network.

> *Talking point: "The tracker is a standalone FastAPI service. REST for humans, MCP for agents. One container, two interfaces."*

---

## 4) Inspect the agent code

```bash
ls sections/08-from-findings-to-tickets/agent/
```

**What it does:** Shows the unified agent — `mcp_client.py` (K8s + tracker MCP), `list_tracker_tools.py`, `prompt_list_tracker_tools.py`, and `tracker_auditor.py`.

---

## 5) Set up the Python environment

In a **working terminal** (repo root):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**What it does:** Creates a virtualenv at the repo root and installs LangChain, OpenAI, and MCP client dependencies used by the agent demos.

> *If `.venv` already exists from Sections 06–07, just activate it: `source .venv/bin/activate`*

> *Re-activate in new shells with: `source .venv/bin/activate`*

Confirm the OpenAI settings are present (needed for the LLM tool-list demo and `tracker_auditor.py`):

```bash
test -n "$OPENAI_API_KEY" && echo "API key is set" || echo "OPENAI_API_KEY is not set"
grep OPENAI .env
```

> *If using a `.env` file, `load_dotenv` in the agent scripts picks it up from the repo root.*

---

## 6) Start both MCP servers (two terminals)

Section 08 needs **two long-running containers**. Leave each in its own terminal for the whole session.

### Terminal 1 — Kubernetes MCP (Section 06/07)

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

**What it does:** Starts the Kubernetes MCP server with native Streamable HTTP on port 8000. Same container as Sections 06–07.

> *If this is already running from Section 06 or 07, keep that terminal open and skip this start.*

### Terminal 2 — FinOps Issue Tracker

```bash
docker run --rm -p 8085:8000 -p 8086:8001 --name finops-issue-tracker finops-issue-tracker:latest
```

**What it does:** Starts the tracker. Port 8085 serves REST + board UI. Port 8086 serves the tracker MCP server (SSE).

> *Expected: FastAPI / Uvicorn startup logs. Leave both terminals running.*

---

## 7) Health-check both services

In a **third terminal** (repo root, virtualenv activated — `source .venv/bin/activate`):

```bash
curl -s http://localhost:8000/mcp -o /dev/null -w "K8s MCP: %{http_code}\n"
curl -s http://localhost:8085/health
```

**What it does:** Confirms Kubernetes MCP on :8000 and the tracker REST health endpoint on :8085.

> *Expected: a non-empty HTTP status for K8s MCP, and a healthy JSON/text response from the tracker.*

Optional deterministic tracker MCP catalog check:

```bash
python3 sections/08-from-findings-to-tickets/agent/list_tracker_tools.py
```

---

## 8) Ready to teach

When both terminals are running and health checks pass, start the live walkthrough with:

- `1_guide.md` — Launch tracker UI / docs (Video 2)
- `2_guide.md` — Test tracker MCP tools with a tiny LLM prompt (Video 3a)
- `3_guide.md` — Code walkthrough: what changed vs Section 07 (Video 3b)
- `4_guide.md` — Tracker backend REST + manual curl (Video 3c)
- `5_guide.md` — Run agent + verify board (Video 5)

## Cleanup after the session

```bash
docker stop finops-issue-tracker
```

**What it does:** Stops the tracker container. Stop the Kubernetes MCP terminal with Ctrl+C when the session ends.
