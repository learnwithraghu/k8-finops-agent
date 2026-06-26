# Section 05 Goal: curl-Validated MCP Server for Local K8s Access

## Goal
Run a prebuilt Kubernetes MCP server against the local kind cluster, expose it as a plain HTTP endpoint with **Supergateway**, and validate the whole chain with a single `curl` command — no client SDK required.

## Scope
- Wrap the OSS `mcp/kubernetes` stdio MCP image as a Streamable HTTP endpoint via `npx supergateway`
- Bind the MCP server to the local kind cluster by mounting `~/.kube/config` into the spawned container
- Validate the endpoint with `curl`:
  - health probe (`GET /healthz`)
  - MCP `initialize` (`POST /mcp`)
  - real cluster read (`kubectl_get namespaces`)
- Explain how MCP output can feed later analysis workflows
- Include cleanup steps so local demo state stays predictable

## Out of scope
- Writing custom MCP tools or Python MCP servers
- Any client SDK or custom scripts — validation is curl-only
- Advanced collector/analyst/tracker implementation details
- Kubernetes deployment packaging
- Metrics-server-dependent resource usage

## Success criteria
The learner can:
1. start a prebuilt MCP server exposed over HTTP using `npx supergateway`
2. `curl` its HTTP endpoint and receive a valid MCP `initialize` response
3. `curl` the `kubectl_get` tool and confirm it returns the namespaces from the local kind cluster
4. explain how this curl-validated setup becomes the input seam for advanced workflows in Sections 06 and 07