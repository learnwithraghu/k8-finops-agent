# Section 02a Goal: Payment Gateway Down

## Goal
Create a real incident scenario — a payment endpoint is down and students must debug it
from scratch. The twist: there are no ownership labels on the failing service, so there
is no way to know which team owns it, who to page, or what Slack channel to post in.
This is the exact pain that motivates FinOps tagging discipline.

## Prerequisites
Complete Section 01 and Section 02 fully before starting this section.

You should already have:
- a working Kind cluster (`finops-cluster`)
- kubectl access confirmed
- all airline services deployed and running in their namespaces (`booking-api`, `flight-search`, `inventory`, `payment`)

## Instructor setup (before the live demo)
Run `0_prerequisite_guide.md` before teaching. It deploys the gateway, starts port-forward, and smoke-checks the broken state. Do not show that setup during the live demo.

## Story viewer (concept intro — open locally)

Before the live demo, walk through the incident story with the animated whiteboard viewer:

```bash
open sections/02a-payment-gateway-down/story_viewer/index.html
```

Three full-screen scenes with draw-on animation. Click **→** (or press `ArrowRight`) to advance — the next scene only plays when you click. Press `F` for fullscreen.

| Scene | Focus |
|-------|-------|
| **1** | Symptom — UI loads, payment fails (503) |
| **2** | Root cause — UI pod up, API at 0/0, empty endpoints |
| **3** | Ownership wall — no labels, scale fix, manual labels are a bad fix |

## Demo structure (3 parts)
| Demo | Focus | Time |
|------|-------|------|
| **1** | Orient in the cluster, confirm the symptom in the UI | 3–4 min |
| **2** | Investigate the `payment` namespace, find root cause | 4–5 min |
| **3** | Hit the ownership wall, apply a quick fix, validate | 3–4 min |

Each demo is one clear beat. Students see *what* is broken before *why*, and only then talk about *who owns it* and *how to restore service*.

## Scope
- Walk through a realistic on-call debug flow using kubectl (discovery commands, not memorized one-liners)
- Reproduce the payment failure in the browser (UI up, API down)
- Find root cause: API deployment scaled to 0 replicas
- Hit the ownership wall: no labels = no team = no one to call
- Apply the "bad fix" (`kubectl scale` + manual labels) as a cautionary example
- Set up the motivation for Section 03

## What this section is NOT
- Not a live deploy walkthrough — app and UI are already running before you start
- Not a permanent fix — labels are applied manually here as a demonstration of what NOT to do
- Not a FinOps scanning exercise — that is Section 03
- No AI/agent work

## Success criteria
A student can:
1. Start from `kubectl get namespaces` and land in the `payment` namespace without being told the exact resource names upfront
2. Open http://localhost:8089 and see the AirPay payment UI load
3. Attempt a payment and watch it fail with a specific error while the UI itself still works
4. Use `kubectl get` / `describe` to discover that the API has no running pods
5. Notice the missing ownership labels on the failing deployment
6. Articulate *why* missing labels make incident response harder
7. Apply the bad fix and see the payment succeed
8. Explain why the manual fix is not a real solution
