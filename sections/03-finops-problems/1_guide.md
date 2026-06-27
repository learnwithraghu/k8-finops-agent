# Demo 1: Identifying Untagged Resources

**Time Budget:** 3-4 mins

### 1) Read the tagging rules
```bash
cat sections/03-finops-problems/examples/tagging-rules.yaml
```
> *Talking point: Highlight required tags: owner, environment, cost-center.*

### 2) Inspect the booking API (Missing tags)
```bash
kubectl get deployment booking-api -n booking-api -o yaml
kubectl get service booking-api -n booking-api -o yaml
```

### 3) Inspect the flight search (Missing FinOps tags)
```bash
kubectl get deployment flight-search-service -n flight-search -o yaml
kubectl get configmap flight-search-config -n flight-search -o yaml
```
