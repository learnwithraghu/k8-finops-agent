# Video 4: Run the Policy Auditor

**Time Budget:** 3–4 mins

**Prerequisites:** [`3_guide.md`](3_guide.md) — understand `structured_auditor.py`; virtualenv activated.

> **Legend:** Blockquote lines are on-screen actions — do not read them aloud. Everything else is your script.

---

### Opening (~15 sec)

We walked through the code. Before we run the policy auditor, let's confirm the cluster is healthy and the MCP service is up — same checks from the prerequisite guide.

> **Do:** Open a terminal at the repo root. Activate the virtualenv.

---

### Step 1 — Confirm the cluster is up

```bash
source .venv/bin/activate
kubectl cluster-info
kubectl get namespaces
kubectl get deploy,svc -A
```

**What it does:** Verifies kubectl access and that airline workloads are running. You should see application namespaces such as `booking-api`, `flight-search`, `inventory`, and `payment`, with deployments and services available.

> **Expected:** Cluster responds; application namespaces and services are listed.

---

### Step 2 — Start the MCP service

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

**What it does:** Starts the Kubernetes MCP server on port 8000. Same container as Section 06.

> **Say:** "If you already have this running from Section 06, keep that terminal open and skip the start."

---

### Step 3 — Validate MCP is reachable

Back in your working terminal:

```bash
python3 sections/06-mcp-data-agent/code/validate_mcp.py
```

**What it does:** Connects to `http://localhost:8000/mcp` and lists namespaces via `kubectl_get`. Confirms MCP can read the same cluster you checked with kubectl.

> **Expected:** `MCP OK — N namespaces via kubectl_get` followed by a namespace list.

---

### Step 4 — Run the policy auditor

```bash
python3 sections/07-llm-structured-agent/code/structured_auditor.py
```

This loads `config/tagging-rules.yaml`, connects to MCP, lets the agent choose `kubectl_get` calls, evaluates labels against the rules, and prints a plain-English summary.

> **Expected:** A multi-paragraph audit grouped by namespace, flagging resources that violate required tags from the rules file.

---

### Step 5 — Read the output

Look for three things in the answer:

**Namespace coverage** — application namespaces listed, system namespaces skipped per `excluded_namespaces`.

**Per-resource detail** — name, kind, and labels as returned by MCP tools.

**Policy gaps** — flags for missing `owner`, `cost-center`, `environment`, or other `required_tags` from the rules file.

If the report stops mid-namespace, the answer hit the token limit — see `5_guide.md`.

> **Do:** Scroll through the output. Point at one flagged resource and the rule it violates.

---

### Compare to Section 06

Run Section 06's label auditor for contrast:

```bash
python3 sections/06-mcp-data-agent/code/label_auditor.py
```

Both scripts use the same agent path. Section 07's answer should reference the full rules file — not just owner and cost-center hard-coded in the prompt.

> **Say:** "Same agent. Section 07 just has a policy file behind it."

---

### Close (~10 sec)

Policy-aware audit on screen — same agent as Section 06, with tagging rules from file. If the report cuts off mid-namespace, that is a token limit issue. Next we fix it.

> **Do:** Keep the MCP container running. Open `5_guide.md` if the output looked truncated.
