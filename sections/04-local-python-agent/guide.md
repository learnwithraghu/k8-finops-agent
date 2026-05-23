# Section 04 Guide: Local Python Agent

This is the only file you need for Section 04.

## Goal
Build and run the first local Python agent that scans Kubernetes resources and produces a FinOps report.

## Tutor note
Run the commands one by one. After each step, point out what the learner should notice in the output.

## What students will learn
- how the agent reads cluster resources
- how tagging rules and pricing inputs affect the report
- how the scanner spots missing tags and orphaned storage
- how to run the agent locally before any AI or tracker integration

## What you need before starting
Complete Sections 01, 02, and 03 first.

You should already have:
- a working Kind cluster
- the airline app deployed
- the problem resources from Section 03
- Python 3 installed

## Where the agent code lives
- `sections/04-local-python-agent/agent/`
- `sections/04-local-python-agent/config/`

## Step 1: Read the tagging rules
```bash
cat sections/04-local-python-agent/config/tagging-rules.yaml
```

What to look for:
- required labels like `owner`, `environment`, `cost-center`, `application`, and `tier`
- the label aliases the agent accepts
- the namespaces and resource types the scan should care about

## Step 2: Read the pricing file
```bash
cat sections/04-local-python-agent/config/pricing.yaml
```

What to look for:
- the example EC2 cost basis
- the storage pricing
- the thresholds that influence “high impact” violations

## Step 3: Create the virtual environment
```bash
python3 -m venv venv
```

What to look for:
- a local Python environment for the agent
- no changes to the system Python

## Step 4: Activate the virtual environment
```bash
source venv/bin/activate
```

What to look for:
- your shell prompt should switch to the project venv
- all Python installs will now stay local to this repo

## Step 5: Install the Python dependencies
```bash
pip install -r requirements.txt
```

What to look for:
- the Kubernetes, YAML, AWS, and GitHub libraries should install cleanly
- this is the one-time setup for local runs

## Step 6: Copy the local environment file
```bash
cp .env.example .env
```

What to look for:
- the agent reads its defaults from `.env`
- the file already points to the local Kind setup and mock mode

## Step 7: Check Kubernetes access
```bash
kubectl cluster-info
```

What to look for:
- the agent needs a reachable kubeconfig
- if this fails, the scan will fail too

## Step 8: Run the agent across the cluster
```bash
PYTHONPATH=sections/04-local-python-agent python -m agent.main --mock --log-level DEBUG
```

What to look for:
- the agent scans all non-system namespaces by default
- system namespaces are skipped using `excluded_namespaces` from the tagging rules
- the report should show the problems from Section 03
- no issue tracker is involved yet

## Step 9: Run the agent against one namespace
```bash
PYTHONPATH=sections/04-local-python-agent python -m agent.main --mock --namespace booking-api --log-level DEBUG
```

What to look for:
- the report should shrink to just one namespace
- this is useful for focused demos
- compare the output with the full-cluster run

## Step 10: Try a different namespace
```bash
PYTHONPATH=sections/04-local-python-agent python -m agent.main --mock --namespace inventory --log-level DEBUG
```

What to look for:
- inventory should look cleaner than the other namespaces
- this gives you a good “better baseline” example for the demo

## Step 11: Raise the threshold for high-impact findings
```bash
PYTHONPATH=sections/04-local-python-agent python -m agent.main --mock --threshold 20 --log-level DEBUG
```
What to look for:
- fewer findings should qualify as high impact
- this shows how tuning changes the output
- useful when demonstrating why some issues become tracker items first

## What the report should show
Look for these sections in the output:
- `FinOps Analysis Report`
- `Cost Summary`
- `Breakdown by Category`
- `Violations Found`

## What to notice
- the agent can scan local Kubernetes resources without Bedrock
- mock mode still produces a realistic report
- the bad metadata from Section 03 should now be easy to spot in machine output
- orphaned PVCs should be treated as waste
- the report becomes the basis for the next section’s decision flow

## Expected outcome
You should be able to run the agent and explain:
- what was scanned
- what was untracked
- what looks orphaned
- why the output is useful for a FinOps review

## Handoff to Section 05
Once the local scan works, move to:
- `sections/05-bedrock-decision-flow/guide.md`

Section 05 adds the AI decision layer on top of this local scanner.
