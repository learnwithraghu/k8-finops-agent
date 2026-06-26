#!/usr/bin/env python3
import asyncio, json, os, shlex, sys
from pathlib import Path
from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

async def fetch_namespaces(command, args):
    params = StdioServerParameters(command=command, args=args, env=os.environ.copy())
    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            response = await session.call_tool("kubectl_get", {"resourceType": "namespaces", "allNamespaces": True, "output": "json"})
    text = "".join(getattr(p, "text", "") for p in getattr(response, "content", []) if getattr(p, "type", "") == "text")
    items = json.loads(text).get("items", []) if text else []
    return [i.get("name") or i.get("metadata", {}).get("name") for i in items if i.get("name") or i.get("metadata", {}).get("name")]

def main():
    env_file = Path(__file__).resolve().parents[2] / ".env"
    if env_file.exists():
        load_dotenv(env_file)
    command = os.getenv("MCP_SERVER_COMMAND", "docker")
    kubeconfig_file = os.getenv("KUBECONFIG_FILE") or os.getenv("KUBECONFIG") or str(Path.home() / ".kube" / "config")
    default_args = f"run --rm -i --network host --user 0:0 -v {kubeconfig_file}:/kubeconfig:ro -e KUBECONFIG=/kubeconfig mcp/kubernetes:latest"
    args = shlex.split(os.getenv("MCP_SERVER_ARGS", default_args))
    prompt = " ".join(sys.argv[1:]) or "show namespaces"
    namespaces = asyncio.run(fetch_namespaces(command, args))
    print("Prompt:", prompt)
    print("Result:", namespaces[:10])

if __name__ == "__main__":
    main()
