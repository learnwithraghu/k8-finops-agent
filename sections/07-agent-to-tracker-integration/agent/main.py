"""Main orchestrator for the agent-to-tracker integration section."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Optional

import requests
from dotenv import load_dotenv

from agent.analyzer import BedrockAnalyzer, IssueDraft, MockAnalyzer
from agent.cost_calculator import CostCalculator
from agent.scanner import K8sScanner
from agent.untracked_money import UntrackedMoneyDetector


logger = logging.getLogger(__name__)


def setup_logging(log_level: str = "INFO") -> None:
    """Setup logging configuration."""
    level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


class IssueTrackerClient:
    """Small client for the local issue tracker service."""

    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self._connected = False

    def connect(self) -> bool:
        """Confirm the tracker is running before sending issues."""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=self.timeout)
            response.raise_for_status()
            self._connected = True
            logger.info(f"Connected to issue tracker at {self.base_url}")
            return True
        except Exception as exc:
            logger.error(f"Failed to connect to issue tracker at {self.base_url}: {exc}")
            return False

    def create_issue(self, payload: dict, dry_run: bool = False) -> dict:
        """Create one issue in the tracker."""
        if dry_run:
            logger.info(f"[DRY RUN] Would create issue: {payload.get('title')}")
            return {"dry_run": True, "payload": payload}

        response = self.session.post(
            f"{self.base_url}/create-issue",
            json=payload,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def create_issues_batch(self, payloads: list[dict], dry_run: bool = False) -> dict:
        """Create multiple issues and track failures."""
        results = {"created": [], "failed": []}

        for payload in payloads:
            try:
                created = self.create_issue(payload, dry_run=dry_run)
                results["created"].append(created)
            except Exception as exc:
                logger.error(f"Failed to create issue '{payload.get('title')}': {exc}")
                results["failed"].append({"payload": payload, "error": str(exc)})

        return results


class FinOpsAgent:
    """Main FinOps agent orchestrator."""

    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        self.scanner = None
        self.calculator = None
        self.detector = None
        self.analyzer = None
        self.tracker = None
        self.analyzer_mode = "unknown"

    def initialize(self) -> bool:
        """Initialize all components."""
        kubeconfig = self.config.get("kubeconfig_path")
        excluded_namespaces = self.config.get("excluded_namespaces", [])
        self.scanner = K8sScanner(kubeconfig_path=kubeconfig, excluded_namespaces=excluded_namespaces)
        if not self.scanner.connect():
            logger.error("Failed to connect to Kubernetes")
            return False

        self.calculator = CostCalculator(self.config.get("pricing_config"))
        self.detector = UntrackedMoneyDetector(self.calculator, self.config.get("tagging_rules"))

        force_mock = self.config.get("force_mock", False)
        if force_mock:
            self.analyzer = MockAnalyzer()
            self.analyzer_mode = "mock"
            logger.info("Using mock analyzer (--mock flag)")
        else:
            self.analyzer = BedrockAnalyzer(
                model_id=self.config.get("bedrock_model_id"),
                region=self.config.get("aws_region", "us-east-1"),
                max_tokens=self.config.get("bedrock_max_tokens", 1024),
                temperature=self.config.get("bedrock_temperature", 0.3),
                tagging_rules=getattr(self.detector, "rules", {}),
            )
            if self.analyzer.connect():
                self.analyzer_mode = "bedrock"
            else:
                logger.warning("Failed to connect to Bedrock, falling back to mock analyzer")
                self.analyzer = MockAnalyzer()
                self.analyzer_mode = "mock-fallback"

        self.tracker = IssueTrackerClient(
            base_url=self.config.get("issue_tracker_url", "http://localhost:8085"),
            timeout=self.config.get("issue_tracker_timeout", 10),
        )
        if not self.tracker.connect():
            logger.error("Issue tracker must be running before this section can create tickets")
            return False

        return True

    def _build_tracker_payload(self, resource, untracked, draft: IssueDraft) -> dict:
        assignee = draft.suggested_owner if draft.suggested_owner and draft.suggested_owner != "unknown" else ""
        suggested_cost_center = draft.suggested_cost_center if draft.suggested_cost_center != "unknown" else ""

        return {
            "title": draft.title,
            "summary": draft.reasoning or untracked.reason,
            "body": draft.body,
            "namespace": resource.namespace,
            "resource_name": resource.name,
            "resource_kind": resource.kind,
            "category": untracked.category.value,
            "priority": draft.priority,
            "cost_impact": round(float(draft.estimated_savings or untracked.untracked_amount), 2),
            "assignee": assignee,
            "suggested_owner": draft.suggested_owner,
            "suggested_cost_center": suggested_cost_center,
            "labels": draft.labels,
            "reasoning": draft.reasoning or untracked.reason,
            "source": "bedrock" if self.analyzer_mode == "bedrock" else "mock",
        }

    def run_scan(self) -> dict:
        """Run the full scan, create tracker issues, and return a summary."""
        target_ns = self.config.get("target_namespace")
        logger.info(f"Scanning resources in namespace: {target_ns or 'all namespaces'}")
        resources = self.scanner.scan_all(target_ns)
        logger.info(f"Found {len(resources)} resources")

        logger.info("Analyzing untracked money...")
        analysis = self.detector.analyze_all(resources)

        report = self.analyzer.generate_summary_report(analysis)
        print("\n" + "=" * 80)
        print(report)
        print("=" * 80 + "\n")
        logger.info(f"Analyzer mode: {self.analyzer_mode}")

        threshold = self.config.get("min_cost_threshold", 1.0)
        violations = self.detector.get_high_impact_violations(resources, threshold)
        logger.info(f"Found {len(violations)} high-impact violations")

        created_count = 0
        tracker_results = {"created": [], "failed": []}
        if violations:
            logger.info("Generating tracker tickets from Bedrock output...")
            payloads = []
            for untracked in violations:
                resource = untracked.resource
                draft = self.analyzer.analyze_resource(resource, untracked)
                if not draft:
                    continue
                if not draft.should_create_issue:
                    logger.info(f"Skipping non-actionable finding: {draft.title}")
                    continue
                payloads.append(self._build_tracker_payload(resource, untracked, draft))

            if payloads:
                if self.config.get("dry_run", False):
                    logger.info(f"[DRY RUN] Would send {len(payloads)} issues to the tracker")
                else:
                    logger.info(f"Sending {len(payloads)} issues to the tracker")

                tracker_results = self.tracker.create_issues_batch(
                    payloads,
                    dry_run=self.config.get("dry_run", False),
                )
                created_count = 0 if self.config.get("dry_run", False) else len(tracker_results["created"])
                logger.info(f"Issues created: {created_count}")
                logger.info(f"Failed: {len(tracker_results['failed'])}")
            else:
                logger.info("No actionable issue drafts returned by Bedrock")

        return {
            "analysis": analysis,
            "violations": len(violations),
            "issues_created": created_count,
            "tracker_results": tracker_results,
            "report": report,
        }


def load_config() -> dict:
    """Load configuration from environment."""
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(override=True)

    return {
        "kubeconfig_path": os.getenv("KUBECONFIG_PATH"),
        "pricing_config": os.getenv("PRICING_CONFIG"),
        "tagging_rules": os.getenv("TAGGING_RULES"),
        "bedrock_model_id": os.getenv("BEDROCK_MODEL_ID"),
        "bedrock_max_tokens": int(os.getenv("BEDROCK_MAX_TOKENS", "1024")),
        "bedrock_temperature": float(os.getenv("BEDROCK_TEMPERATURE", "0.3")),
        "aws_region": os.getenv("AWS_REGION", "us-east-1"),
        "issue_tracker_url": os.getenv("ISSUE_TRACKER_URL", "http://localhost:8085"),
        "issue_tracker_timeout": int(os.getenv("ISSUE_TRACKER_TIMEOUT", "10")),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "dry_run": os.getenv("DRY_RUN", "false").lower() == "true",
        "min_cost_threshold": float(os.getenv("MIN_COST_THRESHOLD", "1.0")),
        "excluded_namespaces": [],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="K8s FinOps Agent - tracker integration")
    parser.add_argument("--kubeconfig", help="Path to kubeconfig file")
    parser.add_argument("--namespace", "-n", help="Target namespace")
    parser.add_argument("--dry-run", "-d", action="store_true", help="Dry run mode")
    parser.add_argument("--mock", "-m", action="store_true", help="Use mock analyzer")
    parser.add_argument("--threshold", "-t", type=float, default=1.0, help="Minimum cost threshold")
    parser.add_argument("--log-level", "-l", default="INFO", help="Log level")
    parser.add_argument("--issue-tracker-url", default=None, help="Issue tracker base URL")

    args = parser.parse_args()

    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    logger.info("Starting K8s FinOps Agent")

    config = load_config()

    if args.kubeconfig:
        config["kubeconfig_path"] = args.kubeconfig
    if args.namespace is not None:
        config["target_namespace"] = args.namespace
    if args.dry_run:
        config["dry_run"] = True
    if args.mock:
        config["force_mock"] = True
    if args.threshold:
        config["min_cost_threshold"] = args.threshold
    if args.issue_tracker_url:
        config["issue_tracker_url"] = args.issue_tracker_url

    agent = FinOpsAgent(config)
    if not agent.initialize():
        logger.error("Failed to initialize agent")
        sys.exit(1)

    try:
        results = agent.run_scan()
        logger.info("FinOps scan completed successfully")
        logger.info(f"Total untracked: ${results['analysis']['total_untracked']}/month")
        logger.info(f"Issues created: {results['issues_created']}")
    except Exception as exc:
        logger.error(f"Scan failed: {exc}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
