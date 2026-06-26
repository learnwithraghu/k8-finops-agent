# Section 07 Guide: LLM Structured Agent

> Status: **skeleton**. The `agent/analyser.py`, `agent/models.py`, and `agent/main.py` files moved here are the starting point from the previous advanced pipeline. The follow-up session adapts them into the snapshot + tagging rules → structured findings flow described here.

## Goal
Turn the Section 06 unstructured snapshot into structured FinOps findings with an LLM. The tagging rules in `config/tagging-rules.yaml` become the evaluation policy the LLM applies.

## Prerequisites
Complete Sections 01 through 06 first.

You should already have:
- the Section 06 collector producing a raw snapshot
- root `.env` configured with `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL_ID`
- Python 3.10+ and the section `requirements.txt` installed

## Step 0: Re-confirm the Section 06 snapshot
Run the Section 06 agent and confirm you get an unstructured snapshot JSON. That JSON is the input for this section.

## Step 1: Install Section 07 dependencies
```bash
python3 -m pip install -r sections/07-llm-structured-agent/requirements.txt
```

## Step 2: Inspect the tagging rules
```bash
cat sections/07-llm-structured-agent/config/tagging-rules.yaml
```
These rules define the mandatory labels the LLM must check for in the Section 06 snapshot.

## Step 3: Inspect the analyser and models starting point
```bash
cat sections/07-llm-structured-agent/agent/analyser.py
cat sections/07-llm-structured-agent/agent/models.py
cat sections/07-llm-structured-agent/agent/main.py
```
Note: these files were moved from the previous advanced pipeline and are a **starting point only**. The next session adapts them so the analyser:
- reads the Section 06 snapshot as input
- loads tagging rules from `config/tagging-rules.yaml`
- prompts the LLM with snapshot + rules
- validates the LLM response against `models.py` schemas

## Step 4: Run the structured agent (to be wired in the next session)
The follow-up "work on 1st agent" session will provide the run command and the expected structured findings output. Until then, this section is scaffold-only.

## Step 5: What the output should look like (target shape)
Structured findings — each finding references a rule, the offending resource, and a severity:
```json
{
  "findings": [
    {
      "rule": "owner-label-required",
      "resource": "payment/payment-gateway",
      "severity": "high",
      "message": "Deployment payment-gateway is missing the owner label"
    }
  ]
}
```
This structured output is what Section 10 later converts into tracker tickets.

## Step 6: Discussion
- Why collection (06) and analysis (07) are separate concerns
- How tagging rules keep LLM output deterministic and auditable
- How Section 10 turns these structured findings into tracker issues

## Cleanup
No long-running process here — the Section 06 collector and Section 05 MCP endpoint are the only things to stop.

## Expected outcome
You should be able to:
- feed the Section 06 snapshot into the Section 07 LLM agent
- explain how tagging rules shape the structured output
- read the structured findings and confirm each maps to a rule violation
- explain why this section deliberately stops short of posting to the tracker (that is Section 10)