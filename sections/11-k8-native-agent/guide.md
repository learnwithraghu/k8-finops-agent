# Section 11 Guide: Helm-Based Deployment

This is the only file you need for Section 11.

## Goal
Package the Section 08 LLM-powered FinOps agent as a Helm chart and deploy it inside Kubernetes as a scheduled CronJob. Instead of managing raw Kubernetes manifests, use Helm for templating, versioning, and lifecycle management, so the FinOps scan runs in-cluster with professional packaging.

## Tutor note
Section 11 is not about rebuilding the agent logic. The code is the same as Section 08. The learning focus is:
- Helm chart structure and templating
- Kubernetes packaging best practices
- Configuration management (ConfigMaps vs Secrets)
- Helm lifecycle operations (install, test, upgrade, rollback)
- How to embed application config files as Helm values

## What you will learn
- How to create a Helm chart from scratch
- How to template Kubernetes manifests with Go templates
- How to separate configuration (ConfigMaps) from secrets
- How to embed application config files (tagging-rules.yaml) as ConfigMap values
- How to use Helm test hooks for deployment validation
- How to manage application lifecycle with Helm commands
- How to customize deployments via values.yaml
- How to document Helm charts with NOTES.txt and README
- Why Helm is better than raw manifests for Kubernetes applications

## What you need before starting
Complete Sections 01 through 08 first.

You should already have:
- a working Kind cluster
- the airline app deployed (from Section 01)
- Section 08 running locally against the cluster
- a working `.env` file with your OpenAI-compatible API key
- Helm 3.x installed (`helm version`)
- Docker installed for building images

## Where the files live
- `sections/11-k8-native-agent/agent/` — same agent code as Section 08
- `sections/11-k8-native-agent/config/` — reference tagging policy
- `sections/11-k8-native-agent/docker/Dockerfile` — container build
- `sections/11-k8-native-agent/helm/` — **NEW: Helm chart**
  - `Chart.yaml` — chart metadata
  - `values.yaml` — default configuration values
  - `templates/` — templated Kubernetes manifests
  - `README.md` — chart documentation

The old `manifests/` and `cronjob/` directories are now replaced by the Helm chart.

## Step 1: Confirm Section 08 still works locally

Before containerizing, verify the agent still works from your laptop:

```bash
PYTHONPATH=sections/11-k8-native-agent python3 -m agent.main
```

What to look for:
- the report prints successfully
- the API key is coming from `.env`
- you see LLM calls being made for each resource
- the report shows tagging compliance results

We are about to move that same agent code into a container and deploy it with Helm.

## Step 2: Review the Helm chart structure

Let's explore the Helm chart before deploying:

```bash
tree sections/11-k8-native-agent/helm/
```

What to look for:
- `Chart.yaml` - chart metadata (name, version, description)
- `values.yaml` - default configuration values
- `templates/` directory - templated Kubernetes manifests
- `templates/_helpers.tpl` - reusable template functions
- `templates/NOTES.txt` - post-install instructions
- `.helmignore` - files to exclude from chart package
- `README.md` - chart documentation

Inspect the Chart.yaml:

```bash
cat sections/11-k8-native-agent/helm/Chart.yaml
```

What to notice:
- Chart version: `0.1.0` (tracks the chart itself, not the app)
- App version: `1.0.0` (tracks the agent application version)
- Type: `application` (not a library chart)
- Keywords and maintainers for discoverability

## Step 3: Review values.yaml and embedded tagging rules

Open the values file:

```bash
cat sections/11-k8-native-agent/helm/values.yaml
```

What to look for:
- `namespace.name` defines where the agent deploys (`finops-agent`)
- `image` configuration with `pullPolicy: Never` for local images
- `schedule` controls CronJob frequency (default: `0 * * * *` = every hour)
- `resources` define CPU and memory requests/limits
- `llm` section contains non-sensitive OpenAI config
- `secretName` references the externally-created secret
- `taggingRules` section embeds the entire tagging policy from Section 08

Compare the embedded tagging rules with the original:

```bash
# View just the tagging rules from values.yaml
yq '.taggingRules' sections/11-k8-native-agent/helm/values.yaml

# Compare with the original from Section 08
cat sections/08-llm-agent-langchain/config/tagging-rules.yaml
```

What to notice:
- The tagging policy is now part of the Helm chart configuration
- Users can customize tagging rules by editing `values.yaml`
- This config gets mounted as a ConfigMap at `/app/config` in the pod
- No need to rebuild the image when tagging rules change

## Step 4: Inspect Helm templates

Look at how raw manifests become templates. Compare the old manifest with the new template:

```bash
# Original namespace manifest
cat sections/11-k8-native-agent/manifests/namespace.yaml

# Templated namespace
cat sections/11-k8-native-agent/helm/templates/namespace.yaml
```

What to notice:
- `{{ .Values.namespace.name }}` replaces hardcoded values
- `{{- include "k8-finops-agent.labels" . | nindent 4 }}` adds common labels
- `{{- toYaml .Values.namespace.labels | nindent 4 }}` preserves YAML structure
- Templates are reusable and customizable via values.yaml

Preview what Helm will deploy without actually installing:

```bash
helm template finops-agent sections/11-k8-native-agent/helm/
```

What to look for:
- All templates rendered with values from `values.yaml`
- Namespace, RBAC, ConfigMaps, CronJob all generated
- Template functions like `{{ include }}` and `{{ toYaml }}` in action
- Final manifests are valid Kubernetes YAML

You can also render to a file for closer inspection:

```bash
helm template finops-agent sections/11-k8-native-agent/helm/ > /tmp/rendered-manifests.yaml
cat /tmp/rendered-manifests.yaml
```

## Step 5: Build the Docker image

Now build the container image locally:

```bash
cd sections/11-k8-native-agent
docker build -f docker/Dockerfile -t finops-agent:latest .
```

What to look for:
- Build completes successfully
- No credentials are copied into the image (no `.env` file)
- The image includes only `agent/` code and a placeholder `config/` directory
- Final image size should be reasonable (Python 3.12 slim base)

Verify the image exists:

```bash
docker images | grep finops-agent
```

What to notice:
- Image is tagged as `finops-agent:latest`
- This tag matches `image.repository` and `image.tag` in `values.yaml`

## Step 6: Load image into Kind cluster

Make the image available inside your Kind cluster:

```bash
kind load docker-image finops-agent:latest --name <your-cluster-name>
```

Replace `<your-cluster-name>` with your actual Kind cluster name. If you don't remember it:

```bash
kind get clusters
```

What to look for:
- Command completes with "Image loaded successfully"
- This makes the image available to the cluster with `imagePullPolicy: Never`

Verify the image is available inside the cluster:

```bash
docker exec <kind-node-name> crictl images | grep finops-agent
```

To find your Kind node name:

```bash
docker ps | grep kindest
```

What to notice:
- The image is now available inside the Kind cluster
- `imagePullPolicy: Never` tells Kubernetes to use this local image
- No remote registry needed for local development

## Step 7: Lint the Helm chart

Before installing, validate the chart structure:

```bash
helm lint sections/11-k8-native-agent/helm/
```

What to look for:
- Output shows "1 chart(s) linted, 0 chart(s) failed"
- No errors or warnings
- If there are issues, fix them before proceeding

You can also validate that the rendered manifests are valid Kubernetes resources:

```bash
helm template finops-agent sections/11-k8-native-agent/helm/ | kubectl apply --dry-run=client -f -
```

What to notice:
- `--dry-run=client` validates without actually creating resources
- Any RBAC or schema errors will be caught here

## Step 8: Create the LLM API key secret

**CRITICAL:** The secret must be created BEFORE installing the Helm chart.

First, create the namespace:

```bash
kubectl create namespace finops-agent
```

Then create the secret from your `.env` file:

```bash
kubectl create secret generic finops-agent-llm \
  --namespace finops-agent \
  --from-literal=OPENAI_API_KEY="$(grep '^OPENAI_API_KEY=' .env | cut -d '=' -f2-)"
```

Or if you want to enter the key manually:

```bash
kubectl create secret generic finops-agent-llm \
  --namespace finops-agent \
  --from-literal=OPENAI_API_KEY="your-api-key-here"
```

Verify the secret exists:

```bash
kubectl get secret finops-agent-llm -n finops-agent
```

What to notice:
- The secret name matches `secretName` in `values.yaml`
- The key inside the secret is `OPENAI_API_KEY` (must match what the agent expects)
- The secret is NOT managed by Helm (security best practice)
- If you forget this step, jobs will fail with authentication errors

View secret details (value is base64 encoded and not shown):

```bash
kubectl describe secret finops-agent-llm -n finops-agent
```

## Step 9: Install the Helm chart

Now install the chart:

```bash
helm install finops-agent sections/11-k8-native-agent/helm/
```

What to look for:
- Installation succeeds with "STATUS: deployed"
- Helm prints the NOTES.txt content with next steps
- Resources are created in the `finops-agent` namespace

The output should show:
```
✅ K8s FinOps Agent has been deployed successfully!
```

Verify the installation:

```bash
helm list
```

What to notice:
- Shows the release name `finops-agent`
- Namespace is `finops-agent`
- Chart version is `0.1.0`
- Status is `deployed`

Get more details:

```bash
helm status finops-agent
```

Check all deployed resources:

```bash
kubectl get all -n finops-agent
kubectl get configmap -n finops-agent
kubectl get clusterrole,clusterrolebinding | grep finops
```

What to notice:
- Job `k8-finops-agent` is created and completed successfully
- ServiceAccount `finops-agent` exists
- ClusterRole and ClusterRoleBinding for RBAC are created
- Two ConfigMaps: one for LLM config, one for tagging rules
- The Job runs once and exits after the scan completes

## Step 10: Verify the Job run

Inspect the Job:

```bash
kubectl get job -n finops-agent
```

What to look for:
- The Job name is `finops-agent`
- `COMPLETIONS` should show `1` and `DURATION` should be non-empty after completion
- `AGE` shows how long ago the Job was created

Get more details:

```bash
kubectl describe job finops-agent -n finops-agent
```

What to notice:
- The Job uses the `finops-agent` service account
- The Job pod is created with the expected container and volume mount
- Any pod-level errors are visible under Events

## Step 11: Run Helm test for validation

Use Helm's built-in test feature to validate the deployment immediately:

```bash
helm test finops-agent
```

What to look for:
- A test pod is created and runs immediately
- Test passes if the pod completes successfully (exit code 0)
- You see "Phase: Succeeded" in the output

The test creates a pod with the Helm test hook annotation that runs the agent once.

View the test results:

```bash
kubectl logs -n finops-agent k8-finops-agent-test
```

What to look for:
- Logs show the agent connected using in-cluster service account config
- No kubeconfig file needed (uses service account token)
- Model ID and base URL are logged from ConfigMap
- One LLM call per resource scanned
- Final report with compliance summary:
  - Total resources scanned
  - Compliant vs non-compliant counts
  - Missing tags breakdown
- The report matches what you saw in Section 08

Example expected output:
```
🔍 FinOps Tagging Compliance Report (LLM-Powered)
================================================

📊 Summary:
- Total Resources Scanned: 15
- Compliant: 3
- Non-Compliant: 12
- Compliance Rate: 20%

⚠️ Non-Compliant Resources:
...
```

If the test fails, check:

```bash
# View test pod status
kubectl get pod k8-finops-agent-test -n finops-agent

# View test pod events
kubectl describe pod k8-finops-agent-test -n finops-agent

# Common issues:
# - Secret not found: verify secret exists
# - RBAC errors: check ClusterRole and ClusterRoleBinding
# - Image pull errors: verify image was loaded into Kind
# - LLM auth errors: check API key in secret
```

## Step 12: Re-run the Job manually

If you want to run another scan, delete the finished Job and upgrade the release so Helm recreates it:

```bash
kubectl delete job finops-agent -n finops-agent || true
helm upgrade finops-agent sections/11-k8-native-agent/helm/ --reuse-values
```

Then view the renewed Job:

```bash
kubectl get job -n finops-agent
kubectl logs -n finops-agent job/finops-agent
```

## Step 13: Customize tagging rules via Helm

Let's add `compliance` as a required tag. Create a custom values file:

Let's add `compliance` as a required tag. Create a custom values file:

```bash
cat > /tmp/custom-values.yaml <<EOF
taggingRules:
  required_tags:
    - owner
    - environment
    - cost-center
    - application
    - tier
    - compliance  # NEW: Add compliance as required
  label_mappings:
    owner:
      - app.kubernetes.io/owner
      - owner
    environment:
      - app.kubernetes.io/env
      - environment
      - env
    cost-center:
      - app.kubernetes.io/cost-center
      - cost-center
      - costcenter
    application:
      - app.kubernetes.io/name
      - app
      - application
    tier:
      - app.kubernetes.io/tier
      - tier
    compliance:
      - compliance-level
      - compliance
  cost_centers:
    - booking-engine
    - payment
    - inventory
    - customer-service
    - analytics
    - platform
  environments:
    - dev
    - staging
    - prod
  tiers:
    - frontend
    - backend
    - database
    - cache
    - messaging
  compliance_levels:
    - pci-dss
    - sox
    - standard
  resource_types:
    - Deployment
    - Service
    - ConfigMap
    - PersistentVolumeClaim
    - Ingress
    - Pod
  excluded_namespaces:
    - kube-system
    - kube-public
    - kube-node-lease
    - local-path-storage
EOF
```

Upgrade with new tagging rules:

```bash
helm upgrade finops-agent sections/11-k8-native-agent/helm/ -f /tmp/custom-values.yaml
```

Verify the ConfigMap was updated:

```bash
kubectl get configmap k8-finops-agent-tagging-rules -n finops-agent -o yaml
```

What to look for:
- The `tagging-rules.yaml` data now includes `compliance` in `required_tags`
- The LLM will now enforce the `compliance` tag on all resources

Trigger a new scan to test the updated rules:

```bash
kubectl create job --from=cronjob/k8-finops-agent test-compliance -n finops-agent
kubectl logs -n finops-agent job/test-compliance -f
```

What to notice:
- Tagging policy changes don't require rebuilding the image
- ConfigMap updates are picked up by new job pods
- The LLM now enforces the `compliance` tag
- More resources will be flagged as non-compliant
- This demonstrates configuration-as-code with Helm

## Step 15: Scan only a specific namespace

Let's limit the scan to only the `booking-api` namespace:

```bash
helm upgrade finops-agent sections/11-k8-native-agent/helm/ --set targetNamespace="booking-api"
```

Trigger a scan:

```bash
kubectl create job --from=cronjob/k8-finops-agent scan-booking -n finops-agent
kubectl logs -n finops-agent job/scan-booking -f
```

What to notice:
- The agent only scans resources in `booking-api` namespace
- Faster execution since fewer resources are scanned
- Useful for targeted compliance checks
- The `TARGET_NAMESPACE` env var is set in the pod

To go back to scanning all namespaces:

```bash
helm upgrade finops-agent sections/11-k8-native-agent/helm/ --set targetNamespace=""
```

## Step 16: View Helm history and rollback

View all revisions of the release:

```bash
helm history finops-agent
```

What to look for:
- Each `helm upgrade` creates a new revision
- Revision numbers increment (1, 2, 3, ...)
- Description shows what changed
- Status shows "deployed" for current revision

If you want to rollback to the previous configuration:

```bash
helm rollback finops-agent
```

Or rollback to a specific revision:

```bash
helm rollback finops-agent 2
```

Verify the rollback:

```bash
helm history finops-agent
kubectl describe cronjob k8-finops-agent -n finops-agent
```

What to notice:
- Helm tracks all configuration changes
- Rollback restores previous values
- No need to manually remember old configuration
- This is a key benefit of Helm over raw manifests

## Step 17: Increase resources for the agent

If the agent needs more memory or CPU, adjust via Helm:

```bash
helm upgrade finops-agent sections/11-k8-native-agent/helm/ \
  --set resources.requests.memory="256Mi" \
  --set resources.limits.memory="1Gi"
```

Verify the change:

```bash
kubectl describe cronjob k8-finops-agent -n finops-agent | grep -A 4 Resources
```

Trigger a job to test:

```bash
kubectl create job --from=cronjob/k8-finops-agent test-resources -n finops-agent
kubectl get pod -n finops-agent -l job-name=test-resources
```

What to notice:
- New pods use the updated resource limits
- Existing jobs are not affected
- Helm makes resource tuning easy

## What to notice

- **Agent code unchanged:** The same agent from Section 08 runs in-cluster
- **Helm replaces raw manifests:** All YAML files are now templated and versioned
- **Configuration as code:** Tagging rules are part of `values.yaml`, not baked into the image
- **Secret management:** API key is external to Helm for security
- **Lifecycle management:** install, upgrade, rollback, test - all standardized
- **Customization:** Change schedule, resources, namespace scope without editing templates
- **Testing:** `helm test` validates deployment automatically
- **Documentation:** NOTES.txt guides users after installation
- **In-cluster execution:** Agent uses service account, no kubeconfig needed
- **ConfigMap mounting:** Tagging rules are mounted as a file, not environment variables
- **RBAC:** Read-only ClusterRole limits blast radius

## Expected outcome

You should be able to explain:
- Why Helm is better than raw Kubernetes manifests for application deployment
- How Helm templates work and how to use `values.yaml`
- The difference between ConfigMaps (non-sensitive config) and Secrets (API keys)
- How to embed application config files (tagging-rules.yaml) as ConfigMap values
- How to use Helm lifecycle commands (install, upgrade, rollback, test)
- How to customize a Helm deployment without modifying templates
- Why the agent can run inside the cluster without a kubeconfig file (in-cluster config + service account)
- How CronJobs schedule recurring workloads
- The security benefits of external secret management

## Troubleshooting

### Jobs fail with "Unauthorized" errors
**Symptom:** Pods fail with 401 authentication errors in logs

**Check:**
```bash
kubectl get secret finops-agent-llm -n finops-agent
kubectl describe secret finops-agent-llm -n finops-agent
```

**Fix:**
```bash
kubectl delete secret finops-agent-llm -n finops-agent
kubectl create secret generic finops-agent-llm \
  --namespace finops-agent \
  --from-literal=OPENAI_API_KEY="your-correct-key"
```

### RBAC permission errors
**Symptom:** Logs show "Forbidden" errors when accessing Kubernetes resources

**Check:**
```bash
kubectl auth can-i list deployments --as=system:serviceaccount:finops-agent:finops-agent
kubectl auth can-i list namespaces --as=system:serviceaccount:finops-agent:finops-agent
```

**Fix:**
```bash
# Verify RBAC resources exist
kubectl get clusterrole | grep finops
kubectl get clusterrolebinding | grep finops

# If missing, reinstall the chart
helm uninstall finops-agent
helm install finops-agent sections/11-k8-native-agent/helm/
```

### Image pull errors
**Symptom:** Pods show `ImagePullBackOff` or `ErrImagePull` status

**Check:**
```bash
docker images | grep finops-agent
kubectl describe pod -n finops-agent -l app.kubernetes.io/name=k8-finops-agent
```

**Fix:**
```bash
# Rebuild and reload image
cd sections/11-k8-native-agent
docker build -f docker/Dockerfile -t finops-agent:latest .
kind load docker-image finops-agent:latest --name <your-cluster-name>

# Trigger a new job to test
kubectl create job --from=cronjob/k8-finops-agent test-image -n finops-agent
```

### No jobs are being created
**Symptom:** CronJob exists but no jobs appear

**Check:**
```bash
kubectl get cronjob k8-finops-agent -n finops-agent
kubectl describe cronjob k8-finops-agent -n finops-agent
```

**Verify:**
- Schedule syntax is valid (use https://crontab.guru)
- CronJob is not suspended
- Time until next run is reasonable

**Fix:**
```bash
# Trigger manual job to test
kubectl create job --from=cronjob/k8-finops-agent manual-test -n finops-agent
```

### ConfigMap not mounted correctly
**Symptom:** Agent logs show "File not found" for tagging-rules.yaml

**Check:**
```bash
kubectl get configmap -n finops-agent
kubectl get configmap k8-finops-agent-tagging-rules -n finops-agent -o yaml
```

**Fix:**
```bash
# Verify volume mount in job
kubectl describe cronjob k8-finops-agent -n finops-agent | grep -A 10 Volumes
```

## Handoff

The main linear track ends here. Related tracks you may want next:
- Section 05 — curl-validated prebuilt MCP setup for the local cluster (now also the entry point for the MCP agent track)
- Sections 06 and 07 — the MCP data agent and LLM structured agent track
- Integrating with the issue tracker service from Sections 09/10

If you want to extend the Helm deployment next, typical follow-ups are:
- Adding persistent storage for reports (mount PVC, upload to S3)
- Using SealedSecrets or External Secrets Operator for production secret management
- Deploying to a production cluster (EKS, GKE, AKS) with a real container registry
- Adding Prometheus metrics and Grafana dashboards
- Setting up alerts for failed jobs or compliance thresholds
- Creating a CI/CD pipeline to build and deploy the chart automatically
