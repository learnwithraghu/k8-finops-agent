# Legacy Manifests (Pre-Helm)

⚠️ **Note:** These raw Kubernetes manifests have been replaced by the Helm chart in `../helm/`.

These files are kept for reference but are no longer the recommended deployment method. 
Please use the Helm chart for Section 11 deployment.

## Migration to Helm

The Helm chart provides significant advantages over raw manifests:

### Benefits of Helm Chart Approach
- **Templating:** Customize deployment via `values.yaml` without editing manifests
- **Embedded configuration:** Tagging rules are now part of values, not separate files
- **Lifecycle management:** Use `helm install`, `upgrade`, `rollback`, and `test` commands
- **Version control:** Track chart versions separately from application versions
- **Documentation:** Built-in NOTES.txt shows next steps after installation
- **Validation:** Helm test hook validates deployment automatically
- **Reusability:** Same chart can be deployed to multiple environments with different values

### What Changed

| Raw Manifest | Helm Template | Key Improvements |
|--------------|---------------|------------------|
| `namespace.yaml` | `templates/namespace.yaml` | Templated with values.yaml |
| `rbac.yaml` | `templates/serviceaccount.yaml`<br>`templates/clusterrole.yaml`<br>`templates/clusterrolebinding.yaml` | Split into logical components with template helpers |
| `configmap.yaml` | `templates/configmap-llm.yaml`<br>`templates/configmap-tagging-rules.yaml` | Separated LLM config from tagging rules; rules embedded from values |
| `secret.yaml` | *Not included* | Secret created manually for security (documented in guide) |

### How to Deploy with Helm

Instead of:
```bash
kubectl apply -f manifests/namespace.yaml
kubectl apply -f manifests/rbac.yaml
kubectl apply -f manifests/configmap.yaml
kubectl apply -f manifests/secret.yaml  # After editing with real API key
```

Use:
```bash
# Create secret manually (one time)
kubectl create namespace finops-agent
kubectl create secret generic finops-agent-llm \
  --namespace finops-agent \
  --from-literal=OPENAI_API_KEY="your-api-key"

# Install chart
helm install finops-agent ../helm/

# Test deployment
helm test finops-agent

# Customize and upgrade
helm upgrade finops-agent ../helm/ --set schedule="*/30 * * * *"
```

### Reference Documentation

For complete Helm deployment instructions, see:
- **Helm Chart:** `../helm/README.md`
- **Deployment Guide:** `../guide.md`

These manifests remain here as reference material for understanding the underlying Kubernetes resources that Helm manages.
