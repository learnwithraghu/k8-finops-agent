# Manifests

Kubernetes manifests for deploying the Section 08 agent.

## Files
- `namespace.yaml` — dedicated `finops-agent` namespace
- `rbac.yaml` — ServiceAccount, ClusterRole, and ClusterRoleBinding
- `secret.yaml` — placeholder Secret for the LLM API key
- `configmap.yaml` — non-secret agent configuration

## Apply order
```bash
kubectl apply -f namespace.yaml
kubectl apply -f rbac.yaml
kubectl apply -f configmap.yaml
```

## Secret creation
Do **not** apply `secret.yaml` with a real key. Instead, create the Secret from the command line:

```bash
kubectl create secret generic finops-agent-llm \
  --namespace finops-agent \
  --from-literal=OPENAI_API_KEY="your-api-key-here"
```

See `../guide.md` Step 5 for the full instructions.
