# Demo 2: Inspecting the Unstructured Snapshot

**Time Budget:** 2-3 mins

### 1) Run the agent
```bash
python3 sections/06-mcp-data-agent/agent.py > k8s_metadata.json
cat k8s_metadata.json | jq 'del(.resources[].annotations)' | head -n 20
```

### 2) Discussion
> *Talking point: Notice we stop at unstructured data here. We keep collection deterministic. LLM analysis happens in Section 07.*

---

**Try it:** Open [`architecture_builder/index.html`](architecture_builder/index.html) in your browser to build the **collection hub** — MCP spokes merge into one unstructured JSON sink (no LLM). Use **Need a hint?** if stuck, then press **Collect Snapshot** to validate.
