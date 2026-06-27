# Demo 2: Querying the Local Cluster via curl

**Time Budget:** 4-5 mins

*(Run these in a new terminal)*

### 1) Validate health probe
```bash
curl -s http://localhost:8000/healthz
```
> *Expected: `ok`*

### 2) Validate MCP initialize
```bash
curl -s -X POST http://localhost:8000/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"curl-test","version":"1.0"}}}'
```
> *Expected: JSON response wrapped in an SSE frame indicating server "kubernetes".*

### 3) Real cluster read (kubectl_get namespaces)
```bash
curl -s -X POST http://localhost:8000/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"kubectl_get","arguments":{"resourceType":"namespaces","allNamespaces":true,"output":"name"}}}' \
  | sed -n 's/^data: //p' | jq -r '.result.content[0].text'
```
> *Expected: A clean list of namespaces from the cluster.*

### 4) Cleanup
- Switch to the Supergateway terminal and press `Ctrl-C` to stop it.
