# K8s FinOps Agent - Helm Chart

## Overview
This Helm chart deploys the K8s FinOps Agent as a scheduled CronJob that scans Kubernetes resources for tagging compliance using an LLM-powered analysis engine.

## Prerequisites
- Kubernetes 1.23+
- Helm 3.8+
- Kind cluster (for local testing) or any Kubernetes cluster
- OpenAI-compatible API key
- Locally built image: `finops-agent:latest`

## Installation

### 1. Build and load the image
```bash
cd sections/08-k8-native-agent
docker build -f docker/Dockerfile -t finops-agent:latest .
kind load docker-image finops-agent:latest --name <your-cluster-name>
```

### 2. Create the LLM API key secret
The secret must be created **before** installing the Helm chart:

```bash
# Create the namespace first
kubectl create namespace finops-agent

# Create the secret
kubectl create secret generic finops-agent-llm \
  --namespace finops-agent \
  --from-literal=OPENAI_API_KEY="your-api-key-here"
```

**Security Note:** Never commit the API key to git. The secret is managed externally from Helm for security best practices.

### 3. Install the chart
```bash
helm install finops-agent ./helm
```

### 4. Verify installation
```bash
helm test finops-agent
```

## Configuration

### Key Values

| Parameter | Description | Default |
|-----------|-------------|---------|
| `namespace.name` | Namespace for agent deployment | `finops-agent` |
| `image.repository` | Image repository | `finops-agent` |
| `image.tag` | Image tag | `latest` |
| `image.pullPolicy` | Image pull policy | `Never` |
| `schedule` | CronJob schedule (cron syntax) | `0 * * * *` (hourly) |
| `concurrencyPolicy` | CronJob concurrency policy | `Forbid` |
| `successfulJobsHistoryLimit` | Number of successful jobs to keep | `3` |
| `failedJobsHistoryLimit` | Number of failed jobs to keep | `3` |
| `resources.requests.cpu` | CPU request | `100m` |
| `resources.requests.memory` | Memory request | `128Mi` |
| `resources.limits.cpu` | CPU limit | `500m` |
| `resources.limits.memory` | Memory limit | `512Mi` |
| `llm.baseUrl` | OpenAI-compatible endpoint URL | `https://api.ai.kodekloud.com/v1` |
| `llm.modelId` | LLM model ID | `gpt-4o` |
| `llm.maxTokens` | Maximum tokens per request | `1024` |
| `llm.temperature` | LLM temperature setting | `0.3` |
| `logLevel` | Logging level | `INFO` |
| `secretName` | Name of secret containing API key | `finops-agent-llm` |
| `targetNamespace` | Limit scan to specific namespace (optional) | `""` (all namespaces) |
| `rbac.create` | Create RBAC resources | `true` |
| `rbac.serviceAccountName` | ServiceAccount name | `finops-agent` |

### Customizing Tagging Rules

The tagging rules are embedded in `values.yaml` under the `taggingRules` section. To customize:

1. Edit `values.yaml`:
```yaml
taggingRules:
  required_tags:
    - owner
    - environment
    - my-custom-tag  # Add your custom tag
  # ... more configuration
```

2. Upgrade the deployment:
```bash
helm upgrade finops-agent ./helm
```

You can also create a custom values file:
```bash
cat > custom-values.yaml <<EOF
taggingRules:
  required_tags:
    - owner
    - environment
    - cost-center
    - application
    - tier
    - compliance  # Add compliance as required
EOF

helm upgrade finops-agent ./helm -f custom-values.yaml
```

## Usage

### Run a manual scan
```bash
kubectl create job --from=cronjob/k8-finops-agent manual-scan -n finops-agent
kubectl logs -n finops-agent job/manual-scan -f
```

### View scheduled runs
```bash
kubectl get jobs -n finops-agent --watch
```

### Change schedule frequency
```bash
# Every 30 minutes
helm upgrade finops-agent ./helm --set schedule="*/30 * * * *"

# Every 6 hours
helm upgrade finops-agent ./helm --set schedule="0 */6 * * *"
```

### Scan only specific namespace
```bash
helm upgrade finops-agent ./helm --set targetNamespace="booking-api"
```

### View CronJob details
```bash
kubectl get cronjob -n finops-agent
kubectl describe cronjob k8-finops-agent -n finops-agent
```

### View logs from completed jobs
```bash
# View most recent job
kubectl logs -n finops-agent -l app.kubernetes.io/name=k8-finops-agent --tail=100

# View specific job
kubectl logs -n finops-agent job/<job-name>
```

## Troubleshooting

### Jobs fail with "Unauthorized" errors
**Symptom:** Pods fail with 401 authentication errors in logs

**Solution:**
- Verify the secret exists: `kubectl get secret finops-agent-llm -n finops-agent`
- Check the API key is correct
- Recreate the secret:
  ```bash
  kubectl delete secret finops-agent-llm -n finops-agent
  kubectl create secret generic finops-agent-llm \
    --namespace finops-agent \
    --from-literal=OPENAI_API_KEY="your-correct-key"
  ```

### RBAC permission errors
**Symptom:** Logs show "Forbidden" errors when accessing Kubernetes resources

**Solution:**
- Verify ClusterRole and ClusterRoleBinding were created:
  ```bash
  kubectl get clusterrole | grep finops
  kubectl get clusterrolebinding | grep finops
  ```
- Check service account permissions:
  ```bash
  kubectl auth can-i list deployments --as=system:serviceaccount:finops-agent:finops-agent
  kubectl auth can-i list namespaces --as=system:serviceaccount:finops-agent:finops-agent
  ```

### Image pull errors
**Symptom:** Pods show `ImagePullBackOff` or `ErrImagePull` status

**Solution:**
- Confirm image exists locally: `docker images | grep finops-agent`
- Ensure Kind loaded the image:
  ```bash
  docker exec <kind-node-name> crictl images | grep finops-agent
  ```
- Verify `imagePullPolicy: Never` in values.yaml
- Reload image into Kind if needed:
  ```bash
  kind load docker-image finops-agent:latest --name <your-cluster-name>
  ```

### No jobs are being created
**Symptom:** CronJob exists but no jobs appear

**Solution:**
- Check CronJob exists: `kubectl get cronjob -n finops-agent`
- Verify schedule syntax is valid (cron format)
- Check CronJob is not suspended:
  ```bash
  kubectl get cronjob k8-finops-agent -n finops-agent -o jsonpath='{.spec.suspend}'
  ```
- Review CronJob events:
  ```bash
  kubectl describe cronjob k8-finops-agent -n finops-agent
  ```

### ConfigMap not mounted correctly
**Symptom:** Agent logs show "File not found" for tagging-rules.yaml

**Solution:**
- Verify ConfigMap exists:
  ```bash
  kubectl get configmap -n finops-agent
  kubectl get configmap k8-finops-agent-tagging-rules -n finops-agent -o yaml
  ```
- Check volume mount in pod spec:
  ```bash
  kubectl describe cronjob k8-finops-agent -n finops-agent
  ```

### Test hook fails
**Symptom:** `helm test` command fails

**Solution:**
- View test pod logs:
  ```bash
  kubectl logs -n finops-agent k8-finops-agent-test
  ```
- Check test pod events:
  ```bash
  kubectl describe pod k8-finops-agent-test -n finops-agent
  ```
- Ensure secret and ConfigMaps exist before running test

## Upgrading the Chart

```bash
# Upgrade with same values
helm upgrade finops-agent ./helm

# Upgrade with custom values file
helm upgrade finops-agent ./helm -f custom-values.yaml

# Upgrade with inline value overrides
helm upgrade finops-agent ./helm --set schedule="*/15 * * * *"
```

### View upgrade history
```bash
helm history finops-agent
```

### Rollback to previous version
```bash
# Rollback to previous revision
helm rollback finops-agent

# Rollback to specific revision
helm rollback finops-agent 2
```

## Uninstallation

```bash
# Remove Helm release (keeps namespace and secrets)
helm uninstall finops-agent

# Clean up namespace and secrets
kubectl delete namespace finops-agent
```

**Note:** The namespace-scoped secret will be deleted with the namespace, but ClusterRole and ClusterRoleBinding are removed by Helm.

## Development

### Lint the chart
```bash
helm lint ./helm
```

### Template rendering (dry-run)
```bash
helm template finops-agent ./helm --debug
```

### Validate generated manifests
```bash
helm template finops-agent ./helm | kubectl apply --dry-run=client -f -
```

## License
Apache 2.0
