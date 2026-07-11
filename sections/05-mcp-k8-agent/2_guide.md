# Video: Demo — Validate the MCP-to-Kubernetes Connection with curl

**Transcript:** [`transcript/2.md`](transcript/2.md)

**Time Budget:** 3–4 min
**Format:** Live terminal demo
**Prerequisites:** [`1_guide.md`](1_guide.md) — Supergateway running on port 8000

---

# Demo 2: Validate with curl

**Time Budget:** 3–4 mins

**Narrative:** Three curls prove the chain — health, MCP handshake, and a real cluster read. If curl works, any MCP client works.

*(Run these in a **new** terminal — Supergateway stays running in the other one.)*

---

### 1) Health probe

```bash
curl -s http://localhost:8000/healthz
```

**What it does:** Confirms Supergateway is up. Expect `ok`.

---

### 2) MCP initialize handshake

```bash
curl -s -X POST http://localhost:8000/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"curl-test","version":"1.0"}}}'
```

**What it does:** Sends the MCP handshake to `/mcp`. The reply comes back in the same curl — look for `"name":"kubernetes"`.

> *Say to students: "Streamable HTTP means request and response travel on one HTTP call — curl in, JSON out."*

> *Talking point: "Every MCP client does initialize first. The server advertises what it can do."*

---

### 3) List namespaces through MCP

```bash
curl -s -X POST http://localhost:8000/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"kubectl_get","arguments":{"resourceType":"namespaces","allNamespaces":true,"output":"name"}}}'
```

**What it does:** Calls the `kubectl_get` tool. Expect namespace names including `booking-api`, `flight-search`, `inventory`, `payment`.

> *Talking point: "We just read the cluster through MCP with curl. No Python, no SDK — the MCP server handled kubectl."*

---

### 4) Cleanup

Switch to the Supergateway terminal and press `Ctrl-C` to stop it.

---

**Next:** MCP endpoint validated with curl. Section 06 upgrades to a persistent HTTP MCP container (no Supergateway) and Python agents → `sections/06-mcp-data-agent`. Stop Supergateway before Section 06 if port 8000 is still in use.
