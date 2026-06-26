# Section 06 Goal: First MCP Data Agent (Prompt → MCP → Unstructured Data)

## Goal
Build the first agent that takes a prompt, calls MCP tools against the local kind cluster, and returns **unstructured** cluster snapshot data. This is the prompt → MCP → raw data loop, with no LLM reasoning and no structured output yet.

## Scope
- Reuse the curl-validated MCP endpoint from Section 05
- Drive MCP `kubectl_get` tool calls from a small Python collector
- Assemble a raw snapshot (namespaces, deployments, pods, services, PVCs, configmaps)
- Print the unstructured result — no tagging policy, no LLM, no tickets
- Adapt `agent/collector.py` (moved from the previous advanced pipeline) into this section's starting point in the follow-up "work on 1st agent" session

## Out of scope
- LLM analysis and structured findings (Section 07)
- Tagging rules / compliance evaluation (Section 07)
- Posting to the issue tracker (Section 09)
- Writing or customizing the MCP server itself (Section 05)

## Success criteria
The learner can:
1. run the Section 06 collector against the local kind cluster
2. explain the prompt → MCP tool call → raw JSON snapshot flow
3. confirm the snapshot contains namespaces and resources from the airline app
4. articulate why this output is deliberately unstructured and why the next section adds LLM structure