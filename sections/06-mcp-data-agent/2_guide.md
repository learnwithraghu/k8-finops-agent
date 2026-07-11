# Guide 2: Run the Standalone MCP Server

**Time Budget:** 4–5 mins

**Narrative:** Section 05 used Supergateway because curl cannot speak stdio MCP. Section 06 runs one Docker container with native Streamable HTTP — no gateway. Leave it running; the Python scripts connect over HTTP.

**Prerequisites:** [`1_guide.md`](1_guide.md) (conceptual overview); [`0_prerequisite_guide.md`](0_prerequisite_guide.md) (instructor — image pulled, venv ready).

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

> *Talking point: "One container, one port — no Supergateway, no npx. The Python agents just connect straight over HTTP."*

---

**Next:** Walk through shared wiring → `3_guide.md`, then validate with Python → `4_guide.md`
