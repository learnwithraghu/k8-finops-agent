"""Convert a plain-English audit report into structured tracker tickets."""
import logging
import os

from langchain_openai import ChatOpenAI

from models import TicketBatch

logger = logging.getLogger(__name__)


def structure_findings(audit_text: str, tagging_rules: str = "") -> TicketBatch:
    logger.info("Structuring audit report into tracker tickets...")
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL_ID", "gpt-4o"),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.ai.kodekloud.com/v1"),
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.2,
        max_tokens=2048,
    )
    sys_prompt = (
        "You are a FinOps assistant. Return ONLY JSON matching this schema: "
        '{"tickets": [{"title": str, "summary": str, "body": str, "namespace": str, '
        '"resource_name": str, "resource_kind": str, "category": str, '
        '"priority": "critical"|"high"|"medium"|"low", "cost_impact": float, '
        '"suggested_owner": str, "suggested_cost_center": str, "reasoning": str, '
        '"source": "mcp-llm-agent"}]}'
    )
    rules_block = f"\n\nTagging rules (YAML):\n{tagging_rules}" if tagging_rules else ""
    prompt = (
        f"Audit report:\n{audit_text}{rules_block}\n\n"
        "- Create one ticket per distinct finding (missing owner, unallocated cost, orphaned PVC, etc.).\n"
        "- If the report says a resource is compliant, do not create a ticket for it.\n"
        "- Use namespace and resource_name from the report; do not invent resources.\n"
    )
    response = llm.invoke([("system", sys_prompt), ("human", prompt)])
    content = str(getattr(response, "content", response)).strip("` \n")
    if content.startswith("json"):
        content = content[4:].strip()
    batch = TicketBatch.model_validate_json(content)
    logger.info("Structured %s ticket(s)", len(batch.tickets))
    return batch
