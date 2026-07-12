# Demo 1: Structuring for Scale and Maintainability

**Time Budget:** 4-5 mins

### 1) Why refactor after Section 08?
> *Talking point: Section 08 kept the integration agent intentionally small — copy Section 06's `mcp_client.py`, add `structure.py` and `tracker_client.py`. That is the right teaching shape. But as we add retries, deduplication, and scheduling, a single orchestration script becomes hard to test. Enterprise agents split by responsibility.*

### 2) The Proposed Refactored Architecture
Instead of one script handling everything, enterprise agents should be split by responsibility:

```text
agent/
├── models.py     (Pydantic schemas like TrackerTicket and TicketBatch)
├── collector.py  (MCP client logic for fetching K8s resources)
├── analyzer.py   (LangChain and OpenAI invocation logic)
├── tracker.py    (MCP SSE client logic for posting issues)
└── main.py       (The orchestrator that glues the components together)
```

### 3) Code Separation Strategies

**1. `models.py`**
Extract all Pydantic classes (`TrackerTicket`, `TicketBatch`).
> *Benefit: Other files can import these definitions without causing circular dependencies. It also makes data contracts explicitly clear.*

**2. `collector.py`**
Move cluster snapshot collection here.
> *Benefit: You can write unit tests for the collector using a mocked MCP client, completely independent of the LLM or Tracker.*

**3. `analyzer.py`**
Move the LLM structuring/analysis logic here.
> *Benefit: Prompt engineering and LLM logic are isolated. You can swap OpenAI for another provider without touching collection or posting.*

**4. `tracker.py`**
Move the `post_tickets()` function here (same pattern as Section 08's `tracker_client.py`).
> *Benefit: Simplifies integration testing and makes the issue tracker service completely modular.*

**5. `main.py`**
This becomes the lightweight entry point:
```python
async def main():
    snapshot = await collect_snapshot()
    batch = analyze_snapshot(snapshot, tagging_rules)
    await post_tickets(batch)
```

### 4) Discussion
> *Talking point: We've structured this for you in `sections/09-agent-refactoring-best-practices`. Let's run it to prove the modular version produces the same end-to-end result as Section 08's integration agent.*

### 5) Run the Refactored Agent
Make sure the K8s MCP container (Section 06) and Issue Tracker (Section 08) are running.

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r sections/09-agent-refactoring-best-practices/requirements.txt

python3 sections/09-agent-refactoring-best-practices/main.py
```

> *Expected: Same ticket creation on the Kanban board as Section 08, but with a cleaner, testable module layout.*
