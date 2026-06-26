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
| 05 LLM Agent (LangChain) | 1 | Video | Where LLM helps in FinOps reasoning | 3 to 4 min |
| 05 LLM Agent (LangChain) | 2 | Video | Prompt design for deterministic recommendations | 3 to 4 min |
| 05 LLM Agent (LangChain) | 3 | Video | Safety boundaries and fallback logic | 3 to 4 min |
| 05 LLM Agent (LangChain) | 4 | Demo | Compare static rules vs LLM-assisted findings | 7 to 8 min |
| 05 LLM Agent (LangChain) | 5 | Quiz | Which decisions should remain rule-only? How do you reduce hallucination risk? What is a good fallback when model output is uncertain? | 2 to 3 min |
| 06 Issue Tracker Service | 1 | Video | Why findings must become trackable work | 3 to 4 min |
| 06 Issue Tracker Service | 2 | Video | Minimal API design for issue lifecycle | 3 to 4 min |
| 06 Issue Tracker Service | 3 | Video | Data model and severity conventions | 3 to 4 min |
| 06 Issue Tracker Service | 4 | Demo | Stand up tracker service and create issues from findings | 7 to 8 min |
| 06 Issue Tracker Service | 5 | Quiz | What fields are mandatory in a FinOps issue? Why severity normalization matters? What closes the loop from alert to action? | 2 to 3 min |
| 07 Agent to Tracker Integration | 1 | Video | Integration contract: payload and idempotency | 3 to 4 min |
| 07 Agent to Tracker Integration | 2 | Video | De-dup and retry strategies | 3 to 4 min |
| 07 Agent to Tracker Integration | 3 | Video | Traceability from scan to ticket | 3 to 4 min |
| 07 Agent to Tracker Integration | 4 | Demo | Auto-create and update tracker tickets from agent output | 7 to 8 min |
| 07 Agent to Tracker Integration | 5 | Quiz | Why idempotency is critical? How to avoid duplicate issue spam? Which correlation key should be stable? | 2 to 3 min |
| 08 Kubernetes-Native Agent | 1 | Video | Containerizing the agent runtime | 3 to 4 min |
| 08 Kubernetes-Native Agent | 2 | Video | CronJob patterns for scheduled scans | 3 to 4 min |
| 08 Kubernetes-Native Agent | 3 | Video | Config and secret handling in-cluster | 3 to 4 min |
| 08 Kubernetes-Native Agent | 4 | Demo | Deploy agent as CronJob and validate periodic scans | 7 to 8 min |
| 08 Kubernetes-Native Agent | 5 | Quiz | Why CronJob over long-running deployment here? What should be ConfigMap vs Secret? Which signals confirm schedule reliability? | 2 to 3 min |
| 09 MCP K8 Setup (Prebuilt) | 1 | Video | Why prebuilt MCP is enough for local cluster demos | 3 to 4 min |
| 09 MCP K8 Setup (Prebuilt) | 2 | Video | Wiring kubeconfig and starting a prebuilt MCP server | 3 to 4 min |
| 09 MCP K8 Setup (Prebuilt) | 3 | Video | Verifying read-only tools and guardrails | 3 to 4 min |
| 09 MCP K8 Setup (Prebuilt) | 4 | Demo | Start prebuilt MCP and query the local cluster | 7 to 8 min |
| 09 MCP K8 Setup (Prebuilt) | 5 | Quiz | Why avoid custom MCP code for this stage? Which checks confirm safe read-only access? What should be cleaned up after the demo? | 2 to 3 min |
| 10 Advanced MCP FinOps | 1 | Video | When to move from setup-only MCP to advanced pipeline orchestration | 3 to 4 min |
| 10 Advanced MCP FinOps | 2 | Video | Collector, analyst, and tracker as a pipeline contract | 3 to 4 min |
| 10 Advanced MCP FinOps | 3 | Video | Extending MCP payloads for deeper compliance workflows | 3 to 4 min |
| 10 Advanced MCP FinOps | 4 | Demo | Run MCP-powered pipeline from snapshot to tracker issues | 7 to 8 min |
| 10 Advanced MCP FinOps | 5 | Quiz | What justifies advanced pipeline complexity? Which stage must remain deterministic? How do you keep tracker payloads reliable? | 2 to 3 min |

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
