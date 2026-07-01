# Demo 2: Investigate the Namespace

**Time Budget:** 4–5 mins

**Narrative:** We know payments fail but the UI loads. Now we work inside the `payment` namespace and discover *why* — using commands you would actually run on call, not pre-baked grep one-liners.

---

### 1) Compare pods — which workloads have running containers?

```bash
kubectl get pods -n payment
```

**What it does:** Lists pods and their status (`Running`, `CrashLoopBackOff`, etc.) and the `READY` column (e.g. `1/1`).

> *Expected: UI pod is `Running` and `1/1`. API pod line is missing or shows `0` ready — something is wrong with the backend.*

---

### 2) Look at deployments — desired vs ready replicas

```bash
kubectl get deployments -n payment
```

**What it does:** Shows each Deployment's `READY` column as `ready/desired` (e.g. `1/1` or `0/0`). This is often the fastest hint that a Deployment is scaled to zero or failing to schedule.

> *Expected: `payment-gateway` shows `1/1`. `payment-gateway-api` shows `0/0` — desired state says zero replicas are running.*

---

### 3) Get details on the suspicious deployment

```bash
kubectl describe deployment payment-gateway-api -n payment
```

**What it does:** Prints human-readable details: labels, events, conditions, and the replica summary (`Replicas: 0 desired | 0 updated | 0 total`). Use this when `get` output is not enough.

> *Expected: Replicas explicitly set to 0. This is the root cause — the API was scaled down (or never scaled up).*
>
> *Talking point: You found this via `get` + `describe`, not by piping YAML through grep. That is how most people actually debug.*

---

### 4) Confirm the Service has no healthy backends

```bash
kubectl get endpoints payment-gateway-api -n payment
```

**What it does:** Shows which pod IPs the Service is routing traffic to. Empty or `<none>` means no pods match the Service selector — requests to the API will fail.

> *Expected: `ENDPOINTS` column is empty or `<none>`.*

---

### 5) Try to fetch logs (and hit a dead end)

```bash
kubectl logs -n payment deploy/payment-gateway-api
```

**What it does:** Streams logs from a pod owned by the Deployment. If no pods exist, this command fails — which is itself useful information.

> *Expected: Error like "unable to find pods" / no containers.*
>
> *Talking point: "No pods → no logs. The failure is at the scheduling/replica level, not inside a crashing container."*
