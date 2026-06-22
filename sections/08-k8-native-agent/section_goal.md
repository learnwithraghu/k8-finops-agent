# Section 08 Goal: Helm-Based Deployment

## Goal
Package the Section 05 LLM decision-flow agent as a Helm chart and deploy it inside Kubernetes as a one-shot Job. Instead of managing raw Kubernetes manifests, use Helm for templating, versioning, and lifecycle management, so the FinOps scan runs once in-cluster and exits cleanly.

## Scope
- Reuse the Section 05 agent code unchanged
- Containerize the agent with a Dockerfile
- Create a complete Helm chart with templated manifests
- Embed the tagging-rules.yaml configuration as ConfigMap values
- Include namespace, ServiceAccount, RBAC, ConfigMaps, and Job templates
- Add Helm test hook for deployment validation
- Support local image deployment (imagePullPolicy: Never)
- Document secret creation workflow (external to Helm)
- Show how configuration is customizable via values.yaml

## Out of scope
- Re-teaching LangChain or the LLM prompt design (covered in Section 05)
- Writing to the issue tracker service (covered in Section 07)
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
