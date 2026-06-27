# Demo 2: Kind Cluster Creation & Verification

**Time Budget:** 3-4 mins

### 1) Create the cluster
```bash
kind create cluster --name finops-cluster
```
> *Expected: Spinnup of a fresh local cluster.*

### 2) Confirm the cluster exists
```bash
kind get clusters
```

### 3) Confirm kubectl can talk to it
```bash
kubectl cluster-info
```

### 4) Confirm nodes are ready
```bash
kubectl get nodes
```
