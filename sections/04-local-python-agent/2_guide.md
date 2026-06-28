# Demo 2: Run Scanner and Review Output

**Time Budget:** 4-5 mins

### 1) Run the collector across the cluster
```bash
PYTHONPATH=sections/04-local-python-agent python -m agent.collect -o k8s_metadata.json
python3 -m json.tool k8s_metadata.json | head -80
```
> *Expected: A messy, raw JSON dump of Kubernetes objects without compliance verdicts.*

### 2) Run collector for one namespace
```bash
PYTHONPATH=sections/04-local-python-agent python -m agent.collect --namespace booking-api -o booking_api_metadata.json
```

### 3) Spot check with kubectl to show how tedious manual checks are
```bash
# All deployments with labels
kubectl get deployments -A --show-labels

# Deployments missing owner
kubectl get deployments -A -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,OWNER:.metadata.labels.owner' | grep '<none>'

# Services missing cost-center
kubectl get services -A -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,COST_CENTER:.metadata.labels.cost-center' | grep '<none>'

# PVCs status
kubectl get pvc -A -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,STATUS:.status.phase'
```
> *Talking point: Raw data is disconnected from policy. This is why we need the LLM in Section 07.*

---

**Try it:** Open [`architecture_builder/index.html`](architecture_builder/index.html) in your browser to wire the **laptop ↔ cluster bridge** — local collect.py reads the Kind API and writes JSON on your machine. Use **Need a hint?** if stuck, then press **Run Scan** to validate.
