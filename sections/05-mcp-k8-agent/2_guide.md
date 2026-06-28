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
curl -s -X POST http://localhost:8000/message \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"curl-test","version":"1.0"}}}'
```
> *Expected: JSON response wrapped in an SSE frame indicating server "kubernetes".*

### 3) Real cluster read (kubectl_get namespaces)
```bash
curl -s -X POST http://localhost:8000/message \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"kubectl_get","arguments":{"resourceType":"namespaces","allNamespaces":true,"output":"name"}}}'
```
> *Expected: A clean list of namespaces from the cluster.*

### 4) Cleanup
- Switch to the Supergateway terminal and press `Ctrl-C` to stop it.

---

**Try it:** Open [`architecture_builder/index.html`](architecture_builder/index.html) in your browser to stack the **gateway layers** bottom-up and complete the **curl proof ladder**. Use **Need a hint?** if stuck, then press **Test Gateway** to validate.
