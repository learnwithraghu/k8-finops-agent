# Guide 0: Start the Persistent MCP Server and Validate

**Time Budget:** 4–5 mins

**Narrative:** Section 05 used Supergateway because curl cannot speak stdio MCP. Section 06 upgrades to a single Docker container that exposes native Streamable HTTP — no gateway, no curl. Leave it running; the agents connect over HTTP.

**Prerequisites:** Sections 01–05 complete; Kind cluster reachable via kubectl; repo-root `.env` and virtualenv from root `requirements.txt`.

---

### 1) Confirm kubectl works

```bash
kubectl get ns
```

**What it does:** Verifies cluster access. The MCP container uses the same kubeconfig.

> *Expected: airline namespaces like `booking-api`, `flight-search`, `inventory`, `payment`.*

---

### 2) Pull the MCP image (if needed)

```bash
docker pull mcp/kubernetes:latest
```

**What it does:** Downloads the same Kubernetes MCP image from Section 05 — now run with native HTTP instead of Supergateway.

---

### 3) Resolve kubeconfig path

```bash
export KUBECONFIG_FILE="${KUBECONFIG:-$HOME/.kube/config}"
test -f "$KUBECONFIG_FILE" && echo "Using $KUBECONFIG_FILE"
```

**What it does:** Sets the path Docker will mount read-only into the MCP container.

---

### 4) Start the persistent MCP server

In a **dedicated terminal** (leave it running for the whole section):

**Kind cluster (`finops-cluster`) — recommended for this course:**

```bash
kind get kubeconfig --name finops-cluster --internal > /tmp/kubeconfig-docker.yaml

docker run --rm -p 8000:8000 --network kind \
  -v /tmp/kubeconfig-docker.yaml:/home/appuser/.kube/config:ro \
  -e ENABLE_UNSAFE_STREAMABLE_HTTP_TRANSPORT=1 \
  -e PORT=8000 \
  -e HOST=0.0.0.0 \
  -e ALLOW_ONLY_READONLY_TOOLS=true \
  mcp/kubernetes:latest
```

**Other clusters (standard kubeconfig mount):**

```bash
docker run --rm -p 8000:8000 \
  -v "${KUBECONFIG_FILE}:/home/appuser/.kube/config:ro" \
  -e ENABLE_UNSAFE_STREAMABLE_HTTP_TRANSPORT=1 \
  -e PORT=8000 \
  -e HOST=0.0.0.0 \
  -e ALLOW_ONLY_READONLY_TOOLS=true \
  mcp/kubernetes:latest
```

**What it does:** Starts `mcp/kubernetes` with Streamable HTTP on port 8000 at `/mcp`. Read-only tools only — safe for demos. The Kind variant joins the `kind` Docker network so the container can reach the control plane.

> *Talking point: "One container, one port. No Supergateway, no npx. Python agents connect directly."*

---

### 5) Validate with Python (no curl)

In a **second terminal**:

```bash
source .venv/bin/activate
python3 sections/06-mcp-data-agent/code/validate_mcp.py
```

**What it does:** Connects to `http://localhost:8000/mcp`, calls `kubectl_get` for namespaces, and prints the list.

> *Expected: `MCP OK — N namespaces via kubectl_get` followed by namespace names.*

> *Talking point: "Same `kubectl_get` tool from Section 05 — we just proved it with Python instead of curl."*

---

**Next:** Walk through the agent code → `1_guide.md`
