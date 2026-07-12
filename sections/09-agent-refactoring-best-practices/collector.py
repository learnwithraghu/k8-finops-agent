import os
import json
import logging
from contextlib import AsyncExitStack
from pathlib import Path
try:
    from mcp import ClientSession
except ImportError:
    from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

logger = logging.getLogger(__name__)

RESOURCE_TYPES = ["deployments", "pods", "services", "pvc", "configmaps"]

def _decode(resp) -> dict:
    for content in resp.content:
        if content.type == "text":
            text = content.text
            if text:
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    pass
    return {"items": []}

async def collect_snapshot() -> dict:
    kubeconfig = os.getenv("KUBECONFIG_FILE") or os.getenv("KUBECONFIG") or str(Path.home() / ".kube" / "config")
    server_params = StdioServerParameters(
        command="docker",
        args=["run", "--rm", "-i", "--network", "host", "--user", "0:0", "-v", f"{kubeconfig}:/kubeconfig:ro", "-e", "KUBECONFIG=/kubeconfig", "mcp/kubernetes:latest"],
        env=os.environ.copy()
    )
    async with AsyncExitStack() as stack:
        logger.info("Connecting to Kubernetes MCP server...")
        read_stream, write_stream = await stack.enter_async_context(stdio_client(server_params))
        session = await stack.enter_async_context(ClientSession(read_stream, write_stream))
        await session.initialize()
        
        payload = _decode(await session.call_tool("kubectl_get", {"namespace": "", "resourceType": "namespaces"}))
        namespaces = [item["name"] for item in payload.get("items", []) if item.get("name")]
        
        resources = []
        for ns in namespaces:
            if ns.startswith("kube-") or ns == "local-path-storage":
                continue
            for r_type in RESOURCE_TYPES:
                resp = await session.call_tool("kubectl_get", {"namespace": ns, "resourceType": r_type})
                items = _decode(resp).get("items", [])
                for item in items:
                    item.pop("annotations", None)
                resources.extend(items)

        resources.sort(key=lambda item: (item.get("namespace", ""), item.get("kind", ""), item.get("name", "")))
        
        return {
            "timestamp": "2026-06-27T12:00:00Z",
            "cluster": "kind-finops-cluster",
            "resources": resources
        }
