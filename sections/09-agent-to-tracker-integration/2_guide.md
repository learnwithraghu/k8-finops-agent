# Demo 2: Auto-creating and Updating Tickets

**Time Budget:** 4-5 mins

### 1) Run the agent to create tickets
```bash
PYTHONPATH=sections/09-agent-to-tracker-integration python3 -m agent.main
```
> *Talking point: Currently running the transitional flow which scans and calls the LLM. Soon this will just read the TicketBatch from Section 07 directly.*

### 2) Verify tickets in the UI
- Open: `http://localhost:8085`
> *Talking point: Look for the 'mcp-llm-agent' source field. Emphasize idempotency (re-running the agent doesn't spam duplicate tickets).*

### 3) Cleanup
*(Switch to the tracker terminal and press `Ctrl-C` to stop it)*
