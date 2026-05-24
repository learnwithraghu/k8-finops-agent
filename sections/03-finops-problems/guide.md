# Section 03 Guide: FinOps Problems

This is the only file you need for Section 03.

## Goal
Show why a large cluster becomes hard to govern: missing tags, inconsistent ownership, and orphaned resources.

## Tutor note
Run the commands one by one. After each command, pause and point out what the learner should notice.

## What students will learn
- how to compare good vs bad Kubernetes metadata
- how missing labels make FinOps and ownership harder
- how to spot orphaned or untracked resources
- why an agent is useful for finding tech debt automatically

## What you need before starting
Complete Sections 01 and 02 first.

You should already have:
- a working Kind cluster
- the airline app deployed
- the five namespaces: `booking-api`, `flight-search`, `inventory`, `payment`, `airline`
- the problem resources (orphaned PVC, untracked ConfigMap) already in the cluster from Section 02

## Where the problem data lives
- Tagging rules: `sections/03-finops-problems/examples/tagging-rules.yaml`

## Step 1: Read the tagging rules
```bash
cat sections/03-finops-problems/examples/tagging-rules.yaml
```

What to look for:
- required tags like `owner`, `environment`, `cost-center`, `application`, `tier`
- the label keys the scanner should accept
- the valid values for environment and cost center

## Step 2: Inspect the booking API deployment
```bash
kubectl get deployment booking-api -n booking-api -o yaml
```

What to look for:
- the `namespace` value
- missing labels like `environment`, `owner`, and `compliance`
- the pod template labels are very minimal

## Step 3: Inspect the booking API service
```bash
kubectl get service booking-api -n booking-api -o yaml
```

What to look for:
- a few labels exist, but not a full tagging standard
- the selector is simple and easy to miss during audits
- this is a good example of partial ownership metadata

## Step 4: Inspect the flight search deployment
```bash
kubectl get deployment flight-search-service -n flight-search -o yaml
```

What to look for:
- missing `cost-center` and `owner`
- the labels are not enough for proper FinOps reporting
- this is a weaker workload than inventory

## Step 5: Inspect the flight search ConfigMap
```bash
kubectl get configmap flight-search-config -n flight-search -o yaml
```

What to look for:
- only a basic app label is present
- ConfigMaps also need ownership metadata
- these are often forgotten in real clusters

## Step 6: Inspect the inventory deployment
```bash
kubectl get deployment inventory-service -n inventory -o yaml
```

What to look for:
- this is the best baseline in the app
- more labels are present than in the other workloads
- it shows what “good enough” looks like for this lesson

## Step 7: Inspect the inventory PVC
```bash
kubectl get pvc inventory-data -n inventory -o yaml
```

What to look for:
- labels match the workload better than other sections
- storage is tied to a clear service owner
- this is the kind of object you want the agent to approve

## Step 8: Inspect the payment deployment
```bash
kubectl get deployment payment-processor -n payment -o yaml
```

What to look for:
- it has some ownership metadata
- it is still missing a full tagging set
- this shows how partial compliance can still be a problem

## Step 9: Inspect the payment PVC
```bash
kubectl get pvc payment-logs -n payment -o yaml
```

What to look for:
- storage exists, but metadata is still incomplete
- it should be easier to trace back to a team
- this is another FinOps gap

## Step 10: Scan deployments for label gaps
```bash
kubectl get deployments -A --show-labels
```

What to look for:
- compare the labels across namespaces
- notice how inconsistent the metadata is
- this is where large clusters become hard to manage

## Step 11: Scan services for label gaps
```bash
kubectl get services -A --show-labels
```

What to look for:
- some services have better labels than others
- service metadata often gets overlooked
- ownership gaps are easier to see across the whole cluster

## Step 12: Scan PVCs
```bash
kubectl get pvc -A
```

What to look for:
- check which claims look owned
- check which claims look suspicious or incomplete
- orphaned storage is a cost problem and an audit problem

## Step 13: Scan ConfigMaps
```bash
kubectl get configmaps -A --show-labels
```

What to look for:
- compare the labels across namespaces
- find the untracked or unlabeled resources
- ConfigMaps are often forgotten, but still matter

## What to notice
- `booking-api` is missing key ownership metadata
- `flight-search` is missing required FinOps labels
- `payment` has partial metadata, but not a full standard
- `inventory` is the closest to a good baseline
- the `airline` PVC has no workload consuming it
- the `default` ConfigMap is untracked and easy to miss

This is the kind of drift an agent should detect and turn into a tech-debt Jira issue later.

## Expected outcome
You should be able to point to:
- one reasonably tagged workload
- one poorly tagged workload
- one orphaned resource
- one untracked resource in the default namespace

## Handoff to Section 04
Once the problem is clear, move to:
- `sections/04-local-python-agent/guide.md`

Section 04 starts building the agent that will find these issues automatically.
