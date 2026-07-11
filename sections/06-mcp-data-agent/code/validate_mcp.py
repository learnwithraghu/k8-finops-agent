"""Validate the Section 06 persistent MCP HTTP endpoint (no curl)."""
import asyncio

from mcp_client import decode_tool_result, get_mcp_tools, tool_by_name


async def main() -> None:
    tools, cleanup = await get_mcp_tools()
    try:
        kubectl_get = tool_by_name(tools, "kubectl_get")
        result = await kubectl_get.ainvoke({"resourceType": "namespaces", "allNamespaces": True})
        payload = decode_tool_result(result)
        namespaces = [item["name"] for item in payload.get("items", []) if item.get("name")]
        if not namespaces:
            raise RuntimeError("kubectl_get returned no namespaces — check MCP container and kubeconfig")

        print(f"MCP OK — {len(namespaces)} namespaces via {kubectl_get.name}")
        for name in namespaces:
            print(f"  - {name}")
    finally:
        await cleanup()


if __name__ == "__main__":
    asyncio.run(main())
