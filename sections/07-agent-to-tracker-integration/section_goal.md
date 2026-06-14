# Section 07 Goal: Agent to Tracker Integration

## Goal
Extend the Section 05 LLM decision-flow agent so actionable findings are automatically posted as tickets to the Section 06 issue tracker service.

## Scope
- Reuse the Section 05 scanner and analyzer unchanged
- Add a minimal HTTP client for the Section 06 tracker service
- Convert LLM decisions (`ResourceDecision`) into tracker payloads
- Post tickets to `POST /create-issue`
- Verify tickets show up in the board UI

## Out of scope
- Cost calculation (removed to keep the section focused)
- Bedrock-specific clients (Section 05 uses an OpenAI-compatible endpoint)
- Mock analyzers (the LLM is the decision layer)
- Kubernetes deployment of the agent (covered in Section 08)

## Success criteria
The learner can run the agent locally with the Section 06 tracker running and see tickets created automatically in the issue tracker board.
