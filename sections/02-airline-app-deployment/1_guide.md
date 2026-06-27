# Demo 1: Inspect Manifests and Deploy App

**Time Budget:** 2-3 mins

### 1) Inspect the manifest layout
```bash
find sections/02-airline-app-deployment/manifests/airline-k8-deployment -maxdepth 2 -type f | sort
```

### 2) Inspect the Kustomize file
```bash
cat sections/02-airline-app-deployment/manifests/airline-k8-deployment/kustomization.yaml
```

### 3) Deploy the app
```bash
kubectl apply -k sections/02-airline-app-deployment/manifests/airline-k8-deployment/
```
> *Expected: Resources created across multiple namespaces.*
