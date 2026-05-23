# Local Usage Guide

This guide runs the K8s FinOps Agent locally against a Kind cluster.

## Prerequisites

- Docker
- kind
- kubectl
- Python 3.9+

Check:
```bash
docker --version
kind version
kubectl version --client
python3 --version
```

## 1) Set up the environment

```bash
cp .env.example .env
```

For local testing, `.env` is already set for:
- mock AWS/GitHub
- host kubeconfig (`~/.kube/config`)
- service-specific namespaces for the airline app
- dry-run mode

If needed, edit it:
```bash
nano .env
```

## 2) Create a local Kind cluster

```bash
kind create cluster --name finops-cluster
kubectl cluster-info
kubectl get nodes
```

If you need kubeconfig refreshed:
```bash
kind export kubeconfig --name finops-cluster
kubectl config current-context
```

## 3) Deploy the demo workload

This repo includes the sample airline app manifests.

```bash
kubectl create namespace booking-api
kubectl create namespace flight-search
kubectl create namespace inventory
kubectl create namespace payment
kubectl apply -k sections/02-airline-app-deployment/manifests/airline-k8-deployment/
kubectl get all -n booking-api
kubectl get all -n flight-search
kubectl get all -n inventory
kubectl get all -n payment
```

## 4) Install Python deps

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 5) Start the Flask issue tracker (Phase 3)

Run this first if you want the agent to POST Bedrock decisions into the local issue tracker UI/API.

```bash
# Start the local tracker before running the agent
# (replace issue-tracker:latest with your built image)
docker run --rm \
  -p 5000:5000 \
  --name issue-tracker \
  issue-tracker:latest
```

Open the tracker in your browser:
- http://localhost:5000

## 6) Run the scanner/agent in two steps

### Step A: Run locally with Python (first teaching step)

This is the host-side scanner run. It reads the Kubernetes cluster and can scan all namespaces if you do not pass `--namespace`.

```bash
python -m agent.main --mock --mock-github --dry-run --log-level DEBUG
```

To focus on one namespace:
```bash
python -m agent.main --mock --mock-github --dry-run --namespace airline --log-level DEBUG
```

### Step B: Run inside Kubernetes (second teaching step)

Deploy the agent as a K8s workload in a **separate namespace** (for example: `finops-agent`). It still scans the whole cluster because the scanner defaults to **all namespaces** unless a target namespace is provided.

```bash
# Example: create a dedicated namespace for the scanner
kubectl create namespace finops-agent

# Then deploy the agent manifest into that namespace
# (use your K8s Deployment/Job manifest for the agent)
kubectl apply -n finops-agent -f sections/08-k8-native-agent/manifests/
```

If you want the in-cluster run to scan everything, do not set `TARGET_NAMESPACE`.
If you want it to scan only one namespace, set `TARGET_NAMESPACE=airline` in `.env`.

### Optional: Use `.env` values

```bash
python -m agent.main --log-level DEBUG
```

To use real Bedrock, set your IAM user credentials in `.env`:
```env
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_SESSION_TOKEN=
```
Set `BEDROCK_MODEL_ID=anthropic.claude-3-5-haiku-20241022-v1:0`.

If you run the agent in Docker instead of Python on the host, override the kubeconfig path:
```bash
docker run --rm \
  -v ~/.kube/config:/home/finops/.kube/config:ro \
  -e KUBECONFIG_PATH=/home/finops/.kube/config \
  --env-file .env \
  k8-finops-agent:latest
```

If the local Flask tracker is running, point the agent at it with the tracker URL env var you define for Phase 3 (for example: `ISSUE_TRACKER_URL=http://host.docker.internal:5000`).

## 7) What to expect

The agent will:
- scan Deployments, Services, ConfigMaps, and PVCs
- detect missing tags / orphaned PVCs
- print a FinOps report
- create no GitHub issues when `DRY_RUN=true` or `--dry-run` is set

## 8) Cleanup

```bash
kubectl delete -k sections/02-airline-app-deployment/manifests/airline-k8-deployment/
kubectl delete namespace airline
kind delete cluster --name finops-cluster
```

## Notes

- Use `.env.example` for the MacBook local setup.
- For host Python runs, use `KUBECONFIG_PATH=~/.kube/config` and ensure `kind export kubeconfig` has been run.
- Bedrock auth uses AWS IAM credentials from `.env`.
- If you want real AWS Bedrock + GitHub issues, remove `--mock` and `--mock-github` and set valid AWS creds.
- Start the Flask tracker before the agent whenever you want local issue capture instead of GitHub-only output.
