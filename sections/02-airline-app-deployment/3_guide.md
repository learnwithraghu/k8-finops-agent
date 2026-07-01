# Demo 3: Workload Deep Dive

**Time Budget:** 2–3 mins

**Narrative:** Let's inspect a single service end-to-end. These five commands cover 90% of on-call triage — describe the deployment, find the pod, read its events, tail its logs, and exec into it.

---

### 1) Describe the deployment

```bash
kubectl describe deployment flight-search-service -n flight-search
```

**What it does:** Shows the deployment spec — labels, pod template, replica count, strategy, and recent events. This is your first stop when something is wrong.

> *Talking point: "Events at the bottom are gold. If a pod is failing to schedule or pulling a bad image, it shows up here."*

---

### 2) Find the pod name

```bash
kubectl get pods -n flight-search
```

**What it does:** Lists pods. Copy the pod name for the next steps (e.g. `flight-search-service-abc123`).

---

### 3) Describe the pod

```bash
kubectl describe pod <pod-name> -n flight-search
```

**What it does:** Shows pod-level detail — container status, resource requests, volumes, and events. Replace `<pod-name>` with the actual name from step 2.

> *Expected: Status `Running`, container `Ready`, no warning events.*

---

### 4) Tail the logs

```bash
kubectl logs -n flight-search deploy/flight-search-service
```

**What it does:** Streams logs from the pod owned by the deployment. Use `deploy/<name>` to target the deployment — kubectl resolves to the active pod automatically.

> *Talking point: "In production you would use a logging stack. For local dev, `kubectl logs` is fast and enough."*

---

### 5) Exec into the container

```bash
kubectl exec -it -n flight-search deploy/flight-search-service -- sh
```

**What it does:** Opens an interactive shell inside the running container. You can inspect files, check environment variables, or test network calls from inside the pod.

> *Expected: Shell prompt inside the container. Type `exit` to leave.*

> *Talking point: "This is your last resort when logs are not enough. You can see exactly what the container sees — env vars, mounted files, network reachability."*

---

**Try it:** Open [`architecture_builder/index.html`](architecture_builder/index.html) in your browser to build the **namespace stack** — deploy gate first, then resources inside the booking-api box. Use **Need a hint?** if stuck, then press **Deploy & Inspect** to validate.

**Next:** App is live and you can inspect it. Next section simulates a payment failure → `sections/02a-payment-gateway-down`
