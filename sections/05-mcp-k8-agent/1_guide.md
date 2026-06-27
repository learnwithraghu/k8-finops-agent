# Demo 1: Starting the MCP HTTP Endpoint

**Time Budget:** 3-4 mins

### 1) Validate local cluster access
```bash
kubectl config current-context
kubectl get ns
```

### 2) Pull the MCP image
```bash
docker pull mcp/kubernetes:latest
```

### 3) Confirm the kubeconfig path
```bash
export KUBECONFIG_FILE="${KUBECONFIG:-$HOME/.kube/config}"
test -f "$KUBECONFIG_FILE" && echo "Using $KUBECONFIG_FILE"
```

### 4) Start the MCP HTTP endpoint (Run in a dedicated terminal)
```bash
export KUBECONFIG_FILE="${KUBECONFIG:-$HOME/.kube/config}"

npx -y supergateway \
  --stdio "docker run --rm -i --network host --user 0:0 \
    -v ${KUBECONFIG_FILE}:/kubeconfig:ro -e KUBECONFIG=/kubeconfig \
    mcp/kubernetes:latest" \
  --outputTransport streamableHttp \
  --streamableHttpPath /mcp \
  --port 8000 \
  --healthEndpoint /healthz
```
> *Expected: "Listening on port 8000". Leave this terminal open.*
