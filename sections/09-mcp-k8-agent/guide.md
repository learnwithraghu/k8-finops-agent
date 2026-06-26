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

## Step 3: Install Section 09 dependencies
Run:

```bash
python3 -m pip install -r sections/09-mcp-k8-agent/requirements.txt
```

Expected:
- only Section 09 MCP + LLM dependencies are installed

## Step 4: Super simple MCP prompt -> result flow
Set MCP runtime variables in the same shell:

```bash
export KUBECONFIG_FILE="${KUBECONFIG:-$HOME/.kube/config}"
export MCP_SERVER_COMMAND=docker
export MCP_SERVER_ARGS="run --rm -i --network host --user 0:0 -v ${KUBECONFIG_FILE}:/kubeconfig:ro -e KUBECONFIG=/kubeconfig mcp/kubernetes:latest"
```

Make sure root `.env` contains your OpenAI-compatible settings (`OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL_ID`).

Then run one tiny script that:
- asks MCP for namespaces
- sends your prompt + MCP context to the LLM
- prints the result

```bash
python3 sections/09-mcp-k8-agent/simple_mcp_prompt.py "What does MCP see in this cluster, and is payment namespace present?"
```

Expected:
- script completes successfully
- you see MCP namespace data printed
- you see an LLM response based on MCP data

## Step 5: Run read-only MCP queries
Try a second prompt:

```bash
python3 sections/09-mcp-k8-agent/simple_mcp_prompt.py "Give me a short health summary from namespace data only."
```

Expected:
- MCP query succeeds again
- LLM output changes according to your prompt

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
- In Codespaces/local container networking, use `--network host` in `MCP_SERVER_ARGS` so MCP can reach the Kubernetes API endpoint from kubeconfig.
- If collector checks fail with missing file, verify `KUBECONFIG_FILE` points to a real kubeconfig.
- If permissions fail, ensure the kubeconfig user has namespace read permissions.

## Expected outcome
You should be able to:
- run an OSS Kubernetes MCP image from Docker Hub
- query local cluster data through MCP tools
- explain how this setup feeds advanced automation in Section 10
