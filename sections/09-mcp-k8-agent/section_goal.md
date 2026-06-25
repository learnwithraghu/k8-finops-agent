# Section 09 Goal: MCP-Powered K8s FinOps Agent

## Goal
Replace the hand-written Kubernetes scanner with an MCP-based cluster interface, then use a deterministic collector, an LLM analyst, and a tracker writer to form a three-step FinOps pipeline.

## Scope
- Expose Kubernetes read operations as MCP tools
- Collect raw cluster data through MCP
- Keep the collector deterministic
- Use the LLM only for compliance analysis
- Transform the compliance report into tracker issues
- Send actionable findings to the local issue tracker

## Out of scope
- Kubernetes deployment packaging
- Metrics-server-dependent resource usage

## Success criteria
The learner can explain how MCP removes the custom scanner layer, how the collector/analyst/tracker steps fit together, and how actionable findings from all non-system namespaces land in the tracker.
