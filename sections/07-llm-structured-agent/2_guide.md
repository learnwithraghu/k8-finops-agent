# Demo 2: Audit the Findings

**Time Budget:** 3–4 mins

**Narrative:** Each finding should map to a tagging rule violation. Let's verify the output is correct — trace one finding back to the rule and the resource.

---

### 1) View the structured findings

```bash
python3 sections/07-llm-structured-agent/agent.py | python3 -m json.tool
```

**What it does:** Runs the agent again and pretty-prints the output. Each ticket in the `tickets` array is a structured finding.

> *Talking point: "Run it twice — the structure stays the same even if the exact wording changes. The schema is deterministic; the LLM fills in the details."*

---

### 2) Pick one finding and trace it

Look at the first ticket in the output. Note:
- `namespace` — which namespace is affected
- `resource_name` — which resource
- `resource_kind` — Deployment, Service, PVC, etc.
- `category` — what rule it violates (e.g. `missing-owner`, `missing-cost-center`)
- `priority` — how severe

Now verify with kubectl:

```bash
kubectl get deployments -n payment --show-labels
```

**What it does:** Shows the actual labels on the deployment. Compare to the finding — does the `owner` label exist?

> *Expected: The deployment is missing the `owner` label, matching the finding.*

> *Talking point: "The LLM did not hallucinate this. It saw the raw data, saw the rule, and produced a structured finding. You can verify every claim with kubectl."*

---

### 3) Check the tagging rules

```bash
cat sections/07-llm-structured-agent/config/tagging-rules.yaml
```

**What it does:** Shows the policy. Find the rule that matches the `category` from the finding.

> *Talking point: "The rule says `owner` is required. The resource does not have it. The LLM connected those two facts into a structured ticket. That is the value of adding policy to raw data."*

---

### 4) Why separate collection from analysis?

> *Talking point: "Section 06 collects — deterministic, testable, no LLM. Section 07 analyzes — applies policy, produces structure. If you mix them, you cannot test collection independently. Keeping them separate means you can swap the LLM without touching data collection."*

---

**Next:** Analysis complete. Next we stand up the issue tracker to receive these findings as tickets → `sections/08-issue-tracker-service`
