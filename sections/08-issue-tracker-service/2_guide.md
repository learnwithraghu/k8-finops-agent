# Demo 2: Manually Creating Issues from Findings

**Time Budget:** 4-5 mins

### 1) Create a ticket through the REST API
```bash
curl -X POST http://localhost:8085/create-issue \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "[FinOps] payment/payment-processor - UNALLOCATED ($8.47/month)",
    "summary": "Missing cost-center and owner metadata",
    "body": "Bedrock flagged this as a tech-debt item.",
    "namespace": "payment",
    "resource_name": "payment-processor",
    "resource_kind": "Deployment",
    "category": "unallocated",
    "priority": "high",
    "cost_impact": 8.47,
    "suggested_owner": "payment-team",
    "suggested_cost_center": "payment",
    "reasoning": "Missing cost-center tag means the workload cannot be billed correctly.",
    "source": "bedrock"
  }'
```
> *Talking point: Switch to browser to show the new ticket on the board.*

### 2) Validate MCP endpoint
```bash
cat sections/08-issue-tracker-service/service/app/mcp_server.py

curl -s http://localhost:8086/mcp -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python3 -m json.tool
```

### 3) Create a ticket through MCP
```bash
curl -s http://localhost:8086/mcp -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "id": 2,
    "params": {
      "name": "create_issue",
      "arguments": {
        "title": "[MCP] payment/payment-processor - UNALLOCATED",
        "summary": "Created via MCP tool call",
        "namespace": "payment",
        "resource_name": "payment-processor",
        "resource_kind": "Deployment",
        "category": "unallocated",
        "priority": "high",
        "cost_impact": 8.47,
        "suggested_owner": "payment-team",
        "source": "mcp-agent"
      }
    }
  }' | python3 -m json.tool
```
> *Expected: See the second ticket appear on the Kanban board.*
