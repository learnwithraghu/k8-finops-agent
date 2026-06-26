# Section 05 Guide: Local MCP Server with curl Validation

This section is setup-only. You do not write custom MCP code here.

## Goal
Run an open-source Kubernetes MCP server against your local kind cluster, expose it as a plain HTTP endpoint with **Supergateway**, and validate it with nothing but `curl`.

## Tutor note
Keep this section practical and short:
- no MCP tool authoring
- no custom Python server implementation
- no client SDK required — every check is a single `curl`
- only setup, verify, query, and clean up

## What students will learn
- how to wrap a stdio MCP server as an HTTP endpoint with one `npx` command
- how to wire kubeconfig so the MCP server talks to the local kind cluster
- how to validate the endpoint with `curl` (health probe + initialize)
- how to run a read-only cluster query (`kubectl_get namespaces`) from a single curl POST
- how to clean up the demo environment after the run

## What you need before starting
Complete Sections 01 through 04 first.

You should already have:
- a working local cluster (kind) — see Section 01 / `helper/local-kind/setup-to-02.sh`
- the airline app deployed — see Section 02
- Docker running locally
- a valid kubeconfig at `~/.kube/config` (kind writes its context here)
- **Node 20+** on the host (Supergateway runs via `npx`):
  ```bash
  node -v     # expect v20 or newer
  ```

## Why not curl the MCP image directly?
The OSS `mcp/kubernetes:latest` Docker image only speaks the MCP protocol over **stdio** (stdin/stdout). There is no HTTP port to point `curl` at. **Supergateway** wraps any stdio MCP server as an HTTP endpoint in one command, so curl Just Works.

- Supergateway: https://github.com/supercorp-ai/supergateway
- MCP image: `mcp/kubernetes:latest`

We use **Streamable HTTP, stateless** transport — every `curl` POST is independent, no session headers, no SSE subscription.

## Step 0: Validate local cluster access
```bash
kubectl config current-context    # expect: kind-finops-cluster
kubectl get ns
```
Expected:
- current context points to your kind cluster
- lab namespaces are visible (booking-api, flight-search, inventory, payment, airline, ...)

## Step 1: Pull the MCP image
```bash
docker pull mcp/kubernetes:latest
```
Expected: image pulls successfully (npx will pull Supergateway's npm package on first run in Step 3).

## Step 2: Confirm the kubeconfig path
```bash
export KUBECONFIG_FILE="${KUBECONFIG:-$HOME/.kube/config}"
test -f "$KUBECONFIG_FILE" && echo "Using $KUBECONFIG_FILE"
```
Expected: prints `Using /Users/<you>/.kube/config` (or whatever `KUBECONFIG` points to). Kind writes the cluster context here by default.

## Step 3: Start the MCP HTTP endpoint
Run this in a dedicated terminal (it stays in the foreground):

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

What each flag does:
- `--stdio "..."` — the command Supergateway launches as the MCP server subprocess (the OSS Kubernetes image, with your kubeconfig mounted inside the container so it binds to your kind cluster automatically).
- `--network host` — lets in-container `kubectl` reach the kind API server endpoint referenced in the kubeconfig.
- `--user 0:0` — avoids kubeconfig file-permission errors when reading the mounted file.
- `--outputTransport streamableHttp` — expose the MCP API over plain HTTP instead of stdio.
- `--streamableHttpPath /mcp` — the endpoint path becomes `http://localhost:8000/mcp`.
- `--port 8000` — listen port (change if 8000 is busy).
- `--healthEndpoint /healthz` — register a trivial `GET /healthz` smoke-test route.

Expected: after a few seconds you see:
```
[supergateway] StreamableHttp endpoint: http://localhost:8000/mcp
[supergateway] Listening on port 8000
```
Leave this terminal running. Open a new terminal for the curl steps.

## Step 4: Validate — health probe
```bash
curl -s http://localhost:8000/healthz
```
Expected:
```
ok
```

## Step 5: Validate — MCP initialize
```bash
curl -s -X POST http://localhost:8000/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"curl-test","version":"1.0"}}}'
```
Expected — a JSON-RPC result wrapped in an SSE frame:
```
event: message
data: {"result":{"protocolVersion":"2024-11-05","capabilities":{"prompts":{},"resources":{},"tools":{}},"serverInfo":{"name":"kubernetes","version":"3.9.1"}},"jsonrpc":"2.0","id":1}
```
The JSON payload on the `data:` line is the MCP response. `serverInfo.name: "kubernetes"` confirms the MCP server is alive and answering MCP protocol calls over HTTP.

## Step 6: Validate — real cluster read (kubectl_get namespaces)
```bash
curl -s -X POST http://localhost:8000/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"kubectl_get","arguments":{"resourceType":"namespaces","allNamespaces":true,"output":"name"}}}'
```
Expected — the MCP `kubectl_get` tool queries your kind cluster and returns the namespaces:
```
event: message
data: {"result":{"content":[{"type":"text","text":"namespace/airline\nnamespace/booking-api\nnamespace/default\nnamespace/flight-search\nnamespace/inventory\nnamespace/kube-node-lease\nnamespace/kube-public\nnamespace/kube-system\nnamespace/local-path-storage\nnamespace/payment\n"}]},"jsonrpc":"2.0","id":2}
```
Your lab namespaces (`airline`, `booking-api`, `flight-search`, `inventory`, `payment`) appearing here proves the whole chain end to end:
`curl → Supergateway (HTTP) → docker run mcp/kubernetes (stdio MCP) → kind cluster`.

> Tip — to read just the namespaces cleanly:
> ```bash
> curl -s -X POST http://localhost:8000/mcp \
>   -H 'Content-Type: application/json' \
>   -H 'Accept: application/json, text/event-stream' \
>   -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"kubectl_get","arguments":{"resourceType":"namespaces","allNamespaces":true,"output":"name"}}}' \
>   | sed -n 's/^data: //p' | jq -r '.result.content[0].text'
> ```

## Step 7: Discussion (FinOps relevance)
Use the returned namespace list to explain:
- ownership visibility — which namespaces exist, which are lab vs system
- label/tag completeness — a follow-up curl with `output: json` returns metadata you can inspect for labels
- where compliance analysis gets layered on next (Sections 06 and 07)

Note: the MCP data agent (Section 06) and LLM structured agent (Section 07) build on this curl-validated baseline.

## Step 8: Cleanup
Stop the Supergateway process with `Ctrl-C` in its terminal. It automatically removes the spawned `mcp/kubernetes` container on exit.

Optional — remove the pulled image if you no longer need it offline:
```bash
docker image rm mcp/kubernetes:latest
```

## Troubleshooting
- **`curl: (52) Empty reply`** — Supergateway has not finished booting. Wait for the `Listening on port 8000` line, then retry.
- **`address already in use` on port 8000** — pick a different port with `--port 8001` and update the curl URLs.
- **`tools/call` returns `uninitialized`** — extremely rare with stateless transport. If you hit it, send the Step 5 `initialize` call first in the same shell session, then the `tools/call`.
- **Namespace list is empty or errors** — check that the kubeconfig context is `kind-finops-cluster` (`kubectl config current-context`), and verify `kubectl get ns` works on the host before starting Supergateway.
- **Kubeconfig permission errors** — keep `--user 0:0` in the `--stdio` docker command.
- **Cannot reach the kind API server from inside the container** — keep `--network host` (needed on macOS Docker Desktop and on Codespaces/container hosts so the in-container kubectl can reach the kind API endpoint embedded in the kubeconfig).

## Expected outcome
You should be able to:
- wrap the OSS Kubernetes MCP stdio image as an HTTP endpoint using `npx supergateway`
- validate the endpoint with plain `curl` (health probe + `initialize`)
- run a read-only cluster query (`kubectl_get namespaces`) from a single curl POST and see your kind namespaces in the response
- explain how this curl-validated MCP setup becomes the input seam for the Section 06 data agent and the Section 07 structured agent