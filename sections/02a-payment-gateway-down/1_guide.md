# Demo 1: Orient & Reproduce the Failure

**Time Budget:** 3–4 mins

**Setup (already done):** Complete `0_prerequisite_guide.md` first — manifests applied, port-forward to `http://localhost:8089` running.

**Narrative:** You are on call. Someone says "payments are broken." You do not yet know which namespace or service is involved — you start from the cluster and work toward the user-visible symptom.

---

### 1) Find relevant namespaces

```bash
kubectl get namespaces
```

**What it does:** Lists every namespace in the cluster. Look for names that might relate to payments (e.g. `payment`).

> *Talking point: In a real incident you often start this blind — alerts rarely hand you the exact deployment name.*

---

### 2) See what is running in the payment namespace

```bash
kubectl get all -n payment
```

**What it does:** Shows common workload types (pods, services, deployments, replicasets) in the `payment` namespace in one view.

> *Expected: You see resources like `payment-gateway` (UI) and `payment-gateway-api` (backend). Pod counts may look uneven — note that, but do not explain the root cause yet.*

---

### 3) Check whether the UI service exists and has a ClusterIP

```bash
kubectl get svc -n payment
```

**What it does:** Lists Services in the namespace. A Service with a ClusterIP and ports means Kubernetes has a stable network endpoint for that app — it does not by itself mean the backend is healthy.

> *Talking point: "The UI endpoint exists. That does not mean payments work — we need to test from the user's perspective."*

---

### 4) Open the UI and try a payment

Open `http://localhost:8089` in the browser (port-forward is already running).

Fill in the payment form and submit.

> *Expected: The page loads fine (UI is up). Submitting a payment fails — e.g. 503 / "service unavailable" style error.*
>
> *Talking point: "The UI is not down. Something behind it — likely the API — is failing. Next demo we dig into the namespace."*
