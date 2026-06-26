"""Entry point for the MCP-powered K8s FinOps agent."""

from __future__ import annotations

import argparse
import json
import logging
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

from agent.analyser import analyze_snapshot
from agent.collector import collect_snapshot_sync
from agent.tracker import post_tickets

REPO_ROOT = Path(__file__).resolve().parents[3]
TAGGING_RULES_PATH = Path(__file__).parent.parent / "config" / "tagging-rules.yaml"
ROOT_ENV_PATH = REPO_ROOT / ".env"


def main() -> None:
    parser = argparse.ArgumentParser(description="MCP-powered K8s FinOps agent")
    parser.add_argument("--dump-raw", action="store_true", help="Print the raw snapshot JSON before the report")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(__name__)

    if ROOT_ENV_PATH.exists():
        load_dotenv(ROOT_ENV_PATH)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not set in environment or .env file")
        raise SystemExit(1)

    snapshot = collect_snapshot_sync(cluster_name=os.getenv("CLUSTER_NAME", "kind"))
    if args.dump_raw:
        print(json.dumps(snapshot, indent=2))

    bundle = analyze_snapshot(
        snapshot=snapshot,
        tagging_rules=yaml.safe_load(TAGGING_RULES_PATH.read_text()) or {},
        model_id=os.getenv("OPENAI_MODEL_ID", "gpt-4o"),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.ai.kodekloud.com/v1"),
        api_key=api_key,
        max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "2048")),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.2")),
    )

    tracker_result = post_tickets(
        base_url=os.getenv("ISSUE_TRACKER_URL", "http://localhost:8085"),
        tickets=bundle.tickets,
        timeout=int(os.getenv("ISSUE_TRACKER_TIMEOUT", "10")),
    )

    print(json.dumps(bundle.model_dump(), indent=2))
    print(json.dumps(tracker_result, indent=2))
    logger.info("MCP FinOps pipeline completed successfully")


if __name__ == "__main__":
    main()
