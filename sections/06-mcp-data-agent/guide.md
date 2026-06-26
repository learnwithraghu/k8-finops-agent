# Section 06 Guide: First MCP Data Agent

> Status: **skeleton**. The `agent/collector.py` in this folder is the starting point moved over from the previous advanced pipeline. The follow-up "work on 1st agent" session adapts it into the prompt → MCP → unstructured data flow described here.

## Goal
A tiny Python agent that reuses the Section 05 MCP endpoint, calls `kubectl_get` tools, and prints raw cluster snapshot JSON. No LLM, no tagging rules, no structured output — just prompt → MCP → unstructured data.

## Prerequisites
Complete Sections 01 through 05 first.

You should already have:
- the local kind cluster running (Section 01 / 02)
- the Section 05 MCP endpoint validated with curl
- the airline app deployed
- Python 3.10+ and the section `requirements.txt` installed

## Step 0: Re-confirm the Section 05 MCP endpoint
Start the MCP HTTP endpoint exactly as in Section 05:
```bash
export KUBECONFIG_FILE="${KUBECONFIG:-$HOME/.kube/config}"
npx -y supergateway \
  --stdio "docker run --rm -i --network host --user 0:0 -v ${KUBECONFIG_FILE}:/kubeconfig:ro -e KUBECONFIG=/kubeconfig mcp/kubernetes:latest" \
  --outputTransport streamableHttp --streamableHttpPath /mcp --port 8000 --healthEndpoint /healthz
```
Verify in another terminal:
```bash
curl -s http://localhost:8000/healthz   # ok
```

## Step 1: Install Section 06 dependencies
```bash
python3 -m pip install -r sections/06-mcp-data-agent/requirements.txt
```

## Step 2: Read the collector starting point
```bash
cat sections/06-mcp-data-agent/agent/collector.py
```
Note: this file was moved from the previous advanced pipeline and is a **starting point only**. The next session adapts it so it:
- talks to the Section 05 MCP HTTP endpoint (not raw stdio Docker)
- accepts a prompt and emits raw unstructured snapshot JSON
- does not yet touch the LLM or tagging rules

## Step 3: Run the agent (to be wired in the next session)
The follow-up "work on 1st agent" session will provide the run command and the expected unstructured snapshot output. Until then, this section is scaffold-only.

## Step 4: What the output should look like (target shape)
The unstructured snapshot is plain JSON — namespaces plus per-namespace resources, no LLM commentary, no severity field, no ticket schema:
```json
{
  "scanned_at": "2026-06-26T21:00:00Z",
  "cluster": "kind",
  "namespaces": ["airline", "booking-api", "flight-search", "inventory", "payment"],
  "resources": [
    { "namespace": "payment", "kind": "Deployment", "name": "payment-gateway", ... },
    ...
  ]
}
```

## Step 5: Discussion
- Why we stop at unstructured data here (keeping collection deterministic)
- Why the LLM + tagging rules belong in Section 07, not here
- How the Section 07 structured agent will consume this snapshot as its input

## Cleanup
Ctrl-C the Section 05 MCP endpoint process when done. No cluster changes are made by this agent — it is read-only.

## Expected outcome
You should be able to describe:
- the prompt → MCP tool call → raw data loop
- why this output is deliberately unstructured
- how Section 07 builds on this snapshot to add LLM analysis and structured findings