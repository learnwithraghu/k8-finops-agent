# Demo 2: Helm Deployment and Validation

**Time Budget:** 3-4 mins

### 1) Create namespace and secret (CRITICAL)
```bash
kubectl create namespace finops-agent

kubectl create secret generic finops-agent-llm \
  --namespace finops-agent \
  --from-literal=OPENAI_API_KEY="your-api-key-here"
```

### 2) Lint and Install the Helm chart
```bash
helm lint sections/11-k8-native-agent/helm/
helm install finops-agent sections/11-k8-native-agent/helm/
```
> *Expected: See "STATUS: deployed"*

### 3) Verify the deployment
```bash
helm list
kubectl get all -n finops-agent
```

### 4) Run Helm test for validation
```bash
helm test finops-agent
kubectl logs -n finops-agent k8-finops-agent-test
```
> *Talking point: Look for the FinOps Tagging Compliance Report in the logs!*
