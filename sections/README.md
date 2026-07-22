# Teaching Flow Sections

This directory is the curriculum skeleton for the repo.

## How to use it
- Each numbered folder is one lesson/section.
- Each section has a `section_goal.md` that defines scope and guardrails.
- Demo scripts live in `N_guide.md` (and `0_prerequisite_guide.md` for instructors).
- Video narration lives in `transcript/N.md` (numbered by playback order within each section).
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
- `sections/06-mcp-data-agent/code/` → Section 06 (`validate_mcp.py`, `query_agent.py`, `label_auditor.py`)
- `sections/07-llm-structured-agent/code/` and `config/` → Section 07 (LLM policy-aware label audit + tagging rules file)
- `sections/08-from-findings-to-tickets/service/` and `agent/` → Section 08 (tracker + agent integration)
- `sections/09-langsmith-observability/` → Section 09 (LangSmith tracing via `.env`, copied Section 07 auditor, full traced run in `5_guide.md`)
- `sections/10-k8-native-agent/` (docker, helm) → Section 10

## Section index (learning flow)

```text
00 Intro → 02a Incident → 02b FinOps → 01 Cluster → 02 Deploy → 03 Pain
    → 04 Design → 05 MCP → 06 Collect → 07 Analyze → 08 Tracker+Integrate
    → 09 Observe (LangSmith) → 10 Helm
```

1. **00** — Course introduction (SkyLine Air, course arc)
2. **02a** — Payment gateway down — incident triage
3. **02b** — Introduction to FinOps (Inform, Optimize, Operate)
4. **01** — Cluster setup and namespaces
5. **02** — Deploy airline services and kubectl basics
6. **03** — FinOps problems: tagging, orphaned resources, ownership gaps
7. **04** — FinOps AI architecture design (whiteboarding)
8. **05** — Prebuilt MCP setup and curl validation
9. **06** — LangChain MCP agents: prompt → MCP → unstructured data
10. **07** — LLM policy-aware label audit: tagging rules from file → policy-grounded agent answer
11. **08** — From findings to tickets: issue tracker service + agent integration
12. **09** — Observability with LangSmith (env-only tracing on copied Section 07 auditor; `5_guide.md` for the full traced policy auditor run)
13. **10** — Kubernetes-native agent (Helm)
