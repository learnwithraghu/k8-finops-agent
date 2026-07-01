# Instructor Prerequisite: MCP Image & Kubeconfig

**Audience:** Instructor only — run this before `1_guide.md`. Do not walk students through Docker pulls during the live demo.

**Time Budget:** 2–3 mins

---

## Before you start

Confirm earlier sections are complete:

- Kind cluster `finops-cluster` is running
- kubectl works against the cluster

Quick check:

```bash
kubectl cluster-info
kubectl get namespaces
```

**What it does:** Verifies cluster connectivity and that expected namespaces are present.

---

## 1) Pull the MCP image

```bash
docker pull mcp/kubernetes:latest
```

**What it does:** Downloads the prebuilt MCP server image. This image wraps kubectl as MCP tools — no custom code needed.

> *Talking point: "This is an open-source MCP server. It exposes tools like `kubectl_get`, `kubectl_describe`, and `kubectl_logs` over the MCP protocol."*

---

## 2) Confirm the kubeconfig path

```bash
export KUBECONFIG_FILE="${KUBECONFIG:-$HOME/.kube/config}"
test -f "$KUBECONFIG_FILE" && echo "Using $KUBECONFIG_FILE"
```

**What it does:** Resolves the kubeconfig path. The MCP server needs this mounted to talk to the Kind cluster.

> *Talking point: "Kind writes kubeconfig to `~/.kube/config` by default. We mount it read-only into the container so the MCP server can authenticate."*

---

## 3) Start the MCP endpoint (instructor only, keep running)

In a **separate terminal**, start Supergateway:

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

**What it does:** Starts the MCP server inside Docker, wrapped by Supergateway as an HTTP endpoint on port 8000. The `/healthz` path is a health probe.

> *Expected: "Listening on port 8000". Leave this terminal open for the whole session.*

---

## 4) Ready to teach

When setup passes and Supergateway is running, start the live walkthrough with:

- `1_guide.md` — Start the MCP endpoint (show the command, explain the pieces)
- `2_guide.md` — Validate with curl

## Cleanup after the session

Switch to the Supergateway terminal and press `Ctrl-C` to stop it.

To restart for another run, repeat step 3.
