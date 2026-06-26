# Teaching Flow Restructure Plan

This document maps the current repository into the teaching sections.

## Guiding rule
Each section should be self-contained for learning, but later sections may refer back to earlier artifacts instead of duplicating them.

## File placement rules
- Section-specific docs stay inside that section folder.
- Shared config should only exist once unless the section needs a teaching-specific copy.
- Avoid mixing "lesson explanation" files with runtime code.
- If a section reuses code from an earlier section, reference it instead of copying it.

## Current top-level structure
```text
sections/
├── 01-cluster-foundation/
│   ├── section_goal.md
│   ├── guide.md
│   ├── manifests/
│   └── commands/
├── 02-airline-app-deployment/
│   ├── section_goal.md
│   ├── guide.md
│   ├── manifests/
│   └── kubectl-examples/
├── 02a-payment-gateway-down/
│   ├── section_goal.md
│   ├── guide.md
│   └── manifests/
├── 03-finops-problems/
│   ├── section_goal.md
│   ├── guide.md
│   ├── manifests/
│   └── examples/
├── 04-local-python-agent/
│   ├── section_goal.md
│   ├── guide.md
│   ├── agent/
│   └── config/
├── 05-mcp-k8-agent/
│   ├── section_goal.md
│   └── guide.md
├── 06-mcp-data-agent/
│   ├── section_goal.md
│   ├── guide.md
│   ├── requirements.txt
│   └── agent/
├── 07-llm-structured-agent/
│   ├── section_goal.md
│   ├── guide.md
│   ├── requirements.txt
│   ├── agent/
│   └── config/
├── 08-llm-agent-langchain/
│   ├── section_goal.md
│   ├── guide.md
│   ├── agent.md
│   ├── agent/
│   ├── config/
│   └── slides/
├── 09-issue-tracker-service/
│   ├── section_goal.md
│   ├── guide.md
│   ├── service/
│   └── slides/
├── 10-agent-to-tracker-integration/
│   ├── section_goal.md
│   ├── guide.md
│   ├── agent.md
│   ├── agent/
│   └── config/
└── 11-k8-native-agent/
    ├── section_goal.md
    ├── guide.md
    ├── agent/
    ├── config/
    ├── docker/
    ├── helm/
    ├── manifests/
    └── slides/
```

## Section mapping

### Section 01: Cluster foundation
- Keep: setup instructions, cluster creation steps, namespace creation steps
- Likely sources:
  - `setup.sh`
  - parts of `USAGE.md`
  - `.env.example`
- Output should teach: Kind/K8 access and namespace setup on a MacBook local machine

### Section 02: Airline deployment
- Keep:
  - `airline-k8-deployment/`
- Output should teach:
  - `kubectl apply -k`
  - `kubectl get`, `describe`, `logs`, `exec`

### Section 02a: Payment gateway down
- Keep:
  - manifests for the broken-API scenario
- Output should teach:
  - symptom vs root cause
  - fast triage with kubectl

### Section 03: FinOps problem statement
- Keep:
  - `airline-k8-deployment/orphaned-resources/`
  - tagging examples from `config/tagging-rules.yaml`
- Output should teach:
  - missing tags/labels
  - orphaned PVCs/configmaps
  - ownership ambiguity

### Section 04: Local Python agent
- Keep:
  - `agent/` (scanner, cost_calculator, untracked_money, main, analyzer, github_client)
  - `config/pricing.yaml`
  - `config/tagging-rules.yaml`
- Output should teach:
  - local scan flow
  - raw report generation

### Section 05: Prebuilt MCP setup for local cluster access (curl-validated)
- Keep:
  - `guide.md`
  - `section_goal.md`
- Output should teach:
  - prebuilt MCP server startup via Supergateway
  - kubeconfig wiring and connectivity verification
  - read-only tool invocation against the local cluster (curl)
  - cleanup after demo run

### Section 06: First MCP data agent (prompt → MCP → unstructured data)
- Keep:
  - `agent/collector.py` (starting point, moved from the previous advanced pipeline)
- Output should teach:
  - the prompt → MCP tool call → raw snapshot loop
  - deliberately unstructured output
  - why structure is added in Section 07, not here

### Section 07: LLM structured agent (snapshot + tagging rules → structured findings)
- Keep:
  - `agent/analyser.py`, `agent/models.py`, `agent/main.py` (starting point, moved from the previous advanced pipeline)
  - `config/tagging-rules.yaml`
- Output should teach:
  - consuming the Section 06 snapshot
  - injecting tagging rules into the LLM prompt
  - producing structured findings
  - why analysis is separate from collection

### Section 08: LLM decision flow (LangChain)
- Keep:
  - `agent/analyzer.py`
  - any prompt/config changes
- Output should teach:
  - prompt design
  - structured decision output
  - better report clarity

### Section 09: Issue tracker service
- Future content:
  - Dockerized FastAPI service
  - `/raise-issue` endpoint
  - OpenAPI docs
- Output should teach:
  - payload contract
  - issue lifecycle basics

### Section 10: Agent to tracker integration
- Keep:
  - `agent/tracker.py` (moved from the previous advanced pipeline)
  - `agent/main.py` integration orchestrator
  - metadata mapping logic
- Output should teach:
  - K8 metadata collection → LLM → issue translation
  - create issue end-to-end

### Section 11: Kubernetes-native agent (Helm)
- Keep:
  - Dockerfile/build logic
  - Helm chart for deployment/cronjob
- Output should teach:
  - containerization
  - deployment in a dedicated namespace
  - scheduled execution
  - Helm lifecycle operations