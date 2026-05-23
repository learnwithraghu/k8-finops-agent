"""Main orchestrator for K8s FinOps Agent."""

import os
import sys
import logging
import argparse
from pathlib import Path
from typing import Optional

import yaml
from dotenv import load_dotenv

from agent.scanner import K8sScanner
from agent.cost_calculator import CostCalculator
from agent.untracked_money import UntrackedMoneyDetector
from agent.analyzer import BedrockAnalyzer, MockAnalyzer

# Configure logging
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


class FinOpsAgent:
    """Main FinOps Agent orchestrator."""

    def __init__(self, config: Optional[dict] = None):
        """Initialize agent with configuration."""
        self.config = config or {}
        self.scanner = None
        self.calculator = None
        self.detector = None
        self.analyzer = None
        self.analyzer_mode = "unknown"
        self.recommendations_generated = 0

    def initialize(self) -> bool:
        """Initialize all components."""
        logger = logging.getLogger(__name__)

        # Initialize scanner
        kubeconfig = self.config.get('kubeconfig_path')
        excluded_namespaces = self.config.get('excluded_namespaces', [])
        self.scanner = K8sScanner(kubeconfig_path=kubeconfig, excluded_namespaces=excluded_namespaces)
        if not self.scanner.connect():
            logger.error("Failed to connect to Kubernetes")
            return False

        # Initialize cost calculator
        pricing_config = self.config.get('pricing_config')
        self.calculator = CostCalculator(pricing_config)

        # Initialize untracked money detector
        tagging_rules = self.config.get('tagging_rules')
        self.detector = UntrackedMoneyDetector(self.calculator, tagging_rules)

        # Initialize analyzer (Bedrock or Mock)
        use_mock = self.config.get('use_mock', False)
        if use_mock:
            self.analyzer = MockAnalyzer()
            self.analyzer_mode = "mock"
            logger.info("Using mock analyzer")
        else:
            model_id = self.config.get('bedrock_model_id')
            region = self.config.get('aws_region', 'us-east-1')
            role_arn = self.config.get('aws_role_arn')
            session_token = self.config.get('aws_session_token')
            max_tokens = self.config.get('bedrock_max_tokens', 1024)
            temperature = self.config.get('bedrock_temperature', 0.3)
            self.analyzer = BedrockAnalyzer(
                model_id=model_id,
                region=region,
                role_arn=role_arn,
                session_token=session_token,
                max_tokens=max_tokens,
                temperature=temperature,
                tagging_rules=getattr(self.detector, 'rules', {})
            )

        if not self.analyzer.connect():
            logger.warning("Failed to connect to Bedrock, falling back to mock analyzer")
            self.analyzer = MockAnalyzer()
            self.analyzer_mode = "mock-fallback"
        else:
            if not use_mock:
                self.analyzer_mode = "bedrock"

        return True

    def run_scan(self) -> dict:
        """Run the full scan and analysis."""
        logger = logging.getLogger(__name__)

        # Scan resources
        target_ns = self.config.get('target_namespace')
        logger.info(f"Scanning resources in namespace: {target_ns or 'all namespaces'}")
        resources = self.scanner.scan_all(target_ns)
        logger.info(f"Found {len(resources)} resources")

        # Calculate costs and detect untracked money
        logger.info("Analyzing untracked money...")
        analysis = self.detector.analyze_all(resources)

        # Generate summary report
        report = self.analyzer.generate_summary_report(analysis)
        print("\n" + "=" * 80)
        print(report)
        print("=" * 80 + "\n")
        logger.info(f"Analyzer mode: {self.analyzer_mode}")
        if self.analyzer_mode == "bedrock":
            logger.info("LLM-powered output generated from Bedrock")
            logger.info(f"Bedrock inference profile ARN: {self.config.get('bedrock_model_id')}")

        # Get high-impact violations
        threshold = self.config.get('min_cost_threshold', 1.0)
        violations = self.detector.get_high_impact_violations(resources, threshold)
        logger.info(f"Found {len(violations)} high-impact violations")

        # Analyze with AI / Bedrock
        recommendations_generated = 0
        if violations:
            if self.analyzer_mode == "bedrock":
                logger.info(f"Sending {len(violations)} findings to Bedrock for LLM-powered decisions")
            else:
                logger.info("Generating recommendation drafts with mock analyzer")

            drafts = []
            for untracked in violations:
                draft = self.analyzer.analyze_resource(
                    untracked.resource,
                    untracked
                )
                if draft:
                    drafts.append(draft)

            recommendations_generated = len(drafts)
            logger.info(f"Prepared {recommendations_generated} recommendation drafts")

        return {
            'analysis': analysis,
            'violations': len(violations),
            'recommendations_generated': recommendations_generated,
            'report': report
        }


def load_config() -> dict:
    """Load configuration from environment."""
    # Load .env file if it exists
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
        'pricing_config': os.getenv('PRICING_CONFIG'),
        'tagging_rules': tagging_rules_path,
        'bedrock_model_id': os.getenv('BEDROCK_MODEL_ID'),
        'bedrock_max_tokens': int(os.getenv('BEDROCK_MAX_TOKENS', '1024')),
        'bedrock_temperature': float(os.getenv('BEDROCK_TEMPERATURE', '0.3')),
        'aws_role_arn': os.getenv('AWS_ROLE_ARN'),
        'aws_session_token': os.getenv('AWS_SESSION_TOKEN'),
        'aws_region': os.getenv('AWS_REGION', 'us-east-1'),
        'log_level': os.getenv('LOG_LEVEL', 'INFO'),
        'dry_run': os.getenv('DRY_RUN', 'false').lower() == 'true',
        'min_cost_threshold': float(os.getenv('MIN_COST_THRESHOLD', '1.0')),
        'use_mock': os.getenv('USE_MOCK', 'false').lower() == 'true',
        'excluded_namespaces': excluded_namespaces,
    }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='K8s FinOps Agent')
    parser.add_argument('--kubeconfig', help='Path to kubeconfig file')
    parser.add_argument('--namespace', '-n', help='Target namespace')
    parser.add_argument('--dry-run', '-d', action='store_true', help='Dry run mode')
    parser.add_argument('--mock', '-m', action='store_true', help='Use mock analyzer')
    parser.add_argument('--threshold', '-t', type=float, default=1.0, help='Minimum cost threshold')
    parser.add_argument('--log-level', '-l', default='INFO', help='Log level')

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)

    logger.info("Starting K8s FinOps Agent")

    # Load configuration
    config = load_config()

    # Override with command line args
    if args.kubeconfig:
        config['kubeconfig_path'] = args.kubeconfig
    if args.namespace is not None:
        config['target_namespace'] = args.namespace
    if args.dry_run:
        config['dry_run'] = True
    if args.mock:
        config['use_mock'] = True
    if args.threshold:
        config['min_cost_threshold'] = args.threshold

    # Prefer Bedrock automatically when a profile ARN is configured.
    # Section 04 can still force mock mode with --mock.
    if not args.mock and config.get('bedrock_model_id'):
        config['use_mock'] = False

    # Initialize and run agent
    agent = FinOpsAgent(config)
    if not agent.initialize():
        logger.error("Failed to initialize agent")
        sys.exit(1)

    try:
        results = agent.run_scan()
        logger.info("FinOps scan completed successfully")
        logger.info(f"Total untracked: ${results['analysis']['total_untracked']}/month")
        logger.info(f"Recommendation drafts prepared: {results['recommendations_generated']}")
    except Exception as e:
        logger.error(f"Scan failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
