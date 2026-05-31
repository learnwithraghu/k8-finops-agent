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

## Scope
- Deploy the AirPay payment gateway UI (Stripe-like browser interface)
- Deploy the payment API backend — intentionally broken (scaled to 0 replicas)
- Open the UI in Chrome and demonstrate the payment failure
- Walk through the real-world debug flow using kubectl
- Hit the ownership wall: no labels = no team = no one to call
- Apply the "bad fix" (kubectl label + kubectl scale) as a cautionary example
- Set up the motivation for Section 03

## What this section is NOT
- Not a permanent fix — labels are applied manually here as a demonstration of what NOT to do
- Not a FinOps scanning exercise — that is Section 03
- No AI/agent work

## Success criteria
A student can:
1. Open http://localhost:8080 in Chrome and see the AirPay payment UI
2. Attempt a payment and watch it fail with a specific error
3. Run the kubectl debug sequence and confirm there are no pods for the backend
4. Notice the missing ownership labels on the failing deployment
5. Articulate *why* missing labels make incident response harder
6. Apply the bad fix and see the payment succeed
7. Explain why the manual fix is not a real solution
