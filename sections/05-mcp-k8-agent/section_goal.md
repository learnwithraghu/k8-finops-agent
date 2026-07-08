# Section 05 Goal: curl-Validated MCP Server for Local K8s Access

## Goal
Run a prebuilt Kubernetes MCP server against the local Kind cluster, expose it as a plain HTTP endpoint with Supergateway, and validate the whole chain with curl — no client SDK required. This is the seam that Sections 06+ plug into.

## Prerequisites
Sections 01, 02, 02a, and 04 complete.

You should already have:
- a working Kind cluster (`finops-cluster`)
- kubectl access confirmed
- the FinOps architecture design understood (Collect → Analyze → Act pipeline)

## Instructor setup (before the live demo)
Run `0_prerequisite_guide.md` before teaching. It pulls the MCP image, confirms kubeconfig, and validates cluster access. Do not walk students through Docker image pulls during the live demo.

Students watch Video 0, then follow Demos 1 and 2.

## Video structure (3 videos)
| Video | Focus | Time | Transcript |
|-------|-------|------|------------|
| **0** | What is MCP; MCP in Kubernetes; why it fits the Gather stage | 1:30 | `transcript/0.md` |
| **1** | Start MCP HTTP endpoint via Supergateway | 3 min | `transcript/1.md` |
| **2** | curl validation — health, handshake, cluster read | 3–4 min | `transcript/2.md` |

## Demo structure (2 parts)
| Demo | Focus | Time |
|------|-------|------|
| **1** | Start the MCP HTTP endpoint via Supergateway | 3 min |
| **2** | Validate with curl — health, MCP handshake, real cluster read | 3–4 min |

Each demo is one clear beat. Students go from "no MCP" to "curl-validated HTTP endpoint" in under 7 minutes.

## Scope
- Wrap the OSS `mcp/kubernetes` stdio MCP image as a Streamable HTTP endpoint via `npx supergateway`
- Bind the MCP server to the local Kind cluster by mounting kubeconfig
- Validate with curl: health probe, MCP initialize, real cluster read
- Explain how MCP output feeds later analysis workflows
- Include cleanup steps so local demo state stays predictable

## Out of scope
- Writing custom MCP tools or Python MCP servers (Section 06+)
- Any client SDK or custom scripts — validation is curl-only
- Collector/analyst/tracker implementation details (Sections 06, 07, 09)
- Kubernetes deployment packaging (Section 10)

## Success criteria
The learner can:
1. Start a prebuilt MCP server exposed over HTTP using `npx supergateway`
2. `curl` its HTTP endpoint and receive a valid MCP `initialize` response
3. `curl` the `kubectl_get` tool and confirm it returns namespaces from the local Kind cluster
4. Explain how this curl-validated setup becomes the input seam for Sections 06 and 07
