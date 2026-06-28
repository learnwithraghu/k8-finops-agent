# Demo 3: Workload Deep Dive

**Time Budget:** 2-3 mins

### 1) Describe a workload
```bash
kubectl describe deployment flight-search-service -n flight-search
```

### 2) Describe a pod (Replace <pod-name>)
```bash
kubectl get pods -n flight-search
kubectl describe pod -n flight-search <pod-name>
```

### 3) Check logs
```bash
kubectl logs -n flight-search deploy/flight-search-service
```

### 4) Exec into a running container
```bash
kubectl exec -it -n flight-search deploy/flight-search-service -- sh
```
> *Expected: Shell access to the running container. Type `exit` to leave.*

---

**Try it:** Open [`architecture_builder/index.html`](architecture_builder/index.html) in your browser to build the **namespace stack** — deploy gate first, then resources inside the booking-api box. Use **Need a hint?** if stuck, then press **Deploy & Inspect** to validate.
