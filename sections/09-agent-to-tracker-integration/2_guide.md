# Demo 2: Verifying the Automation

**Time Budget:** 4-5 mins

### 1) Verify tickets in the UI
- Open: `http://localhost:8085`
> *Talking point: Our end-to-end flow is complete! We pulled raw cluster data via an MCP standard IO client, passed it to a structured LLM, and posted the resulting tickets back to our Tracker using an MCP SSE client.*

### 2) Cleanup
```bash
docker stop finops-issue-tracker
```
