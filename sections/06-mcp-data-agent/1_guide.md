# Video 1: Standalone MCP vs Supergateway

**Time Budget:** 1:30

### Opening

In Section 05 we proved MCP with curl. The Kubernetes MCP server spoke stdio inside Docker, and Supergateway translated that into HTTP on port 8000. That bridge worked — but it is an extra process to start, explain, and keep alive.

---

### Two ways to get HTTP MCP

**Supergateway path (Section 05):** Run `mcp/kubernetes` over stdio, wrap it with Supergateway, expose Streamable HTTP. Good for quick validation with curl when the server has no native HTTP.

**Standalone path (Section 06):** Run `mcp/kubernetes` with native Streamable HTTP enabled. One Docker container, one port, no gateway. Python agents connect directly to `http://localhost:8000/mcp`.

Same MCP protocol. Same tools — `kubectl_get`, `kubectl_describe`, and the rest. Different packaging.

---

### Why switch for agents

Curl needed HTTP. LangChain and `langchain-mcp-tools` also need a stable HTTP endpoint they can call repeatedly. A persistent container is simpler than stdio plus a gateway for that job.

You still mount kubeconfig read-only. You still use read-only tools in demos. You just drop the middle layer.

---

### Close

Next we start the standalone MCP server and validate it with Python. Open `2_guide.md` when you are ready.
