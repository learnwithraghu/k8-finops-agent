"""Entry point for the MCP-powered K8s FinOps agent."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda

from agent.analyser import analyze_snapshot
from agent.collector import ClusterCollector
from agent.models import AnalysisEnvelope, ClusterSnapshot
from agent.tracker import IssueTrackerClient

REPO_ROOT = Path(__file__).resolve().parents[3]
TAGGING_RULES_PATH = Path(__file__).parent.parent / "config" / "tagging-rules.yaml"
ROOT_ENV_PATH = REPO_ROOT / ".env"


def main() -> None:
    parser = argparse.ArgumentParser(description="MCP-powered K8s FinOps agent")
    parser.add_argument("--dump-raw", action="store_true", help="Print the raw snapshot JSON before the report")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    if ROOT_ENV_PATH.exists():
        load_dotenv(ROOT_ENV_PATH)

    model_id = os.getenv("OPENAI_MODEL_ID", "gpt-4o")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.ai.kodekloud.com/v1")
    api_key = os.getenv("OPENAI_API_KEY")
    max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "2048"))
    temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.2"))
    tracker_url = os.getenv("ISSUE_TRACKER_URL", "http://localhost:8085")
    tracker_timeout = int(os.getenv("ISSUE_TRACKER_TIMEOUT", "10"))

    if not api_key:
        logger.error("OPENAI_API_KEY not set in environment or .env file")
        sys.exit(1)

    tagging_rules = _load_yaml(TAGGING_RULES_PATH)

    collector = ClusterCollector(
        cluster_name=os.getenv("CLUSTER_NAME", "kind"),
    )
    tracker = IssueTrackerClient(tracker_url, timeout=tracker_timeout)

    if not tracker.connect():
        logger.error("Issue tracker is not running. Start it with Section 06.")
        sys.exit(1)

    def collect_step(_: object) -> ClusterSnapshot:
        return collector.collect_sync()

    def analyze_step(snapshot: ClusterSnapshot) -> AnalysisEnvelope:
        report = analyze_snapshot(
            snapshot=snapshot,
            tagging_rules=tagging_rules,
            model_id=model_id,
            base_url=base_url,
            api_key=api_key,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return AnalysisEnvelope(snapshot=snapshot, report=report)

    def tracker_step(envelope: AnalysisEnvelope):
        tracker_result = tracker.create_from_envelope(envelope)
        return {
            "snapshot": envelope.snapshot.model_dump(),
            "report": envelope.report.model_dump(),
            "tracker": tracker_result,
        }

    pipeline = RunnableLambda(collect_step) | RunnableLambda(analyze_step) | RunnableLambda(tracker_step)

    logger.info("Running collector → analyst → tracker pipeline")
    result = pipeline.invoke(None)

    if args.dump_raw:
        print(json.dumps(result["snapshot"], indent=2))

    print(json.dumps(result["report"], indent=2))
    print(json.dumps(result["tracker"], indent=2))
    logger.info("MCP FinOps pipeline completed successfully")


def _load_yaml(path: Path):
    return yaml.safe_load(path.read_text()) or {}


if __name__ == "__main__":
    main()
