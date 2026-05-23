# Section 07 Goal: Agent to Tracker Integration

## Goal
Extend the Python agent so it gathers the right metadata from Kubernetes, asks Bedrock for a decision flow, and creates issues in the tracker.

## Scope
- Collect metadata from K8 resources
- Map owners/managers and other reference data
- Send structured context to Bedrock
- Turn Bedrock output into tracker issues
- Use the issue tracker API end to end

## Out of scope
- Kubernetes deployment of the agent itself
- Teaching the initial cluster/app setup again

## Success criteria
The learner can run the agent locally and see issues created automatically in the tracker.
