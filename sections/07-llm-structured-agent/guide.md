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

## Step 4: Run the structured agent
The agent reads a Section 06 snapshot from `--snapshot <file>` (or stdin if not provided) and prints the structured findings as `TicketBatch` JSON.

```bash
PYTHONPATH=sections/07-llm-structured-agent \
  python3 -m agent.main --snapshot /tmp/section06-snapshot.json
```

Or piped from the Section 06 collector:
```bash
PYTHONPATH=sections/06-mcp-data-agent python3 -m agent.main --dump-raw > /tmp/section06-snapshot.json
PYTHONPATH=sections/07-llm-structured-agent python3 -m agent.main --snapshot /tmp/section06-snapshot.json
```

> The exact 06 -> 07 file-path contract is finalized in the follow-up "work on 1st agent" session. Until then, `--snapshot` / stdin is the contract.

## Step 5: What the output should look like (target shape)
Structured findings — a `TicketBatch` whose `tickets` are ready for the Section 08 tracker (Section 09 posts them):
```json
{
  "tickets": [
    {
      "title": "[FinOps] payment/payment-gateway missing owner label",
      "namespace": "payment",
      "resource_name": "payment-gateway",
      "resource_kind": "Deployment",
      "category": "missing-owner",
      "priority": "high",
      "suggested_owner": "payment-team",
      "reasoning": "Deployment payment-gateway has no owner label; ownership ambiguity blocks FinOps cost allocation.",
      "source": "mcp-llm-agent"
    }
  ]
}
```
This structured output is what Section 09 later POSTs to the Section 08 tracker. The `TrackerTicket` schema in `agent/models.py` already matches the tracker's `IssueCreate` contract.

## Step 6: Discussion
- Why collection (06) and analysis (07) are separate concerns
- How tagging rules keep LLM output deterministic and auditable
- How Section 09 turns these structured findings into tracker tickets (POSTed to the Section 08 tracker)

## Cleanup
No long-running process here — the Section 06 collector and Section 05 MCP endpoint are the only things to stop.

## Expected outcome
You should be able to:
- feed the Section 06 snapshot into the Section 07 LLM agent
- explain how tagging rules shape the structured output
- read the structured findings and confirm each maps to a rule violation
- explain why this section deliberately stops short of posting to the tracker (that is Section 09, which POSTs to the Section 08 tracker)