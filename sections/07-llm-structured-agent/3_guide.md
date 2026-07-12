# Video 3: Walk the Policy Auditor

**Time Budget:** 4–5 mins

**Prerequisites:** [`2_guide.md`](2_guide.md) — understand tagging rules file; MCP container running; virtualenv activated.

> **Legend:** Blockquote lines are on-screen actions — do not read them aloud. Everything else is your script.

---

### Opening (~20 sec)

In Videos 1 and 2 we covered the why — policy from file on the same agent path as Section 06. Now let's walk through `structured_auditor.py`. Same thin shape as `label_auditor.py` — a prompt, a call into `mcp_client`, and a print.

> **Do:** Open `sections/07-llm-structured-agent/code/structured_auditor.py` in the editor.

---

### Block 1 — Module docstring (line 1)

```python
"""Ask a LangChain agent to audit labels against tagging rules and print its final answer."""
```

Same agent path as Section 06. The only addition is loading tagging rules from file.

---

### Block 2 — Imports and path (lines 2–8)

```python
import asyncio
from pathlib import Path

from mcp_client import run_agent

TAGGING_RULES_PATH = Path(__file__).parents[1] / "config" / "tagging-rules.yaml"
```

`run_agent` is the same helper as Section 06, extended with an optional `tagging_rules` argument. `TAGGING_RULES_PATH` points at the policy file — we read it at runtime.

---

### Block 3 — The instruction prompt (lines 10–24)

```python
PROMPT = """
You are auditing Kubernetes resource labels for FinOps governance through MCP tools.

Use the available Kubernetes MCP tools to:
1. List all namespaces.
2. For each application namespace (skip kube-* and excluded namespaces from the rules),
   fetch deployments, configmaps, and persistent volume claims.
3. Report each resource's name, namespace, kind, and labels exactly as returned by the tools.
4. Evaluate each resource against the tagging rules provided separately.
5. Flag resources that violate required tags or label mappings.
6. Summarize the label audit in plain English, grouped by namespace.

Use only data returned by the tools. Do not invent labels or resources.
"""
```

Instruction only — what to do. No YAML here. Compare to Section 06's `label_auditor.py`: same steps, but step 4 now says "evaluate against the tagging rules provided separately."

---

### Block 4 — Load tagging rules from file (lines 27–30)

```python
def load_tagging_rules() -> str:
    if not TAGGING_RULES_PATH.exists():
        raise FileNotFoundError(f"Tagging rules not found: {TAGGING_RULES_PATH}")
    return TAGGING_RULES_PATH.read_text()
```

Policy lives in `config/tagging-rules.yaml`. Change the file, re-run — no prompt edits.

---

### Block 5 — `main` (lines 33–41)

```python
async def main() -> None:
    print(
        await run_agent(
            PROMPT,
            tagging_rules=load_tagging_rules(),
            max_tokens=2048,
        )
    )
```

Three pieces: instruction prompt, rules from file, print the answer. Inside `mcp_client`, `run_agent` attaches the rules as a system message, runs the ReAct agent with MCP tools, and returns plain text.

---

### Block 6 — `mcp_client.run_agent` (in `code/mcp_client.py`)

```python
async def run_agent(prompt, max_tokens=None, tagging_rules=None) -> str:
    ...
    if tagging_rules:
        messages.append(SystemMessage(content="Apply the tagging rules below...\n" + tagging_rules))
    messages.append(HumanMessage(content=prompt))
```

This is the only plumbing change from Section 06. Rules arrive as a separate system message — not embedded in the prompt constant.

---

### Close (~10 sec)

That's the full script — thin like Section 06, with a rules file. Next we run it and read the audit on screen. Open `4_guide.md`.

> **Do:** Save the file. Keep the MCP container running.
