# k8-finops-agent Course Syllabus (Delivery-First)

## Delivery model and pacing

- Audience level: beginner-to-intermediate platform and FinOps learners.
- Teaching style: medium pace, concept first, proof through short demos.
- Video segment length: 3 to 4 minutes each.
- Demo segment length: 7 to 8 minutes each.
- Section shape (recommended):
  - 2 to 3 short concept videos
  - 1 main demo
  - 1 quick quiz block
- Section completion target: 20 to 28 minutes total (including quiz discussion).

## Section-wise syllabus

Flow legend: Video -> Video -> Video -> Demo -> Quiz

| Section | Step | Type | Topic / Title | Time |
|---|---|---|---|---|
| 01 Cluster Foundation | 1 | Video | Why FinOps starts with cluster hygiene | 3 to 4 min |
| 01 Cluster Foundation | 2 | Video | Namespaces, labels, and ownership metadata | 3 to 4 min |
| 01 Cluster Foundation | 3 | Video | Foundation commands and guardrails | 3 to 4 min |
| 01 Cluster Foundation | 4 | Demo | Build a clean training cluster baseline | 7 to 8 min |
| 01 Cluster Foundation | 5 | Quiz | Why labels are not optional for FinOps? Which namespace strategy helps cost isolation? What is the first validation after cluster setup? | 2 to 3 min |
| 02 Airline App Deployment | 1 | Video | Workload anatomy: deployment, service, config | 3 to 4 min |
| 02 Airline App Deployment | 2 | Video | kubectl flow for day-1 visibility | 3 to 4 min |
| 02 Airline App Deployment | 3 | Video | Mapping app components to cost centers | 3 to 4 min |
| 02 Airline App Deployment | 4 | Demo | Deploy airline app and verify runtime footprint | 7 to 8 min |
| 02 Airline App Deployment | 5 | Quiz | Which resources are mandatory to inspect post-deploy? How do you tie workloads to team ownership? What indicates a healthy rollout? | 2 to 3 min |
| 02a Payment Gateway Down | 1 | Video | Failure storytelling for learning retention | 3 to 4 min |
| 02a Payment Gateway Down | 2 | Video | Symptom vs root cause in Kubernetes incidents | 3 to 4 min |
| 02a Payment Gateway Down | 3 | Video | Fast triage checklist | 3 to 4 min |
| 02a Payment Gateway Down | 4 | Demo | Reproduce and diagnose payment gateway outage | 7 to 8 min |
| 02a Payment Gateway Down | 5 | Quiz | Which signal is symptom only, not root cause? Which kubectl output narrows blast radius fastest? What should be captured for postmortem? | 2 to 3 min |
| 03 FinOps Problems | 1 | Video | Untagged resources and cost blind spots | 3 to 4 min |
| 03 FinOps Problems | 2 | Video | Orphaned assets and idle burn | 3 to 4 min |
| 03 FinOps Problems | 3 | Video | Ownership gaps and escalation pain | 3 to 4 min |
| 03 FinOps Problems | 4 | Demo | Detect 3 classic FinOps anti-patterns in the cluster | 7 to 8 min |
| 03 FinOps Problems | 5 | Quiz | Why do orphaned resources survive normal cleanup? What minimum tagging set is practical? Which problem creates the highest reporting noise? | 2 to 3 min |
| 04 Local Python Agent | 1 | Video | Agent loop: collect, analyze, report | 3 to 4 min |
| 04 Local Python Agent | 2 | Video | Rule-based scanning design | 3 to 4 min |
| 04 Local Python Agent | 3 | Video | Output formats for actionability | 3 to 4 min |
| 04 Local Python Agent | 4 | Demo | Run a local scanner against sample cluster state | 7 to 8 min |
| 04 Local Python Agent | 5 | Quiz | Why separate data collection from analysis? Which rule types should fail hard vs warn? What makes a report operator-friendly? | 2 to 3 min |
| 05 MCP K8 Setup (curl) | 1 | Video | Why a prebuilt MCP server is enough for local cluster demos | 3 to 4 min |
| 05 MCP K8 Setup (curl) | 2 | Video | Wrapping a stdio MCP server as an HTTP endpoint with Supergateway | 3 to 4 min |
| 05 MCP K8 Setup (curl) | 3 | Video | curl-validated health, initialize, and cluster read | 3 to 4 min |
| 05 MCP K8 Setup (curl) | 4 | Demo | Start the MCP HTTP endpoint and query the local cluster with curl | 7 to 8 min |
| 05 MCP K8 Setup (curl) | 5 | Quiz | Why a stdio-only MCP server needs a gateway for curl? Which checks confirm safe read-only access? What should be cleaned up after the demo? | 2 to 3 min |
| 06 MCP Data Agent | 1 | Video | Why an agent layer on top of MCP | 3 to 4 min |
| 06 MCP Data Agent | 2 | Video | Prompt → MCP tool call → raw snapshot | 3 to 4 min |
| 06 MCP Data Agent | 3 | Video | Keeping collection deterministic | 3 to 4 min |
| 06 MCP Data Agent | 4 | Demo | Run the first MCP data agent and inspect the unstructured snapshot | 7 to 8 min |
| 06 MCP Data Agent | 5 | Quiz | Why stop at unstructured output? What stays deterministic here? Why is LLM analysis deferred to Section 07? | 2 to 3 min |
| 07 LLM Structured Agent | 1 | Video | From raw snapshot to structured findings | 3 to 4 min |
| 07 LLM Structured Agent | 2 | Video | Tagging rules as the evaluation policy | 3 to 4 min |
| 07 LLM Structured Agent | 3 | Video | Schemas that keep LLM output auditable | 3 to 4 min |
| 07 LLM Structured Agent | 4 | Demo | Feed Section 06 snapshot + rules to the LLM and read structured findings | 7 to 8 min |
| 07 LLM Structured Agent | 5 | Quiz | Why separate collection (06) from analysis (07)? How do tagging rules constrain the LLM? Which field ties a finding to a rule? | 2 to 3 min |
| 08 From Findings to Tickets | 1 | Video | The Issue Tracker Landscape: Jira, Linear, GitHub Issues, and Custom | 3 to 4 min |
| 08 From Findings to Tickets | 2 | Demo | Launch the FinOps Issue Tracker | 2 to 3 min |
| 08 From Findings to Tickets | 3 | Demo | Tracker Backend Walkthrough: REST, MCP, and the Ticket Schema | 4 to 5 min |
| 08 From Findings to Tickets | 4 | Video | Whiteboard: Wiring the MCP Agent to the Tracker | 3 to 4 min |
| 08 From Findings to Tickets | 5 | Demo | Agent Walkthrough: Post Per-Finding Tickets Instead of Printing | 4 to 5 min |
| 08 From Findings to Tickets | 6 | Video | Architecture Update: The Closed-Loop FinOps Pipeline | 3 to 4 min |
| 08 From Findings to Tickets | 7 | Quiz | What fields are mandatory in a FinOps issue? Why per-finding beats one blob? What closes the loop from alert to action? | 2 to 3 min |
| 09 Agent Refactoring Best Practices | 1 | Video | collector / analyzer / tracker modules; testability | 3 to 4 min |
| 09 Agent Refactoring Best Practices | 2 | Demo | Run the refactored modular agent | 7 to 8 min |
| 09 Agent Refactoring Best Practices | 3 | Quiz | Why separate collection from analysis? What belongs in tracker.py? How does modularity help testing? | 2 to 3 min |
| 10 Kubernetes-Native Agent | 1 | Video | Containerizing the agent runtime | 3 to 4 min |
| 10 Kubernetes-Native Agent | 2 | Video | Helm chart patterns for scheduled scans | 3 to 4 min |
| 10 Kubernetes-Native Agent | 3 | Video | Config and secret handling in-cluster | 3 to 4 min |
| 10 Kubernetes-Native Agent | 4 | Demo | Deploy agent via Helm and validate periodic scans | 7 to 8 min |
| 10 Kubernetes-Native Agent | 5 | Quiz | Why Helm over raw manifests here? What should be ConfigMap vs Secret? Which signals confirm schedule reliability? | 2 to 3 min |

## Practical delivery pattern per section

Use the same 5-step pattern in every section to keep learner rhythm consistent:

1. Hook (45 to 60 sec): one real incident or cost pain.
2. Concept mini-video(s): 2 to 3 short clips.
3. Live demo (7 to 8 min): one crisp outcome, no side quests.
4. Quiz (2 to 3 min): 3 focused questions.
5. Wrap (60 sec): what changed, what to practice next.

## How to split demos without breaking code

You raised the key challenge correctly: small demos need stable code progression without creating maintenance-heavy duplication.

### Option A: Multiple guides inside each section (low code duplication)

- Keep one canonical code path in each section.
- Add guide files per demo, for example:
  - guide-demo-01.md
  - guide-demo-02.md
  - guide-demo-03.md
- Each guide references exact files/commands and expected checkpoints.

Pros:
- Minimal duplication.
- Easy to maintain correctness.

Cons:
- Learners do not get frozen per-demo code snapshots unless you add explicit checkpoints.

### Option B: Sub-copies for each demo (high duplication)

- Create demo-wise folders with copied code states.
- Example:
  - demos/demo-01/
  - demos/demo-02/
  - demos/demo-03/

Pros:
- Very easy for learners to jump directly to a demo state.

Cons:
- Heavy duplication and drift risk across copies.
- High maintenance overhead when bugs are fixed.

### Option C (Recommended): Hybrid checkpoints with one canonical codebase

- Keep one source of truth per section.
- Add lightweight checkpoints rather than full code copies.
- For each section, use:
  - one canonical code folder
  - a demos/ folder with guide files and checkpoint notes
  - optional patch/checkpoint artifacts only when needed

Suggested section layout:

- section-name/
  - guide.md
  - demos/
    - 01-topic-name.md
    - 02-topic-name.md
    - 03-topic-name.md
  - checkpoints/
    - 01-baseline.md
    - 02-after-change.md
    - 03-final.md
  - code/ (or existing agent/manifests folders as source of truth)

Pros:
- Near-zero code duplication.
- Clear demo slicing for 7 to 8 minute delivery.
- Easy to keep section continuity.

Cons:
- Requires discipline in writing checkpoint notes.

## Suggested standards for all future sections

- One outcome per demo, never multiple learning goals in one 7 to 8 min slot.
- Stable naming convention:
  - Video: V01, V02, V03
  - Demo: D01
  - Quiz: Q01
- Every demo guide includes:
  - starting state
  - commands to run
  - expected output
  - rollback/reset step
- Add a “time budget” line at top of each demo guide.
- If a demo needs a true isolated code state, prefer tiny patches/checkpoints before full folder copies.

## Quiz style recommendation

- Keep quizzes scenario-based, not definition-based.
- 3 questions per section is enough.
- Use one operational question, one diagnostic question, one decision question.
- End with answer rationale in 1 line each for instructor notes.

## Immediate next content work (optional)

If you want, next I can generate:

1. A reusable demo guide template file for all sections.
2. A reusable quiz template file with answer key format.
3. A concrete split for one sample section (for example Section 04) into V01/V02/V03 + D01 assets.
