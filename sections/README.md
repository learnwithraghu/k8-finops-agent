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
- `sections/04-finops-architecture-design/` → Section 04 (architecture whiteboarding)
- `sections/05-mcp-k8-agent/` → Section 05 (prebuilt MCP setup and curl validation)
- `sections/06-mcp-data-agent/agent/` → Section 06 (prompt → MCP → unstructured data)
- `sections/07-llm-structured-agent/agent/` and `config/` → Section 07 (snapshot + tagging rules → structured findings)
- `sections/08-issue-tracker-service/service/` → Section 08
- `sections/09-agent-to-tracker-integration/agent/` → Section 09
- `sections/10-k8-native-agent/` (docker, helm) → Section 10

## Section index
1. Cluster setup and namespaces
2. Deploy airline services and kubectl basics
2a. Payment gateway down — incident triage
3. FinOps problems: tagging, orphaned resources, ownership gaps
4. FinOps AI architecture design (whiteboarding)
5. Prebuilt MCP setup and curl validation
6. First MCP data agent: prompt → MCP → unstructured data
7. LLM structured agent: snapshot + tagging rules → structured findings
8. Issue tracker service
9. Agent to tracker integration
10. Kubernetes-native agent (Helm)