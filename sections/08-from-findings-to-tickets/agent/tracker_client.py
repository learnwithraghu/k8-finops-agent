import logging
import os
from contextlib import AsyncExitStack

from mcp.client.sse import sse_client

try:
    from mcp import ClientSession
except ImportError:
    from mcp.client.session import ClientSession

from models import TicketBatch

logger = logging.getLogger(__name__)


async def post_tickets(batch: TicketBatch) -> None:
    if not batch.tickets:
        logger.info("No tickets to create.")
        return

    tracker_url = os.getenv("TRACKER_MCP_URL", "http://localhost:8086/sse")

    async with AsyncExitStack() as stack:
        logger.info("Connecting to Issue Tracker MCP server at %s...", tracker_url)
        read_stream, write_stream = await stack.enter_async_context(sse_client(tracker_url))
        session = await stack.enter_async_context(ClientSession(read_stream, write_stream))
        await session.initialize()

        for idx, ticket in enumerate(batch.tickets, start=1):
            logger.info(
                "[%s/%s] Creating ticket for %s (%s)...",
                idx,
                len(batch.tickets),
                ticket.resource_name,
                ticket.namespace,
            )
            payload = ticket.model_dump()
            payload["labels"] = ",".join(payload.get("labels", []))

            try:
                resp = await session.call_tool("create_issue", payload)
                for item in resp.content:
                    if item.type == "text":
                        logger.info("  Result: %s", item.text)
            except Exception as exc:
                logger.error("  Error creating ticket: %s", exc)
