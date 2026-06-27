# Demo 2: Triage and Diagnose Root Cause

**Time Budget:** 4-5 mins

### 1) Check the services and pods
```bash
kubectl get services -n payment
kubectl get pods -n payment
```

### 2) Inspect the deployment
```bash
kubectl describe deployment payment-gateway-api -n payment
kubectl get deployment payment-gateway-api -n payment -o yaml | grep -A3 'replicas:'
```
> *Expected: Replicas is explicitly set to 0.*

### 3) Try to get logs (Fails)
```bash
kubectl logs -n payment deploy/payment-gateway-api
```

### 4) Check the service endpoints
```bash
kubectl get endpoints payment-gateway-api -n payment
```
> *Expected: Endpoints show `<none>`.*

### 5) Look for ownership labels
```bash
kubectl get deployments -n payment --show-labels
kubectl get deployments -A --show-labels | grep payment
```
> *Talking point: We can't find who owns this because of missing metadata.*

### 6) The bad fix (Scale up and label manually)
```bash
kubectl scale deployment payment-gateway-api -n payment --replicas=1

kubectl label deployment payment-gateway-api -n payment \
  owner=payments-team \
  cost-center=cc-payments \
  tier=backend \
  environment=prod \
  --overwrite
```
> *Talking point: This works temporarily but doesn't fix the underlying GitOps/governance issue.*

### 7) Reset for next time (Optional)
```bash
kubectl scale deployment payment-gateway-api -n payment --replicas=0
```
