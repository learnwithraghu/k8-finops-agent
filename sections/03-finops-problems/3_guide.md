# Demo 3: Pinpointing Ownership Gaps

**Time Budget:** 3-4 mins

### 1) Inspect a good baseline (Inventory)
```bash
kubectl get deployment inventory-service -n inventory -o yaml
kubectl get pvc inventory-data -n inventory -o yaml
```

### 2) Inspect partial compliance (Payment)
```bash
kubectl get deployment payment-processor -n payment -o yaml
kubectl get pvc payment-logs -n payment -o yaml
```

### 3) Scan all Deployments and Services for gaps
```bash
kubectl get deployments -A --show-labels
kubectl get services -A --show-labels
```
> *Talking point: Compare labels across namespaces to show inconsistency.*
