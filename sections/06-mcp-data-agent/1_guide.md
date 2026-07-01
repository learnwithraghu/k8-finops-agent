# Demo 1: Run the Data Agent

**Time Budget:** 3 mins

**Narrative:** The agent connects to our MCP endpoint, calls `kubectl_get` for each resource type across all namespaces, and writes a JSON snapshot. This is deterministic collection — same input, same output every time.

---

### 1) Confirm MCP endpoint is alive

```bash
curl -s http://localhost:8000/healthz
```

**What it does:** Quick health check before running the agent. If this fails, Supergateway is not running.

> *Expected: `ok`*

---

### 2) Run the agent

```bash
python3 sections/06-mcp-data-agent/agent.py > k8s_metadata.json
```

**What it does:** Connects to the MCP endpoint, lists namespaces, fetches resources per namespace, and writes the snapshot to `k8s_metadata.json`.

> *Talking point: "The agent calls `kubectl_get` through MCP — the same tool we validated with curl in Section 05. Python just automates the loop."*

---

### 3) Review the output

```bash
cat k8s_metadata.json | jq 'del(.resources[].annotations)' | head -n 20
```

**What it does:** Pretty-prints the first 20 lines of the snapshot, stripping annotations for readability.

> *Expected: JSON with `scanned_at`, `cluster`, `namespaces`, and `resources` keys. Resources include deployments, pods, services, PVCs, and configmaps from the airline namespaces.*

> *Talking point: "This is raw data. No compliance verdicts, no severity scores, no ownership recommendations. Just facts from the cluster."*

---

**Next:** We have a snapshot. Next we inspect what is in it and discuss why it is unstructured → `2_guide.md`
