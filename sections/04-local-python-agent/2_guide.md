# Demo 2: Manual vs Automated

**Time Budget:** 3–4 mins

**Narrative:** The collector gave us JSON. Let's see what it would take to get the same information by hand — and why raw data alone is not enough.

---

### 1) List all deployments with labels (manual)

```bash
kubectl get deployments -A --show-labels
```

**What it does:** Shows every deployment across all namespaces with their full label set. This is what you would scan manually to check for missing tags.

> *Talking point: "Now imagine doing this for 50 namespaces, 200 deployments. The collector does it in one API call."*

---

### 2) Find deployments missing an owner label (manual)

```bash
kubectl get deployments -A -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,OWNER:.metadata.labels.owner' | grep '<none>'
```

**What it does:** Lists deployments where the `owner` label is not set. Lines with `<none>` are the gaps.

> *Expected: Several deployments with `<none>` — these are the FinOps problems.*

> *Talking point: "This grep approach works for one label. But what about `cost-center`, `tier`, `environment`? And what about services, configmaps, PVCs? It gets unwieldy fast."*

---

### 3) Find services missing cost-center (manual)

```bash
kubectl get services -A -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,COST_CENTER:.metadata.labels.cost-center' | grep '<none>'
```

**What it does:** Same approach, checking `cost-center` on services. Shows which services are not tagged for billing.

---

### 4) Check PVC status (manual)

```bash
kubectl get pvc -A -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,STATUS:.status.phase'
```

**What it does:** Shows PVCs and their binding status. Unbound PVCs may be orphaned or misconfigured.

> *Talking point: "Raw data is disconnected from policy. The collector gives you the data; the tagging rules define what 'good' looks like. But connecting the two requires logic — and that is where the LLM comes in Section 07."*

---

**Try it:** Open [`architecture_builder/index.html`](architecture_builder/index.html) in your browser to wire the **laptop ↔ cluster bridge** — local collect.py reads the Kind API and writes JSON on your machine. Use **Need a hint?** if stuck, then press **Run Scan** to validate.

**Next:** Collector works but output is unstructured. Next we add MCP for standardized tool access → `sections/05-mcp-k8-agent`
