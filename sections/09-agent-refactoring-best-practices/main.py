import os
import yaml
import asyncio
import logging
from pathlib import Path

from collector import collect_snapshot
from analyzer import analyze_snapshot
from tracker import post_tickets

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_tagging_rules() -> dict:
    rules_path = Path(__file__).parent / "config" / "tagging-rules.yaml"
    if not rules_path.exists():
        logger.warning(f"Rules not found at {rules_path}, returning empty rules.")
        return {}
    with open(rules_path, "r") as f:
        return yaml.safe_load(f)

async def main():
    logger.info("--- Step 1: Data Collection ---")
    snapshot = await collect_snapshot()
    logger.info(f"Collected {len(snapshot.get('resources', []))} resources.")
    
    logger.info("--- Step 2: LLM Analysis ---")
    rules = load_tagging_rules()
    batch = analyze_snapshot(snapshot, rules)
    logger.info(f"LLM produced {len(batch.tickets)} tickets.")
    
    logger.info("--- Step 3: Issue Tracking ---")
    await post_tickets(batch)
    logger.info("--- Done ---")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable is required")
    asyncio.run(main())
