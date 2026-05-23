# K8s FinOps Agent - Step-by-Step Usage Guide

> Teaching flow is now organized under `sections/`. Use the section guides and `section_goal.md` files as the source of truth.

This guide walks you through setting up and running the K8s FinOps Agent from scratch.

## Quick Start (Automated)

```bash
# Run the automated setup script
bash sections/01-cluster-foundation/commands/setup.sh
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
bash sections/01-cluster-foundation/commands/setup.sh --help          # Show help
bash sections/01-cluster-foundation/commands/setup.sh --mock          # Setup for mock mode (no AWS/GitHub)
bash sections/01-cluster-foundation/commands/setup.sh --cleanup       # Full cleanup (cluster + image)
bash sections/01-cluster-foundation/commands/setup.sh --skip-build    # Skip Docker image build
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
# Copy the local example environment file
cp .env.example .env

# Use the local example on your MacBook
# cp .env.example .env

# Edit .env if needed
nano .env
```

**Common variables in `.env`:**
```bash
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_SESSION_TOKEN=
AWS_REGION=us-east-1
GITHUB_TOKEN=...
GITHUB_REPO=your-org/tech-debt
INSTANCE_TYPE=t2.medium
AWS_PRICING_REGION=us-east-1
KUBECONFIG_PATH=~/.kube/config
TARGET_NAMESPACE=airline
PRICING_CONFIG=sections/04-local-python-agent/config/pricing.yaml
TAGGING_RULES=sections/04-local-python-agent/config/tagging-rules.yaml
BEDROCK_MAX_TOKENS=1024
BEDROCK_TEMPERATURE=0.3
LOG_LEVEL=DEBUG
DRY_RUN=true
USE_MOCK=true
USE_MOCK_GITHUB=true
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
# Create the four service namespaces
kubectl create namespace booking-api
kubectl create namespace flight-search
kubectl create namespace inventory
kubectl create namespace payment

# Deploy all airline services
kubectl apply -k sections/02-airline-app-deployment/manifests/airline-k8-deployment/

# Verify deployments
kubectl get all -n booking-api
kubectl get all -n flight-search
kubectl get all -n inventory
kubectl get all -n payment
```

**Expected output:**
- flight-search-service (missing cost-center, owner)
- booking-api (missing environment, compliance)
- payment-processor (missing tier, application)
- inventory-service (properly tagged - baseline)

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
kubectl delete -k sections/02-airline-app-deployment/manifests/airline-k8-deployment/

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
kubectl apply -f sections/08-k8-native-agent/cronjob/agent-job.yaml

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
sections/
├── 01-cluster-foundation/
│   ├── commands/
│   │   └── setup.sh
│   └── section_goal.md
├── 02-airline-app-deployment/
│   └── manifests/
│       └── airline-k8-deployment/
├── 03-finops-problems/
│   ├── idea.md
│   └── manifests/
│       └── orphaned-resources/
├── 04-local-python-agent/
│   ├── agent/
│   ├── config/
│   └── local-usage.md
├── 05-bedrock-decision-flow/
├── 06-issue-tracker-service/
├── 07-agent-to-tracker-integration/
└── 08-k8-native-agent/
```

## Next Steps

1. Review GitHub issues created by the agent
2. Apply recommended tags to resources
3. Re-run agent to verify fixes
4. Set up scheduled runs (e.g., weekly)

## Support

For issues or questions:
- Check logs with `--log-level DEBUG`
- Review agent code in `sections/04-local-python-agent/agent/`
- Check configuration in `sections/04-local-python-agent/config/`
