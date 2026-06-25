# Teaching Flow Sections

This directory is the curriculum skeleton for the repo.

## How to use it
- Each numbered folder is one lesson/section.
- Each section has a `section_goal.md` that defines scope and guardrails.
- Future code/docs should stay inside the section that owns the lesson.
- If a change crosses sections, update the relevant `section_goal.md` files first.

## Current repo mapping
- `sections/01-cluster-foundation/commands/setup.sh` → Section 01
- `sections/02-airline-app-deployment/manifests/airline-k8-deployment/` → Sections 02, 03
- `sections/04-local-python-agent/agent/` → Sections 04, 05, 07
- `sections/04-local-python-agent/config/` → Sections 04, 05, 07
- Future issue tracker service → Section 06
- Future Kubernetes-native deployment/cronjob → Section 08
- Future MCP-powered cluster interface → Section 09

## Section index
1. Cluster setup and namespaces
2. Deploy airline services and kubectl basics
3. FinOps problems: tagging, orphaned resources, ownership gaps
4. Local Python agent: scan + report
5. Bedrock-enhanced decision flow
6. Issue tracker service
7. Agent to tracker integration
8. Kubernetes deployment and scheduled runs
9. MCP-powered K8s cluster access and compliance analysis
