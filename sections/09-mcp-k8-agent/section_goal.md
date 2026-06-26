# Section 09 Goal: Prebuilt MCP Setup for Local K8s Access

## Goal
Set up a prebuilt Kubernetes MCP server against the local running cluster, validate read-only tool access, and use MCP outputs as the foundation for later FinOps analysis.

## Scope
- Connect a prebuilt MCP server to the local cluster
- Validate MCP connectivity and available tool surface
- Run read-only namespace and workload queries through MCP
- Explain how MCP output can feed later analysis workflows
- Include cleanup steps so local demo state stays predictable

## Out of scope
- Writing custom MCP tools or Python MCP servers
- Advanced collector/analyst/tracker implementation details
- Kubernetes deployment packaging
- Metrics-server-dependent resource usage

## Success criteria
The learner can start a prebuilt MCP server, connect to it, run read-only cluster queries successfully, and explain how this setup becomes the input seam for advanced workflows in Section 10.
