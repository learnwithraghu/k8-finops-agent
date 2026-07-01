# Demo 2: Inspect the Snapshot

**Time Budget:** 3–4 mins

**Narrative:** Let's see what the agent collected — and what it deliberately leaves out. The snapshot is unstructured on purpose. Analysis happens in Section 07.

---

### 1) Count resources by type

```bash
cat k8s_metadata.json | jq '[.resources[] | .kind] | group_by(.) | map({kind: .[0], count: length})'
```

**What it does:** Groups resources by kind and counts them. Shows the breakdown — how many deployments, pods, services, etc.

> *Talking point: "In a real cluster with hundreds of namespaces, this snapshot would be thousands of lines. The collector handles scale — manual kubectl does not."*

---

### 2) Find resources in a specific namespace

```bash
cat k8s_metadata.json | jq '[.resources[] | select(.namespace == "payment")]'
```

**What it does:** Filters the snapshot to only `payment` namespace resources. Shows what the agent found for that service.

> *Expected: Deployments, pods, services, and configmaps for the payment service.*

---

### 3) Compare to kubectl (spot check)

```bash
kubectl get all -n payment
kubectl get configmaps -n payment
```

**What it does:** Shows the same resources via kubectl. Compare the output to what the agent collected — they should match.

> *Talking point: "The agent sees the same data as kubectl. The difference is the agent writes it to a file, structured for downstream processing."*

---

### 4) Check what is missing

```bash
cat k8s_metadata.json | jq '[.resources[] | select(.labels.owner == null)]'
```

**What it does:** Filters resources that have no `owner` label. This is the raw material for FinOps analysis — but the agent does not judge it yet.

> *Talking point: "We can see the gaps — missing labels, missing ownership. But the agent does not know what 'good' looks like. That requires policy, and policy requires the LLM. That is Section 07."*

---

**Try it:** Open [`architecture_builder/index.html`](architecture_builder/index.html) in your browser to build the **collection hub** — MCP spokes merge into one unstructured JSON sink (no LLM). Use **Need a hint?** if stuck, then press **Collect Snapshot** to validate.

**Next:** Raw data collected. Next we add LLM analysis to produce structured findings → `sections/07-llm-structured-agent`
