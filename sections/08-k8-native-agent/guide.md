# Section 08 Guide: Kubernetes-Native Agent

This is the only file you need for Section 08.

## Goal
Package the Section 05 LLM decision-flow agent as a container, deploy it inside the cluster, and run it on a schedule. Instead of pointing the agent at the cluster from your laptop, the agent now lives inside Kubernetes and uses a service account to read resources directly.

## Tutor note
Section 08 is not about rebuilding the agent logic. The code is the same as Section 05. The learning focus is containerization, Kubernetes RBAC, scheduling, and — most importantly — how to keep the LLM API key out of the container image and out of git by using a Kubernetes Secret.

## What students will learn
- how to containerize the agent from Section 05
- how a pod inside the cluster talks to the Kubernetes API using a service account
- how to create and mount a Kubernetes Secret for the LLM API key
- how to separate secrets (`OPENAI_API_KEY`) from non-secret config (`OPENAI_BASE_URL`, `OPENAI_MODEL_ID`) using a Secret vs. a ConfigMap
- how to run the agent on a schedule with a CronJob
- how to trigger a one-off run with a manual Job

## What you need before starting
Complete Sections 01 through 05 first.

You should already have:
- a working Kind cluster
- the airline app deployed
- Section 05 running locally against the cluster
- a working `.env` file with your OpenAI-compatible API key

## Where the files live
- `sections/08-k8-native-agent/agent/` — same agent code as Section 05
- `sections/08-k8-native-agent/config/` — same tagging policy as Section 05
- `sections/08-k8-native-agent/docker/Dockerfile` — container build
- `sections/08-k8-native-agent/manifests/` — namespace, RBAC, Secret, ConfigMap
- `sections/08-k8-native-agent/cronjob/` — CronJob and manual Job

## Step 1: Confirm Section 05 still works locally
```bash
PYTHONPATH=sections/05-llm-agent-langchain python3 -m agent.main --namespace booking-api
```

What to look for:
- the report prints successfully
- the API key is coming from `.env`
- we are about to move that same key into Kubernetes instead

## Step 2: Look at the Dockerfile
```bash
cat sections/08-k8-native-agent/docker/Dockerfile
```

What to look for:
- it starts from `python:3.12-slim`
- it copies only the agent package and config
- it does **not** copy `.env` or embed any API key
- the image is intentionally small and focused

## Step 3: Build the image
```bash
cd sections/08-k8-native-agent
docker build -f docker/Dockerfile -t finops-agent:latest .
```

What to look for:
- the build completes with no credentials in the layers
- if you are using Kind, load the image into the cluster:
  ```bash
  kind load docker-image finops-agent:latest --name <your-cluster-name>
  ```

## Step 4: Create the namespace and RBAC
```bash
kubectl apply -f sections/08-k8-native-agent/manifests/namespace.yaml
kubectl apply -f sections/08-k8-native-agent/manifests/rbac.yaml
```

What to look for:
- a dedicated `finops-agent` namespace
- a `ServiceAccount` named `finops-agent`
- a `ClusterRole` that only reads Deployments, Services, ConfigMaps, PVCs, Pods, and Namespaces
- a `ClusterRoleBinding` linking the role to the service account

The agent needs these permissions because it scans the same resources Section 05 scanned, but now it does so from inside the cluster.

## Step 5: Create the Kubernetes Secret for the LLM API key
This is the most important step. The API key that lives in `.env` for local runs must become a Kubernetes Secret.

Replace `your-api-key-here` with the real value from your `.env` file:

```bash
kubectl create secret generic finops-agent-llm \
  --namespace finops-agent \
  --from-literal=OPENAI_API_KEY="$(grep '^OPENAI_API_KEY=' .env | cut -d '=' -f2-)"
```

What to look for:
- the Secret is created in the `finops-agent` namespace
- the key name inside the Secret is exactly `OPENAI_API_KEY`
- no key value is written to any file in the repo

> Security note: `manifests/secret.yaml` exists as a placeholder, but it contains a dummy value. For real usage, always create the Secret from the command line, a sealed-secret, or an external-secret operator. Never commit a real key.

Verify the Secret exists (the value is hidden):
```bash
kubectl get secret finops-agent-llm -n finops-agent
```

## Step 6: Apply the ConfigMap for non-secret settings
```bash
kubectl apply -f sections/08-k8-native-agent/manifests/configmap.yaml
```

What to look for:
- `OPENAI_BASE_URL`, `OPENAI_MODEL_ID`, `OPENAI_MAX_TOKENS`, `OPENAI_TEMPERATURE`, and `LOG_LEVEL` live here
- these values are not sensitive, so a ConfigMap is appropriate
- the Secret and ConfigMap are both referenced by the same pod

## Step 7: Inspect the CronJob
```bash
cat sections/08-k8-native-agent/cronjob/cronjob.yaml
```

What to look for:
- `envFrom` pulls all values from the ConfigMap **and** the Secret
- the pod uses `serviceAccountName: finops-agent`
- `image: finops-agent:latest` — update this if you pushed to a real registry
- the default schedule is once per hour

## Step 8: Run the agent once with a manual Job
```bash
kubectl apply -f sections/08-k8-native-agent/cronjob/manual-job.yaml
```

Wait for the job to complete:
```bash
kubectl wait --for=condition=complete job/finops-agent-manual -n finops-agent --timeout=120s
```

Then read the logs:
```bash
kubectl logs -n finops-agent job/finops-agent-manual
```

What to look for:
- logs show the agent connected using in-cluster service account config
- the model ID and OpenAI-compatible base URL are logged
- one LLM call is made per resource
- the final report matches what you saw in Section 05

If the job fails:
- check that the Secret exists and the key is correct: `kubectl describe secret finops-agent-llm -n finops-agent`
- check that the ConfigMap values are correct: `kubectl get configmap finops-agent-config -n finops-agent -o yaml`
- check RBAC: the service account must have permission to list resources cluster-wide

## Step 9: Apply the CronJob
```bash
kubectl apply -f sections/08-k8-native-agent/cronjob/cronjob.yaml
```

What to look for:
- `kubectl get cronjob -n finops-agent` shows `finops-agent`
- the schedule column shows `0 * * * *`
- the next run time is listed

## Step 10: Verify a scheduled run
Trigger an immediate run (optional, for demo purposes):
```bash
kubectl create job --from=cronjob/finops-agent finops-agent-demo-run -n finops-agent
```

Watch the pods and logs:
```bash
kubectl get pods -n finops-agent -w
kubectl logs -n finops-agent job/finops-agent-demo-run
```

What to look for:
- a pod starts from the CronJob template
- it completes and prints the same LLM-powered report
- after completion, the CronJob schedules the next run automatically

## What to notice
- The agent code did not change from Section 05. The only differences are packaging and how config is injected.
- The API key moves from `.env` on disk to a Kubernetes Secret in the cluster.
- The scanner automatically falls back to in-cluster config when no kubeconfig is provided.
- RBAC is intentionally read-only and limited to the resource types the agent scans.
- Secrets and ConfigMaps are separate because they have different security and lifecycle needs.

## Expected outcome
You should be able to explain:
- why the agent can run inside the cluster without a kubeconfig file
- how the service account provides the required API permissions
- how the LLM API key is protected by a Kubernetes Secret
- the difference between a Kubernetes Secret and a ConfigMap
- how a CronJob turns the agent into a scheduled in-cluster workload

## Handoff to Section 09
Section 09 is a standalone simple-agent reference. It is not part of the main teaching flow.

If you want to extend the Kubernetes-native agent next, typical follow-ups are:
- writing the LLM decisions to the issue tracker service from Section 06
- storing reports in object storage or sending them to Slack
- using a `SealedSecret` or External Secrets Operator instead of a plain kubectl-created Secret
