# Video: Demo — Prove the Chain with curl (Health, Handshake, and a Cluster Read)

**Transcript:** [`transcript/2.md`](transcript/2.md)

**Time Budget:** 3–4 min
**Format:** Live terminal demo
**Prerequisites:** [`1_guide.md`](1_guide.md) — Supergateway running on port 8000

---

# Demo 2: Validate with curl

**Time Budget:** 3–4 mins

**Narrative:** Three curl calls prove the whole chain works — health check, MCP handshake, and a real cluster read. If curl works, any MCP client works.

*(Run these in a new terminal — Supergateway stays running in the other one.)*

---

### 1) Health probe

```bash
curl -s http://localhost:8000/healthz
```

**What it does:** Hits the health endpoint. If Supergateway is running, this returns `ok`.

> *Expected: `ok`*

> *Talking point: "Health checks are table stakes for any service. This confirms the HTTP layer is up before we try MCP."*

---

### 2) MCP initialize handshake

```bash
curl -s -X POST http://localhost:8000/message \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"curl-test","version":"1.0"}}}'
```

**What it does:** Sends the MCP `initialize` request. The server responds with its capabilities and name (should be `kubernetes`).

> *Expected: JSON response indicating server name "kubernetes" with supported tools.*

> *Talking point: "This is the MCP handshake. Every client — curl, Python, VS Code — does this first. The server advertises what tools it has."*

---

### 3) Real cluster read — list namespaces

```bash
curl -s -X POST http://localhost:8000/message \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"kubectl_get","arguments":{"resourceType":"namespaces","allNamespaces":true,"output":"name"}}}'
```

**What it does:** Calls the `kubectl_get` MCP tool to list namespaces. The MCP server runs `kubectl get namespaces` inside Docker and returns the result.

> *Expected: A clean list of namespaces from the cluster — `booking-api`, `flight-search`, `inventory`, `payment`, etc.*

> *Talking point: "We just read the cluster through MCP using nothing but curl. No Python, no SDK, no kubeconfig on this terminal. The MCP server handled authentication and execution."*

---

### 4) Cleanup

Switch to the Supergateway terminal and press `Ctrl-C` to stop it.

---

**Try it:** Open [`architecture_builder/index.html`](architecture_builder/index.html) in your browser to stack the **gateway layers** bottom-up and complete the **curl proof ladder**. Use **Need a hint?** if stuck, then press **Test Gateway** to validate.

**Next:** MCP endpoint validated. Next we build a Python agent that calls it → `sections/06-mcp-data-agent`
