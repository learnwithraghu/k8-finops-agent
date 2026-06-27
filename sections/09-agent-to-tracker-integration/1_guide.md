# Demo 1: The Full End-to-End Agent

**Time Budget:** 3-4 mins

> *Note: Ensure your `supergateway` from Section 05 is still running in the background!*

### 1) Ensure the tracker is running
*(If it is already running from Section 08, skip this)*
```bash
docker run -d --rm -p 8085:8000 -p 8086:8001 --name finops-issue-tracker finops-issue-tracker:latest
```

### 2) Inspect the new script
```bash
cat sections/09-agent-to-tracker-integration/agent.py
```
> *Talking point: We've now added MCP SSE client logic to our agent to POST the structured output directly into the Issue Tracker, using `call_tool("create_issue")`.*

### 3) Run the full agent
```bash
python3 sections/09-agent-to-tracker-integration/agent.py
```
