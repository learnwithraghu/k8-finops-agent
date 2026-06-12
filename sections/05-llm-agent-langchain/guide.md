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
- how Pydantic models structure LLM output
- how this becomes the handoff point before the tracker service

## What you need before starting
Complete Sections 01, 02, 03, and 04 first.

You should already have:
- a working Kind cluster
- the airline app deployed
- the local agent working
- an API key for the LLM endpoint

## Where the agent code lives
- `sections/05-bedrock-decision-flow/agent/`

This is the same scanner from Section 04, now with:
- `tagging_violations.py` - detects missing tags (no cost calculations)
- `analyzer.py` - LLM analysis functions using LangChain + OpenAI-compatible client
- `main.py` - simplified orchestrator

## Step 1: Read the tagging violation detector
```bash
cat sections/05-bedrock-decision-flow/agent/tagging_violations.py
```

What to look for:
- the `TaggingViolationDetector` class
- how it checks for missing required tags (owner, cost-center, etc.)
- the different violation categories (unallocated, unowned, orphaned, unknown)
- no cost calculations - purely focused on tagging compliance

## Step 2: Read the LLM analyzer
```bash
cat sections/05-bedrock-decision-flow/agent/analyzer.py
```

What to look for:
- the `analyze_resource()` function that uses LangChain
- the `ChatOpenAI` from `langchain_openai` — configured with a custom `base_url`
- why `base_url` is what makes it work with any OpenAI-compatible endpoint
- the prompt that asks for JSON output
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

## Step 5: Look at the plain violation report
The scanner identifies resources with missing tags. The raw output shows what's missing but doesn't provide context or recommendations.

What to look for:
- the report shows tagging compliance percentages
- it lists violations by category
- it shows missing tags but doesn't suggest what to add
- this is the gap the LLM will help close

## Step 6: Run the agent with the LLM enabled
```bash
PYTHONPATH=sections/05-bedrock-decision-flow python3 -m agent.main
```

What to look for:
- the logs should show the model ID being used
- the logs should say that findings are being sent to the LLM
- the report title should say it is LLM powered
- if it fails, check that `OPENAI_API_KEY` and `OPENAI_BASE_URL` are set correctly in `.env`

## Step 7: Read the LLM output
What to look for:
- the report should feel cleaner and more decision-oriented
- the reasoning should be easier to present to a team
- the suggestions should read like action items, not raw scan output
- the structure should be more useful for a tech-debt review
- this is the handoff point: the next step is tracking, not more scanning

## What to notice
- the API key is the only credential needed — no AWS setup, no `aws configure`
- `base_url` is what makes `ChatOpenAI` talk to a non-OpenAI endpoint
- the same LangChain chain works with any OpenAI-compatible API — only the URL changes
- the same violation data produces a cleaner decision layer
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
