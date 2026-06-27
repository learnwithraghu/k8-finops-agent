# Demo 1: Reproduce the Outage

**Time Budget:** 3-4 mins

### 1) Deploy the payment gateway (with broken API)
```bash
kubectl apply -k sections/02a-payment-gateway-down/manifests/
```

### 2) Check what is running
```bash
kubectl get all -n payment
kubectl get pods -n payment
```
> *Expected: Notice that payment-gateway-api has 0/0 pods running.*

### 3) Port-forward the UI
```bash
kubectl port-forward svc/payment-gateway -n payment 8089:80
```
*(Keep this running, open `http://localhost:8089` in Chrome, and attempt a payment to see the 503 error)*
