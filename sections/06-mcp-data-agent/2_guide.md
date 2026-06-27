# Demo 2: Inspecting the Unstructured Snapshot

**Time Budget:** 2-3 mins

### 1) Run the agent
```bash
python3 sections/06-mcp-data-agent/agent.py > k8s_metadata.json
cat k8s_metadata.json | jq 'del(.resources[].annotations)' | head -n 20
```

### 2) Discussion
> *Talking point: Notice we stop at unstructured data here. We keep collection deterministic. LLM analysis happens in Section 07.*
