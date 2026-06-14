# Section 05 Guide: LLM Decision Flow

This is the only file you need for Section 05.

## Goal
Use an OpenAI-compatible LLM endpoint with LangChain to turn tagging violations into clearer, more decision-oriented recommendations.

## Tutor note
Show the plain violation report first, then switch the LLM on and show how the output becomes more decision-oriented.

## What you will learn
- how to use LangChain with an OpenAI-compatible endpoint
- how a custom `base_url` lets you point LangChain at any OpenAI-compatible API
- how to keep API keys out of code using `.env`
- how a single prompt can hand the LLM both the K8s metadata and the FinOps
  tagging config, and let it decide compliance AND draft the fix
- how Pydantic models structure that LLM output
- how this becomes the handoff point before the tracker service

## What you need before starting
Complete Sections 01, 02, 03, and 04 first.

You should already have:
- a working Kind cluster
- the airline app deployed
- the local agent working
- an API key for the LLM endpoint

## Where the agent code lives
- `sections/05-llm-agent-langchain/agent/`

This is the same scanner from Section 04, now with:
- `analyzer.py` - sends each resource + the FinOps tagging policy to the LLM
  and gets back one structured decision (compliance verdict + issue draft)
- `main.py` - simplified orchestrator

## Step 1: Read the tagging policy
```bash
cat sections/05-llm-agent-langchain/config/tagging-rules.yaml
```

What to look for:
- `required_tags` and `label_mappings` — this is the same FinOps config from
  Section 04, but this time it's the LLM that applies it
- there is no Python code left that checks tags directly — the policy is
  handed to the LLM as part of the prompt

## Step 2: Read the LLM analyzer
```bash
cat sections/05-llm-agent-langchain/agent/analyzer.py
```

What to look for:
- the `ResourceDecision` Pydantic model — one model that covers both the
  compliance verdict (`is_compliant`, `category`, `missing_tags`, `reason`)
  and the issue draft (`issue_title`, `issue_body`, `priority`, ...)
- the `PROMPT_TEMPLATE` — it includes the resource's K8s metadata AND the
  full tagging policy, and asks the LLM to apply the policy itself
- the `analyze_resource()` function that uses LangChain
- the `ChatOpenAI` from `langchain_openai` — configured with a custom `base_url`
- why `base_url` is what makes it work with any OpenAI-compatible endpoint
- the `PydanticOutputParser` for structured output
- the `model` value being passed to the client

## Step 3: Set the API key in `.env`
Open the environment file:
```bash
nano .env
```

What to look for:
- set `OPENAI_API_KEY` to the key provided for your endpoint
- `OPENAI_BASE_URL` points to the KodeKloud API gateway (`https://api.ai.kodekloud.com/v1`)
- `OPENAI_MODEL_ID` is the model name the endpoint exposes (e.g. `gpt-4o`)
- no AWS credentials, no ARNs, no region config needed

Example:
```env
OPENAI_BASE_URL=https://api.ai.kodekloud.com/v1
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL_ID=gpt-4o
OPENAI_MAX_TOKENS=1024
OPENAI_TEMPERATURE=0.3
```

## Step 4: Confirm the environment values
```bash
grep -nE '^(OPENAI_BASE_URL|OPENAI_API_KEY|OPENAI_MODEL_ID|OPENAI_MAX_TOKENS|OPENAI_TEMPERATURE)=' .env
```

What to look for:
- `OPENAI_BASE_URL` should be the full endpoint URL
- `OPENAI_API_KEY` should be set (the value itself does not need to be shown)
- `OPENAI_MODEL_ID` should be a valid model name for this endpoint
- no AWS region, no inference profile ARN, no bearer token header

## Step 5: Recall the Section 04 report
In Section 04, `SimpleTagChecker` computed compliance in Python — missing
tags, orphaned PVCs, percentages — with no LLM call at all.

What to look for:
- that report was fast, free, and deterministic
- it told you *what* was wrong but not what to do about it
- this is the gap the LLM will help close

## Step 6: Run the agent with the LLM enabled
```bash
PYTHONPATH=sections/05-llm-agent-langchain python3 -m agent.main
```

What to look for:
- the logs should show the model ID being used
- the logs should show one LLM call per resource ("Sending resource to
  OpenAI-compatible endpoint...")
- the agent always scans all namespaces, except those listed in `excluded_namespaces`
- the report title should say it is LLM powered
- if it fails, check that `OPENAI_API_KEY` and `OPENAI_BASE_URL` are set correctly in `.env`

## Step 7: Read the LLM output
What to look for:
- `category`, `missing_tags`, and `reason` are now decided by the LLM itself —
  compare them against what you saw in Section 04 for the same resources
- the report should feel cleaner and more decision-oriented
- the suggestions should read like action items, not raw scan output
- this is the handoff point: the next step is tracking, not more scanning

## What to notice
- the API key is the only credential needed — no AWS setup, no `aws configure`
- `base_url` is what makes `ChatOpenAI` talk to a non-OpenAI endpoint
- the same LangChain chain works with any OpenAI-compatible API — only the URL changes
- Section 04's tagging-rules.yaml is reused as-is — only *who* applies it changed
- the LLM is now doing the policy matching that Python used to do — discuss
  whether you'd trust it to get every label alias right every time
- no cost calculations - purely focused on tagging compliance

## Expected outcome
You should be able to explain:
- how LangChain simplifies LLM integration with a custom endpoint
- why `base_url` matters and how it makes the client provider-agnostic
- how the LLM turns tagging violations into actionable recommendations
- the difference between raw violation output and LLM-enhanced recommendations

## Handoff to Section 06
Once the decision flow is clear, move to:
- `sections/06-issue-tracker-service/guide.md`

Section 06 will introduce the service that stores or routes the decision output.
