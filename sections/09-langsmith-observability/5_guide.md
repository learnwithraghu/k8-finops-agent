# Video 5: Full Traced Policy Auditor Run

**Time Budget:** 5–6 mins

**Prerequisites:** [`2_guide.md`](2_guide.md) — LangSmith env vars set in repo-root `.env`; virtualenv activated.

> **Legend:** Blockquote lines are on-screen actions — do not read them aloud. Everything else is your script.

---

### Opening (~15 sec)

This is the complete Section 09 hands-on path: confirm the cluster, confirm MCP, run the copied policy auditor, read the on-screen audit, then inspect the LangSmith trace. Same script as Section 07 — observability comes from `.env` only.

> **Do:** Open a terminal at the repo root. Activate the virtualenv.

---

### Step 1 — Confirm the cluster is up

```bash
source .venv/bin/activate
kubectl cluster-info
kubectl get namespaces
kubectl get deploy,svc -A
```

**What it does:** Verifies kubectl access and that airline workloads are running.

> **Expected:** Cluster responds; application namespaces and deployments/services are listed.

---

### Step 2 — Start or confirm the MCP service

In a **dedicated terminal** (leave it running):

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

> **Say:** "If you already have this running from an earlier section, keep that terminal open and skip the start."

---

### Step 3 — Run the policy auditor

Back in your working terminal:

```bash
python3 sections/09-langsmith-observability/code/structured_auditor.py
```

This loads `config/tagging-rules.yaml`, connects to MCP at `http://localhost:8000/mcp`, lets the agent choose `kubectl_get` calls, evaluates labels against the rules, prints a plain-English summary — and sends the full run to LangSmith when `LANGSMITH_TRACING=true`.

> **Expected:** A multi-paragraph audit grouped by namespace, flagging resources that violate required tags from the rules file. Terminal may also show a LangSmith run URL.

> **Do:** Let the run finish. Note the timestamp — you will match it in LangSmith.

---

### Step 4 — Read the terminal output

Look for three things in the answer:

**Namespace coverage** — application namespaces listed, system namespaces skipped per `excluded_namespaces`.

**Per-resource detail** — name, kind, and labels as returned by MCP tools.

**Policy gaps** — flags for missing `owner`, `cost-center`, `environment`, or other `required_tags` from the rules file.

> **Do:** Scroll through the output. Point at one flagged resource and the rule it violates.

> **Say:** "Same answer shape as Section 07. The difference is LangSmith captured every step behind this paragraph."

---

### Step 5 — Read the trace in LangSmith

Open [https://smith.langchain.com](https://smith.langchain.com) → your project (`LANGSMITH_PROJECT` from `.env`) → the latest run from this auditor.

**What to look for:**
- Timestamp matching your terminal run
- A tree of nested spans — LLM calls and MCP tool calls (`kubectl_get`, etc.)
- Tool spans showing arguments (namespace, resource kind) and returned payload previews
- LLM spans showing prompts, responses, token usage, and latency

Connect three layers on screen:

1. **Cluster** — data via MCP
2. **Policy** — `tagging-rules.yaml` shaping judgment
3. **Trace** — LangSmith showing how the agent used tools to apply that policy

> **Say:** "When an audit looks wrong later, start here: wrong tool args, truncated tool output, or a weak model step — not only the final paragraph."

---

### Close (~10 sec)

Full traced run complete: same `structured_auditor.py` as Section 07, observability from `.env`, audit on screen and flight recorder in LangSmith.

> **Do:** Leave LangSmith open if students want to re-run; stop the MCP container when the session ends.
