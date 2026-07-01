# Section 04 Goal: Local Python Agent

## Goal
Build the first local Python agent that connects to Kubernetes, scans resources, and produces a raw FinOps report. This is the first step toward automation — replacing manual kubectl checks with code.

## Prerequisites
Complete Sections 01, 02, and 02a first.

You should already have:
- a working Kind cluster (`finops-cluster`)
- kubectl access confirmed
- airline app deployed and running in its namespaces
- Section 02a completed (payment gateway scenario understood)

## Instructor setup (before the live demo)
Run `0_prerequisite_guide.md` before teaching. It sets up the Python environment, installs dependencies, and inspects the config files. Do not walk students through pip install during the live demo.

## Demo structure (2 parts)
| Demo | Focus | Time |
|------|-------|------|
| **1** | Run the collector across the cluster, review raw JSON output | 3 min |
| **2** | Compare automated output to manual kubectl checks | 3–4 min |

Each demo is one clear beat. Students go from "manual kubectl" to "automated Python collection" in under 7 minutes.

## Scope
- Read cluster resources using the Kubernetes Python client
- Load tagging rules from config
- Detect missing tags and orphaned resources
- Produce a local JSON report

## Out of scope
- MCP tool access (Section 05)
- LLM analysis and structured findings (Section 07)
- Issue tracker writes (Section 08)
- Kubernetes deployment of the agent (Section 10)

## Success criteria
The learner can:
1. Run the collector and get a JSON snapshot of the cluster
2. Explain what the collector reads and why it is useful
3. Compare the automated output to manual kubectl commands
4. Articulate why raw data alone is not enough — policy is needed (motivation for Section 07)
