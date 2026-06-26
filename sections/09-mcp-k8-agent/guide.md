# Section 09 Guide: MCP Setup for Local Cluster (Docker Hub OSS Image)

This section is setup-only. You do not write custom MCP code here.

## Goal
Use an open-source Kubernetes MCP server image from Docker Hub, connect it to your local cluster, validate read-only tool calls, and establish a clean MCP baseline for later sections.

## Tutor note
Keep this section practical and short:
- no MCP tool authoring
- no custom Python server implementation
- only setup, verify, query, and clean up

## What students will learn
- how to run an OSS MCP image from Docker Hub
- how to wire kubeconfig for MCP server access
- how to verify MCP tool availability and connectivity
- how to run read-only queries for namespaces and workloads
- how to clean up the demo environment after the run

## What you need before starting
Complete Sections 01 through 08 first.

You should already have:
- a working local cluster (Kind)
- the airline app deployed
- Docker running locally
- a valid kubeconfig on the host

## MCP image used in this section
Use this Docker Hub image:
- `mcp/kubernetes:latest`

This image starts an MCP server over stdio and supports Kubernetes read operations.

## Step 0: Validate local cluster access
Run:
```bash
kubectl config current-context
kubectl get ns
```

Expected:
- current context points to your local cluster
- non-system namespaces for your lab are visible

## Step 1: Pull the OSS MCP image
Run:
```bash
docker pull mcp/kubernetes:latest
```

Expected:
- image pulls successfully

## Step 2: Pick the kubeconfig file to mount
Use this to derive the kubeconfig path:

```bash
export KUBECONFIG_FILE="${KUBECONFIG:-$HOME/.kube/config}"
test -f "$KUBECONFIG_FILE" && echo "Using $KUBECONFIG_FILE"
```

Expected:
- kubeconfig file path resolves correctly

## Step 3: Install collector dependencies
Run:

```bash
python3 -m pip install -r sections/10-advanced-mcp-finops/requirements.txt
```

Expected:
- Python MCP client dependencies are installed

## Step 4: Verify MCP by querying through the Docker image
Set MCP runtime variables in the same shell:

```bash
export KUBECONFIG_FILE="${KUBECONFIG:-$HOME/.kube/config}"
export MCP_SERVER_COMMAND=docker
export MCP_SERVER_ARGS="run --rm -i --user 0:0 -v ${KUBECONFIG_FILE}:/kubeconfig:ro -e KUBECONFIG=/kubeconfig mcp/kubernetes:latest"
```

Then run a quick collector check that uses Docker as the MCP server process:

```bash
python3 - <<'PY'
from pathlib import Path
import sys

sys.path.insert(0, str(Path("sections/10-advanced-mcp-finops").resolve()))
from agent.collector import collect_snapshot_sync

snapshot = collect_snapshot_sync(cluster_name="kind")
print("namespaces:", len(snapshot.get("namespaces", [])))
print("resources:", len(snapshot.get("resources", [])))
print("sample_namespaces:", snapshot.get("namespaces", [])[:5])
PY
```

Expected:
- command completes successfully
- non-zero namespace/resource counts are returned

## Step 5: Run read-only MCP queries
Inspect a small portion of raw MCP-collected data:

```bash
python3 - <<'PY'
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path("sections/10-advanced-mcp-finops").resolve()))
from agent.collector import collect_snapshot_sync

snapshot = collect_snapshot_sync(cluster_name="kind")
print(json.dumps({
    "namespaces": snapshot.get("namespaces", [])[:5],
    "resources_sample": snapshot.get("resources", [])[:5],
}, indent=2))
PY
```

Expected:
- responses are structured and parseable
- returned namespace/workload data matches `kubectl` spot checks

## Step 6: Discuss FinOps relevance
Use returned metadata to explain:
- ownership visibility
- label/tag completeness checks
- where compliance analysis can be layered next

Note: Advanced collector/analyst/tracker flow is in Section 10.

## Step 7: Cleanup
No long-running local MCP process is required in this flow because Docker is invoked per collection run.

Optional cleanup:
```bash
docker image rm mcp/kubernetes:latest
```

## Troubleshooting
- If no cluster data appears, verify kubeconfig mount and context.
- If collector checks fail with kubeconfig permission issues, keep `--user 0:0` in `MCP_SERVER_ARGS`.
- If collector checks fail with missing file, verify `KUBECONFIG_FILE` points to a real kubeconfig.
- If permissions fail, ensure the kubeconfig user has namespace read permissions.

## Expected outcome
You should be able to:
- run an OSS Kubernetes MCP image from Docker Hub
- query local cluster data through MCP tools
- explain how this setup feeds advanced automation in Section 10
