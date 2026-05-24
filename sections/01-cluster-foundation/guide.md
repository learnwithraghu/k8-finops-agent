# Section 01 Guide: Cluster Foundation

This is the only file you need for Section 01.

## Goal
Prepare the machine and Kubernetes cluster one command at a time.

## What students will do
1. Run the cleanup helper to clear old Kind/Kubernetes leftovers
2. Verify Docker, Helm, Kind, and kubectl are available
3. Verify Docker daemon is running
4. Create the Kind cluster
5. Verify the Kind cluster is running
6. Validate kubectl access
7. Create the four app namespaces
8. Confirm everything is ready for the next section

## What this section is not
- No app deployment
- No FinOps logic
- No Bedrock/AI
- No issue tracker integration
- No setup script as the primary teaching path

> `setup.sh` still exists in the repo as a helper, but do not use it for the lesson flow here.

## Prerequisites
- MacBook local shell access
- Docker installed
- Helm installed
- Kind installed
- kubectl installed

## Note
Use `helper/cleanup.sh` first to clear old Kind/Kubernetes state before starting the lesson.

## Verify the tools
Run each command and confirm it returns a version or status.

### 1) Verify Docker is installed
```bash
docker --version
```

### 2) Verify Docker is running
```bash
docker info
```

### 3) Verify Helm is installed
```bash
helm version --short
```

### 4) Verify Kind is installed
```bash
kind version
```

### 5) Verify kubectl is installed
```bash
kubectl version --client
```

## Create the cluster
Now create the Kind cluster from scratch.

### 6) Create the cluster
```bash
kind create cluster --name finops-cluster
```

### 7) Confirm the cluster exists
```bash
kind get clusters
```

### 8) Confirm kubectl can talk to it
```bash
kubectl cluster-info
```

### 9) Confirm nodes are ready
```bash
kubectl get nodes
```

## Create the baseline namespaces
These namespaces are needed for the later sections.

### 10) Create the booking-api namespace
```bash
kubectl create namespace booking-api
```

### 11) Create the flight-search namespace
```bash
kubectl create namespace flight-search
```

### 12) Create the inventory namespace
```bash
kubectl create namespace inventory
```

### 13) Create the payment namespace
```bash
kubectl create namespace payment
```

### 14) Create the airline namespace
```bash
kubectl create namespace airline
```

### 15) Verify namespaces
```bash
kubectl get namespaces
```

## Final validation
Run these checks at the end of the section.

### 16) Confirm kubectl access works
```bash
kubectl auth can-i get pods -A
```

### 17) Confirm there are no app workloads yet
```bash
kubectl get pods -A
```

## What success looks like
You should have:
- one Kind cluster: `finops-cluster`
- working `kubectl cluster-info`
- these namespaces: `booking-api`, `flight-search`, `inventory`, `payment`, `airline`
- no app deployments yet

## Handoff to Section 02
Once all commands above work, go to:
- `sections/02-airline-app-deployment/guide.md`

Section 02 uses the cluster and namespaces created here.
