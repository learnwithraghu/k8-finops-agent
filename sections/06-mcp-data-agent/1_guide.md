# Demo 1: Running the Data Agent

**Time Budget:** 3-4 mins

### 1) Start the MCP HTTP endpoint
```bash
export KUBECONFIG_FILE="${KUBECONFIG:-$HOME/.kube/config}"
npx -y supergateway \
  --stdio "docker run --rm -i --network host --user 0:0 -v ${KUBECONFIG_FILE}:/kubeconfig:ro -e KUBECONFIG=/kubeconfig mcp/kubernetes:latest" \
  --outputTransport streamableHttp --streamableHttpPath /mcp --port 8000 --healthEndpoint /healthz
```
*(Leave this terminal running and open a new one)*

### 2) Verify endpoint
```bash
curl -s http://localhost:8000/healthz
```

### 3) Install dependencies
```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r sections/06-mcp-data-agent/requirements.txt
```

### 4) Inspect the collector script
```bash
cat sections/06-mcp-data-agent/agent/collector.py
```
> *Talking point: This is just a scaffold for the agent we will build next. It connects to the HTTP MCP endpoint and dumps unstructured JSON.*
