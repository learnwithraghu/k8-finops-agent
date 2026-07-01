# Section 01 Goal: Cluster Foundation

## Goal
Set up the Kubernetes learning environment: a local Kind cluster, kubectl access, and the baseline namespaces the airline app will use.

## Prerequisites
None — this is the first section.

## Instructor setup (before the live demo)
Run `0_prerequisite_guide.md` before teaching. It verifies tools are installed and old state is cleaned up. Do not walk students through tool installation during the live demo.

## Demo structure (3 parts)
| Demo | Focus | Time |
|------|-------|------|
| **1** | Create the Kind cluster and verify it is healthy | 2 min |
| **2** | Create the airline namespaces and validate access | 2 min |
| **3** | Confirm the cluster baseline is clean | 3 min |

Each demo is one clear beat. Students go from "no cluster" to "cluster with namespaces ready for app deployment" in under 7 minutes.

## Scope
- Create a local Kind cluster (`finops-cluster`)
- Validate kubectl access against the cluster
- Create the namespaces used by the airline app (`booking-api`, `flight-search`, `inventory`, `payment`, `airline`)
- Establish a clean baseline with no workloads running

## Out of scope
- Application deployment (Section 02)
- Cost analysis (Section 03)
- AI/agent logic (Section 04+)
- Issue creation (Section 08)

## Success criteria
A learner can:
1. Create a Kind cluster from scratch
2. Run `kubectl cluster-info` and get a valid response
3. List namespaces and see the airline ones present
4. Confirm no app workloads are running before Section 02
