"""Entry point for the LLM-powered K8s FinOps Agent.

Pipeline: scan Kubernetes metadata -> send each resource + the FinOps tagging
config to the LLM -> print a decision-oriented report.
"""

import argparse
import logging
import os
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

from agent.scanner import K8sScanner
from agent.analyzer import analyze_resource, generate_summary_report

# Path to tagging rules is fixed — always lives in config/ next to the agent
TAGGING_RULES_PATH = Path(__file__).parent.parent / "config" / "tagging-rules.yaml"


def main():
    parser = argparse.ArgumentParser(description="LLM-powered K8s FinOps agent")
    parser.add_argument("--namespace", help="Limit the scan to a single namespace")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    if Path('.env').exists():
        load_dotenv()

    model_id = os.getenv('OPENAI_MODEL_ID', 'gpt-4o')
    base_url = os.getenv('OPENAI_BASE_URL', 'https://api.ai.kodekloud.com/v1')
    api_key = os.getenv('OPENAI_API_KEY')
    max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', '1024'))
    temperature = float(os.getenv('OPENAI_TEMPERATURE', '0.3'))

    if not api_key:
        logger.error("OPENAI_API_KEY not set in environment or .env file")
        sys.exit(1)

    logger.info(f"Using OpenAI-compatible model: {model_id}")

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

    # 2. Send each resource + the FinOps tagging policy to the LLM
    logger.info(f"Sending {len(resources)} resources to the LLM for decisions")
    results = []
    for resource in resources:
        try:
            decision = analyze_resource(
                resource, model_id, base_url, api_key, max_tokens, temperature, tagging_rules,
            )
            results.append((resource, decision))
        except Exception as e:
            logger.error(f"Failed to analyze {resource.namespace}/{resource.name}: {e}")

    # 3. Report
    report = generate_summary_report(results)
    print("\n" + "=" * 80)
    print(report)
    print("=" * 80 + "\n")

    violation_count = sum(1 for _, d in results if not d.is_compliant)
    logger.info("FinOps scan completed successfully")
    logger.info(f"Total resources analyzed: {len(results)}")
    logger.info(f"Violations: {violation_count}")


if __name__ == '__main__':
    main()
