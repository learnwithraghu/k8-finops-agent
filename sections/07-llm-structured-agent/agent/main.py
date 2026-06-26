"""Entry point for the Section 07 LLM structured agent.

Consumes a raw cluster snapshot (produced by Section 06) and emits structured
FinOps findings as a TicketBatch. Analysis-only: no collection, no tracker
posting (those live in Sections 06 and 09 respectively).
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

from agent.analyser import analyze_snapshot
from agent.models import TicketBatch

REPO_ROOT = Path(__file__).resolve().parents[3]
TAGGING_RULES_PATH = Path(__file__).parent.parent / "config" / "tagging-rules.yaml"
ROOT_ENV_PATH = REPO_ROOT / ".env"


def _load_snapshot(snapshot_path: str | None) -> dict:
    """Load the Section 06 snapshot from a file path or stdin."""
    if snapshot_path:
        data = json.loads(Path(snapshot_path).read_text())
    else:
        logger.info("--snapshot not provided; reading Section 06 snapshot from stdin")
        data = json.loads(sys.stdin.read())
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Section 07 LLM structured agent")
    parser.add_argument(
        "--snapshot",
        default=os.getenv("SNAPSHOT_PATH"),
        help="Path to the Section 06 raw snapshot JSON (default: stdin or $SNAPSHOT_PATH)",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    if ROOT_ENV_PATH.exists():
        load_dotenv(ROOT_ENV_PATH)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not set in environment or .env file")
        raise SystemExit(1)

    # TODO(work-on-first-agent): wire the live 06 -> 07 handoff (collector emits
    # snapshot to a known path; this agent reads it). For now --snapshot / stdin
    # is the contract.
    snapshot = _load_snapshot(args.snapshot)

    bundle = analyze_snapshot(
        snapshot=snapshot,
        tagging_rules=yaml.safe_load(TAGGING_RULES_PATH.read_text()) or {},
        model_id=os.getenv("OPENAI_MODEL_ID", "gpt-4o"),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.ai.kodekloud.com/v1"),
        api_key=api_key,
        max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "2048")),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.2")),
    )

    print(bundle.model_dump_json(indent=2))
    logger.info("Section 07 analysis completed: %s ticket(s)", len(bundle.tickets))


if __name__ == "__main__":
    main()
