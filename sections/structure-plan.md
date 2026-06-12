# Teaching Flow Restructure Plan

This document maps the current repository into the 8 teaching sections.

## Guiding rule
Each section should be self-contained for learning, but later sections may refer back to earlier artifacts instead of duplicating them.

## Proposed top-level structure
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
├── 05-llm-agent-langchain/
│   ├── section_goal.md
│   ├── guide.md
│   └── agent-changes/
├── 06-issue-tracker-service/
│   ├── section_goal.md
│   ├── guide.md
│   └── service/
├── 07-agent-to-tracker-integration/
│   ├── section_goal.md
│   ├── guide.md
│   └── agent/
└── 08-k8-native-agent/
    ├── section_goal.md
    ├── guide.md
    ├── docker/
    ├── manifests/
    └── cronjob/
```

## Current code -> future section mapping

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
  - `agent/`
    - `scanner.py`
    - `cost_calculator.py`
    - `untracked_money.py`
    - `main.py`
    - `analyzer.py`
    - `github_client.py`
  - `config/pricing.yaml`
  - `config/tagging-rules.yaml`
- Output should teach:
  - local scan flow
  - raw report generation

### Section 05: LLM decision flow (LangChain)
- Keep:
  - `agent/analyzer.py`
  - any prompt/config changes
- Output should teach:
  - prompt design
  - structured decision output
  - better report clarity

### Section 06: Issue tracker service
- Future content:
  - Dockerized FastAPI service
  - `/raise-issue` endpoint
  - OpenAPI docs
- Output should teach:
  - payload contract
  - issue lifecycle basics

### Section 07: Agent to tracker integration
- Keep:
  - `agent/github_client.py` (or replace with tracker client)
  - metadata mapping logic
- Output should teach:
  - K8 metadata collection
  - LLM-to-issue translation
  - create issue end-to-end

### Section 08: Kubernetes-native agent
- Keep:
  - Dockerfile/build logic
  - Kubernetes manifests for deployment/cronjob
- Output should teach:
  - containerization
  - deployment in a dedicated namespace
  - scheduled execution

## File placement rules
- Section-specific docs stay inside that section folder.
- Shared config should only exist once unless the section needs a teaching-specific copy.
- Avoid mixing “lesson explanation” files with runtime code.
- If a section reuses code from an earlier section, reference it instead of copying it.

## Next implementation step
Create `guide.md` in each section and then move/copy the relevant code and manifests into the section-owned folders.
