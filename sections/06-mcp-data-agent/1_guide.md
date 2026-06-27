# Demo 1: Running the Data Agent

**Time Budget:** 3-4 mins

> *Note: Ensure your `supergateway` from Section 05 is still running in the background!*

### 1) Install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r sections/06-mcp-data-agent/requirements.txt
```

### 2) Inspect the agent script
```bash
cat sections/06-mcp-data-agent/agent.py
```
> *Talking point: This is our base agent. It connects to the Kubernetes MCP via SSE to our supergateway, calls the tool to list resources, and prints the raw JSON.*
