# Section 01 Guide: Cluster Foundation

This is the only file you need for Section 01.

## Goal
Prepare the machine and Kubernetes cluster one command at a time.

## What students will do
1. Clean up any old Kind/Kubernetes leftovers
2. Verify Docker, Helm, Kind, and kubectl are available
3. Verify Docker is actually running
4. Create the Kind cluster
5. Validate kubectl access
6. Create the four app namespaces
7. Confirm everything is ready for the next section

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

## Cleanup first
Run these commands one by one to clear old state.

### 1) See existing Kind clusters
```bash
kind get clusters
```

### 2) Delete the FinOps Kind cluster if it exists
```bash
kind delete cluster --name finops-cluster
```

### 3) Check for old Docker images from the agent
```bash
docker images | grep k8-finops-agent
```

### 4) Remove the old agent image if present
```bash
docker rmi k8-finops-agent:latest
```

### 5) Check for leftover namespaces
```bash
kubectl get namespaces
```

### 6) Remove the lesson namespaces if they already exist
```bash
kubectl delete namespace booking-api --ignore-not-found=true
kubectl delete namespace flight-search --ignore-not-found=true
kubectl delete namespace inventory --ignore-not-found=true
kubectl delete namespace payment --ignore-not-found=true
```

## Verify the tools
Run each command and confirm it returns a version or status.

### 7) Verify Docker is installed
```bash
docker --version
```

### 8) Verify Docker is running
```bash
docker info
```

### 9) Verify Helm is installed
```bash
helm version --short
```

### 10) Verify Kind is installed
```bash
kind version
```

### 11) Verify kubectl is installed
```bash
kubectl version --client
```

## Create the cluster
Now create the Kind cluster from scratch.

### 12) Create the cluster
```bash
kind create cluster --name finops-cluster
```

### 13) Confirm the cluster exists
```bash
kind get clusters
```

### 14) Confirm kubectl can talk to it
```bash
kubectl cluster-info
```

### 15) Confirm nodes are ready
```bash
kubectl get nodes
```

## Create the baseline namespaces
These namespaces are needed for the later sections.

### 16) Create the booking-api namespace
```bash
kubectl create namespace booking-api
```

### 17) Create the flight-search namespace
```bash
kubectl create namespace flight-search
```

### 18) Create the inventory namespace
```bash
kubectl create namespace inventory
```

### 19) Create the payment namespace
```bash
kubectl create namespace payment
```

### 20) Verify namespaces
```bash
kubectl get namespaces
```

## Final validation
Run these checks at the end of the section.

### 20) Confirm kubectl access works
```bash
kubectl auth can-i get pods -A
```

### 21) Confirm there are no app workloads yet
```bash
kubectl get pods -A
```

## What success looks like
You should have:
- one Kind cluster: `finops-cluster`
- working `kubectl cluster-info`
- these namespaces: `booking-api`, `flight-search`, `inventory`, `payment`
- no app deployments yet

## Common issues
### Docker info fails
Start Docker first.

### Kind create cluster fails
Check that Docker is running and has enough resources.

### kubectl cannot connect
Run:
```bash
kind export kubeconfig --name finops-cluster
```

### Namespace already exists
That is fine. Continue.

## Handoff to Section 02
Once all commands above work, go to:
- `sections/02-airline-app-deployment/guide.md`

Section 02 uses the cluster and namespaces created here.
