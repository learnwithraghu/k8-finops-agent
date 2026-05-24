# Section 05 Guide: Bedrock Decision Flow

This is the only file you need for Section 05.

## Goal
Use Bedrock to turn the local FinOps scan into a clearer, more decision-oriented report.

## Tutor note
Show the plain local report first, then switch to Bedrock and show how the output becomes more decision-oriented.

## What students will learn
- what looks weak in the plain local report
- how Bedrock improves the report structure and reasoning
- how to use an **Inference Profile ARN** with Bedrock
- why AWS IAM credentials are enough
- how this becomes the handoff point before the tracker service

## What you need before starting
Complete Sections 01, 02, 03, and 04 first.

You should already have:
- a working Kind cluster
- the airline app deployed
- the local agent working in mock mode
- an AWS account with Bedrock access

Bedrock uses your AWS credentials. Configure them with:
```bash
aws configure
```

This writes to `~/.aws/credentials` and `~/.aws/config`. The agent picks them up automatically — no access keys go in `.env`.

## Where the agent code lives
- `sections/05-bedrock-decision-flow/agent/`

This is the same scanner, calculator, and detector from Section 04, now with the Bedrock analyzer wired in.

## Step 1: Read the Bedrock analyzer
```bash
cat sections/05-bedrock-decision-flow/agent/analyzer.py
```

What to look for:
- the `BedrockAnalyzer` class
- the prompt that asks for JSON output
- the fallback path when Bedrock is unavailable
- the `modelId` value being passed into Bedrock

## Step 2: Set the Bedrock profile in `.env`
Open the environment file:
```bash
nano .env
```

What to look for:
- set `BEDROCK_MODEL_ID` to your **Inference Profile ARN**
- only `BEDROCK_MODEL_ID`, `BEDROCK_MAX_TOKENS`, and `BEDROCK_TEMPERATURE` are needed
- AWS credentials are picked up automatically from `aws configure` / `~/.aws/credentials`
- no access keys or session tokens belong in `.env`

Example:
```env
BEDROCK_MODEL_ID=arn:aws:bedrock:us-east-1:123456789012:inference-profile/example
```

## Step 3: Confirm the environment values
```bash
grep -nE '^(BEDROCK_MODEL_ID|BEDROCK_MAX_TOKENS|BEDROCK_TEMPERATURE|AWS_REGION)=' .env
```

What to look for:
- the profile ARN should be in `BEDROCK_MODEL_ID`
- no bearer token, access key, or secret key is needed
- AWS credentials come from your configured profile (`aws configure`)

## Step 4: Look at the plain local report
Use the Section 04 run as your baseline.

What to look for:
- the report is useful, but still very mechanical
- it lists findings, but does not decide what matters most
- this is the gap Bedrock will help close

## Step 5: Run the agent with Bedrock enabled
```bash
PYTHONPATH=sections/05-bedrock-decision-flow python -m agent.main --log-level INFO
```

What to look for:
- the logs should clearly say Bedrock connected
- the logs should show the inference profile ARN
- the logs should say that findings are being sent to Bedrock
- the report title should say it is LLM powered
- no issue tracker is involved yet
- if Bedrock fails, check the AWS credentials and profile ARN first

## Step 6: Read the Bedrock output
What to look for:
- the report should feel cleaner and more decision-oriented
- the reasoning should be easier to present to a team
- the suggestions should read like action items, not raw scan output
- the structure should be more useful for a tech-debt review
- this is the handoff point: the next step is tracking, not more scanning

## What to notice
- credentials are picked up from `aws configure` / `~/.aws/credentials` — no access keys in `.env`
- the inference profile ARN is used in place of a model id value
- no bearer token is involved
- the same scan data can produce a cleaner decision layer

## Expected outcome
You should be able to explain:
- what changed between mock and Bedrock mode
- why the inference profile ARN matters
- how Bedrock helps turn a report into a decision input

## Handoff to Section 06
Once the decision flow is clear, move to:
- `sections/06-issue-tracker-service/guide.md`

Section 06 will introduce the service that stores or routes the decision output.
