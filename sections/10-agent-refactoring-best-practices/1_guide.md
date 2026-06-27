# Demo 1: Structuring for Scale and Maintainability

**Time Budget:** 4-5 mins

### 1) The Problem with Monoliths
> *Talking point: In Section 09, our agent reached over 140 lines of code in a single file (`agent.py`). It handled cluster communication, JSON parsing, Pydantic data modeling, LLM API calls, and Issue Tracker SSE integration. If we leave it like this, it becomes a nightmare to test and maintain.*

### 2) The Proposed Refactored Architecture
Instead of one massive script, enterprise agents should be split by responsibility. We recommend creating an `agent/` package with the following structure:

```text
agent/
├── __init__.py
├── models.py     (Pydantic schemas like TrackerTicket and TicketBatch)
├── collector.py  (MCP Stdio client logic for fetching K8s resources)
├── analyzer.py   (LangChain and OpenAI invocation logic)
├── tracker.py    (MCP SSE client logic for posting issues)
└── main.py       (The orchestrator that glues the components together)
```

### 3) Code Separation Strategies

**1. `models.py`**
Extract all Pydantic classes (`TrackerTicket`, `TicketBatch`). 
> *Benefit: Other files can import these definitions without causing circular dependencies. It also makes data contracts explicitly clear.*

**2. `collector.py`**
Move the `collect_snapshot()` function here.
> *Benefit: You can write unit tests for the collector using a mocked `mcp` client, completely independent of the LLM or Tracker.*

**3. `analyzer.py`**
Move the `analyze_snapshot()` function here.
> *Benefit: The prompt engineering and LLM logic are isolated. You can easily swap out OpenAI for Anthropic or a local model in the future without touching the data collection logic.*

**4. `tracker.py`**
Move the `post_tickets()` function here.
> *Benefit: Simplifies integration testing and makes the downstream issue tracking service completely modular.*

**5. `main.py`**
This becomes the lightweight entry point:
```python
# Pseudo-code for a refactored main.py
async def main():
    snapshot = await collect_snapshot()
    batch = analyze_snapshot(snapshot, tagging_rules)
    await post_tickets(batch)
```

### 4) Discussion
> *Talking point: We've gone ahead and structured this for you! Take a look at the files in `sections/10-agent-refactoring-best-practices`. Let's test it out to prove it works identically to Section 09 but with a cleaner architecture.*

### 5) Run the Refactored Agent
Make sure your Supergateway (Section 05) and Issue Tracker (Section 08) are still running in the background.

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r sections/10-agent-refactoring-best-practices/requirements.txt

# Run the refactored main agent
python3 sections/10-agent-refactoring-best-practices/main.py
```

> *Expected: You should see the exact same output as Section 09, but the underlying code is now scalable and maintainable!*
