"""Entry point for the K8s FinOps Agent.

Pipeline: scan Kubernetes metadata -> check it against the FinOps tagging
config -> print a compliance report.
"""

import argparse
import logging
import os
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

from agent.scanner import K8sScanner
from agent.simple_checker import SimpleTagChecker

# Path to tagging rules is fixed — always lives in config/ next to the agent
TAGGING_RULES_PATH = Path(__file__).parent.parent / "config" / "tagging-rules.yaml"


def main():
    parser = argparse.ArgumentParser(description="K8s FinOps tagging compliance scanner")
    parser.add_argument("--namespace", help="Limit the scan to a single namespace")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    if Path('.env').exists():
        load_dotenv()

    tagging_rules = yaml.safe_load(TAGGING_RULES_PATH.read_text()) or {}
    excluded_namespaces = tagging_rules.get('excluded_namespaces', []) or []

    # 1. Scan Kubernetes metadata
    scanner = K8sScanner(
        kubeconfig_path=os.getenv('KUBECONFIG_PATH'),
        excluded_namespaces=excluded_namespaces,
    )
    if not scanner.connect():
        logger.error("Failed to connect to Kubernetes")
        sys.exit(1)

    logger.info(f"Scanning resources in namespace: {args.namespace or 'all namespaces'}")
    resources = scanner.scan_all(args.namespace)
    logger.info(f"Found {len(resources)} resources")

    # 2. Check resources against the FinOps tagging config
    checker = SimpleTagChecker(str(TAGGING_RULES_PATH))
    analysis = checker.check_all(resources)

    # 3. Report
    checker.print_report(analysis)
    logger.info("FinOps scan completed successfully")
    logger.info(f"Total resources: {analysis['total_resources']}")
    logger.info(f"Compliant: {analysis['compliant_count']}")
    logger.info(f"Non-compliant: {analysis['non_compliant_count']}")


if __name__ == '__main__':
    main()
