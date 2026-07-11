# Demo 2: Run the Snapshot Collector

**Time Budget:** 3 mins

**Narrative:** The query agent answers one question. FinOps needs every resource with labels — `snapshot_collector.py` connects to MCP, loops through namespaces and resource types, and writes a JSON snapshot. Deterministic — same input, same output every time.

**Prerequisites:** [`1_guide.md`](1_guide.md) — query agent working; virtualenv activated.

---

### 1) Confirm MCP endpoint is alive

```bash
curl -s http://localhost:8000/healthz
```

**What it does:** Quick health check before running the collector. If this fails, Supergateway is not running.

> *Expected: `ok`*

---

### 2) Peek at the collector code

```bash
cat sections/06-mcp-data-agent/snapshot_collector.py
```

**What it does:** Shows the difference from `query_agent.py` — no LLM, just deterministic `kubectl_get` loops via the same `mcp_client.py`.

> *Talking point: "Same MCP tools, different job. The query agent asks one question; the collector gathers everything for downstream analysis."*

---

### 3) Run the collector

```bash
source .venv/bin/activate
python3 sections/06-mcp-data-agent/snapshot_collector.py > k8s_metadata.json
```

**What it does:** Connects to MCP via `mcp_client.py`, lists namespaces, fetches resources per namespace, and writes the snapshot to `k8s_metadata.json`.

> *Talking point: "Same `kubectl_get` tool we validated with curl — Python automates the loop across every namespace."*

---

### 4) Review labels in the output

```bash
cat k8s_metadata.json | jq '.resources[] | {name, namespace, kind, labels}' | head -n 30
```

**What it does:** Shows resource names, namespaces, kinds, and **labels** — the raw material for FinOps analysis in Section 07.

> *Expected: JSON with `scanned_at`, `cluster`, `namespaces`, and `resources` keys. Resources include deployments, pods, services, PVCs, and configmaps from the airline namespaces.*

> *Talking point: "This is structured data with labels attached. No compliance verdicts yet — Section 07 adds tagging rules and structured findings."*

---

**Next:** Add policy and structured output → `sections/07-llm-structured-agent`
