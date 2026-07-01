# Demo 1: Deploy the Airline App

**Time Budget:** 2 mins

**Narrative:** We have a cluster with empty namespaces. Now we deploy the airline services using Kustomize — one command, multiple namespaces, all resources created.

---

### 1) Inspect the Kustomize entry point

```bash
cat sections/02-airline-app-deployment/manifests/airline-k8-deployment/kustomization.yaml
```

**What it does:** Shows the Kustomize configuration — which resource directories will be applied. This is the single source of truth for the deployment.

> *Talking point: "Kustomize is built into kubectl. No Helm, no templating engine — just declarative manifests composed together."*

---

### 2) Deploy the app

```bash
kubectl apply -k sections/02-airline-app-deployment/manifests/airline-k8-deployment/
```

**What it does:** Applies all manifests through Kustomize. Creates deployments, services, configmaps, and PVCs across the airline namespaces.

> *Expected: Multiple "created" lines — one per resource, spread across `booking-api`, `flight-search`, `inventory`, `payment`.*

---

### 3) Confirm resources were created

```bash
kubectl get all -A | grep -v kube-system
```

**What it does:** Lists all workloads across namespaces, filtering out system components. You should see pods, services, and deployments in the airline namespaces.

> *Talking point: "One apply, five namespaces, multiple resource types. That is the power of Kustomize — you define the desired state, Kubernetes makes it real."*

---

**Next:** Resources are created. Next we validate each namespace individually → `2_guide.md`
