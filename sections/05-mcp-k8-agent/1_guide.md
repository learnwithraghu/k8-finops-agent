# Demo 1: Start the MCP Endpoint

**Time Budget:** 3 mins

**Narrative:** We have a prebuilt MCP server that wraps kubectl. Supergateway exposes it as HTTP so we can test with curl — no SDK, no client library, just raw requests. This is the fastest way to prove MCP works.

---

### 1) Validate local cluster access

```bash
kubectl config current-context
kubectl get ns
```

**What it does:** Confirms kubectl is pointed at the Kind cluster and namespaces exist. If this fails, the MCP server will also fail.

> *Talking point: "The MCP server uses the same kubeconfig as kubectl. If kubectl works, the MCP server will work."*

---

### 2) Confirm the kubeconfig path

```bash
export KUBECONFIG_FILE="${KUBECONFIG:-$HOME/.kube/config}"
test -f "$KUBECONFIG_FILE" && echo "Using $KUBECONFIG_FILE"
```

**What it does:** Resolves and validates the kubeconfig file path. We need this for the Docker volume mount.

---

### 3) Start the MCP HTTP endpoint

In a **dedicated terminal**:

```bash
export KUBECONFIG_FILE="${KUBECONFIG:-$HOME/.kube/config}"

npx -y supergateway \
  --stdio "docker run --rm -i --network host --user 0:0 \
    -v ${KUBECONFIG_FILE}:/kubeconfig:ro -e KUBECONFIG=/kubeconfig \
    mcp/kubernetes:latest" \
  --outputTransport sse \
  --port 8000 \
  --healthEndpoint /healthz
```

**What it does:** Starts the MCP server inside Docker, wrapped by Supergateway as an HTTP endpoint. Port 8000 serves the SSE transport; `/healthz` is a liveness probe.

> *Expected: "Listening on port 8000". Leave this terminal open.*

> *Talking point: "Supergateway converts the MCP server's stdio protocol into HTTP/SSE. That is the bridge — stdio for local tools, HTTP for remote clients."*

---

**Next:** Server is running. Next we prove it works with three curl calls → `2_guide.md`
