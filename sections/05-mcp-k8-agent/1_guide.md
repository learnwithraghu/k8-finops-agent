# Video: Demo — Start the MCP Gateway (Supergateway Exposes kubectl as HTTP)

**Transcript:** [`transcript/1.md`](transcript/1.md)

**Time Budget:** 3 min
**Format:** Live terminal demo
**Prerequisites:** [`transcript/0.md`](transcript/0.md), [`0_prerequisite_guide.md`](0_prerequisite_guide.md) (instructor)

---

# Demo 1: Start the MCP Endpoint

**Time Budget:** 3 mins

**Narrative:** We have a prebuilt MCP server that wraps kubectl. Supergateway exposes it as HTTP so we can test with curl — no SDK, no client library, just raw requests. This is the fastest way to prove MCP works.

---

### 1) Confirm kubectl context

```bash
kubectl config current-context
```

**What it does:** Shows which cluster kubectl is pointed at. Expect `kind-finops-cluster`.

---

### 2) List namespaces

```bash
kubectl get ns
```

**What it does:** Confirms the Kind cluster is reachable and the airline namespaces exist. If this fails, the MCP server will also fail.

> *Talking point: "The MCP server uses the same kubeconfig as kubectl. If kubectl works, the MCP server will work."*

---

### 3) Resolve the kubeconfig path

```bash
export KUBECONFIG_FILE="${KUBECONFIG:-$HOME/.kube/config}"
```

**What it does:** Sets `KUBECONFIG_FILE` to your kubeconfig path (defaults to `~/.kube/config`). Docker will mount this into the MCP container.

---

### 4) Verify the kubeconfig file exists

```bash
test -f "$KUBECONFIG_FILE" && echo "Using $KUBECONFIG_FILE"
```

**What it does:** Confirms the file is present before starting Supergateway. Expect `Using ~/.kube/config` (or your resolved path).

---

### 5) Free port 8000 (if needed)

```bash
lsof -tiTCP:8000 -sTCP:LISTEN | xargs kill 2>/dev/null || true
```

**What it does:** Stops whatever is already listening on port 8000 so Supergateway can bind. Fixes `EADDRINUSE` from a leftover process.

---

### 6) Start the MCP HTTP endpoint

In a **dedicated terminal** (leave it running):

```bash
npx -y supergateway \
  --stdio "docker run --rm -i --network host --user 0:0 \
    -v ${KUBECONFIG_FILE}:/kubeconfig:ro -e KUBECONFIG=/kubeconfig \
    mcp/kubernetes:latest" \
  --outputTransport streamableHttp \
  --port 8000 \
  --healthEndpoint /healthz
```

**What it does:** Starts `mcp/kubernetes` in Docker and wraps its stdio MCP protocol as HTTP on port 8000. Clients POST to `/mcp`; `/healthz` is a liveness probe.

**Streamable HTTP:** One POST to `/mcp` sends the MCP request and gets the reply in the same response — no separate SSE stream or session id to manage.

> *Say to students: "Streamable HTTP means request and response travel on one HTTP call — curl in, JSON out."*

> *Expected: "Listening on port 8000" and "StreamableHttp endpoint: http://localhost:8000/mcp". Leave this terminal open.*

> *Talking point: "Supergateway converts the MCP server's stdio protocol into HTTP. That is the bridge — stdio for local tools, HTTP for remote clients."*

---

**Next:** Server is running. Next we prove it works with curl → `2_guide.md`
