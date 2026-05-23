# Section 07 Goal: Agent to Tracker Integration

## Goal
Extend the Python agent so it gathers the right Kubernetes metadata, asks Bedrock for a decision, and creates issue tracker tickets automatically.

## Scope
- Collect metadata from K8 resources
- Send structured context to Bedrock
- Convert Bedrock output into tracker payloads
- Post tickets to the local issue tracker
- Verify tickets show up in the board UI

## Out of scope
- Kubernetes deployment of the agent itself
- Teaching the initial cluster/app setup again

## Success criteria
The learner can run the agent locally and see tickets created automatically in the issue tracker.
