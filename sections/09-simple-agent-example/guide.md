# Section 09 Guide: Simple Agent Example

> **Not part of the taught course.** This is a standalone reference example kept for
> comparison — it is not covered in the guided sections and is not a prerequisite for
> any other section.

This is the only file you need for Section 09.

## Goal
Build and run the simplest possible FinOps agent using plain functions, environment variables, and a virtual environment.

## What students will do
1. Set up a Python virtual environment
2. Install dependencies inside the virtual environment
3. Review the four agent files (`.env`, `k8_data`, `bedrock_client`, `issue_tracker`)
4. Run the agent end-to-end
5. Verify findings are posted to the issue tracker

## What this section is not
- No classes or dataclasses
- No complex orchestration frameworks
- No Kubernetes deployment of the agent itself
- No advanced prompt engineering

## Prerequisites
- Python 3.10+ installed
- `kubectl` configured and pointing to your cluster
- **AWS credentials configured locally** (see Step 1 below)
- Issue tracker running from Section 06

## AWS Credentials Setup (IMPORTANT)

**DO NOT commit AWS credentials to `.env` or any file in the repo.**

Instead, configure your AWS credentials **locally in your terminal** using one of these methods:

### Option A: Use `aws configure` (Recommended)
```bash
aws configure
```

You will be prompted for:
```
AWS Access Key ID: AKIA<your_key>
AWS Secret Access Key: <your_secret>
Default region name: us-east-1
Default output format: json
```

This creates `~/.aws/credentials` and `~/.aws/config` locally on your machine.

### Option B: Set environment variables in your shell
```bash
export AWS_ACCESS_KEY_ID="AKIA<your_key>"
export AWS_SECRET_ACCESS_KEY="<your_secret>"
export AWS_REGION="us-east-1"
```

Add these to your `~/.bashrc`, `~/.zshrc`, or shell profile to persist them.

### Option C: Temporary environment variables for a single command
```bash
AWS_ACCESS_KEY_ID="AKIA<your_key>" \
AWS_SECRET_ACCESS_KEY="<your_secret>" \
AWS_REGION="us-east-1" \
PYTHONPATH=sections/09-simple-agent-example python -m main
```

### Get Your AWS Credentials
1. Go to [AWS Console](https://console.aws.amazon.com/)
2. IAM → Users → Your User
3. Security Credentials → Create Access Key
4. Copy the Access Key ID and Secret Access Key
5. Make sure your user has permission: `bedrock:InvokeModel`

**The `.env` file in this repo does NOT contain real credentials** (for security). Boto3 will automatically find your credentials from:
- Environment variables (`AWS_ACCESS_KEY_ID`, etc.)
- `~/.aws/credentials` file
- IAM role (if running on AWS)

## Virtual environment setup

Always use a virtual environment. Never install packages into the system Python.

All commands below should be run from the **project root folder** (`/Users/raghunandanask/Desktop/github-repo/k8-finops-agent`).

### 1) Activate the root virtual environment
```bash
source venv/bin/activate
```

All dependencies are already installed in the root `venv/` (see `requirements.txt`). No need to create a local venv for this section.

## Review the agent files

These are the four files that make up the agent. Review each one before running. All configuration comes from the root `.env` file.

### 2) Review the root `.env`
```bash
cat .env
```

This contains the **non-secret** configuration:
- `AWS_REGION`: AWS region for Bedrock (from `.env`)
- `BEDROCK_MODEL_ID`: The Bedrock model ARN (from `.env`)
- `ISSUE_TRACKER_URL`: URL of the issue tracker service (from `.env`)
- `BEDROCK_MAX_TOKENS`: Max tokens for Bedrock response (from `.env`)
- `BEDROCK_TEMPERATURE`: Temperature for model sampling (from `.env`)

**AWS credentials are NOT in `.env`** - they come from your local terminal setup (see AWS Credentials Setup above).

Boto3 will automatically use credentials from:
1. Environment variables you set in your shell
2. `~/.aws/credentials` file (from `aws configure`)
3. IAM role (if running on AWS instances)

### 3) Review `k8_data.py`
```bash
cat sections/09-simple-agent-example/k8_data.py
```

This module fetches Kubernetes pod data. It first tries `kubectl top pods` for live metrics. If the Metrics Server is not available (common in Kind clusters), it automatically falls back to reading resource requests and limits from pod specs.

### 4) Review `bedrock_client.py`
```bash
cat sections/09-simple-agent-example/bedrock_client.py
```

This module sends the pod usage data to AWS Bedrock with a FinOps prompt. It expects a JSON array response with fields: `pod_name`, `namespace`, `issue`, `recommendation`.

### 5) Review `issue_tracker.py`
```bash
cat sections/09-simple-agent-example/issue_tracker.py
```

This module posts each finding as an issue to the tracker service.

### 6) Review `main.py`
```bash
cat sections/09-simple-agent-example/main.py
```

This is the orchestrator:
1. Loads the root `.env` file
2. Calls `get_k8_data()` to fetch Kubernetes pod data (metrics or resource specs)
3. Sends the raw data to Bedrock via `analyze_with_bedrock()`
4. Parses the JSON array of findings from the LLM response
5. Calls `send_to_tracker()` to create one issue per finding

## Run the agent

### 7) Verify the issue tracker is running
```bash
curl http://localhost:8085/issues
```

You should get a JSON array (possibly empty).

### 8) Verify kubectl can access the cluster
```bash
kubectl get pods --all-namespaces
```

You should see pods running across the four app namespaces. If this fails, the agent cannot fetch data.

> **Note:** `kubectl top pods` requires the Metrics Server, which is not installed in this Kind cluster. The agent will automatically fall back to reading resource requests/limits from pod specs if metrics are unavailable.

### 9) Run the agent from repo root

Make sure you're in the repo root, then run:

```bash
PYTHONPATH=sections/09-simple-agent-example python -m main
```

Watch the log output:
- `.env` loading from root
- Kubernetes data fetch (metrics API or fallback to pod specs)
- Bedrock API call
- Response parsing
- Issue tracker posts

**Key points:**
- `PYTHONPATH=sections/09-simple-agent-example` tells Python where to find the agent modules
- `python -m main` runs the main module as a script
- Environment variables are loaded from root `.env` automatically
- The root `venv` is used (activated with `source venv/bin/activate`)

### 10) Verify findings in the issue tracker
```bash
curl http://localhost:8085/issues
```

You should see new issues created by the agent, with titles like `[namespace/pod-name] issue description`.

## What success looks like
You should have:
- a running virtual environment (`.venv/`)
- all dependencies installed inside it
- the agent executed without errors
- one or more issues created in the issue tracker

## End of this example
This section is a standalone reference and does not hand off to another section.
