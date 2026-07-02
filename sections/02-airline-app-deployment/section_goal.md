# Section 02 Goal: Airline App Deployment

## Goal
Deploy the airline workload into Kubernetes and teach how to inspect and interact with it using kubectl. By the end, students can navigate the cluster and understand what is running where.

## Prerequisites
Complete Section 01 first.

You should already have:
- a working Kind cluster (`finops-cluster`)
- kubectl access confirmed
- airline namespaces created (`booking-api`, `flight-search`, `inventory`, `payment`, `airline`)

## Instructor setup (before the live demo)
Run `0_prerequisite_guide.md` before teaching. It confirms the cluster is healthy and shows the manifest layout. Do not walk students through manifest discovery during the live demo.

## Video structure (2 videos)
| Video | Focus | Time |
|-------|------------|-------|------|
| **1** | Booking, search, inventory, payment, analytics services | 3–4 min |
| **2** | Kind demo footprint vs production scale | 3–4 min |

## Demo structure (3 parts)
| Demo | Focus | Time |
|------|-------|------|
| **1** | Deploy the airline app with Kustomize | 2 min |
| **2** | Validate the runtime footprint across namespaces | 2–3 min |
| **3** | Deep dive into a single workload (describe, logs, exec) | 2–3 min |

Each demo is one clear beat. Students go from "empty namespaces" to "running app they can inspect" in under 7 minutes.

## Scope
- Deploy airline services using `kubectl apply -k`
- Explain namespaces, pods, services, configmaps, and PVCs in context
- Show common kubectl commands for inspection and troubleshooting
- Walk through a realistic on-call triage flow

## Out of scope
- Cost/FinOps analysis (Section 03)
- AI recommendations (Section 04+)
- Issue tracker integration (Section 08)

## Success criteria
The learner can:
1. Deploy the app using Kustomize and confirm resources created
2. List deployments, pods, services, and configmaps across namespaces
3. Describe a deployment and read its events
4. Tail logs from a running pod
5. Exec into a container and run a command
