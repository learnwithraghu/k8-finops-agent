# Demo 1: Run the Collector

**Time Budget:** 3 mins

**Narrative:** Instead of running 20 kubectl commands by hand, we let Python do it. The collector reads the cluster and dumps raw JSON — every namespace, every deployment, every pod. This is the foundation for automation.

---

### 1) Run the collector across the whole cluster

```bash
PYTHONPATH=sections/04-local-python-agent python -m agent.collect -o k8s_metadata.json
```

**What it does:** Connects to the Kind cluster, reads all namespaces, and writes a JSON snapshot to `k8s_metadata.json`.

> *Talking point: "The collector uses the same API server that kubectl talks to — just from Python instead of the command line."*

---

### 2) Review the output

```bash
python3 -m json.tool k8s_metadata.json | head -80
```

**What it does:** Pretty-prints the first 80 lines of the JSON output. You will see namespaces, deployments, pods, services — raw, unstructured data.

> *Expected: A large JSON blob with resource metadata. No analysis, no compliance verdicts — just facts.*

> *Talking point: "This is messy on purpose. The collector does not judge — it just dumps what the cluster has. We add intelligence in Section 07."*

---

### 3) Run the collector for a single namespace

```bash
PYTHONPATH=sections/04-local-python-agent python -m agent.collect --namespace booking-api -o booking_api_metadata.json
```

**What it does:** Same collector, scoped to one namespace. Useful when you only care about a specific service.

> *Talking point: "In production you might scan per-team or per-namespace. The collector supports both — whole cluster or targeted."*

---

**Next:** We have automated output. Next we compare it to what manual kubectl checks look like → `2_guide.md`
