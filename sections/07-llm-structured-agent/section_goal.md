# Section 07 Goal: LLM Structured Agent (Snapshot + Tagging Rules → Structured Findings)

## Goal
Take the **unstructured** cluster snapshot produced by Section 06, add the `tagging-rules.yaml` policy, send both to an LLM, and produce **structured** FinOps findings. This is the MCP → LLM → structured data step that was missing from Section 06.

## Scope
- Consume the Section 06 raw snapshot as input
- Inject `config/tagging-rules.yaml` into the LLM prompt as policy context
- Use `agent/analyser.py`, `agent/models.py`, and `agent/main.py` (moved from the previous advanced pipeline) as the starting point
- Produce deterministic structured findings (missing tags, ownership gaps, severity)
- Keep the agent prompt and schema together in this section

## Out of scope
- Collecting cluster data directly (Section 06)
- Posting findings to the issue tracker (Section 09)
- Building or recreating the MCP server (Section 05)
- Multi-cluster scale or metrics-server cost telemetry

## Success criteria
The learner can:
1. feed the Section 06 snapshot into the Section 07 LLM agent
2. explain how tagging rules shape the LLM's structured output
3. read the structured findings JSON and confirm each finding maps to a rule violation
4. articulate why collection (06) and analysis (07) are separate steps