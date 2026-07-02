# Teaching Flow Sections

This directory is the curriculum skeleton for the repo.

## How to use it
- Each numbered folder is one lesson/section.
- Each section has a `section_goal.md` that defines scope and guardrails.
- Demo scripts live in `N_guide.md` (and `0_prerequisite_guide.md` for instructors).
- Future code/docs should stay inside the section that owns the lesson.
- If a change crosses sections, update the relevant `section_goal.md` files first.

## Current repo mapping
- `sections/00-course-introduction/` → Course intro
- `sections/01-cluster-foundation/commands/setup.sh` → Section 01
- `sections/02-airline-app-deployment/manifests/airline-k8-deployment/` → Sections 02, 03
- `sections/02a-payment-gateway-down/` → Incident scenario and demos
- `sections/02b-introduction-to-finops/` → FinOps framework
- `sections/04-finops-architecture-design/` → Section 04 (architecture whiteboarding; `1_guide.md`–`3_guide.md`)
- `sections/05-mcp-k8-agent/` → Section 05 (prebuilt MCP setup and curl validation)
- `sections/06-mcp-data-agent/agent/` → Section 06 (prompt → MCP → unstructured data)
- `sections/07-llm-structured-agent/agent/` and `config/` → Section 07 (snapshot + tagging rules → structured findings)
- `sections/08-issue-tracker-service/service/` → Section 08
- `sections/09-agent-to-tracker-integration/agent/` → Section 09
- `sections/10-agent-refactoring-best-practices/` → Section 10 (modular agent architecture)
- `sections/11-k8-native-agent/` (docker, helm) → Section 11

## Section index (learning flow)

```text
00 Intro → 02a Incident → 02b FinOps → 01 Cluster → 02 Deploy → 03 Pain
    → 04 Design → 05 MCP → 06 Collect → 07 Analyze → 08 Tracker
    → 09 Integrate → 10 Refactor → 11 Helm
```

1. **00** — Course introduction (SkyLine Air, course arc)
2. **02a** — Payment gateway down — incident triage
3. **02b** — Introduction to FinOps (Inform, Optimize, Operate)
4. **01** — Cluster setup and namespaces
5. **02** — Deploy airline services and kubectl basics
6. **03** — FinOps problems: tagging, orphaned resources, ownership gaps
7. **04** — FinOps AI architecture design (whiteboarding)
8. **05** — Prebuilt MCP setup and curl validation
9. **06** — First MCP data agent: prompt → MCP → unstructured data
10. **07** — LLM structured agent: snapshot + tagging rules → structured findings
11. **08** — Issue tracker service
12. **09** — Agent to tracker integration
13. **10** — Agent refactoring best practices
14. **11** — Kubernetes-native agent (Helm)
