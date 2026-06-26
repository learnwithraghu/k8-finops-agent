# Section 08 Goal: LLM Decision Flow

## Goal
Enhance the local agent with an OpenAI-compatible LLM endpoint so the report becomes cleaner, more contextual, and more decision-oriented.

## Scope
- Add LangChain + OpenAI-compatible LLM integration
- Configure the endpoint via `OPENAI_BASE_URL` and `OPENAI_API_KEY` in `.env`
- Feed scan results into a prompt
- Improve the report with AI-guided structure and recommendations
- Compare raw output vs LLM output

## Out of scope
- Issue tracker writes
- Kubernetes deployment
- Full automation of remediation

## Success criteria
The learner sees a cleaner, more actionable report produced by the local agent using the LLM endpoint.
