# Section 06 Goal: First MCP Data Agent (Prompt → MCP → Unstructured Data)

## Goal
Build the first agent that takes a prompt, calls MCP tools against the local Kind cluster, and returns unstructured cluster snapshot data. This is the prompt → MCP → raw data loop, with no LLM reasoning and no structured output yet.

## Prerequisites
Sections 01–05 complete.

You should already have:
- a working Kind cluster (`finops-cluster`)
- Supergateway running from Section 05 (port 8000)

## Instructor setup (before the live demo)
Run `0_prerequisite_guide.md` before teaching. It confirms Supergateway is alive, installs Python deps, and inspects the agent code. Do not walk students through pip install during the live demo.

## Demo structure (2 parts)
| Demo | Focus | Time |
|------|-------|------|
| **1** | Run the data agent, review raw JSON snapshot | 3 min |
| **2** | Inspect the snapshot, compare to kubectl, discuss why unstructured | 3–4 min |

Each demo is one clear beat. Students go from "MCP endpoint exists" to "Python agent producing a cluster snapshot" in under 7 minutes.

## Scope
- Reuse the curl-validated MCP endpoint from Section 05
- Drive MCP `kubectl_get` tool calls from a small Python collector
- Assemble a raw snapshot (namespaces, deployments, pods, services, PVCs, configmaps)
- Print the unstructured result — no tagging policy, no LLM, no tickets

## Out of scope
- LLM analysis and structured findings (Section 07)
- Tagging rules / compliance evaluation (Section 07)
- Posting to the issue tracker (Section 09)
- Writing or customizing the MCP server itself (Section 05)

## Success criteria
The learner can:
1. Run the data agent against the local Kind cluster
2. Explain the prompt → MCP tool call → raw JSON snapshot flow
3. Confirm the snapshot contains namespaces and resources from the airline app
4. Articulate why this output is deliberately unstructured and why the next section adds LLM structure
