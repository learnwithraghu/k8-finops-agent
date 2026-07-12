# Video 4: Run the Policy Auditor

**Time Budget:** 3–4 mins

**Prerequisites:** [`3_guide.md`](3_guide.md) — understand `structured_auditor.py`; MCP container running; virtualenv activated.

> **Legend:** Blockquote lines are on-screen actions — do not read them aloud. Everything else is your script.

---

### Opening (~15 sec)

We walked through the code. Now let's run it. The agent loads tagging rules from file, calls MCP tools, and prints a policy-aware label audit to the terminal.

> **Do:** Open a terminal at the repo root. Activate the virtualenv.

---

### Step 1 — Validate MCP is alive

```bash
source .venv/bin/activate
python3 sections/06-mcp-data-agent/code/validate_mcp.py
```

Quick smoke check before the LLM call. Same pattern as Section 06 — Python validation, no curl.

> **Expected:** `MCP OK — N namespaces via kubectl_get` followed by a namespace list.

---

### Step 2 — Run the policy auditor

```bash
python3 sections/07-llm-structured-agent/code/structured_auditor.py
```

This loads `config/tagging-rules.yaml`, connects to MCP, lets the agent choose `kubectl_get` calls, evaluates labels against the rules, and prints a plain-English summary.

> **Expected:** A multi-paragraph audit grouped by namespace, flagging resources that violate required tags from the rules file.

---

### Step 3 — Read the output

Look for three things in the answer:

**Namespace coverage** — application namespaces listed, system namespaces skipped per `excluded_namespaces`.

**Per-resource detail** — name, kind, and labels as returned by MCP tools.

**Policy gaps** — flags for missing `owner`, `cost-center`, `environment`, or other `required_tags` from the rules file.

> **Do:** Scroll through the output. Point at one flagged resource and the rule it violates.

---

### Compare to Section 06

Run Section 06's label auditor for contrast:

```bash
python3 sections/06-mcp-data-agent/code/label_auditor.py
```

Both scripts use the same agent path. Section 07's answer should reference the full rules file — not just owner and cost-center hard-coded in the prompt.

> **Say:** "Same agent. Section 07 just has a policy file behind it."

---

### Close (~10 sec)

Policy-aware audit on screen. Section 07 complete — same agent as Section 06, with tagging rules from file.

> **Do:** Keep the MCP container running if continuing to later sections.
