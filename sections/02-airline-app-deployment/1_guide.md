# Demo 1: Deploy & Validate the Airline App

**Time Budget:** 4–5 mins

**Narrative:** We have a cluster with empty namespaces. Deploy the airline services with Kustomize, then confirm pods, services, and config are healthy across each namespace. In production you would have monitoring dashboards — for now, kubectl is our dashboard.

---

### 1) Deploy the app

```bash
kubectl apply -k sections/02-airline-app-deployment/manifests/airline-k8-deployment/
```

**What it does:** Applies all manifests through Kustomize. Creates deployments, services, configmaps, and PVCs across the airline namespaces.

> *Expected: Multiple "created" lines — one per resource, spread across `booking-api`, `flight-search`, `inventory`, `payment`.*

> *Talking point: "Kustomize is built into kubectl. One command, multiple namespaces, all resources created."*

---

### 2) Confirm resources were created

```bash
kubectl get all -A | grep -v kube-system
```

**What it does:** Lists all workloads across namespaces, filtering out system components. You should see pods, services, and deployments in the airline namespaces.

---

### 3) Check deployments across namespaces

```bash
kubectl get deployments -n booking-api
kubectl get deployments -n flight-search
kubectl get deployments -n inventory
kubectl get deployments -n payment
```

**What it does:** Shows deployments per namespace with `READY` count (e.g. `1/1`). All should be fully ready.

> *Talking point: "If you see `0/1` or `1/2`, something is wrong — pod is crashing or not scheduling. Here everything should be green."*

---

### 4) Check pods across namespaces

```bash
kubectl get pods -n booking-api
kubectl get pods -n flight-search
```

**What it does:** Lists pods and their status. You should see `Running` and `1/1` for each.

> *Expected: One pod per deployment, all in `Running` state.*

---

### 5) Check services and configmaps

```bash
kubectl get services -n inventory
kubectl get configmaps -n payment
```

**What it does:** Shows Services (ClusterIP endpoints) and ConfigMaps (configuration data) in the given namespaces.

> *Talking point: "Services give you a stable DNS name. ConfigMaps inject configuration without rebuilding images. Both are core K8 primitives."*

---

### 6) Check persistent volume claims

```bash
kubectl get pvc -n booking-api
```

**What it does:** Shows PVCs — persistent storage requests. If a PVC is `Pending`, the storage class is missing or the volume cannot provision.

> *Expected: PVCs in `Bound` state. In Kind, local-path provisioner handles this automatically.*

---

### 7) Access the Booking UI (Skyscanner-style)

The `booking-api` now serves a full Skyscanner-style flight booking wizard with 5 steps:

```bash
kubectl port-forward -n booking-api svc/booking-api 8080:8080 --address 127.0.0.1
```

Then open **http://booking-api.local:8080** in your browser.

> *Note: Add `127.0.0.1 booking-api.local` to your `/etc/hosts` if needed, or access directly via `http://localhost:8080`.*

**The booking wizard includes:**
- **Step 1:** Search flights (origin, destination, date, passengers)
- **Step 2:** Select from mock flight results
- **Step 3:** Enter passenger details
- **Step 4:** Enter payment info (card preview updates live)
- **Step 5:** Confirmation with booking ID

> *Talking point: "This UI is served directly from the booking-api nginx container — no separate frontend deployment needed. The ConfigMap holds both the nginx config and the HTML/JS, mounted as a volume. This is a lightweight pattern for demos."*

---

**Next:** Resources are healthy. Next we go deeper into one workload — describe, logs, exec → `2_guide.md`
