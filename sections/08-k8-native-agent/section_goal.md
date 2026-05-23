# Section 08 Goal: Kubernetes-Native Agent

## Goal
Containerize the finished agent, deploy it back into Kubernetes, and run it on a schedule so the workflow becomes fully in-cluster.

## Scope
- Dockerize the agent
- Deploy it into a separate namespace
- Add a CronJob or equivalent scheduler
- Run once and verify the generated issue/output in the tracker

## Out of scope
- Re-teaching the earlier sections
- Rebuilding the agent logic from scratch

## Success criteria
The learner can see the agent execute inside Kubernetes on a schedule and create tracker output automatically.
