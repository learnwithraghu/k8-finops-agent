# Demo 2: Validating Runtime Footprint

**Time Budget:** 3-4 mins

### 1) Check the default namespace (where drift happened)
```bash
kubectl get all -n default
```
> *Expected: See analytics-collector mixed with system pods without ownership tags.*

### 2) Verify specific namespaces
```bash
kubectl get namespace booking-api
kubectl get all -n booking-api

kubectl get namespace flight-search
kubectl get all -n flight-search
```

### 3) Inspect specific resource types
```bash
kubectl get deployments -n booking-api
kubectl get pods -n flight-search -o wide
kubectl get services -n inventory
kubectl get configmaps -n payment
kubectl get pvc -n booking-api
```
