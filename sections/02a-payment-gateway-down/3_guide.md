# Demo 3: Ownership Wall, Fix, and Validate

**Time Budget:** 3–4 mins

**Narrative:** Root cause is clear (API at 0 replicas). Before you fix it, you would normally page the owning team. That is where this scenario gets painful.

---

### 1) Look for ownership metadata

```bash
kubectl get deployments -n payment --show-labels
```

**What it does:** Lists Deployments with their label key/value pairs visible in the output. Teams usually rely on labels like `owner`, `team`, or `cost-center` to know who to contact.

> *Expected: You see `app`, `environment`, `tier` — but no `owner` or `cost-center` on the failing API.*

---

### 2) Search more broadly (still no owner)

```bash
kubectl get deployments -A --show-labels | grep payment
```

**What it does:** Lists Deployments in **all** namespaces with labels, then filters lines containing `payment`. Useful when you are not sure which namespace holds the workload.

> *Talking point: "We know what is broken and how to patch it, but we still do not know who owns it, what Slack channel to use, or whose cost center pays for this. That is the FinOps gap Section 03 addresses."*

---

### 3) Apply the quick fix — scale the API back up

```bash
kubectl scale deployment payment-gateway-api -n payment --replicas=1
```

**What it does:** Changes the Deployment's desired replica count to 1. Kubernetes will create a pod and the Service should get an endpoint.

Wait a few seconds, then confirm:

```bash
kubectl get pods -n payment
kubectl get endpoints payment-gateway-api -n payment
```

**What they do:** Verify a pod is `Running` and the Service now has an endpoint IP.

---

### 4) Validate in the UI

Go back to `http://localhost:8089`, submit a payment again.

> *Expected: Payment succeeds (or returns a success-style response). Service is restored.*

---

### 5) The "bad fix" — slap labels on manually (cautionary)

```bash
kubectl label deployment payment-gateway-api -n payment \
  owner=payments-team \
  cost-center=cc-payments \
  tier=backend \
  environment=prod \
  --overwrite
```

**What it does:** Adds or overwrites labels directly on the live Deployment. This does **not** update Git/manifests — the next deploy or GitOps sync can wipe them.

> *Talking point: "This unblocks the incident but does not fix governance. Real fixes belong in manifests and tagging policy — Section 03."*

---

### 6) Reset for the next run (optional, instructor only)

```bash
kubectl scale deployment payment-gateway-api -n payment --replicas=0
```

**What it does:** Scales the API back to 0 so the broken state is ready for the next demo.
