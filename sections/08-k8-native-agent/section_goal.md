# Section 08 Goal: Kubernetes-Native Agent

## Goal
Package the Section 05 LLM decision-flow agent as a container and deploy it inside Kubernetes as a scheduled CronJob, so the FinOps scan runs in-cluster instead of from a laptop.

## Scope
- Reuse the Section 05 agent code unchanged
- Containerize the agent with a Dockerfile
- Add a Kubernetes namespace, ServiceAccount, RBAC, Secret, and ConfigMap
- Run the agent as a CronJob (plus a manual Job for verification)
- Show how the `OPENAI_API_KEY` from `.env` becomes a Kubernetes Secret

## Out of scope
- Re-teaching LangChain or the LLM prompt design (covered in Section 05)
- Writing to the issue tracker service (covered in Section 07)
- Production-grade secret management such as Sealed Secrets or vaults

## Success criteria
The learner can build the image, create the LLM API key Secret, apply the manifests, and see the agent execute inside the cluster on a schedule with the same decision-oriented report produced by Section 05.
