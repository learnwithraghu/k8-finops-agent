# Section 04 Guide: Local Python Agent

This is the only file you need for Section 04.

## Goal
Build and run a simple Python agent that scans Kubernetes resources and checks their FinOps tagging compliance.

## Tutor note
Run the commands one by one. After each step, point out what the learner should notice in the output.

## What students will learn
- how the agent reads cluster resources
- how tagging rules are defined and checked
- how the scanner identifies missing tags and orphaned storage
- how to run the agent locally and interpret the results

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
- required labels like `owner`, `environment`, `cost-center`, `application`, `tier`, and `criticality`
- the label aliases the agent accepts (e.g., `app.kubernetes.io/owner` vs `owner`)
- the namespaces and resource types the scan should care about

## Step 2: Create the virtual environment
```bash
python3 -m venv venv
```

What to look for:
- a local Python environment for the agent
- no changes to the system Python

## Step 3: Activate the virtual environment
```bash
source venv/bin/activate
```

What to look for:
- your shell prompt should switch to the project venv
- all Python installs will now stay local to this repo

## Step 4: Install the Python dependencies
```bash
pip install -r requirements.txt
```

What to look for:
- the Kubernetes and YAML libraries should install cleanly
- this is the one-time setup for local runs

## Step 5: Copy the local environment file
```bash
cp .env.example .env
```

What to look for:
- the agent reads its defaults from `.env`
- the file already points to the local Kind setup

## Step 6: Check Kubernetes access
```bash
kubectl cluster-info
```

What to look for:
- the agent needs a reachable kubeconfig
- if this fails, the scan will fail too

## Step 7: Run the agent across the cluster
```bash
PYTHONPATH=sections/04-local-python-agent python -m agent.main --log-level DEBUG
```

What to look for:
- the agent scans all non-system namespaces by default
- system namespaces are skipped using `excluded_namespaces` from the tagging rules
- the report should show the problems from Section 03
- simple print output shows compliant vs non-compliant resources

## Step 8: Run the agent against one namespace
```bash
PYTHONPATH=sections/04-local-python-agent python -m agent.main --namespace booking-api --log-level DEBUG
```

What to look for:
- the report should shrink to just one namespace
- this is useful for focused demos
- compare the output with the full-cluster run

## Step 9: Try a different namespace
```bash
PYTHONPATH=sections/04-local-python-agent python -m agent.main --namespace inventory --log-level DEBUG
```

What to look for:
- inventory should look cleaner than the other namespaces
- this gives you a good "better baseline" example for the demo

## What the report should show
Look for these sections in the output:
- `FINOPS TAGGING COMPLIANCE REPORT`
- Total resources scanned
- Compliant vs non-compliant counts
- List of compliant resources with their tags
- List of non-compliant resources with missing tags

## What to notice
- the agent can scan local Kubernetes resources without any cloud services
- the simple Python code checks for required tags
- the bad metadata from Section 03 should now be easy to spot in the output
- orphaned PVCs are identified as waste
- the report becomes the basis for understanding FinOps compliance

## Expected outcome
You should be able to run the agent and explain:
- what was scanned
- which resources are properly tagged
- which resources are missing tags
- which PVCs are orphaned
- why proper tagging helps with cost allocation and accountability

## Handoff to Section 05
Once the local scan works, move to:
- `sections/05-bedrock-decision-flow/guide.md`

Section 05 adds the AI decision layer on top of this local scanner.