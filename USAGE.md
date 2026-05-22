# K8s FinOps Agent - Step-by-Step Usage Guide

This guide walks you through setting up and running the K8s FinOps Agent from scratch.

## Quick Start (Automated)

```bash
# Run the automated setup script
./setup.sh
```

This script will:
1. Validate Docker, Kind, and kubectl are installed
2. Check Docker is running
3. Create a Kind cluster (or use existing)
4. Clean up any existing resources
5. Build the Docker image
6. Check your .env file

**Setup script options:**
```bash
./setup.sh --help          # Show help
./setup.sh --mock          # Setup for mock mode (no AWS/GitHub)
./setup.sh --cleanup       # Full cleanup (cluster + image)
./setup.sh --skip-build    # Skip Docker image build
```

## Prerequisites

- Docker installed
- Kind (Kubernetes in Docker) installed
- kubectl installed
- Python 3.9+ (for local development)
- AWS account with Bedrock access
- GitHub account with a repository for tech-debt issues

## Manual Setup

If you prefer manual setup instead of the automated script, follow these steps:

## Step 1: Clone the Repository

```bash
git clone <repository-url>
cd k8-finops-agent
```

## Step 2: Create Environment File

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

**Required variables in `.env`:**
```bash
# AWS Configuration (for Bedrock)
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_REGION=us-east-1

# GitHub Configuration
GITHUB_TOKEN=ghp_your_github_token_here
GITHUB_REPO=your-org/tech-debt

# Infrastructure
INSTANCE_TYPE=t2.medium
```

## Step 3: Create a Kind Cluster

```bash
# Create a Kind cluster named finops-cluster
kind create cluster --name finops-cluster

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

## Step 4: Deploy Airline Services

```bash
# Create the airline namespace
kubectl create namespace airline

# Deploy all airline services
kubectl apply -k airline-k8-deployment/

# Verify deployments
kubectl get all -n airline
```

**Expected output:**
- flight-search-service (missing cost-center, owner)
- booking-api (missing environment, compliance)
- payment-processor (missing tier, application)
- inventory-service (properly tagged - baseline)
- orphaned-pvc (not mounted)

## Step 5: Build the FinOps Agent Docker Image

```bash
# Build the Docker image
docker build -t k8-finops-agent:latest .

# Verify image was created
docker images | grep k8-finops-agent
```

## Step 6: Run the FinOps Agent

### Option A: Run Locally (with kubeconfig mounted)

```bash
# Run the agent against your Kind cluster
docker run --rm \
  -v ~/.kube/config:/home/finops/.kube/config:ro \
  --env-file .env \
  k8-finops-agent:latest
```

### Option B: Run in Mock Mode (no AWS/GitHub required)

```bash
# Run with mock analyzer and mock GitHub client
docker run --rm \
  -v ~/.kube/config:/home/finops/.kube/config:ro \
  -e USE_MOCK=true \
  -e USE_MOCK_GITHUB=true \
  k8-finops-agent:latest
```

### Option C: Dry Run (scan only, no issues created)

```bash
# Scan and show report without creating GitHub issues
docker run --rm \
  -v ~/.kube/config:/home/finops/.kube/config:ro \
  --env-file .env \
  k8-finops-agent:latest \
  --dry-run
```

## Step 7: View Results

### Console Output

The agent will print a report showing:
```
# FinOps Analysis Report

## Cost Summary
- Total Monthly Cost: $XX.XX
- Tracked: $XX.XX (XX%)
- Untracked: $XX.XX (XX%)

## Breakdown by Category
- Unallocated: $XX.XX/month
- Orphaned: $XX.XX/month
- Unowned: $XX.XX/month

## Violations Found: X
...
```

### GitHub Issues

Check your GitHub repository for new issues:
- Each violation creates one issue
- Issues include cost impact and AI recommendations
- Labels: finops, category, priority, cost level

## Step 8: Clean Up

```bash
# Delete airline services
kubectl delete -k airline-k8-deployment/

# Delete Kind cluster
kind delete cluster --name finops-cluster

# Remove Docker image (optional)
docker rmi k8-finops-agent:latest
```

## Troubleshooting

### Issue: Cannot connect to Kubernetes
```bash
# Verify kubeconfig exists
cat ~/.kube/config

# Check Kind cluster is running
kind get clusters

# Export kubeconfig for Kind
kind export kubeconfig --name finops-cluster
```

### Issue: AWS Bedrock connection failed
```bash
# Verify AWS credentials
aws sts get-caller-identity

# Check Bedrock access in AWS Console
# Ensure IAM user has bedrock:InvokeModel permission
```

### Issue: GitHub authentication failed
```bash
# Verify GitHub token
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user

# Check token has repo scope
```

### Issue: Agent runs but no issues created
```bash
# Check if issues already exist (duplicate detection)
# Run with --dry-run to see what would be created
# Check GitHub repo name is correct in .env
```

## Advanced Usage

### Run Against Specific Namespace

```bash
docker run --rm \
  -v ~/.kube/config:/home/finops/.kube/config:ro \
  --env-file .env \
  k8-finops-agent:latest \
  --namespace airline
```

### Adjust Cost Threshold

```bash
# Only report violations costing more than $5/month
docker run --rm \
  -v ~/.kube/config:/home/finops/.kube/config:ro \
  --env-file .env \
  k8-finops-agent:latest \
  --threshold 5.0
```

### Run as Kubernetes Job

```bash
# Load image into Kind
kind load docker-image k8-finops-agent:latest --name finops-cluster

# Deploy the agent job
kubectl apply -f demo/manifests/agent-job.yaml

# Check job logs
kubectl logs -l job-name=finops-agent-scan
```

## Development Mode

### Install Dependencies Locally

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run agent locally
python -m agent.main --mock --mock-github
```

### Run Tests

```bash
# Run unit tests (if available)
python -m pytest tests/
```

## File Structure Reference

```
k8-finops-agent/
├── agent/                      # Agent code
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   ├── scanner.py              # K8s scanner
│   ├── cost_calculator.py      # Cost engine
│   ├── untracked_money.py      # Untracked detection
│   ├── analyzer.py             # Bedrock AI
│   └── github_client.py        # GitHub integration
├── airline-k8-deployment/      # Airline services
│   ├── flight-search-service/
│   ├── booking-api/
│   ├── payment-processor/
│   ├── inventory-service/
│   └── orphaned-resources/
├── config/                     # Configuration
│   ├── pricing.yaml
│   └── tagging-rules.yaml
├── demo/                       # Demo scripts
│   └── deploy.sh
├── setup.sh                    # Automated setup script
├── Dockerfile
├── requirements.txt
├── .env.example
└── USAGE.md                    # This file
```

## Next Steps

1. Review GitHub issues created by the agent
2. Apply recommended tags to resources
3. Re-run agent to verify fixes
4. Set up scheduled runs (e.g., weekly)

## Support

For issues or questions:
- Check logs with `--log-level DEBUG`
- Review agent code in `agent/` directory
- Check configuration in `config/` directory
