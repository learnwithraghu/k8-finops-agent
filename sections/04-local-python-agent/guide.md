# Section 04 Guide: Local Python Agent

This is the only file you need for Section 04.

## Goal
Build and run a tiny local Python agent that collects raw Kubernetes metadata and dumps it as JSON. This is the bridge between the cluster and the LLM in Section 07.

## Tutor note
Run the commands one by one. After each step, point out what the learner should notice in the output. This section deliberately does **not** decide compliance or draft issues. Those decisions are delegated to the LLM in Section 07.

## What students will learn
- how to read Kubernetes metadata from Python
- why we keep the collector stupid and the decision layer smart
- how to spot missing labels with plain `kubectl` commands
- that having raw metadata is not enough — something has to interpret it

## What you need before starting
Complete Sections 01, 02, and 03 first.

You should already have:
- a working Kind cluster
- the airline app deployed
- the problem resources from Section 03
- Python 3 installed

## Where the agent code lives
- `sections/04-local-python-agent/agent/collect.py`
- `sections/04-local-python-agent/config/tagging-rules.yaml`

## Step 1: Read the tagging rules
```bash
cat sections/04-local-python-agent/config/tagging-rules.yaml
```

What to look for:
- required labels like `owner`, `environment`, `cost-center`, `application`, `tier`, and `criticality`
- the label aliases we will hand to the LLM later (e.g., `app.kubernetes.io/owner` vs `owner`)
- the namespaces the scan should skip (`excluded_namespaces`)

We are not going to enforce these rules in Python. We are just reading the policy file so the collector knows which namespaces to skip.

## Step 2: Look at the collector code
```bash
cat sections/04-local-python-agent/agent/collect.py
```

What to look for:
- it only collects metadata: name, namespace, kind, labels, annotations, plus request/replicas/PVC facts
- it does **not** check tags
- it does **not** calculate cost
- it dumps everything to JSON

This is intentional. The script is a dumb pipe from Kubernetes to the next section.

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
pip install -r sections/04-local-python-agent/requirements.txt
```

What to look for:
- the Kubernetes and YAML libraries should install cleanly
- this is the one-time setup for local runs

## Step 6: Check Kubernetes access
```bash
kubectl cluster-info
```

What to look for:
- the agent needs a reachable kubeconfig
- if this fails, the collection will fail too

## Step 7: Run the collector across the cluster
```bash
PYTHONPATH=sections/04-local-python-agent python -m agent.collect -o k8s_metadata.json
```

What to look for:
- it skips the system namespaces from the tagging rules
- it writes a JSON file named `k8s_metadata.json`
- the output says how many resources it collected

## Step 8: Inspect the raw JSON
```bash
python3 -m json.tool k8s_metadata.json | head -80
```

What to look for:
- every Deployment, Service, ConfigMap, and PVC shows up as a flat object
- the `labels` and `annotations` fields are raw key/value dictionaries
- there is no verdict like `is_compliant` anywhere

## Step 9: Look at one namespace only
```bash
PYTHONPATH=sections/04-local-python-agent python -m agent.collect --namespace booking-api -o booking_api_metadata.json
```

What to look for:
- the JSON file is much smaller
- this is useful for focused demos in Section 07

## Step 10: Use `kubectl` to spot the missing labels
The point of this section is to show that the raw data is messy. Run a few quick checks:

```bash
# All deployments with their labels
kubectl get deployments -A --show-labels
```

```bash
# Which deployments are missing an owner label?
kubectl get deployments -A -o json | jq -r '.items[] | select(.metadata.labels.owner == null) | "\(.metadata.namespace)/\(.metadata.name)"'
```

If `jq` is not installed, use this instead:

```bash
kubectl get deployments -A -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,OWNER:.metadata.labels.owner' | grep '<none>'
```

```bash
# Which services have no cost-center?
kubectl get services -A -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,COST_CENTER:.metadata.labels.cost-center' | grep '<none>'
```

```bash
# Which PVCs are not mounted by any pod?
kubectl get pvc -A -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,STATUS:.status.phase'
```

What to look for:
- you can see the gaps with `kubectl`, but it is tedious
- every command answers one question at a time
- there is no single view that says "here is all the waste and who owns it"

## Step 11: The mapping problem
You now have:
- a JSON file full of Kubernetes metadata
- a YAML file with the FinOps tagging policy
- a cluster full of resources that clearly need owners, cost centers, and cleanup

But the JSON does not say which resource violates which rule. The YAML does not know about the cluster. They are disconnected.

**Pause here and ask the class:**
> "We have all the facts. We have the policy. How do we turn this raw metadata into a decision like 'deployment X is missing owner and cost-center, so create a P1 ticket for the platform team'?"
>
> You could write a giant `if` tree in Python. That is what Section 04 used to do. But every new rule, every new label alias, every edge case becomes another branch. It becomes brittle fast.
>
> A better approach: hand the metadata and the policy to something that can reason about both — a Large Language Model.

This is the handoff to Section 07.

## Expected outcome
You should be able to run the collector and explain:
- what was scanned
- what the JSON file contains
- which labels are missing in the cluster
- why raw metadata alone is not enough
- why the next section adds an LLM to interpret this data

## Handoff to Section 07
Once the collection works, move to:
- `sections/07-llm-structured-agent/guide.md`

Section 07 takes the JSON you just produced, sends each resource plus the tagging policy to an LLM, and lets the LLM decide compliance and draft the fix.
