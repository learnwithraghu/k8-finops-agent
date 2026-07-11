# Video 2: Start and Validate MCP

**Time Budget:** 7–9 mins

**Narrative:** Start one Docker container with native Streamable HTTP — no Supergateway — then prove the endpoint works with `validate_mcp.py`. Same `kubectl_get` tool as Section 05, validated with Python instead of curl.

**Prerequisites:** [`1_guide.md`](1_guide.md) (conceptual overview); [`0_prerequisite_guide.md`](0_prerequisite_guide.md) (instructor — image pulled, venv ready).

---

## Part A — Start the standalone MCP server

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

## Part B — Validate with `code/validate_mcp.py`

Before any LLM call, prove the standalone MCP endpoint works with a direct `kubectl_get` — no curl, no agent.

Open the file:

```bash
cat sections/06-mcp-data-agent/code/validate_mcp.py
```

---

### Block 1 — Module docstring (line 1)

```python
"""Validate the Section 06 persistent MCP HTTP endpoint (no curl)."""
```

**Highlight:** Purpose — health check for the HTTP MCP server, not an agent demo.

---

### Block 2 — Imports (lines 2–4)

```python
import asyncio

from mcp_client import decode_tool_result, get_mcp_tools, tool_by_name
```

**Highlight:** Reuses three helpers from `mcp_client.py` — connect, find tool, parse result.

> *Talking point: "Same wiring the agents use — we're just calling `kubectl_get` directly instead of letting the LLM choose."*

---

### Block 3 — `main` — connect and find tool (lines 7–10)

```python
async def main() -> None:
    tools, cleanup = await get_mcp_tools()
    try:
        kubectl_get = tool_by_name(tools, "kubectl_get")
```

**Highlight:** `get_mcp_tools()` opens the MCP session; `tool_by_name` grabs the namespace-listing tool by name.

> *Talking point: "If you see 'MCP tool not found', the handshake worked but the tool list is off — worth checking the container image."*

---

### Block 4 — `main` — invoke and parse (lines 11–15)

```python
        result = await kubectl_get.ainvoke({"resourceType": "namespaces", "allNamespaces": True})
        payload = decode_tool_result(result)
        namespaces = [item["name"] for item in payload.get("items", []) if item.get("name")]
        if not namespaces:
            raise RuntimeError("kubectl_get returned no namespaces — check MCP container and kubeconfig")
```

**Highlight:** Deterministic tool call — list all namespaces. Empty list raises a clear error.

> *Talking point: "Same `kubectl_get` tool Section 05 called with curl — here Python invokes it through LangChain's tool wrapper."*

---

### Block 5 — `main` — print results (lines 17–21)

```python
        print(f"MCP OK — {len(namespaces)} namespaces via {kubectl_get.name}")
        for name in namespaces:
            print(f"  - {name}")
    finally:
        await cleanup()
```

**Highlight:** Success line plus indented namespace list. `finally` always closes the MCP session.

---

### Block 6 — Entry point (lines 24–25)

```python
if __name__ == "__main__":
    asyncio.run(main())
```

**Highlight:** Standard async entry — same pattern as the agent scripts.

---

### Run it

In a **second terminal** (MCP container still running in the first):

```bash
source .venv/bin/activate
python3 sections/06-mcp-data-agent/code/validate_mcp.py
```

**What it does:** Connects to `http://localhost:8000/mcp`, calls `kubectl_get` for namespaces, prints the list.

---

### Expected output

```text
MCP OK — 9 namespaces via kubectl_get
  - airline
  - booking-api
  - default
  - flight-search
  - inventory
  - kube-node-lease
  - kube-public
  - kube-system
  - payment
```

**How to read the logs:**

| Line | Meaning |
|------|---------|
| `MCP OK — N namespaces via kubectl_get` | HTTP handshake succeeded; tool call returned data |
| `  - <name>` | Each namespace from the cluster — same data kubectl would show |
| *(no output, traceback)* | Container not running, wrong port, or kubeconfig mount broken — restart Part A |
| `kubectl_get returned no namespaces` | MCP connected but cluster returned empty — check kubeconfig inside the container |

> *Talking point: "If this passes, you've proven the read path works. The next video adds the LLM on top of the same endpoint."*

---

**Next:** Walk through shared wiring → `3_guide.md`
