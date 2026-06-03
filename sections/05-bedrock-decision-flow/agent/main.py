"""Main orchestrator for K8s FinOps Agent."""

import os
import sys
import logging
import argparse
from pathlib import Path

import yaml
from dotenv import load_dotenv

from agent.scanner import K8sScanner
from agent.tagging_violations import TaggingViolationDetector
from agent.analyzer import analyze_resource, generate_summary_report


def setup_logging(log_level: str = "INFO"):
    """Setup logging configuration."""
    level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def load_config() -> dict:
    """Load configuration from environment."""
    env_path = Path('.env')
    if env_path.exists():
        load_dotenv()

    tagging_rules_path = os.getenv('TAGGING_RULES')
    excluded_namespaces = []
    if tagging_rules_path:
        try:
            rules_file = Path(tagging_rules_path).expanduser()
            if rules_file.exists():
                with open(rules_file, 'r') as f:
                    tagging_rules_data = yaml.safe_load(f) or {}
                excluded_namespaces = tagging_rules_data.get('excluded_namespaces', []) or []
        except Exception:
            excluded_namespaces = []

    return {
        'kubeconfig_path': os.getenv('KUBECONFIG_PATH'),
        'tagging_rules': tagging_rules_path,
        'bedrock_model_id': os.getenv('BEDROCK_MODEL_ID'),
        'bedrock_max_tokens': int(os.getenv('BEDROCK_MAX_TOKENS', '1024')),
        'bedrock_temperature': float(os.getenv('BEDROCK_TEMPERATURE', '0.3')),
        'aws_region': os.getenv('AWS_REGION', 'us-east-1'),
        'log_level': os.getenv('LOG_LEVEL', 'INFO'),
        'excluded_namespaces': excluded_namespaces,
    }


def load_tagging_rules(tagging_rules_path: str) -> dict:
    """Load tagging rules from YAML file."""
    try:
        with open(tagging_rules_path, 'r') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.warning(f"Could not load tagging rules from {tagging_rules_path}: {e}")
        return {}


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='K8s FinOps Agent')
    parser.add_argument('--kubeconfig', help='Path to kubeconfig file')
    parser.add_argument('--namespace', '-n', help='Target namespace')
    parser.add_argument('--log-level', '-l', default='INFO', help='Log level')

    args = parser.parse_args()

    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)

    logger.info("Starting K8s FinOps Agent")

    config = load_config()

    if args.kubeconfig:
        config['kubeconfig_path'] = args.kubeconfig
    if args.namespace is not None:
        config['target_namespace'] = args.namespace

    model_id = config.get('bedrock_model_id')
    if not model_id:
        logger.error("BEDROCK_MODEL_ID not set in environment or .env file")
        sys.exit(1)

    logger.info(f"Using Bedrock inference profile ARN: {model_id}")

    scanner = K8sScanner(
        kubeconfig_path=config.get('kubeconfig_path'),
        excluded_namespaces=config.get('excluded_namespaces', [])
    )
    if not scanner.connect():
        logger.error("Failed to connect to Kubernetes")
        sys.exit(1)

    tagging_rules = load_tagging_rules(config.get('tagging_rules')) if config.get('tagging_rules') else {}
    detector = TaggingViolationDetector(config.get('tagging_rules'))

    target_ns = config.get('target_namespace')
    logger.info(f"Scanning resources in namespace: {target_ns or 'all namespaces'}")
    resources = scanner.scan_all(target_ns)
    logger.info(f"Found {len(resources)} resources")

    logger.info("Analyzing tagging violations...")
    analysis = detector.analyze_all(resources)

    report = generate_summary_report(analysis)
    print("\n" + "=" * 80)
    print(report)
    print("=" * 80 + "\n")

    violations = detector.get_violations(resources)
    logger.info(f"Found {len(violations)} tagging violations")

    recommendations_generated = 0
    if violations:
        logger.info(f"Sending {len(violations)} findings to Bedrock for LLM-powered decisions")

        drafts = []
        for violation in violations:
            try:
                draft = analyze_resource(
                    violation.resource,
                    violation,
                    model_id,
                    config.get('aws_region', 'us-east-1'),
                    config.get('bedrock_max_tokens', 1024),
                    config.get('bedrock_temperature', 0.3),
                    tagging_rules,
                )
                drafts.append(draft)
            except Exception as e:
                logger.error(f"Failed to analyze {violation.resource.namespace}/{violation.resource.name}: {e}")

        recommendations_generated = len(drafts)
        logger.info(f"Prepared {recommendations_generated} recommendation drafts")

    logger.info("FinOps scan completed successfully")
    logger.info(f"Total violations: {analysis['violations']}")
    logger.info(f"Recommendation drafts prepared: {recommendations_generated}")


if __name__ == '__main__':
    main()