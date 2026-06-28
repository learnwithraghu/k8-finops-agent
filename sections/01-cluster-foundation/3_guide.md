# Demo 3: Baseline Namespaces Creation & Validation

**Time Budget:** 2-3 mins

### 1) Create the baseline namespaces
```bash
kubectl create namespace booking-api
kubectl create namespace flight-search
kubectl create namespace inventory
kubectl create namespace payment
kubectl create namespace airline
```

### 2) Verify namespaces
```bash
kubectl get namespaces
```

### 3) Confirm kubectl access works
```bash
kubectl auth can-i get pods -A
```

### 4) Confirm there are no app workloads yet
```bash
kubectl get pods -A
```
> *Expected: No app deployments returned, cluster is clean.*

---

**Try it:** Open [`architecture_builder/index.html`](architecture_builder/index.html) in your browser to assemble the cluster foundation flow from memory — drag components into the correct slots, use **Need a hint?** if stuck, then press **Run Flow** to validate. Placed components move to **On canvas** so you can reassign them.
