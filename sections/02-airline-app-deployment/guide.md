# Section 02 Guide: Airline App Deployment

This is the only file you need for Section 02.

## Goal
Deploy the airline app into four separate namespaces and learn how to inspect it with `kubectl`.

## What students will learn
- how a Kustomize app is structured
- how to deploy with `kubectl apply -k`
- how to inspect Deployments, Pods, Services, ConfigMaps, and PVCs
- how to use `describe`, `logs`, and `exec`
- how to verify the workload is actually running

## What you need before starting
Complete Section 01 first.

You should already have:
- a working Kind cluster
- kubectl access
- the four namespaces created in Section 01:
  - `booking-api`
  - `flight-search`
  - `inventory`
  - `payment`

## What gets deployed
The airline app contains:
- `flight-search-service` in namespace `flight-search`
- `booking-api` in namespace `booking-api`
- `payment-processor` in namespace `payment`
- `inventory-service` in namespace `inventory`

Each service has:
- a Deployment
- a Service
- a ConfigMap
- a PVC

This mirrors real ownership boundaries better than putting everything into one namespace.

## Where the manifests live
- `sections/02-airline-app-deployment/manifests/airline-k8-deployment/`

## Step 1: Inspect the manifest layout
Look at the directory structure first:

```bash
find sections/02-airline-app-deployment/manifests/airline-k8-deployment -maxdepth 2 -type f | sort
```

Then inspect the Kustomize file:

```bash
cat sections/02-airline-app-deployment/manifests/airline-k8-deployment/kustomization.yaml
```

## Step 2: Deploy the app
Apply the whole app at once:

```bash
kubectl apply -k sections/02-airline-app-deployment/manifests/airline-k8-deployment/
```

Kustomize will apply each service into its own namespace.

## Step 3: Verify one namespace
```bash
kubectl get namespace booking-api
kubectl get all -n booking-api
```

## Step 4: Verify a different namespace
```bash
kubectl get namespace flight-search
kubectl get all -n flight-search
```

## Step 5: Inspect other resource types in different namespaces
### Deployments
```bash
kubectl get deployments -n booking-api
```

### Pods
```bash
kubectl get pods -n flight-search -o wide
```

### Services
```bash
kubectl get services -n inventory
```

### ConfigMaps
```bash
kubectl get configmaps -n payment
```

### PVCs
```bash
kubectl get pvc -n booking-api
```

## Step 6: Describe a workload
Pick one service and inspect it fully:

```bash
kubectl describe deployment flight-search-service -n flight-search
```

Then inspect the pod behind it:

```bash
kubectl get pods -n flight-search
kubectl describe pod -n flight-search <pod-name>
```

## Step 7: Check logs
```bash
kubectl logs -n flight-search deploy/flight-search-service
```

## Step 8: Exec into a running container
If the image supports shell access:

```bash
kubectl exec -it -n flight-search deploy/flight-search-service -- sh
```

## Step 9: Inspect the YAML for learning
```bash
kubectl get deployment flight-search-service -n flight-search -o yaml
kubectl get service flight-search-service -n flight-search -o yaml
kubectl get configmap flight-search-service -n flight-search -o yaml
kubectl get pvc -n flight-search -o yaml
```

## What to notice
As you inspect the app, pay attention to:
- labels and selectors
- namespace placement
- resource requests and limits
- storage usage
- the relationship between Deployments and Services

Do not fix the tagging gaps yet. That is the point of Section 03.

## Expected output behavior
You should see:
- pods becoming `Running`
- services created in their own namespaces
- configmaps present for each service
- PVCs present for each workload

## Handoff to Section 03
Once the app is deployed and verified, move to:
- `sections/03-finops-problems/guide.md`

Section 03 will use this same deployment to show the FinOps problem.
