# Demo 2: Validate the Runtime Footprint

**Time Budget:** 2–3 mins

**Narrative:** Deployments succeeded. Let's check each namespace to confirm pods, services, and config are healthy. In production you would have monitoring dashboards — for now, kubectl is our dashboard.

---

### 1) Check deployments across namespaces

```bash
kubectl get deployments -n booking-api
kubectl get deployments -n flight-search
kubectl get deployments -n inventory
kubectl get deployments -n payment
```

**What it does:** Shows deployments per namespace with `READY` count (e.g. `1/1`). All should be fully ready.

> *Talking point: "If you see `0/1` or `1/2`, something is wrong — pod is crashing or not scheduling. Here everything should be green."*

---

### 2) Check pods across namespaces

```bash
kubectl get pods -n booking-api
kubectl get pods -n flight-search
```

**What it does:** Lists pods and their status. You should see `Running` and `1/1` for each.

> *Expected: One pod per deployment, all in `Running` state.*

---

### 3) Check services and configmaps

```bash
kubectl get services -n inventory
kubectl get configmaps -n payment
```

**What it does:** Shows Services (ClusterIP endpoints) and ConfigMaps (configuration data) in the given namespaces.

> *Talking point: "Services give you a stable DNS name. ConfigMaps inject configuration without rebuilding images. Both are core K8 primitives."*

---

### 4) Check persistent volume claims

```bash
kubectl get pvc -n booking-api
```

**What it does:** Shows PVCs — persistent storage requests. If a PVC is `Pending`, the storage class is missing or the volume cannot provision.

> *Expected: PVCs in `Bound` state. In Kind, local-path provisioner handles this automatically.*

---

**Next:** Resources are healthy. Next we go deeper into one workload — describe, logs, exec → `3_guide.md`
