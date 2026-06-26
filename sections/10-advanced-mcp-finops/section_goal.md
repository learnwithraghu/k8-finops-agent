# Section 10 Goal: Advanced MCP FinOps Pipeline

## Goal
Use an MCP-enabled collection layer, an LLM analyst, and a tracker writer to run an end-to-end FinOps pipeline from cluster snapshot to issue creation.

## Scope
- Run MCP-backed collection for Kubernetes resources
- Keep collection deterministic and read-only
- Apply tagging policy through LLM analysis
- Convert actionable findings into tracker tickets
- Explain separation of responsibilities across collector, analyst, and tracker

## Out of scope
- Replacing Section 09 setup flow
- Building a local custom MCP server implementation in this section
- Production hardening for multi-cluster scale
- Metrics-server-dependent cost telemetry

## Success criteria
The learner can run the full advanced pipeline, trace data from MCP tool output to tracker issue payloads, and explain how setup-only usage in Section 09 extends into a full analysis and ticketing flow.
