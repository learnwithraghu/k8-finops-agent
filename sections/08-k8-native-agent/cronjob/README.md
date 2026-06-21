# Legacy CronJob Manifests (Pre-Helm)

⚠️ **Note:** These CronJob manifests have been replaced by the Helm chart in `../helm/`.

These files are kept for reference but are no longer the recommended deployment method.
Please use the Helm chart for Section 08 deployment.

## Migration to Helm

The Helm chart includes several improvements over raw CronJob manifests:

### Benefits of Helm Chart Approach
- **Templated CronJob:** Customize schedule, resources, and other settings via `values.yaml`
- **Helm test hook:** The `manual-job.yaml` functionality is now provided by `helm test` command
- **Configuration management:** Tagging rules mounted as ConfigMap from values, not from separate files
- **Validation:** Built-in testing and validation with `helm test`
- **Lifecycle management:** Easy schedule changes, rollbacks, and upgrades

### What Changed

| Raw Manifest | Helm Template | Key Improvements |
|--------------|---------------|------------------|
| `cronjob.yaml` | `templates/cronjob.yaml` | Fully templated with schedule, resources, namespace filtering all configurable |
| `manual-job.yaml` | `templates/test-job.yaml` | Replaced by Helm test hook; run with `helm test` command |

### How to Use with Helm

Instead of:
```bash
kubectl apply -f cronjob.yaml
kubectl create job --from=cronjob/finops-agent finops-agent-demo-run -n finops-agent
kubectl logs -n finops-agent job/finops-agent-demo-run
```

Use:
```bash
# Install with Helm
helm install finops-agent ../helm/

# Test deployment (replaces manual-job.yaml)
helm test finops-agent

# View test results
kubectl logs -n finops-agent k8-finops-agent-test

# Trigger manual run from CronJob
kubectl create job --from=cronjob/k8-finops-agent manual-run -n finops-agent
kubectl logs -n finops-agent job/manual-run -f

# Customize schedule
helm upgrade finops-agent ../helm/ --set schedule="*/30 * * * *"
```

### Reference Documentation

For complete Helm deployment instructions, see:
- **Helm Chart:** `../helm/README.md`
- **Deployment Guide:** `../guide.md`

These manifests remain here as reference material for understanding the underlying Kubernetes resources that Helm manages.
