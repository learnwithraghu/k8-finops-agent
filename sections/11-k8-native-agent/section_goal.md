# Section 11 Goal: Helm-Based Deployment

## Goal
Package the MCP-agent pipeline (Sections 06 + 07, transitioning toward full in-cluster MCP access) as a Helm chart and deploy it inside Kubernetes as a one-shot Job. Use Helm for templating, versioning, and lifecycle management, so the FinOps scan runs once in-cluster and exits cleanly.

## Video structure (2 videos)
| Video | Focus | Time |
|-------|------------|-------|------|
| **1** | CronJob vs Deployment; RBAC; secrets | 3–4 min |
| **2** | Chart structure; validating scheduled scans | 3–4 min |

## Scope
- Reuse the existing agent code unchanged (transitional LangChain scanner-based code at present)
- Containerize the agent with a Dockerfile
- Create a complete Helm chart with templated manifests
- Embed the tagging-rules.yaml configuration as ConfigMap values
- Include namespace, ServiceAccount, RBAC, ConfigMaps, and Job templates
- Add Helm test hook for deployment validation
- Support local image deployment (imagePullPolicy: Never)
- Document secret creation workflow (external to Helm)
- Show how configuration is customizable via values.yaml

## Out of scope
- Re-teaching the LLM prompt design or the MCP collection flow (covered in Sections 05–07)
- Writing to the issue tracker service (covered in Section 09)
- Full in-cluster MCP server wiring (follow-up work; for now the in-cluster agent reads Kubernetes directly via the service account)
- Production-grade secret management such as Sealed Secrets or vaults (though Helm chart is compatible with these)
- Remote container registries (focus on local Kind deployment)

## Success criteria
The learner can:
- Build the image and load it into Kind
- Create the LLM API key Secret manually
- Install the Helm chart with `helm install`
- Verify the deployment with `helm test`
- See the agent execute inside the cluster on a schedule
- Customize the deployment via values.yaml
- Use Helm lifecycle commands (upgrade, rollback, history)