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
- airline namespace
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
kubectl create namespace airline
kubectl apply -k airline-k8-deployment/
kubectl get all -n airline
```

## 4) Install Python deps

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 5) Run the agent locally

### Mock mode (recommended for local testing)

```bash
python -m agent.main --mock --mock-github --dry-run --namespace airline --log-level DEBUG
```

### Use `.env` values

```bash
python -m agent.main --namespace airline --log-level DEBUG
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

## 6) What to expect

The agent will:
- scan Deployments, Services, ConfigMaps, and PVCs
- detect missing tags / orphaned PVCs
- print a FinOps report
- create no GitHub issues when `DRY_RUN=true` or `--dry-run` is set

## 7) Cleanup

```bash
kubectl delete -k airline-k8-deployment/
kubectl delete namespace airline
kind delete cluster --name finops-cluster
```

## Notes

- For EC2/Amazon Linux, use `.env.ec2.example` instead of the local template.
- For host Python runs, use `KUBECONFIG_PATH=~/.kube/config` and ensure `kind export kubeconfig` has been run.
- Bedrock auth uses AWS IAM credentials from `.env`.
- If you want real AWS Bedrock + GitHub issues, remove `--mock` and `--mock-github` and set valid AWS creds.
