# Section 09 Goal: Agent to Tracker Integration

## Goal
Consume the Section 07 structured findings (`TicketBatch`) and post each actionable `TrackerTicket` to the Section 08 issue tracker service.

## Scope
- Read the Section 07 `TicketBatch` JSON output
- Add an HTTP tracker client (`agent/tracker.py`)
- Map each `TrackerTicket` to the tracker `IssueCreate` schema and POST `/create-issue`
- Verify tickets show up in the Section 08 board UI
- Explain idempotency and retry considerations

## Out of scope
- Collecting cluster data (Section 06)
- LLM analysis and tagging rule enforcement (Section 07)
- Kubernetes deployment of the agent (Section 10)
- De-duplication / persistent state across runs (handled in a future hardening section)

## Notes on the current code
`agent/scanner.py`, `agent/analyzer.py`, `agent/main.py`, and `agent/config/tagging-rules.yaml` are **transitional**: they reproduce the legacy LangChain scanner pipeline and produce `ResourceDecision` objects that the current `tracker.py` knows how to POST. In the follow-up "work on 1st agent" session, this section's agent is being rewritten to consume Section 07's `TicketBatch` directly, dropping the scanner + analyzer + `ResourceDecision` and shrinking `tracker.py`'s role to a thin POST layer.

Until that rewrite lands, the integration still works end to end (scan → LLM decision → tracker ticket) but bypasses Section 07.

## Success criteria
The learner can run the agent with the Section 08 tracker running and see tickets created automatically in the issue tracker board, and can articulate how the rewrite will switch the agent from scanning on its own to consuming Section 07's structured findings.