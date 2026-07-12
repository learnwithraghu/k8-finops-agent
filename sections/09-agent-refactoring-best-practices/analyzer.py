import os
import json
import yaml
import logging
from langchain_openai import ChatOpenAI
from models import TicketBatch

logger = logging.getLogger(__name__)

def analyze_snapshot(snapshot: dict, tagging_rules: dict) -> TicketBatch:
    logger.info("Sending %d resources to LLM", len(snapshot.get("resources", [])))
    
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL_ID", "gpt-4o"),
        base_url="https://api.ai.kodekloud.com/v1",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.2, max_tokens=2048,
    )
    
    sys_prompt = "You are a FinOps assistant. Return ONLY JSON matching schema: {\"tickets\": [TrackerTicket, ...]}"
    prompt = (
        f"Snapshot:\n{json.dumps(snapshot)}\n\nRules:\n{yaml.safe_dump(tagging_rules)}\n"
        "- If an orphaned PVC, or missing cost-center, or no owner, create a ticket.\n"
        "- Do not create tickets for correct resources."
    )
    
    messages = [
        ("system", sys_prompt),
        ("human", prompt)
    ]
    response = llm.invoke(messages)
    content = response.content
    
    if content.startswith("```json"):
        content = content[7:-3]
    elif content.startswith("```"):
        content = content[3:-3]
        
    return TicketBatch.model_validate_json(content)
