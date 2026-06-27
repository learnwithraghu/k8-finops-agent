# Demo 2: Inspecting the Unstructured Snapshot

**Time Budget:** 2-3 mins

### 1) Target Output Format
*(Run the agent command once it's implemented. The expected output is plain JSON.)*
```json
{
  "scanned_at": "2026-06-26T21:00:00Z",
  "cluster": "kind",
  "namespaces": ["airline", "booking-api", "flight-search", "inventory", "payment"],
  "resources": [
    { "namespace": "payment", "kind": "Deployment", "name": "payment-gateway" }
  ]
}
```

### 2) Discussion
> *Talking point: Notice we stop at unstructured data here. We keep collection deterministic. LLM analysis happens in Section 07.*

### 3) Cleanup
*(Go back to the Supergateway terminal and press `Ctrl-C` to stop it)*
