# Video 5: Fix Truncated Audit Output

**Time Budget:** 2–3 mins

**Prerequisites:** [`4_guide.md`](4_guide.md) — policy auditor run at least once; virtualenv activated.

> **Legend:** Blockquote lines are on-screen actions — do not read them aloud. Everything else is your script.

---

### Opening (~15 sec)

You ran the policy auditor and got a label audit — but the report stopped mid-namespace. That is a token limit issue, not a cluster or MCP problem. Let's trace where the limit is set and raise it.

> **Do:** Open `sections/07-llm-structured-agent/code/structured_auditor.py` in the editor.

---

### Step 1 — Spot the truncation

Scroll to the bottom of your last audit output.

**What to look for:**
- Report cuts off inside a namespace (for example, `inventory-config` labels end at `app.`)
- No closing summary across all namespaces
- Last paragraph ends abruptly — no natural finish

> **Say:** "The agent gathered all the data. The answer just ran out of room to print it."

---

### Step 2 — Find the limit in `structured_auditor.py`

Open the `main` function near the bottom of the file:

```python
async def main() -> None:
    print(
        await run_agent(
            PROMPT,
            tagging_rules=load_tagging_rules(),
            max_tokens=4096,
        )
    )
```

**What it does:** `max_tokens` caps how many tokens the LLM can write in its final answer. A namespace-by-namespace audit across six application namespaces needs more than a short namespace list.

> **Do:** Point at `max_tokens=4096`.

---

### Step 3 — See where the value flows

Open `sections/07-llm-structured-agent/code/mcp_client.py` and find `build_llm`:

```python
def build_llm(max_tokens: int | None = None) -> ChatOpenAI:
    return ChatOpenAI(
        model=os.environ["OPENAI_MODEL_ID"],
        base_url=os.environ["OPENAI_BASE_URL"],
        api_key=os.environ["OPENAI_API_KEY"],
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.3")),
        max_tokens=max_tokens or int(os.getenv("OPENAI_MAX_TOKENS", "512")),
    )
```

**The chain:**
1. `structured_auditor.py` passes `max_tokens=4096` into `run_agent`
2. `run_agent` passes it into `build_llm`
3. `build_llm` uses that value for `ChatOpenAI(max_tokens=...)`
4. If you omit `max_tokens`, it falls back to `OPENAI_MAX_TOKENS` in `.env` (default `512`)

> **Say:** "Same pattern as Section 06's label auditor — caller sets the limit when the answer needs more room."

---

### Step 4 — Reproduce the problem (optional demo beat)

Temporarily lower the limit to show truncation:

```python
            max_tokens=2048,
```

Run the auditor:

```bash
python3 sections/07-llm-structured-agent/code/structured_auditor.py
```

> **Expected:** Output may cut off before the last namespaces finish — same symptom you saw earlier.

> **Do:** Scroll to the end of the truncated run. Show where the report stops.

---

### Step 5 — Raise the limit and re-run

Restore a higher limit:

```python
            max_tokens=4096,
```

Re-run:

```bash
python3 sections/07-llm-structured-agent/code/structured_auditor.py
```

> **Expected:** Full audit — every application namespace covered, report ends with a complete summary.

> **Do:** Scroll to the bottom. Confirm the last namespace and summary are present.

---

### When to adjust

| Symptom | Fix |
|---------|-----|
| Report cuts off mid-namespace | Increase `max_tokens` in `structured_auditor.py` |
| Very short one-line answers | Check you are passing `max_tokens` — default `.env` fallback is `512` |
| Still truncated at 4096 | Try `8192` if your model supports it, or ask for a shorter summary in the prompt |

> **Say:** "Start with 4096 for a full cluster audit. Tune up only if you still see truncation."

---

### Close (~10 sec)

Truncation fixed — same agent, same rules file, just more room for the answer. Section 07 complete.

> **Do:** Save `structured_auditor.py` with `max_tokens=4096`. Keep the MCP container running if continuing to later sections.
