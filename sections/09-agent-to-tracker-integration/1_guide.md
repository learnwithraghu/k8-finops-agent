# Demo 1: Testing Integration and Idempotency

**Time Budget:** 3-4 mins

### 1) Ensure the tracker is running
```bash
docker run --rm -p 8085:8000 -p 8086:8001 --name finops-issue-tracker finops-issue-tracker:latest
```
*(If it is already running from Section 08, skip this)*

### 2) Check environment configuration
```bash
grep -nE '^(OPENAI_BASE_URL|OPENAI_API_KEY|OPENAI_MODEL_ID|ISSUE_TRACKER_MCP_URL)=' .env
```
> *Expected: Ensure `ISSUE_TRACKER_MCP_URL` points to `http://localhost:8086/mcp`.*

### 3) Inspect MCP tracker client and main logic
```bash
cat sections/09-agent-to-tracker-integration/agent/tracker.py
cat sections/09-agent-to-tracker-integration/agent/main.py
```
> *Talking point: Compare 15 lines of MCP client code to the legacy 104-line REST client.*
